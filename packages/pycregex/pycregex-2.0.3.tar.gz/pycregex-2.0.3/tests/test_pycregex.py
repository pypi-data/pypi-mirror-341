import pycregex
from pycregex import PyCRegexCFlag


def test_compile():
    p = pycregex.compile(b"f\\(oo\\)")
    assert p.r
    assert not p.m
    assert p.nmatch == 0
    assert not p.span()


def test_compile_nmatch():
    p = pycregex.compile(b"f\\(oo\\)", nmatch=2)
    assert p.r
    assert p.m
    assert p.nmatch == 2
    assert not p.span()


def test_compile_cflags():
    p = pycregex.compile(
        b"f\\(oo\\)", cflags=PyCRegexCFlag.REG_EXTENDED | PyCRegexCFlag.REG_ICASE
    )
    assert p.r
    assert not p.m
    assert p.nmatch == 0
    assert not p.span()


def test_search():
    p = pycregex.compile(b"f\\(oo\\)", nmatch=2)
    result = p.search(b"foo")
    assert result == 0
    s = p.span()
    assert len(s) == 2
    assert s[0] == (0, 3)
    assert s[1] == (1, 3)


def test_search_icase():
    p = pycregex.compile(b"f\\(oo\\)", nmatch=2, cflags=PyCRegexCFlag.REG_ICASE)
    result = p.search(b"fOo")
    assert result == 0
    s = p.span()
    assert len(s) == 2
    assert s[0] == (0, 3)
    assert s[1] == (1, 3)


def test_search_alphabet():
    p = pycregex.compile(b"[a-z]\\+", nmatch=1)
    result = p.search(b"foo")
    assert result == 0
    s = p.span()
    assert len(s) == 1
    assert s[0] == (0, 3)
