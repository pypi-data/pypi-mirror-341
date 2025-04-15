import pycregex
from pycregex import PyCRegexCFlag


def test_compile():
    r = pycregex.compile(b"f\\(oo\\)")
    assert r.r
    assert not r.m
    assert r.nmatch == 0
    assert not r.span()


def test_compile_nmatch():
    r = pycregex.compile(b"f\\(oo\\)", nmatch=2)
    assert r.r
    assert r.m
    assert r.nmatch == 2
    assert not r.span()


def test_compile_cflags():
    r = pycregex.compile(
        b"f\\(oo\\)", cflags=PyCRegexCFlag.REG_EXTENDED | PyCRegexCFlag.REG_ICASE
    )
    assert r.r
    assert not r.m
    assert r.nmatch == 0
    assert not r.span()


def test_match():
    r = pycregex.compile(b"f\\(oo\\)", nmatch=2)
    result = r.match(b"foo")
    assert result == 0
    s = r.span()
    assert len(s) == 2
    assert s[0] == (0, 3)
    assert s[1] == (1, 3)


def test_match_icase():
    r = pycregex.compile(b"f\\(oo\\)", nmatch=2, cflags=PyCRegexCFlag.REG_ICASE)
    result = r.match(b"fOo")
    assert result == 0
    s = r.span()
    assert len(s) == 2
    assert s[0] == (0, 3)
    assert s[1] == (1, 3)
