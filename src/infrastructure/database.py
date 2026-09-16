import os
import csv
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.join(os.path.dirname(__file__), "MovieList.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "Movielist.csv")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MovieModel(Base):
    __tablename__ = "Movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    studios = Column(String, nullable=False)
    producers = Column(String, nullable=False)
    winner = Column(String, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        count = session.query(MovieModel).count()
        if count == 0 and os.path.exists(CSV_PATH):
            with open(CSV_PATH, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    movie = MovieModel(
                        year=int(row["year"]),
                        title=row["title"],
                        studios=row["studios"],
                        producers=row["producers"],
                        winner=row.get("winner", "no").strip().lower()
                    )
                    session.add(movie)
                session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

class DataBaseMovies:
    def insert_movie(self, year: int, title: str, studios: str, producers: str, winner: str = "no") -> bool:
        session = SessionLocal()
        try:
            movie = MovieModel(year=year, title=title, studios=studios, producers=producers, winner=winner)
            session.add(movie)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def update_movie(self, movie_id: int, data: Dict[str, Any]) -> bool:
        session = SessionLocal()
        try:
            movie = session.query(MovieModel).filter(MovieModel.id == movie_id).first()
            if not movie:
                return False
            for key, value in data.items():
                if hasattr(movie, key):
                    setattr(movie, key, value)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def delete_movie(self, movie_id: int) -> bool:
        session = SessionLocal()
        try:
            movie = session.query(MovieModel).filter(MovieModel.id == movie_id).first()
            if not movie:
                return False
            session.delete(movie)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def get_all_movies(self) -> List[Dict[str, Any]]:
        session = SessionLocal()
        try:
            movies = session.query(MovieModel).all()
            return [
                {
                    "id": m.id,
                    "year": m.year,
                    "title": m.title,
                    "studios": m.studios,
                    "producers": m.producers,
                    "winner": m.winner
                }
                for m in movies
            ]
        finally:
            session.close()

    def get_winner_movies(self) -> List[Dict[str, Any]]:
        session = SessionLocal()
        try:
            movies = session.query(MovieModel).filter(MovieModel.winner.ilike("yes")).all()
            return [
                {
                    "id": m.id,
                    "year": m.year,
                    "title": m.title,
                    "studios": m.studios,
                    "producers": m.producers,
                    "winner": m.winner
                }
                for m in movies
            ]
        finally:
            session.close()