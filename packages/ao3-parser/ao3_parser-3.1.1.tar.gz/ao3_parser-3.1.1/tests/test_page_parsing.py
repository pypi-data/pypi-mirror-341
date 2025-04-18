import AO3Parser
import pickle


def writePickledPage(filename: str, page: AO3Parser.Page):
    with open(filename, 'wb+') as write_page:
        pickle.dump(page, write_page)

def readPickledPage(filename: str) -> AO3Parser.Page:
    with open(filename, 'rb') as read_page:
        return pickle.load(read_page)

def testParsing():
    page_pickled = readPickledPage("test_page.parsed")
    with open(file="test_page.html", mode='rb') as read_html:
        page_parsed = AO3Parser.Page(read_html.read())

    assert page_pickled.Total_Works == page_parsed.Total_Works
    assert len(page_pickled.Works) == len(page_parsed.Works)

    for i in range(len(page_pickled.Works)):
        assert page_pickled.Works[i].ID == page_parsed.Works[i].ID
        assert page_pickled.Works[i].Title == page_parsed.Works[i].Title
        assert page_pickled.Works[i].Authors == page_parsed.Works[i].Authors
        assert page_pickled.Works[i].Fandoms == page_parsed.Works[i].Fandoms
        assert page_pickled.Works[i].Summary == page_parsed.Works[i].Summary

        assert page_pickled.Works[i].Language == page_parsed.Works[i].Language
        assert page_pickled.Works[i].Words == page_parsed.Works[i].Words
        assert page_pickled.Works[i].Chapters == page_parsed.Works[i].Chapters
        assert page_pickled.Works[i].Expected_Chapters == page_parsed.Works[i].Expected_Chapters
        assert page_pickled.Works[i].Comments == page_parsed.Works[i].Comments
        assert page_pickled.Works[i].Kudos == page_parsed.Works[i].Kudos
        assert page_pickled.Works[i].Bookmarks == page_parsed.Works[i].Bookmarks
        assert page_pickled.Works[i].Hits == page_parsed.Works[i].Hits
        assert page_pickled.Works[i].Updated == page_parsed.Works[i].Updated

        assert page_pickled.Works[i].Rating == page_parsed.Works[i].Rating
        assert page_pickled.Works[i].Categories == page_parsed.Works[i].Categories
        assert page_pickled.Works[i].Warnings == page_parsed.Works[i].Warnings
        assert page_pickled.Works[i].Completed == page_parsed.Works[i].Completed

        assert page_pickled.Works[i].Relationships == page_parsed.Works[i].Relationships
        assert page_pickled.Works[i].Characters == page_parsed.Works[i].Characters
        assert page_pickled.Works[i].Additional_Tags == page_parsed.Works[i].Additional_Tags


if __name__ == "__main__":
    testParsing()
