from solaar import dbus


def test_watch_suspend_resume_without_dbus(monkeypatch):
    # Windows has no system D-Bus: --restart-on-wake-up passes both callbacks and must not crash
    monkeypatch.setattr(dbus, "bus", None)
    dbus.watch_suspend_resume(lambda: None, lambda: None)
