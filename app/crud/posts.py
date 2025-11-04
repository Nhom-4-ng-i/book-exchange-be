from app.services.supabase import get_supabase
from app.schemas.posts import Status, Course, BookStatus, Location


def search_posts(status: Status, book_title: str, author: str, course: Course, book_status: BookStatus, location: Location, min_price: int, max_price: int):
    supabase = get_supabase()

    # Search with filters
    if book_title:
        response = (
            supabase.table("posts")
            .select("*")
            .in_("status", [status.value for status in status])
            .text_search("book_title", f"'{book_title}'")
            .execute()
        ).data

        if author:
            response = [x for x in response if x["author"] == author]
        if course:
            response = [x for x in response if x["course"] == course]
        if book_status:
            response = [x for x in response if x["book_status"] == book_status]
        if location:
            response = [x for x in response if x["location"] == location]
        if min_price:
            response = [x for x in response if x["price"] >= min_price]
        if max_price:
            response = [x for x in response if x["price"] <= max_price]
        return response

    # Search all posts with
    else:
        response = (
            supabase.table("posts")
            .select("*")
            .in_("status", [status.value for status in status])
            .execute()
        ).data
        return response
