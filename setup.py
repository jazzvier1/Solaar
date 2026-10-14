import subprocess
import textwrap

from glob import glob
from os.path import dirname
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

NAME = "Solaar"
version = Path("lib/solaar/version").read_text().strip()

try:  # get commit from git describe
    commit = subprocess.check_output(["git", "describe", "--always"], stderr=subprocess.DEVNULL).strip().decode()
    Path("lib/solaar/commit").write_text(f"{commit}\n")
except Exception:  # get commit from Ubuntu dpkg-parsechangelog
    try:
        commit = (
            subprocess.check_output(["dpkg-parsechangelog", "--show-field", "Version"], stderr=subprocess.DEVNULL)
            .strip()
            .decode()
        )
        commit = commit.split("~")
        Path("lib/solaar/commit").write_text(f"{commit[0]}\n")
    except Exception as e:
        print("Exception using dpkg-parsechangelog", e)


def _data_files():
    yield "share/icons/hicolor/scalable/apps", glob("share/solaar/icons/solaar*.svg")
    yield "share/icons/hicolor/32x32/apps", glob("share/solaar/icons/solaar-light_*.png")

    for mo in glob("share/locale/*/LC_MESSAGES/solaar.mo"):
        yield dirname(mo), [mo]


setup(
    name=NAME.lower(),
    version=version,
    description="Windows device manager for Logitech G headsets and mice (port of Solaar).",
    long_description=textwrap.dedent(
        """
        Solaar for Windows is a port of Solaar, a device manager for Logitech peripherals.
        It shows and modifies device settings such as headset sidetone and equalizer, or mouse DPI and lights.
        Download the portable build from https://github.com/jazzvier1/Solaar-Windows/releases/latest"""
    ),
    author="Daniel Pavel",
    license="GPLv2",
    url="https://github.com/jazzvier1/Solaar-Windows",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: DFSG approved",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities",
    ],
    platforms=["linux"],
    python_requires=">=3.8",
    install_requires=[
        'evdev (>= 1.1.2) ; platform_system=="Linux"',
        'pyudev (>= 0.13) ; platform_system=="Linux"',
        "PyYAML (>= 3.12)",
        'python-xlib (>= 0.27) ; platform_system=="Linux"',
        "psutil (>= 5.4.3)",
        'dbus-python ; platform_system=="Linux"',
        "PyGObject",
        "pycairo",
        "typing_extensions",
    ],
    extras_require={
        "report-descriptor": ["hid-parser"],
        "desktop-notifications": ["Notify (>= 0.7)"],
        "git-commit": ["python-git-info"],
        "test": ["pytest", "pytest-mock", "pytest-cov"],
        "dev": ["ruff"],
    },
    package_dir={"": "lib"},
    packages=find_packages(where="lib"),
    data_files=list(_data_files()),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "solaar = solaar.gtk:main",
        ],
    },
)
