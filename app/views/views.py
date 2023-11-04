
# Imports que son nativos del Framework y Librerias
from app import app, db
from flask import (
    jsonify,
    redirect,
    request,
    url_for,
)
from marshmallow import ValidationError

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
        try:
            username = request.json['username']
            email = request.json['email']
            password = request.json['password']

            new_user = User(username=username, email=email, password=password)

            db.session.add(new_user)
            db.session.commit()

            return UserSchema().jsonify(new_user), 201
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400
    
    def put(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            user.username = request.json.get('username', user.username)
            user.email = request.json.get('email', user.email)
            user.password = request.json.get('password', user.password)

            db.session.commit()

            return UserSchema().jsonify(user), 200
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'Usuario eliminado satisfactoriamente'}), 200
        
app.add_url_rule('/user', view_func=UserView.as_view('user_api'))
app.add_url_rule('/user/<int:user_id>', view_func=UserView.as_view('single_user_api'))

class CategoryView(MethodView):
    
    def get(self, category_id=None):
        if category_id == None:
            categories = Category.query.all()
            return CategorySchema(many=True).jsonify(categories)
        else:
            category = Category.query.get_or_404(category_id)
            return CategorySchema().jsonify(category)
    
    def post(self):
        try:
            name = request.json['name']

            new_category = Category(name=name)

            db.session.add(new_category)
            db.session.commit()

            return CategorySchema().jsonify(new_category), 201
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400
        
    def put(self, category_id):
        try:
            category = Category.query.get_or_404(category_id)
            category.name = request.json.get('name', category.name)

            db.session.commit()

            return CategorySchema().jsonify(category), 200
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400
        
    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Categorìa eliminada satisfactoriamente'})

app.add_url_rule('/category', view_func=CategoryView.as_view('category_api'))
app.add_url_rule('/category/<int:category_id>', view_func=CategoryView.as_view('single_category_api'))