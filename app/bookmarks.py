from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import validators
from app.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from app.database import Bookmark, db
from flask_jwt_extended import get_jwt_identity, jwt_required

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route("/", methods=['GET', 'POST'])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'GET':
        return render_template('bookmarks_get.html')

    if request.method == 'POST':
        return render_template('bookmarks_post.html')

#         body = request.get_json().get('body', '')
#         url = request.get_json().get('url', '')
#
#         if not validators.url(url):
#             return jsonify({
#                 'error': 'Enter a valid URL'
#             }), HTTP_400_BAD_REQUEST
#
#         if Bookmark.query.filter_by(url=url).first():
#             return jsonify({
#                 'error': 'URL already exists'
#             }), HTTP_409_CONFLICT
#
#         bookmark = Bookmark(
#             url=url,
#             body=body,
#             user_id=current_user
#         )
#
#         db.session.add(bookmark)
#         db.session.commit()
#         return redirect(url_for('bookmarks_post.html'))

        # return jsonify({
        #     'id': bookmark.id,
        #     'url': bookmark.url,
        #     'short_url': bookmark.short_url,
        #     'visit': bookmark.visits,
        #     'body': bookmark.body,
        #     'created_at': bookmark.created_at,
        #     'updated_at': bookmark.updated_at
        # }), HTTP_201_CREATED
    # else:
    #     return render_template('bookmarks_get.html')
    #     bookmarks = Bookmark.query.filter_by(user_id=current_user)
    #
    #     data = []
    #
    #     for bookmark in bookmarks:
    #         data.append({
    #             'id': bookmark.id,
    #             'url': bookmark.url,
    #             'short_url': bookmark.short_url,
    #             'visit': bookmark.visits,
    #             'body': bookmark.body,
    #             'created_at': bookmark.created_at,
    #             'updated_at': bookmark.updated_at
    #         })
    #     return render_template('bookmarks_get.html', bookmarks=data)

        # return jsonify({'data': data}), HTTP_200_OK


@bookmarks.get("/abc")
def get_abc():
    return {"bookmarks": 'abc'}
