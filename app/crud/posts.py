from app.services.supabase import get_supabase
from app.schemas.posts import Status


def search_posts(status: Status, book_title: str, author: str, publisher: str, location: str, min_price: int, max_price: int):
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
        if publisher:
            response = [x for x in response if x["publisher"] == publisher]
        if location:
            response = [x for x in response if x["location"] == location]
        if min_price:
            response = [x for x in response if x["price"] >= min_price]
        if max_price:
            response = [x for x in response if x["price"] <= max_price]
        return response

    # Get all posts with status
    else:
        response = (
            supabase.table("posts")
            .select("*")
            .in_("status", [status.value for status in status])
            .execute()
        ).data
        return response
