from typing import Match, Optional

from pelican_xref.pelican_xref import (
    XREF_RE,
    Xref,
    _find_references,
    _replace_references,
)
import pytest


@pytest.mark.parametrize(
    "md_input,expected",
    [
        ("[xref:abc]", ["abc", None, None]),
        ('[xref:abc title="abcd"]', ["abc", "abcd", None]),
        ('[xref:abc title="abcd" blank=0]', ["abc", "abcd", "0"]),
        ('[xref:abc title="abcd" blank=1]', ["abc", "abcd", "1"]),
        ('[xref:abc title="abcd" blank=1]', ["abc", "abcd", "1"]),
        ("[xref:abc blank=1]", ["abc", None, "1"]),
    ],
)
def test_xref_re(md_input, expected):
    # The first group contains the original input
    expected.insert(0, md_input)
    expected = tuple(expected)

    match: Optional[Match[str]] = XREF_RE.match(md_input)
    assert match.groups() == expected


def test_find_references_on_article__xref_attribute_set(
    articles_generator, article_with_xref
):
    articles_generator.articles.append(article_with_xref)

    references = _find_references(articles_generator)

    assert len(references) == 1
    assert references["abcd"] == Xref(
        "hello-world.html", "published", "First article with xref"
    )


def test_find_references_on_article__xref_attribute_not_set(
    articles_generator, article
):
    articles_generator.articles.append(article)

    references = _find_references(articles_generator)

    assert len(references) == 0


def test_find_references_on_draft__xref_attribute_set(
    articles_generator, article_with_xref
):
    article_with_xref.status = "draft"
    articles_generator.drafts.append(article_with_xref)

    references = _find_references(articles_generator)

    assert len(references) == 1
    assert references["abcd"] == Xref(
        "hello-world.html", "draft", "First article with xref"
    )


def test_find_references_on_draft__xref_attribute_not_set(articles_generator, article):
    article.status = "draft"
    articles_generator.drafts.append(article)

    references = _find_references(articles_generator)

    assert len(references) == 0


@pytest.mark.parametrize(
    "content,expected",
    [
        (
            'something [xref:abcd title="Hello, world"] amazing',
            'something <a href="/hello-world.html">Hello, world</a> amazing',
        ),
        (
            "something [xref:abcd] amazing",
            'something <a href="/hello-world.html">First article with xref</a> amazing',  # Uses title from referenced article
        ),
    ],
)
def test_replace_references__reference_replaced(
    article, articles_generator, article_with_xref, content, expected
):
    article._content = content

    articles_generator.drafts.append(article)
    articles_generator.drafts.append(article_with_xref)

    references = _find_references(articles_generator)

    _replace_references(article, references)

    assert article_with_xref._content == expected


def test_replace_references__reference_not_found(
    articles_generator, article, logger_warning_mock
):
    article._content = 'something [xref:abcd title="Hello, world"] amazing'

    articles_generator.drafts.append(article)

    references = dict()

    _replace_references(article, references)

    assert article._content == 'something [xref:abcd title="Hello, world"] amazing'
    logger_warning_mock.assert_called_once_with("No article found with xref 'abcd'")


def test_replace_references__reference_to_draft_in_published_article(
    article, logger_warning_mock
):
    article._content = 'something [xref:abcd title="Hello, world"] amazing'
    references = {"abcd": Xref("hello-world.html", "draft", "The title")}

    _replace_references(article, references)

    assert (
        article._content
        == 'something <a href="/hello-world.html">Hello, world</a> amazing'
    )

    logger_warning_mock.assert_called_once_with(
        "Xref 'abcd' belongs to a draft, but it is used in a published article."
    )


def test_replace_references__target_blank(article, logger_warning_mock):
    article._content = 'something [xref:abcd title="Hello, world" blank=1] amazing'
    references = {"abcd": Xref("hello-world.html", "published", "The title")}

    _replace_references(article, references)

    assert (
        article._content
        == 'something <a href="/hello-world.html" target="_blank">Hello, world</a> amazing'
    )
