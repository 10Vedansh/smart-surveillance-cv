import main


def test_parser_defaults(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py"])
    args = main.parse_args()
    assert args.input == "input/test_video.mp4"
    assert args.width > 0
    assert args.conf > 0
