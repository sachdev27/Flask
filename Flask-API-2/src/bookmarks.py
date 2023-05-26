from flask import Blueprint



bookmarks = Blueprint("bookmarks",__name__,url_prefix="/api/v1/bookmark")


@bookmarks.get("/")
def register():
    return []
