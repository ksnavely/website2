"""
_blog_

Create/read blog posts from a database.
"""
import arrow
from bson.objectid import ObjectId
from pymongo import MongoClient as MongoClient


CLIENT = None


# Public interface


def create_post(title, author, text, tags=None):
    tags = tags or []
    post = {
        "title": title,
        "author": author,
        "text": text,
        "date": arrow.utcnow().for_json(),
        "tags": tags,
    }
    return _get_blog_posts_collection().insert_one(post)


def get_posts(count=None, date=None, skip=None):
    """
    Return all blog posts, sorted by date. A basic pagination is available
    via the count and skip parameters.

    The date and count/skip features are mutually exlusive.

    :param int count: How many posts to return.
    :param str date: A date substring for a regex used in the mongo
        find like "2016-3"
    :param int skip: The number of date sorted posts to skip before returning count posts.
    """
    if date is not None:
        cursor = _get_blog_posts_collection().find({"date": {"$regex": date}})
    else:
        cursor = _get_blog_posts_collection().find()

    blogs = sorted(list(cursor), key=lambda x: x["date"], reverse=True)

    if date is None:
        if skip is not None:
            blogs = blogs[skip:]
        if count is not None:
            blogs = blogs[:count]

    return blogs


def get_post(post_id):
    """ "
    Get a single post.

    :param str post_id: The mongo id for the blog post.

    :returns: A dict of post attributes, or None if post_id is not
        found in mongo.
    """
    if ObjectId.is_valid(post_id):
        post = _get_blog_posts_collection().find_one({"_id": ObjectId(post_id)})
    else:
        post = None

    return post


def update_post(post_id, title, author, text, date, tags):
    if not ObjectId.is_valid(post_id):
        raise Exception("blog.update_post: Invalid post_id.")

    tags = tags or []
    selector = {"_id": ObjectId(post_id)}
    post = {"title": title, "author": author, "text": text, "date": date, "tags": tags}
    return _get_blog_posts_collection().update_one(selector, {"$set": post})


# Private interface


def _client():
    global CLIENT
    if CLIENT is None:
        CLIENT = MongoClient()
    return CLIENT


def _get_blog_posts_collection():
    return _client().blog.posts
