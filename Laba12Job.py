from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

# Определение моделей для базы данных
class AuthorModel(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    books = db.relationship('BookModel', backref='author')

class BookModel(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    category = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    books = db.relationship('BookModel', backref='category_name')

# Запуск создания таблиц
db.create_all()

# Определение полей для сериализации ответов
book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author_id': fields.Integer,
    'category': fields.String,
    'year': fields.Integer,
    'isbn': fields.String,
    'quantity': fields.Integer
}

# Пример ресурса для книги
class BookResource(Resource):
    @marshal_with(book_fields)
    def get(self, book_id):
        book = BookModel.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message="Book not found")
        return book

    @marshal_with(book_fields)
    def post(self):
        # Здесь должен быть код для обработки данных запроса и создания книги
        pass

    @marshal_with(book_fields)
    def put(self, book_id):
        # Здесь должен быть код для обновления информации о книге
        pass

    @marshal_with(book_fields)
    def delete(self, book_id):
        # Здесь должен быть код для удаления книги
        pass

# Пример добавления ресурса в API
api.add_resource(BookResource, '/books/<int:book_id>')

# Дополнительно нужно будет добавить остальные ресурсы и методы для полной реализации задания.

if __name__ == '__main__':
    app.run(debug=True)