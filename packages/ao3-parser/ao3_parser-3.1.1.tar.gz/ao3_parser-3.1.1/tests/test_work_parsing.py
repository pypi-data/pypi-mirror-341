import AO3Parser
import pickle


def writePickledWork(filename: str, page: AO3Parser.Work):
    with open(filename, 'wb+') as write_page:
        pickle.dump(page, write_page)

def readPickledWork(filename: str) -> AO3Parser.Work:
    with open(filename, 'rb') as read_page:
        return pickle.load(read_page)

def testParsing():
    work_pickled = readPickledWork("test_work.parsed")
    with open(file="test_work.html", mode='rb') as read_html:
        work_parsed = AO3Parser.Work.FromHTML(read_html.read())

    assert work_pickled.ID == work_parsed.ID
    assert work_pickled.Title == work_parsed.Title
    assert work_pickled.Authors == work_parsed.Authors
    assert work_pickled.Fandoms == work_parsed.Fandoms
    assert work_pickled.Summary == work_parsed.Summary

    assert work_pickled.Language == work_parsed.Language
    assert work_pickled.Words == work_parsed.Words
    assert work_pickled.Chapters == work_parsed.Chapters
    assert work_pickled.Expected_Chapters == work_parsed.Expected_Chapters
    assert work_pickled.Comments == work_parsed.Comments
    assert work_pickled.Kudos == work_parsed.Kudos
    assert work_pickled.Bookmarks == work_parsed.Bookmarks
    assert work_pickled.Hits == work_parsed.Hits
    assert work_pickled.Updated == work_parsed.Updated

    assert work_pickled.Rating == work_parsed.Rating
    assert work_pickled.Categories == work_parsed.Categories
    assert work_pickled.Warnings == work_parsed.Warnings
    assert work_pickled.Completed == work_parsed.Completed

    assert work_pickled.Relationships == work_parsed.Relationships
    assert work_pickled.Characters == work_parsed.Characters
    assert work_pickled.Additional_Tags == work_parsed.Additional_Tags

    assert work_pickled.Published == work_parsed.Published


if __name__ == "__main__":
    testParsing()
