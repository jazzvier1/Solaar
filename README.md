# <img src="https://pwr-solaar.github.io/Solaar/img/solaar.svg" width="60px"/> Solaar for Windows

> **This is a Windows-only port of [Solaar](https://github.com/pwr-Solaar/Solaar).**
> It is meant as a lightweight, telemetry-free alternative to Logitech G HUB:
> no background services, no account, no data collection.
> On Linux, use the upstream project instead.

Solaar is a manager for many Logitech keyboards, mice, headsets and other devices.
It is not a device driver: it only talks to devices through Logitech's HID++ protocol.
This port uses the [hidapi](https://github.com/libusb/hidapi) backend that Solaar already ships
and fixes HID++ device detection on Windows.

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2+-blue.svg)](LICENSE.txt)

## Windows port status

Tested on a Logitech **G733** headset (USB Lightspeed dongle, PID `0AB5`):

| Feature | Status |
|---|---|
| Sidetone | ✅ read and write |
| 10-band equalizer | ✅ read |
| Battery level | ✅ |
| LED effects | ✅ read |
| GTK window | ✅ starts and shows the device |
| Blue VO!CE | ❌ not possible: on the G733 it is audio processing done by G HUB on the PC, not a device setting |
| Unifying / Bolt / Lightspeed receivers for mice and keyboards | ❌ not yet: Windows splits HID++ short and long reports into separate HID collections |
| Rules and simulated input (evdev / uinput / X11) | ❌ Linux only |
| Desktop notifications, suspend/resume detection (libnotify / dbus) | ❌ Linux only |

Other Logitech G devices that expose the HID++ collection `FF43/0202` should work the same way, but are untested.

## Installation

No installer, no admin rights, nothing else to install (Python and GTK are bundled):

1. Download **[Solaar-Windows.zip](https://github.com/jazzvier1/Solaar/releases/latest/download/Solaar-Windows.zip)** (~37 MB).
2. Extract it anywhere, e.g. `C:\Tools\Solaar-Windows`.
3. Double-click **`Solaar.bat`**.

If Windows warns that the file came from the internet, choose *More info → Run anyway*
(or right-click the zip → *Properties* → *Unblock* before extracting).

Close G HUB first (ideally uninstall it): it re-applies its own settings to the device.
Settings are stored in `%USERPROFILE%\.config\solaar\config.yaml`.

## Usage

- **Start with Windows, minimized to the tray:** press `Win+R`, type `shell:startup`, and in that folder create a
  shortcut to `Solaar.bat` with `--window=hide` added at the end of its *Target*.
- **Command line:** in the extracted folder, `solaar-cli show` prints every device and its settings,
  `solaar-cli config G733 sidetone 50` changes one setting.

## Run from source / build the zip

1. Install [MSYS2](https://www.msys2.org/) (or `winget install MSYS2.MSYS2`), then in the **MSYS2 UCRT64** shell:

   ```bash
   pacman -S --needed git zip mingw-w64-ucrt-x86_64-ntldd mingw-w64-ucrt-x86_64-gtk3 mingw-w64-ucrt-x86_64-python-gobject mingw-w64-ucrt-x86_64-python-yaml mingw-w64-ucrt-x86_64-python-psutil mingw-w64-ucrt-x86_64-python-typing_extensions mingw-w64-ucrt-x86_64-hidapi mingw-w64-ucrt-x86_64-adwaita-icon-theme
   git clone https://github.com/jazzvier1/Solaar.git && cd Solaar
   ```

2. Run it with `python bin/solaar`, or build `dist/Solaar-Windows.zip` with `bash packaging/windows/build.sh`.

## Upstream

All device support comes from upstream Solaar; see
<a href="https://pwr-solaar.github.io/Solaar/index">its documentation</a> for
<a href="https://pwr-solaar.github.io/Solaar/usage">usage</a> and
<a href="https://pwr-solaar.github.io/Solaar/capabilities">capabilities</a>.
Its Linux installation packages and udev instructions do not apply to this port.
