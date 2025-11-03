from app.services.supabase import get_supabase


def search_posts(book_title: str, author: str, publisher: str, location: str, min_price: int, max_price: int):
    supabase = get_supabase()
    
    response = supabase.table("posts").select("*").text_search("book_title", f"'{book_title}'").execute().data
    
    if author:
        response = response.filter(lambda x: x["author"] == author)
    if publisher:
        response = response.filter(lambda x: x["publisher"] == publisher)
    if location:
        response = response.filter(lambda x: x["location"] == location)
    if min_price:
        response = response.filter(lambda x: x["price"] >= min_price)
    if max_price:
        response = response.filter(lambda x: x["price"] <= max_price)
    return response
    