import arrow
from flask import jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from website import __version__, blog


COUNT = 5
REQUIRED_CREATE_FIELDS = ["title", "tags", "text", "author"]
REQUIRED_UPDATE_FIELDS = ["title", "tags", "text", "author", "date"]
SKIP = 0


def index():
    """
    Returns the frontpage.
    """
    count = request.args.get("count", COUNT)
    date = request.args.get("date")
    skip = request.args.get("skip", SKIP)

    try:
        if count is not None:
            count = int(count)
        if skip is not None:
            skip = int(skip)
        if date is not None:
            arrow.get(date)
    except ValueError:
        return ("Invalid count or skip specified.", 400)
    except arrow.parser.ParserError:
        return ("Invalid date specified.", 400)

    return render_template(
        "index.html",
        blog_posts=blog.get_posts(count=count, date=date, skip=skip),
        count=count,
        skip=skip,
    )


def get_blog_entry(post_id):
    """
    Render a single blog post.

    :param str post_id: The blog post mongo id
    """
    post = blog.get_post(post_id)

    if post is not None:
        post["_id"] = post_id  # don't render the objectid

    return render_template("get_post.html", post=post)


@login_required
def create_blog_entry():
    """
    View the new blog post page.
    """
    return render_template(
        "create_post.html",
    )


@login_required
def update_blog_entry(post_id):
    """
    View the update-blog-post page.

    :param str post_id: The blog post mongo id
    """
    post = blog.get_post(post_id)

    if post is not None:
        post["_id"] = post_id  # don't render the objectid

    return render_template("update_post.html", post=post)


@login_required
def create_blog_entry_submit():
    """
    Creates a new blog post.
    """
    if not request.form:
        return ("create_blog_entry: Blog entry form data is required.", 404)

    if not all([r in request.form.keys() for r in REQUIRED_CREATE_FIELDS]):
        return (
            "create_blog_entry: Blog entries require the following"
            " fields: {0}".format(REQUIRED_CREATE_FIELDS)
        ), 404

    p = request.form
    tags = [t.strip() for t in p["tags"].split(",")]
    blog.create_post(p["title"], p["author"], p["text"], tags=tags)

    return redirect(url_for("index", _external=True, _scheme="https"))


@login_required
def update_blog_entry_submit(post_id):
    """
    Updates an existing blog post.
    """
    if not request.form:
        return ("update_blog_entry: Blog entry form data is required.", 404)

    if not all([r in request.form.keys() for r in REQUIRED_UPDATE_FIELDS]):
        return (
            "update_blog_entry: Blog entries require the following"
            " fields: {0}, given: {1}".format(REQUIRED_UPDATE_FIELDS, request.form)
        ), 404

    p = request.form
    tags = [t.strip() for t in p["tags"].split(",")]
    blog.update_post(post_id, p["title"], p["author"], p["text"], p["date"], tags)

    return redirect(url_for("index", _external=True, _scheme="https"))
