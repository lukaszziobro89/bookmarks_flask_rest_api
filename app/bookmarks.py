from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
import validators
from app.database import Bookmark, db
from flask_jwt_extended import get_jwt_identity, jwt_required

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route("/", methods=['GET', 'POST'])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()

    if request.method == 'POST':

        url = request.form['input-url']
        body = request.form['input-body']

        if not validators.url(url):
            flash("Not a valid URL (example: http://www.abc.com)", 'warning'), 304
            return render_template('bookmarks_post.html')

        if Bookmark.query.filter_by(url=url).first():
            flash("Bookmark already exists", 'warning'), 304
            return render_template('bookmarks_post.html')

        bookmark = Bookmark(
            url=url,
            body=body,
            user_id=current_user
        )

        db.session.add(bookmark)
        db.session.commit()
        flash("Bookmark added!", 'success'), 302
        return render_template('bookmarks_post.html')

    else:
        bookmarks_list = Bookmark.query.filter_by(user_id=current_user)

        data = []

        for bookmark in bookmarks_list:
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visit': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
            })
        return render_template('bookmarks_get.html', bookmarks=data)


@bookmarks.post("/bookmark")
@jwt_required()
def show_add_bookmark_form():
    return render_template('bookmarks_post.html')
