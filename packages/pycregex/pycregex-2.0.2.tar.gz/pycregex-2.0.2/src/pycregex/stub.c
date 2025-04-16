/* Stub functions for libc's regex header, useful for Python FFI.
 * Copyright (C) 2025  Nikolaos Chatzikonstantinou
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <regex.h>
#include <stdlib.h>

void *pycregex_make_regex_t(void) { return malloc(sizeof(regex_t)); }
size_t pycregex_get_re_nsub(const regex_t *r) { return r->re_nsub; }
void *pycregex_make_regmatch_t(size_t n) {
  return malloc(n * sizeof(regmatch_t));
}
long pycregex_get_rm_so(regmatch_t *p, size_t i) { return (long)p[i].rm_so; }
long pycregex_get_rm_eo(regmatch_t *p, size_t i) { return (long)p[i].rm_eo; }
/* Error codes */
int pycregex_err_REG_BADBR(void) { return REG_BADBR; }
int pycregex_err_REG_BADPAT(void) { return REG_BADPAT; }
int pycregex_err_REG_BADRPT(void) { return REG_BADRPT; }
int pycregex_err_REG_ECOLLATE(void) { return REG_ECOLLATE; }
int pycregex_err_REG_ECTYPE(void) { return REG_ECTYPE; }
int pycregex_err_REG_EESCAPE(void) { return REG_EESCAPE; }
int pycregex_err_REG_ESUBREG(void) { return REG_ESUBREG; }
int pycregex_err_REG_EBRACK(void) { return REG_EBRACK; }
int pycregex_err_REG_EPAREN(void) { return REG_EPAREN; }
int pycregex_err_REG_EBRACE(void) { return REG_EBRACE; }
int pycregex_err_REG_ERANGE(void) { return REG_ERANGE; }
int pycregex_err_REG_ESPACE(void) { return REG_ESPACE; }
/* Flag codes for regcomp. */
int pycregex_flag_REG_EXTENDED(void) { return REG_EXTENDED; }
int pycregex_flag_REG_ICASE(void) { return REG_ICASE; }
int pycregex_flag_REG_NOSUB(void) { return REG_NOSUB; }
int pycregex_flag_REG_NEWLINE(void) { return REG_NEWLINE; }
/* Flag codes for regexec. */
int pycregex_flag_REG_NOTBOL(void) { return REG_NOTBOL; }
int pycregex_flag_REG_NOTEOL(void) { return REG_NOTEOL; }
int pycregex_flag_REG_NOMATCH(void) { return REG_NOMATCH; }
