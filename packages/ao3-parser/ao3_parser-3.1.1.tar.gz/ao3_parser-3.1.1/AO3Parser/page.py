from .extra import RateLimitException, FormatException
from .params import Params
from .work import Work

import bs4
from datetime import datetime

class Page:
    Total_Works: int
    Works: list[Work]


    def __init__(self, html: bytes):
        if html == b"Retry later\n":
            raise RateLimitException()
        html = bs4.BeautifulSoup(html, "html.parser")

        html = html.find("div", id="main")
        if not html:
            raise FormatException("Missing div main")

        self.Works = []
        if html.find('p').text.strip() == "No results found. You may want to edit your search to make it less specific.":
            self.Total_Works = 0
            return
        self.Total_Works = int(html.find("h3", class_="heading").text.strip()[0:-9].replace(',', ''))

        for work in html.findAll(role="article"):
            authors: list[str] = []
            for author in work.find("h4", class_="heading").findAll("a", rel="author"):
                authors.append(author.text)

            fandoms: list[str] = []
            for fandom in work.find("h5", class_="fandoms heading").findAll("a", class_="tag"):
                fandoms.append(fandom.text)

            summary: str = ""
            summary_block = work.find("blockquote", class_="userstuff summary")
            if summary_block:
                for paragraph in summary_block.findAll("p"):
                    for child in paragraph.children:
                        if type(child) == bs4.Tag and child.name == "br":
                            summary += '\n'
                        else:
                            summary += child.text
                    summary += '\n'
            del summary_block

            stats = work.find(class_="stats")
            chapters, expected_chapters = stats.find("dd", class_="chapters").text.split('/')

            req_tags = work.find("ul", class_="required-tags").findAll("span", class_="text")

            tags = work.find("ul", class_="tags commas").findAll("li")
            relationships: list[str] = []
            characters: list[str] = []
            freeforms: list[str] = []
            for tag in tags:
                name = tag.find("a", class_="tag").text
                if tag["class"] == ['relationships']:
                    relationships.append(name)
                elif tag["class"] == ['characters']:
                    characters.append(name)
                elif tag["class"] == ['freeforms']:
                    freeforms.append(name)

            def parseStats(stat: bs4.element.Tag | None) -> int | None:
                return int(stat.text.replace(',', '')) if stat and stat.text else None

            self.Works.append(
                Work(int(work["id"].split('_')[1]),                                             # ID
                work.find("a").text,                                                            # Title
                authors,                                                                        # Authors
                fandoms,                                                                        # Fandoms
                summary.strip() if summary else None,                                           # Summary
                stats.find("dd", class_="language").text,                                       # Language
                parseStats(stats.find("dd", class_="words")),                                   # Words
                int(chapters.replace(',', '')),                                                 # Chapters
                int(expected_chapters.replace(',', '')) if expected_chapters != '?' else None,  # Expected Chapters
                parseStats(stats.find("dd", class_="comments")),                                # Comments
                parseStats(stats.find("dd", class_="kudos")),                                   # Kudos
                parseStats(stats.find("dd", class_="bookmarks")),                               # Bookmarks
                parseStats(stats.find("dd", class_="hits")),                                    # Hits
                datetime.strptime(work.find(class_="datetime").text, "%d %b %Y"),               # UpdateDate
                Params.parseRating(req_tags[0].text),                                           # Rating
                Params.parseCategories(req_tags[2].text.split(", ")),                           # Categories
                Params.parseWarnings(req_tags[1].text.split(", ")),                             # Warnings
                True if work.find("span", class_="complete-yes iswip") else False,              # Completed
                relationships, characters, freeforms))                                          # Tags
