from app import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')
        load_only = ('password',)
    
class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'date_created', 'user_id')

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

class PostCategorySchema(ma.Schema):
    post = fields.Nested('PostSchema', exclude=('categories',))
    category = fields.Nested('CategorySchema')

class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'content', 'date_created', 'post_id', 'user_id')
