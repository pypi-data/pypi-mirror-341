from enum import Enum

class Params:
    class Sort(Enum):
        Best_Match = "_score"
        Author = "authors_to_sort_on"
        Title = "title_to_sort_on"
        Created = "created_at"
        Revised = "revised_at"
        Words = "word_count"
        Hits = "hits"
        Kudos = "kudos_count"
        Comments = "comments_count"
        Bookmarks = "bookmarks_count"

    class Direction(Enum):
        Ascending = "asc"
        Descending = "desc"

    class Rating(Enum):
        Not_Rated = 9
        General_Audiences = 10
        Teen_And_Up_Audiences = 11
        Mature = 12
        Explicit = 13

    class Warning(Enum):
        Choose_Not_To_Use_Archive_Warnings = 14
        No_Archive_Warnings_Apply = 16
        Graphic_Depictions_Of_Violence = 17
        Major_Character_Death = 18
        Rape_Non_Con = 19
        Underage_Sex = 20

    class Category(Enum):
        No_Category = -1 # Non-existent ID, used for parsing
        Gen = 21
        F_M = 22
        M_M = 23
        Other = 24
        F_F = 116
        Multi = 2246

    class Crossovers(Enum):
        Include = None
        Exclude = 'F'
        Only = 'T'

    class Completion(Enum):
        All = None
        Complete_Only = 'T'
        InProgress_Only = 'F'


    @staticmethod
    def parseRating(rating: str) -> Rating:
        rating = rating.strip().lower()
        if rating == "general audiences":
            return Params.Rating.General_Audiences
        elif rating == "teen and up audiences":
            return Params.Rating.Teen_And_Up_Audiences
        elif rating == "mature":
            return Params.Rating.Mature
        elif rating == "explicit":
            return Params.Rating.Explicit
        return Params.Rating.Not_Rated

    @staticmethod
    def parseWarning(warning: str) -> Warning:
        warning = warning.strip().lower()
        if warning == "choose not to use archive warnings":
            return Params.Warning.Choose_Not_To_Use_Archive_Warnings
        elif warning == "no archive warnings apply":
            return Params.Warning.No_Archive_Warnings_Apply
        elif warning == "graphic depictions of violence":
            return Params.Warning.Graphic_Depictions_Of_Violence
        elif warning == "major character death":
            return Params.Warning.Major_Character_Death
        elif warning == "rape/non-con":
            return Params.Warning.Rape_Non_Con
        elif warning == "underage sex":
            return Params.Warning.Underage_Sex
        return Params.Warning.No_Archive_Warnings_Apply
    @staticmethod
    def parseWarnings(warnings: list[str]) -> list[Warning]:
        warnings_ids: list[Params.Warning] = []
        for warning in warnings:
            warnings_ids.append(Params.parseWarning(warning))
        return warnings_ids

    @staticmethod
    def parseCategory(category: str) -> Category:
        category = category.strip().lower()
        if category == "no category":
            return Params.Category.No_Category
        elif category == "gen":
            return Params.Category.Gen
        elif category == "f/m":
            return Params.Category.F_M
        elif category == "m/m":
            return Params.Category.M_M
        elif category == "other":
            return Params.Category.Other
        elif category == "f/f":
            return Params.Category.F_F
        elif category == "multi":
            return Params.Category.Multi
        return Params.Category.No_Category
    @staticmethod
    def parseCategories(categories: list[str]) -> list[Category]:
        categories_ids: list[Params.Category] = []
        for category in categories:
            categories_ids.append(Params.parseCategory(category))
        return categories_ids