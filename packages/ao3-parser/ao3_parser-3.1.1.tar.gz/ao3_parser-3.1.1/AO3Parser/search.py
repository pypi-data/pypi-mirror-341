from .extra import Extra
from .params import Params

import urllib.parse

class SearchWorks:
    Any_Field: str | None
    Title: str | None
    Author: str | None
    Date: str | None

    Completion_Status: Params.Completion
    Crossovers: Params.Crossovers
    Single_Chapter: bool

    Words_Count: str | None

    Fandoms: list[str] | None
    Rating: Params.Rating | None
    Warnings: list[Params.Warning] | None
    Categories: list[Params.Category] | None

    Characters: list[str] | None
    Relationships: list[str] | None
    Additional_Tags: list[str] | None

    Hits_Count: str | None
    Kudos_Count: str | None
    Comments_Count: str | None
    Bookmarks_Count: str | None

    Sort_by: Params.Sort
    Sort_Direction: Params.Direction

    def __init__(self, Any_Field: str | None = None, Title: str | None = None, Author: str | None = None, Date: str | None = None,
                 Completion_Status: Params.Completion = Params.Completion.All, Crossovers: Params.Crossovers = Params.Crossovers.Include, Single_Chapter: bool = False,
                 Words_Count: str | None = None, # TODO: Add support for language
                 Fandoms: list[str] | None = None, Rating: Params.Rating | None = None,
                 Warnings: list[Params.Warning] | None = None, Categories: list[Params.Category] | None = None,
                 Characters: list[str] | None = None, Relationships: list[str] | None = None, Additional_Tags: list[str] | None = None,
                 Hits_Count: str | None = None, Kudos_Count: str | None = None, Comments_Count: str | None = None, Bookmarks_Count: str | None = None,
                 Sort_by: Params.Sort = Params.Sort.Best_Match, Sort_Direction: Params.Direction = Params.Direction.Descending):
        self.Any_Field = Any_Field
        self.Title = Title
        self.Author = Author
        self.Date = Date

        self.Completion_Status = Completion_Status
        self.Crossovers = Crossovers
        self.Single_Chapter = Single_Chapter

        self.Words_Count = Words_Count

        self.Fandoms = Fandoms
        self.Rating = Rating
        self.Warnings = Warnings
        self.Categories = Categories

        self.Characters = Characters
        self.Relationships = Relationships
        self.Additional_Tags = Additional_Tags

        self.Hits_Count = Hits_Count
        self.Kudos_Count = Kudos_Count
        self.Comments_Count = Comments_Count
        self.Bookmarks_Count = Bookmarks_Count

        self.Sort_by = Sort_by
        self.Sort_Direction = Sort_Direction


    def getParams(self, page=1) -> dict:
        params = {
            "page": page,
            "work_search[sort_column]": self.Sort_by.value,
            "work_search[sort_direction]": self.Sort_Direction.value
        }

        if self.Any_Field:
            params["work_search[query]"] = self.Any_Field
        if self.Title:
            params["work_search[title]"] = self.Title
        if self.Author:
            params["work_search[creators]"] = self.Author
        if self.Date:
            params["work_search[revised_at]"] = self.Date

        if self.Completion_Status and self.Completion_Status.value:
            params["work_search[complete]"] = self.Completion_Status.value
        if self.Crossovers and self.Crossovers.value:
            params["work_search[crossover]"] = self.Crossovers.value
        if self.Single_Chapter:
            params["work_search[single_chapter]"] = 1

        if self.Words_Count:
            params["work_search[word_count]"] = self.Words_Count

        if self.Fandoms:
            params["work_search[fandom_names]"] = ','.join(self.Fandoms)
        if self.Rating:
            params["work_search[rating_ids]"] = self.Rating.value
        if self.Warnings:
            params["work_search[archive_warning_ids][]"] = Extra.EnumsToValues(self.Warnings)
        if self.Categories:
            params["work_search[category_ids][]"] = Extra.EnumsToValues(self.Categories)

        if self.Characters:
            params["work_search[character_names]"] = ','.join(self.Characters)
        if self.Relationships:
            params["work_search[relationship_names]"] = ','.join(self.Relationships)
        if self.Additional_Tags:
            params["work_search[freeform_names]"] = ','.join(self.Additional_Tags)

        if self.Hits_Count:
            params["work_search[hits]"] = self.Hits_Count
        if self.Kudos_Count:
            params["work_search[kudos_count]"] = self.Kudos_Count
        if self.Comments_Count:
            params["work_search[comments_count]"] = self.Comments_Count
        if self.Bookmarks_Count:
            params["work_search[bookmarks_count]"] = self.Bookmarks_Count

        return params

    def GetUrl(self, page=1) -> str:
        return f"https://archiveofourown.org/works/search?commit=Search&{urllib.parse.urlencode(self.getParams(page), doseq=True)}"
