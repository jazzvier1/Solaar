#!/usr/bin/env bash
# Builds dist/Solaar-Windows.zip: Solaar plus a trimmed MSYS2 UCRT64 runtime (Python, GTK3, hidapi).
# Run from the MSYS2 UCRT64 shell after installing the packages listed in README.md plus git, zip and ntldd.
set -euo pipefail
cd "$(dirname "$0")/../.."
git -c core.autocrlf=true diff --quiet HEAD || { echo "Commit your changes first: the zip is built from HEAD"; exit 1; }

P=/ucrt64
PY=$($P/bin/python -c 'import sys; print(f"python{sys.version_info[0]}.{sys.version_info[1]}")')
OUT=dist/Solaar-Windows
RT=$OUT/runtime
rm -rf dist
mkdir -p "$OUT/app" "$RT/bin" "$RT/lib/$PY/site-packages" "$RT/lib/gdk-pixbuf-2.0" "$RT/share/icons" "$RT/share/glib-2.0"

# App: committed sources only
git archive HEAD bin lib share LICENSE.txt | tar -x -C "$OUT/app"
cp packaging/windows/*.bat README.md LICENSE.txt "$OUT/"

# Python stdlib without tests/IDE/Tk, plus only the site-packages Solaar imports
cp $P/bin/python.exe $P/bin/pythonw.exe "$RT/bin/"
tar -C $P/lib -c --exclude=__pycache__ --exclude="$PY/site-packages" --exclude="$PY/test" --exclude="$PY/idlelib" \
    --exclude="$PY/tkinter" --exclude="$PY/turtledemo" --exclude="$PY/ensurepip" \
    --exclude="$PY/lib-dynload/_tkinter*" "$PY" | tar -x -C "$RT/lib"
for m in gi cairo yaml _yaml psutil typing_extensions.py; do
    cp -r "$P/lib/$PY/site-packages/$m" "$RT/lib/$PY/site-packages/"
done
find "$RT/lib" -name __pycache__ -prune -exec rm -rf {} +

# GTK data: typelibs, image loaders, icon themes, GSettings schemas
cp -r $P/lib/girepository-1.0 "$RT/lib/"
cp -r $P/lib/gdk-pixbuf-2.0/2.10.0 "$RT/lib/gdk-pixbuf-2.0/"
find "$RT/lib/gdk-pixbuf-2.0" -name '*.dll.a' -delete
cp -r $P/share/icons/Adwaita $P/share/icons/hicolor "$RT/share/icons/"
cp -r $P/share/glib-2.0/schemas "$RT/share/glib-2.0/"

# DLLs: everything from /ucrt64 that Python, the extension modules, GTK (loaded by gi at runtime) and hidapi need
deps=($P/bin/python.exe $(cd "$RT" && find lib -name '*.pyd' -o -name '*.dll' | sed "s|^|$P/|") $P/bin/libgtk-3-0.dll $P/bin/libhidapi-0.dll)
ntldd -R "${deps[@]}" | awk '{print $3}' | grep -i 'ucrt64.bin' | sort -u | cygpath -u -f - | xargs -I{} cp -n {} "$RT/bin/"
cp -n $P/bin/libgtk-3-0.dll $P/bin/libhidapi-0.dll "$RT/bin/"

(cd dist && zip -qr9 Solaar-Windows.zip Solaar-Windows)
du -sh "$OUT" dist/Solaar-Windows.zip
