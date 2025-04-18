from .extra import RateLimitException, FormatException
from .params import Params

import bs4
from datetime import datetime

class Work:
    ID: int
    Title: str
    Authors: list[str]
    Fandoms: list[str]
    Summary: str | None

    Language: str
    Words: int | None
    Chapters: int
    Expected_Chapters: int | None
    Comments: int | None
    Kudos: int | None
    Bookmarks: int | None
    Hits: int | None
    Updated: datetime

    Rating: Params.Rating
    Categories: list[Params.Category]
    Warnings: list[Params.Warning]
    Completed: bool

    Relationships: list[str]
    Characters: list[str]
    Additional_Tags: list[str]

    Published: datetime | None

    def __init__(self, ID: int, Title: str, Authors: list[str], Fandoms: list[str], Summary: str | None,
                 Language: str, Words: int | None, Chapters: int, Expected_Chapters: int | None, Comments: int | None, Kudos: int | None, Bookmarks: int | None, Hits: int | None, Updated: datetime,
                 Rating: Params.Rating, Categories: list[Params.Category], Warnings: list[Params.Warning], Completed: bool,
                 Relationships: list[str], Characters: list[str], Additional_Tags: list[str],
                 Published: datetime | None = None):
        self.ID = ID
        self.Title = Title
        self.Authors = Authors
        self.Fandoms = Fandoms
        self.Summary = Summary

        self.Language = Language
        self.Words = Words
        self.Chapters = Chapters
        self.Expected_Chapters = Expected_Chapters
        self.Comments = Comments
        self.Kudos = Kudos
        self.Bookmarks = Bookmarks
        self.Hits = Hits
        self.Updated = Updated

        self.Rating = Rating
        self.Categories = Categories
        self.Warnings = Warnings
        self.Completed = Completed

        self.Relationships = Relationships
        self.Characters = Characters
        self.Additional_Tags = Additional_Tags

        self.Published = Published

    @classmethod
    def FromHTML(cls, html: bytes):
        if html == b"Retry later\n":
            raise RateLimitException()
        html = bs4.BeautifulSoup(html, "html.parser")

        html = html.find("div", id="main")
        if not html:
            raise FormatException("Missing div main")

        authors: list[str] = []
        for author in html.find("h3", class_="byline heading").findAll("a", rel="author"):
            authors.append(author.text)

        meta = html.find("dl", class_="work meta group")

        warnings: list[str] = []
        categories: list[str] = []
        fandoms: list[str] = []
        relationships: list[str] = []
        characters: list[str] = []
        freeforms: list[str] = []
        for tag_group in meta.findAll("dd", class_="tags"):
            tag_type = tag_group["class"][0]
            for tag in tag_group.find("ul", class_="commas").findAll("li"):
                if tag_type == "warning":
                    warnings.append(tag.text)
                elif tag_type == "category":
                    categories.append(tag.text)
                elif tag_type == "fandom":
                    fandoms.append(tag.text)
                elif tag_type == "relationship":
                    relationships.append(tag.text)
                elif tag_type == "character":
                    characters.append(tag.text)
                elif tag_type == "freeform":
                    freeforms.append(tag.text)

        stats = html.find("dd", class_="stats")
        chapters, expected_chapters = stats.find("dd", class_="chapters").text.split('/')

        summary: str = ""
        summary_block = html.find("div", class_="summary module").find("blockquote", class_="userstuff")
        if summary_block:
            for paragraph in summary_block.findAll("p"):
                for child in paragraph.children:
                    if type(child) == bs4.Tag and child.name == "br":
                        summary += '\n'
                    else:
                        summary += child.text
                summary += '\n'
        del summary_block

        def parseStats(stat: bs4.element.Tag | None) -> int | None:
            return int(stat.text.replace(',', '')) if stat and stat.text else None

        published = datetime.strptime(stats.find("dd", class_="published").text, "%Y-%m-%d")
        updated = stats.find("dd", class_="status")

        return cls(
            int(html.find("div", id="feedback").find("form", id="new_kudo").find("input", id="kudo_commentable_id")["value"]),  # ID
            html.find("h2", class_="title heading").text.strip(),                             # Title
            authors,                                                                          # Authors
            fandoms,                                                                          # Fandoms
            summary.strip() if summary else None,                                             # Summary
            meta.find("dd", class_="language").text.strip(),                                  # Language
            parseStats(stats.find("dd", class_="words")),                                     # Words
            int(chapters.replace(',', '')),                                                   # Chapters
            int(expected_chapters.replace(',', '')) if expected_chapters != '?' else None,    # Expected Chapters
            parseStats(stats.find("dd", class_="comments")),                                  # Comments
            parseStats(stats.find("dd", class_="kudos")),                                     # Kudos
            parseStats(stats.find("dd", class_="bookmarks")),                                 # Bookmarks
            parseStats(stats.find("dd", class_="hits")),                                      # Hits
            datetime.strptime(updated.text, "%Y-%m-%d") if updated else published,            # Updated
            Params.parseRating(meta.find("dd", class_="rating tags").text.strip()),           # Rating
            Params.parseCategories(categories),                                               # Categories
            Params.parseWarnings(warnings),                                                   # Warnings
            chapters == expected_chapters,                                                    # Completed
            relationships, characters, freeforms,                                             # Tags
            published                                                                         # Published
        )

    def __str__(self):
        return f"<Work_{self.ID}>"

    def __repr__(self):
        return self.__str__()