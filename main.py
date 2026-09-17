import argparse
import os
import time

import cv2

from analytics.analytics import SurveillanceAnalytics
from config.config import (
    VIDEO_PATH, OUTPUT_DIR, MODEL_PATH, OUTPUT_WIDTH, CONFIDENCE_THRESHOLD,
    MOTION_THRESHOLD, MOTION_PIXEL_THRESHOLD, MOTION_MIN_FLOW,
    EVENT_COOLDOWN_FRAMES, SAVE_VIDEO,
)
from input.video_reader import VideoReader
from logging_module.event_logger import EventLogger
from motion.motion_detector import MotionDetector
from preprocessing.image_processor import ImageProcessor
from tracking.object_tracker import ObjectTracker


def parse_args():
    parser = argparse.ArgumentParser(
        description="Command-line smart surveillance and motion analysis pipeline."
    )
    parser.add_argument("--input", default=VIDEO_PATH, help="Input video path")
    parser.add_argument("--output-dir", default=OUTPUT_DIR, help="Output directory")
    parser.add_argument("--model", default=MODEL_PATH, help="YOLO model path/name")
    parser.add_argument("--width", type=int, default=OUTPUT_WIDTH, help="Processing width")
    parser.add_argument("--conf", type=float, default=CONFIDENCE_THRESHOLD, help="YOLO confidence")
    parser.add_argument("--motion-threshold", type=int, default=MOTION_THRESHOLD)
    parser.add_argument("--motion-pixels", type=int, default=MOTION_PIXEL_THRESHOLD)
    parser.add_argument("--min-flow", type=float, default=MOTION_MIN_FLOW)
    parser.add_argument("--cooldown", type=int, default=EVENT_COOLDOWN_FRAMES)
    parser.add_argument("--max-frames", type=int, default=None, help="Optional frame limit")
    parser.add_argument("--no-video", action="store_true", help="Skip annotated video output")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.width <= 0 or not (0 < args.conf <= 1):
        raise ValueError("Width must be positive and confidence must be in (0, 1].")
    if args.cooldown < 0:
        raise ValueError("Cooldown must be non-negative.")

    os.makedirs(args.output_dir, exist_ok=True)
    event_path = os.path.join(args.output_dir, "events.csv")
    summary_path = os.path.join(args.output_dir, "summary.json")
    video_path = os.path.join(args.output_dir, "surveillance_output.mp4")

    reader = VideoReader(args.input)
    properties = reader.get_properties()
    processor = ImageProcessor(args.width)
    tracker = ObjectTracker(args.model, args.conf)
    motion_detector = MotionDetector(
        args.motion_threshold, args.motion_pixels, args.min_flow
    )
    logger = EventLogger(event_path, reset=True)

    output_height = max(1, int(properties["height"] * args.width / properties["width"]))
    writer = None
    if not args.no_video and SAVE_VIDEO:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(video_path, fourcc, properties["fps"], (args.width, output_height))
        if not writer.isOpened():
            reader.release()
            raise RuntimeError(f"Could not create output video: {video_path}")

    last_logged_frame = {}
    frame_number = 0
    started = time.perf_counter()

    try:
        for frame in reader.read_frames():
            frame_number += 1
            processed = processor.process(frame)
            display_frame = processed["resized"].copy()

            result = tracker.track(display_frame)
            tracks = tracker.get_tracks(result)
            motion = motion_detector.detect(display_frame)

            for track in tracks:
                x1, y1, x2, y2 = map(int, track["box"])
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"ID {track['track_id']} {track['class_name']} {track['confidence']:.2f}"
                cv2.putText(display_frame, label, (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                track_id = track["track_id"]
                can_log = frame_number - last_logged_frame.get(track_id, -10**9) >= args.cooldown
                if motion["motion_detected"] and can_log:
                    logger.log_event(
                        frame_number, "Motion Detected", track_id,
                        track["class_name"], track["confidence"],
                        motion["motion_pixels"], motion["mean_flow"],
                    )
                    last_logged_frame[track_id] = frame_number

            status = "MOTION DETECTED" if motion["motion_detected"] else "NO MOTION"
            cv2.putText(display_frame, status, (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(display_frame, f"Flow: {motion['mean_flow']:.2f} | Changed px: {motion['motion_pixels']}",
                        (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

            if writer is not None:
                writer.write(display_frame)

            if args.max_frames is not None and frame_number >= args.max_frames:
                break
    finally:
        reader.release()
        if writer is not None:
            writer.release()

    elapsed = time.perf_counter() - started
    analytics = SurveillanceAnalytics(event_path)
    summary = analytics.analyze()
    analytics.save_json(summary_path, summary, frame_number, elapsed)

    print("\n========== SURVEILLANCE SUMMARY ==========")
    print(f"Frames processed: {frame_number}")
    print(f"Processing time: {elapsed:.2f} s")
    print(f"Total logged events: {summary['total_events']}")
    print(f"Unique tracked IDs in log: {summary['unique_objects']}")
    print(f"Average confidence: {summary['average_confidence']:.3f}")
    print(f"Average motion pixels: {summary['average_motion_pixels']:.2f}")
    print(f"Average optical-flow magnitude: {summary['average_flow']:.3f}")
    print("Object classes:")
    for name, count in sorted(summary["object_types"].items()):
        print(f"  - {name}: {count}")
    print("==========================================")
    print(f"Events: {event_path}")
    print(f"Summary: {summary_path}")
    if writer is not None:
        print(f"Video: {video_path}")


if __name__ == "__main__":
    main()
