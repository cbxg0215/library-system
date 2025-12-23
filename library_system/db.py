import sqlite3

def get_db():
    return sqlite3.connect("library.db")

def init_db():
    db = get_db()
    cursor = db.cursor()

    # 用户表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # 图书表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        isbn TEXT,
        total INTEGER,
        available INTEGER
    )
    """)

    # 借阅表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        borrow_date TEXT,
        return_date TEXT
    )
    """)

    # 初始化管理员账号
    cursor.execute("""
    INSERT OR IGNORE INTO user(username, password, role)
    VALUES ('admin', '123456', 'admin')
    """)

    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    print("数据库初始化完成")
