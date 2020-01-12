from dataclasses import dataclass
from enum import Enum
import logging
import re
from typing import Dict, Match

from pelican import signals
from pelican.contents import Article
from pelican.generators import ArticlesGenerator

XREF_RE = re.compile(
    r"\[xref:([a-zA-Z_-]+)(?:\| ?title=([^|\n\r]+))?(?:\| ?blank=([01]))?\]"
)

logger = logging.getLogger(__name__)


class Status(Enum):
    PUBLISHED = 1
    DRAFT = 2
    HIDDEN = 3


@dataclass
class Xref:
    href: str
    status: Status


class PelicanXref:
    def __init__(self, generator: ArticlesGenerator):
        self.generator = generator
        self.references = None

    def process(self):
        self.references = self._get_references()

        article: Article
        for article in self.generator.articles:
            article._content = self._replace_references(
                article._content, article.title, self.references
            )

        draft: Article
        for draft in self.generator.drafts:
            draft._content = self._replace_references(
                draft._content, draft.title, self.references
            )

    def _get_references(self) -> Dict[str, Xref]:
        references = dict()
        for article in self.generator.articles:
            if hasattr(article, "xref"):
                references[article.xref] = Xref(article.url, Status.PUBLISHED)
        for draft in self.generator.drafts:
            if hasattr(draft, "xref"):
                references[draft.xref] = Xref(draft.url, Status.DRAFT)

        return references

    def _replace_references(
        self,
        content: str,
        article_title: str,
        references: Dict[str, Xref],
        status: Status,
    ):
        def replace_reference(match: Match) -> str:
            xref_key = match.group(1)
            title = match.group(3) if match.group(3) else article_title
            blank = (
                ' target="_blank"' if match.group(5) and match.group(5) == "1" else ""
            )
            reference = references[xref_key]

            print(f"href: {reference.href}")

            return f"<a href=/{reference.href}{blank}>{title}</a>"

        return XREF_RE.sub(replace_reference, content)


def pelican_xref(generator: ArticlesGenerator):
    xref = PelicanXref(generator)
    xref.process()


def register():
    signals.article_generator_finalized.connect(pelican_xref)
