from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Создание подключения к базе данных SQLite в памяти
engine = create_engine('sqlite:///example.db', echo=True)

Base = declarative_base()

# Определение классов для моделей базы данных
class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="author")
    
    def __repr__(self):
        return f"<Author(name={self.name})>"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="books")
    publication_date = Column(Date)
    
    def __repr__(self):
        return f"<Book(title={self.title}, publication_date={self.publication_date})>"

# Создание таблиц
Base.metadata.create_all(engine)

# Функции для работы с базой данных
def add_author(session, name):
    author = Author(name=name)
    session.add(author)
    session.commit()
    return author

def add_book(session, title, author_name, publication_date):
    author = session.query(Author).filter_by(name=author_name).first()
    if author is None:
        author = add_author(session, author_name)
    book = Book(title=title, author=author, publication_date=publication_date)
    session.add(book)
    session.commit()
    return book

def get_all_books(session):
    return session.query(Book).all()

def get_books_by_author(session, author_name):
    return session.query(Book).join(Author).filter(Author.name == author_name).all()

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Пример использования функций
if __name__ == "__main__":
    add_author(session, 'Leo Tolstoy')
    add_book(session, 'War and Peace', 'Leo Tolstoy', '1869-01-01')
    add_book(session, 'Anna Karenina', 'Leo Tolstoy', '1877-01-01')
    
    print(get_all_books(session))
    print(get_books_by_author(session, 'Leo Tolstoy'))