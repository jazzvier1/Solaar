from unittest import mock

from solaar import listener


def test_repeated_add_keeps_running_listener(monkeypatch):
    running = mock.Mock()
    info = mock.Mock(path="p")
    monkeypatch.setattr(listener, "_all_listeners", {"p": running})
    monkeypatch.setattr(listener, "_error_callback", mock.Mock())
    start = mock.Mock()
    monkeypatch.setattr(listener, "_process_add", start)

    listener._process_receiver_event(listener.ACTION_ADD, info)
    running.stop.assert_not_called()
    start.assert_not_called()

    listener._all_listeners.clear()  # the listener stopped, e.g. the device was unplugged and replugged
    listener._process_receiver_event(listener.ACTION_ADD, info)
    start.assert_called_once_with(info, 3)
