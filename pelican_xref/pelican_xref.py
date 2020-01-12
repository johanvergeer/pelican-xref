from dataclasses import dataclass
import logging
import re
from typing import Dict, Match

from pelican import signals
from pelican.contents import Article
from pelican.generators import ArticlesGenerator

XREF_RE = re.compile(
    # r"(\[xref:([a-zA-Z0-9_-]+)(?:\| ?title=([^|\n\r]+))?(?:\| ?blank=([01]))?\])"
    r'(\[xref:([a-zA-Z0-9_-]+)(?: +title="([^"\n\r]+)")?(?: +blank=([01]))?\])'
)

logger = logging.getLogger(__name__)


@dataclass
class Xref:
    href: str
    """relative url to the article or draft"""
    status: str
    """'draft' or 'published'"""


def _find_references(generator: ArticlesGenerator) -> Dict[str, Xref]:
    """Finds the `xref` attribute value of each article if it exists"""
    references = dict()
    article: Article
    for article in generator.articles:
        if hasattr(article, "xref"):
            references[article.xref] = Xref(article.url, "published")
    draft: Article
    for draft in generator.drafts:
        if hasattr(draft, "xref"):
            references[draft.xref] = Xref(draft.url, "draft")

    return references


def _replace_references(article: Article, references: Dict[str, Xref],) -> None:
    """replaces xrefs in the article with <a> tags.

    Args:
        article: Article that needs to have xref elements replaced
        references: dictionary containing references to other articles

    Returns:
        None

    """

    def replace_reference(match: Match) -> str:
        xref_key = match.group(2)
        title = match.group(3) if match.group(3) else article.title
        blank = ' target="_blank"' if match.group(4) and match.group(4) == "1" else ""
        reference = references.get(xref_key, None)

        if reference is None:
            logger.warning(f"No article found with xref '{xref_key}'")
            return match.group(1)  # original input

        if reference.status == "draft" and article.status == "published":
            logger.warning(
                f"Xref '{xref_key}' belongs to a draft, but it is used in a published article."
            )

        return f'<a href="/{reference.href}"{blank}>{title}</a>'

    article._content = XREF_RE.sub(replace_reference, article._content)


def pelican_xref(generator: ArticlesGenerator):
    references = _find_references(generator)

    article: Article
    for article in generator.articles:
        _replace_references(article, references)

    draft: Article
    for draft in generator.drafts:
        _replace_references(draft, references)


def register():
    signals.article_generator_finalized.connect(pelican_xref)
