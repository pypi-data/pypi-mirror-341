# Pycregex, C-style POSIX.2 BRE syntax regex for Python
# Copyright (C) 2025  Nikolaos Chatzikonstantinou
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import ctypes
import ctypes.util
from enum import IntEnum
from pathlib import Path
import platform

libc_path = ctypes.util.find_library("c")
libc = ctypes.CDLL(libc_path)
ext = {"Linux": ".so", "Darwin": ".dylib", "Windows": ".dll"}.get(
    platform.system(), ".so"
)
stub_path = Path(__file__).parent / f"stub{ext}"
stub = ctypes.CDLL(str(stub_path))
libc.free.restype = None
libc.regfree.restype = None
stub.pycregex_make_regex_t.restype = ctypes.c_void_p
stub.pycregex_get_re_nsub.restype = ctypes.c_size_t
stub.pycregex_make_regmatch_t.restype = ctypes.c_void_p
stub.pycregex_get_rm_so.restype = ctypes.c_long
stub.pycregex_get_rm_eo.restype = ctypes.c_long


class PyCRegexCFlag(IntEnum):
    """The flags to compile() (underlying 'regcomp')."""

    REG_EXTENDED = stub.pycregex_flag_REG_EXTENDED()
    REG_ICASE = stub.pycregex_flag_REG_ICASE()
    REG_NOSUB = stub.pycregex_flag_REG_NOSUB()
    REG_NEWLINE = stub.pycregex_flag_REG_NEWLINE()


class PyCRegexEFlag(IntEnum):
    """The flags to match() (underlying 'regexec')."""

    REG_NOTBOL = stub.pycregex_flag_REG_NOTBOL()
    REG_NOTEOL = stub.pycregex_flag_REG_NOTEOL()
    REG_NOMATCH = stub.pycregex_flag_REG_NOMATCH()


class PyCRegexError(IntEnum):
    """Errors that may be returned from compile()"""

    REG_BADBR = stub.pycregex_err_REG_BADBR()
    REG_BADPAT = stub.pycregex_err_REG_BADPAT()
    REG_BADRPT = stub.pycregex_err_REG_BADRPT()
    REG_ECOLLATE = stub.pycregex_err_REG_ECOLLATE()
    REG_ECTYPE = stub.pycregex_err_REG_ECTYPE()
    REG_EESCAPE = stub.pycregex_err_REG_EESCAPE()
    REG_ESUBREG = stub.pycregex_err_REG_ESUBREG()
    REG_EBRACK = stub.pycregex_err_REG_EBRACK()
    REG_EPAREN = stub.pycregex_err_REG_EPAREN()
    REG_EBRACE = stub.pycregex_err_REG_EBRACE()
    REG_ERANGE = stub.pycregex_err_REG_ERANGE()
    REG_ESPACE = stub.pycregex_err_REG_ESPACE()


class Pattern:
    """A regex pattern, including its match information."""

    def __init__(self, nmatch: int):
        self.r = stub.pycregex_make_regex_t()
        self.m_span = []
        if self.r is None:
            raise MemoryError("Out of memory in pycregex_make_regex_t()!")
        if nmatch <= 0:
            self.nmatch = 0
            self.m = ctypes.c_void_p(None)
        else:
            self.nmatch = nmatch
            self.m = stub.pycregex_make_regmatch_t(ctypes.c_size_t(self.nmatch))
            if self.m is None:
                raise MemoryError("Out of memory in pycregex_make_regmatch_t()!")

    def __del__(self):
        libc.regfree(self.r)
        libc.free(self.r)
        self.r = ctypes.c_void_p(None)
        libc.free(self.m)
        self.m = ctypes.c_void_p(None)

    def search(self, string: bytes, eflags: int = 0):
        """Attempt to search the pattern in the (binary) string."""
        result = libc.regexec(
            self.r,
            ctypes.c_char_p(string),
            ctypes.c_size_t(self.nmatch),
            self.m,
            ctypes.c_int(eflags),
        )
        if result != 0:
            return result
        self.m_span = [
            (stub.pycregex_get_rm_so(self.m, i), stub.pycregex_get_rm_eo(self.m, i))
            for i in range(self.nmatch)
        ]
        return result

    def span(self) -> list[tuple[int, int]]:
        """The list of group spans. First is whole match."""
        return self.m_span


def compile(pattern: bytes, cflags: int = 0, nmatch: int = 0) -> Pattern:
    """Compile a regex pattern."""
    p = Pattern(nmatch)
    err = libc.regcomp(p.r, pattern, ctypes.c_int(cflags))
    if err == 0:
        return p
    elif err == PyCRegexError.REG_BADBR:
        raise RuntimeError(
            "There was an invalid \\{...\\} construct in "
            "the regular expression. A valid \\{...\\} construct "
            "must contain either a single number, or two "
            "numbers in increasing order separated by a comma."
        )
    elif err == PyCRegexError.REG_BADPAT:
        raise RuntimeError("There was a syntax error in the regular expression.")
    elif err == PyCRegexError.REG_BADRPT:
        raise RuntimeError(
            "A repetition operator such as ? or * appeared "
            "in a bad position (with no preceding subexpression "
            "to act on)."
        )
    elif err == PyCRegexError.REG_ECOLLATE:
        raise RuntimeError(
            "The regular expression referred to an invalid "
            "collating element (one not defined in the current "
            "locale for string collation)."
        )
    elif err == PyCRegexError.REG_ECTYPE:
        raise RuntimeError(
            "The regular expression referred to an invalid " "character class name."
        )
    elif err == PyCRegexError.REG_EESCAPE:
        raise RuntimeError("The regular expression ended with \\.")
    elif err == PyCRegexError.REG_ESUBREG:
        raise RuntimeError("There was an invalid number in the '\\DIGIT' " "construct.")
    elif err == PyCRegexError.REG_EBRACK:
        raise RuntimeError(
            "There were unbalanced square brackets in the " "regular expression."
        )
    elif err == PyCRegexError.REG_EPAREN:
        raise RuntimeError(
            "An extended regular expression had unbalanced "
            "parentheses, or a basic regular expression had "
            "unbalanced \\( and \\)."
        )
    elif err == PyCRegexError.REG_EBRACE:
        raise RuntimeError("The regular expression had unbalanced \\{ and \\}.")
    elif err == PyCRegexError.REG_ERANGE:
        raise RuntimeError("One of the endpoints in a range expression was invalid.")
    elif err == PyCRegexError.REG_ESPACE:
        raise MemoryError("'regcomp' ran out of memory.")
    else:
        raise RuntimeError(f"Unknown exception (code {err} from 'regcomp').")
