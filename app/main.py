# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Book, Base
from app.schemas import BookCreate, BookRead
import random

# Создание таблиц (не нужно после Alembic, но пока можно оставить)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books", response_model=list[BookRead])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.post("/books", response_model=BookRead)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/random", response_model=BookRead)
def get_random_book(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books available")
    return random.choice(books)


@app.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

