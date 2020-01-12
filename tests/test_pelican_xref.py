from typing import Match, Optional

import pytest

from pelican_xref import XREF_RE


@pytest.mark.parametrize(
    "md_input,expected",
    [
        ("[xref:abc]", ("abc", None, None)),
        ("[xref:abc| title=abcd]", ("abc", "abcd", None)),
        ("[xref:abc| title=abcd| blank=0]", ("abc", "abcd", "0")),
        ("[xref:abc| title=abcd| blank=1]", ("abc", "abcd", "1")),
        ("[xref:abc|title=abcd|blank=1]", ("abc", "abcd", "1")),
        ("[xref:abc| blank=1]", ("abc", None, "1")),
    ],
)
def test_xref_re(md_input, expected):
    match: Optional[Match[str]] = XREF_RE.match(md_input)
    assert match.groups() == expected
