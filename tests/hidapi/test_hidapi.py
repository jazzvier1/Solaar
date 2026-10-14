import platform

from unittest import mock

import pytest

if platform.system() == "Linux":
    import hidapi.udev_impl as hidapi
else:
    import hidapi.hidapi_impl as hidapi


def test_find_paired_node():
    hidapi.enumerate(mock.Mock())


@pytest.mark.skipif(platform.system() == "Linux", reason="hidapi backend only")
def test_match_windows_uses_collection_usage():
    base = dict(
        vendor_id=0x046D,
        product_id=0x0AB5,
        bus_type=0x01,
        path=b"p",
        manufacturer_string="",
        product_string="G733",
        serial_number="",
        release_number=0,
    )
    with mock.patch("platform.system", return_value="Windows"):
        hidpp = hidapi._match("add", dict(base, usage_page=0xFF43, usage=0x0202), lambda *a: {"isDevice": True})
        audio = hidapi._match("add", dict(base, usage_page=0xFF00, usage=0x0001), lambda *a: {"isDevice": True})
    assert hidpp.hidpp_long and not hidpp.hidpp_short
    assert audio is None
