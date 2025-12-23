from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "library_secret_key"


# =========================
# 数据库连接
# =========================
def get_db():
    return sqlite3.connect("library.db")


# =========================
# 登录
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM user WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        db.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect("/books")

    return render_template("login.html")


# =========================
# 退出登录
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# 图书列表 + 查询
# =========================
@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect("/")

    keyword = request.args.get("keyword", "")

    db = get_db()
    cur = db.cursor()

    if keyword:
        cur.execute(
            "SELECT * FROM book WHERE title LIKE ? OR author LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
    else:
        cur.execute("SELECT * FROM book")

    books = cur.fetchall()
    db.close()

    return render_template("books.html", books=books)


# =========================
# 添加图书（管理员）
# =========================
@app.route("/add_book", methods=["POST"])
def add_book():
    if session.get("role") != "admin":
        return redirect("/books")

    title = request.form.get("title")
    author = request.form.get("author")
    isbn = request.form.get("isbn")
    total = int(request.form.get("total"))

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO book(title, author, isbn, total, available)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, isbn, total, total))
    db.commit()
    db.close()

    return redirect("/books")


# =========================
# 借书
# =========================
@app.route("/borrow/<int:book_id>")
def borrow(book_id):
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT available FROM book WHERE id=?", (book_id,))
    result = cur.fetchone()

    if result and result[0] > 0:
        cur.execute("""
            INSERT INTO borrow(user_id, book_id, borrow_date)
            VALUES (?, ?, ?)
        """, (user_id, book_id, datetime.now()))
        cur.execute("""
            UPDATE book SET available = available - 1 WHERE id=?
        """, (book_id,))
        db.commit()

    db.close()
    return redirect("/books")


# =========================
# 我的借阅
# =========================
@app.route("/my_borrow")
def my_borrow():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT borrow.id, book.title, borrow.borrow_date, borrow.return_date
        FROM borrow
        JOIN book ON borrow.book_id = book.id
        WHERE borrow.user_id=?
    """, (user_id,))
    records = cur.fetchall()
    db.close()

    return render_template("borrow.html", records=records)


# =========================
# 还书
# =========================
@app.route("/return/<int:borrow_id>")
def return_book(borrow_id):
    if "user_id" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT book_id FROM borrow WHERE id=?", (borrow_id,))
    result = cur.fetchone()

    if result:
        book_id = result[0]
        cur.execute("""
            UPDATE borrow SET return_date=? WHERE id=?
        """, (datetime.now(), borrow_id))
        cur.execute("""
            UPDATE book SET available = available + 1 WHERE id=?
        """, (book_id,))
        db.commit()

    db.close()
    return redirect("/my_borrow")


# =========================
# 程序入口
# =========================
if __name__ == "__main__":
    app.run(debug=True)
