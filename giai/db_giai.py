"""ĐÁP ÁN app/db.py — chỉ mở khi đã TỰ LÀM xong hoặc để đối chiếu.

Chép nội dung 2 hàm dưới đây đè lên phần TODO trong app/db.py là chạy được.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def lay_ket_noi():
    if not DATABASE_URL:
        raise RuntimeError("Chưa có DATABASE_URL trong .env.")
    return psycopg2.connect(DATABASE_URL)


def luu_tin_nhan(role: str, content: str) -> int:
    conn = lay_ket_noi()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (role, content) VALUES (%s, %s) RETURNING id",
        (role, content),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


def doc_lich_su(gioi_han: int = 50):
    conn = lay_ket_noi()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT id, role, content, created_at FROM messages ORDER BY created_at LIMIT %s",
        (gioi_han,),
    )
    ket_qua = cur.fetchall()
    cur.close()
    conn.close()
    return ket_qua
