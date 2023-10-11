
# Imports que son nativos del Framework y Librerias
from app import app, db
from flask import (
    jsonify,
    redirect,
    request,
    url_for,
)


# Imports de variables generadas por nosotros
from app.models.models import (
    User, 
    Post,
    Category,
    post_category,
    Comment,

)
from app.schemas.schema import (
    UserSchema,
    PostSchema,
    CategorySchema,
    PostCategorySchema,
    CommentSchema
)

from flask.views import MethodView

class UserView(MethodView):
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            return UserSchema(many=True).jsonify(users)
        else:
            user = User.query.get_or_404(user_id)
            return UserSchema().jsonify(user)

    def post(self):
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return UserSchema().jsonify(new_user)

    
app.add_url_rule('/user', view_func=UserView.as_view('user_api'))
app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('single_user_api'))

