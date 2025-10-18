from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import uvicorn

# Database setup
engine = create_engine("sqlite:///./books.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BookModel(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    author = Column(String(100), nullable=False)
    rating = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="Not Read")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class BookCreate(BaseModel):
    title: str = Field(..., max_length=150)
    author: str = Field(..., max_length=100)
    rating: float
    status: str = Field(default="Not Read", max_length=20)

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: float) -> float:
        if v < 0 or v > 5:
            raise ValueError("rating must be between 0 and 5")
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=150)
    author: Optional[str] = Field(None, max_length=100)
    rating: Optional[float] = None
    status: Optional[str] = Field(None, max_length=20)

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v < 0 or v > 5):
            raise ValueError("rating must be between 0 and 5")
        return v

class Book(BaseModel):
    id: int
    title: str
    author: str
    rating: float
    status: str

    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="Simple Book Tracker")

# Templates
templates = Jinja2Templates(directory="templates")

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Web routes
@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

@app.get("/add", response_class=HTMLResponse)
def add_book_form(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@app.post("/add")
def add_book(
    title: str = Form(...),
    author: str = Form(...),
    rating: float = Form(...),
    status: str = Form("Not Read"),
    db: Session = Depends(get_db)
):
    book = BookModel(title=title, author=author, rating=rating, status=status)
    db.add(book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/edit/{book_id}", response_class=HTMLResponse)
def edit_book_form(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("edit.html", {"request": request, "book": book})

@app.post("/edit/{book_id}")
def edit_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    rating: float = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.title = title
    book.author = author
    book.rating = rating
    book.status = status
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete/{book_id}")
def delete_book_web(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# API routes
@app.get("/api/books", response_model=List[Book])
def list_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return books

@app.post("/api/books", response_model=Book, status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    book = BookModel(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.get("/api/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/api/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book

@app.delete("/api/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookModel, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None

@app.get("/api")
def api_root():
    return {"message": "Simple Book Tracker API is running"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
