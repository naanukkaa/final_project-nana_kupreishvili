from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "books.json"


def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)


@app.route("/")
def index():
    books = load_books()
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add_book_page():
    if request.method == "POST":
        books = load_books()
        new_id = max([book["id"] for book in books], default=0) + 1
        new_book = {
            "id": new_id,
            "title": request.form["title"],
            "author": request.form["author"],
            "rate": int(request.form["rate"]),
            "status": request.form["status"]
        }
        books.append(new_book)
        save_books(books)
        return redirect(url_for("index"))
    return render_template("add_book.html")


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book_page(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return "წიგნი ვერ მოიძებნა", 404

    if request.method == "POST":
        book["title"] = request.form["title"]
        book["author"] = request.form["author"]
        book["rate"] = int(request.form["rate"])
        book["status"] = request.form["status"]
        save_books(books)
        return redirect(url_for("index"))

    return render_template("edit_book.html", book=book)


@app.route("/delete/<int:book_id>")
def delete_book(book_id):
    books = load_books()
    books = [b for b in books if b["id"] != book_id]
    save_books(books)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
