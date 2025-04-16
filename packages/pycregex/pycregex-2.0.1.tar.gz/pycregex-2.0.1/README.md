# Pycregex, C-style POSIX BRE (and ERE) syntax regex for Python

This package brings libc's `<regex.h>` API to Python. While Python has [re](https://docs.python.org/3/library/re.html) and there's the [regex](https://pypi.org/project/regex/) package, they do not have the syntax of `<regex.h>`. The simplest example is the regex pattern `f\(oo\)` which is not supported by either of the mentioned packages, because neither supports escaping the parentheses. The syntax of `<regex.h>` is specified in POSIX, see the [Base Specification v8 Regular Expressions chapter](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html).

This is not a glorious API, but if you need it, here it is.

## Example

We search with subgroups, and show how the subgroup begin/end indices are accessed.

```python
import pycregex
# Note that this package only works with binary strings. nmatch is
# number of groups plus one because we must include the entire match.
p = pycregex.compile(b"f\\(oo\\)", nmatch=2)
p.search(b"foo") # ==> 0
p.span() # ==> [(0, 3), (1, 3)]
```
