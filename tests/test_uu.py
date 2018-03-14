# Copyright (C) 2018 Jurriaan Bremer.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import pytest

from sflock.abstracts import File
from sflock.main import unpack
from sflock.unpack import UuFile

def f(filename):
    return File.from_path("tests/files/%s" % filename)

@pytest.mark.skipif("not UuFile(None).supported()")
class TestCabFile(object):
    def test_invoice(self):
        assert f("invoice.uu").magic.startswith("ASCII")
        t = UuFile(f("invoice.uu"))
        assert t.handles() is True
        assert not t.f.selected
        files = list(t.unpack())
        assert len(files) == 1
        assert not files[0].filepath
        assert files[0].relapath == "New Inquiry-876126F.exe"
        assert files[0].filesize == 516096
        assert "PE32" in files[0].magic
        assert files[0].parentdirs == []
        assert files[0].selected is True

    def test_heuristics(self):
        t = unpack("tests/files/invoice.uu", filename="foo")
        assert t.unpacker == "uufile"
        assert t.filename == "foo"

        t = unpack("tests/files/phrack.xx", filename="foo")
        assert t.unpacker == "uufile"
        assert t.filename == "foo"

    def test_inmemory(self):
        contents = open("tests/files/invoice.uu", "rb").read()
        t = unpack(contents=contents)
        assert t.unpacker == "uufile"
        assert t.filename is None
        assert t.filepath is None
        assert len(t.children) == 1

    def test_garbage(self):
        t = UuFile(f("garbage.bin"))
        assert t.handles() is False
        assert not t.f.selected
        assert not t.unpack()
        assert t.f.mode == "failed"

@pytest.mark.skipif("UuFile(None).supported()")
def test_nouudeview():
    t = UuFile(f("invoice.uu"))
    assert t.handles() is True
    assert not t.f.selected
