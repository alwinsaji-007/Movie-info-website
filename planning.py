from datetime import date

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


genre_movies = db.Table(
    "genre_movies",
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.genre_id"), primary_key=True),
)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date)
    gross_collection = db.Column(db.Integer)
    synopsis = db.Column(db.Text)
    movie_poster = db.Column(db.String(250))

    genres = db.relationship("Genre", secondary=genre_movies, backref="movies")
    reviews = db.relationship(
        "Review", backref="movie", cascade="all, delete-orphan"
    )

    @property
    def average_rating(self):
        if not self.reviews:
            return 0

        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)

    @property
    def is_new(self):
        return self.release_date is not None and self.release_date.year in [2025, 2026]


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)


class Review(db.Model):
    reviews_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    review_date = db.Column(db.Date, nullable=False, default=date.today)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)