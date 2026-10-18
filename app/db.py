"""Lớp kết nối cơ sở dữ liệu cho bài lab buổi 4.

Ý tưởng "lớp kết nối" (slide 11): ứng dụng KHÔNG rải câu lệnh SQL khắp nơi,
mà gom hết vào một chỗ (file này). Phần còn lại của ứng dụng chỉ gọi các hàm
luu_tin_nhan() và doc_lich_su(), không cần biết SQL bên trong.

>>> BẠN PHẢI HOÀN THIỆN 2 hàm có chữ TODO ở dưới. <<<
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Nạp các biến trong tập tin .env vào môi trường (giống cách làm với API key buổi 3).
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def lay_ket_noi():
    """Mở một kết nối tới PostgreSQL dựa trên DATABASE_URL trong .env.

    Bạn KHÔNG cần sửa hàm này — nhưng hãy đọc để hiểu nó làm gì.
    """
    if not DATABASE_URL:
        raise RuntimeError(
            "Chưa có DATABASE_URL. Hãy tạo tập tin .env từ .env.example và điền "
            "connection string (xem README.md - Bước 1)."
        )
    return psycopg2.connect(DATABASE_URL)


def luu_tin_nhan(role: str, content: str) -> int:
    """Lưu MỘT bản ghi vào bảng messages và trả về id vừa được tạo.

    ┌── TODO (BẠN LÀM) ─────────────────────────────────────────────────┐
    │ Thay dòng `raise NotImplementedError(...)` bên dưới bằng đoạn:      │
    │                                                                    │
    │   conn = lay_ket_noi()                                             │
    │   cur = conn.cursor()                                              │
    │   cur.execute(                                                     │
    │       "INSERT INTO messages (role, content) "                      │
    │       "VALUES (%s, %s) RETURNING id",                              │
    │       (role, content),                                            │
    │   )                                                                │
    │   new_id = cur.fetchone()[0]                                       │
    │   conn.commit()          # <-- QUÊN dòng này thì dữ liệu KHÔNG lưu │
    │   cur.close()                                                     │
    │   conn.close()                                                    │
    │   return new_id                                                    │
    │                                                                    │
    │ LƯU Ý: luôn truyền dữ liệu qua tham số %s, ĐỪNG nối chuỗi bằng tay │
    │        (tránh lỗi và tránh lỗ hổng SQL injection).                 │
    └────────────────────────────────────────────────────────────────────┘
    """
    conn = lay_ket_noi()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (role, content) "
        "VALUES (%s, %s) RETURNING id",
        (role, content),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


def doc_lich_su(gioi_han: int = 50):
    """Đọc các bản ghi trong bảng messages theo thứ tự thời gian.

    Trả về: danh sách dict, mỗi dict gồm id, role, content, created_at.

    ┌── TODO (BẠN LÀM) ─────────────────────────────────────────────────┐
    │ Thay dòng `raise NotImplementedError(...)` bên dưới bằng đoạn:      │
    │                                                                    │
    │   conn = lay_ket_noi()                                             │
    │   cur = conn.cursor(cursor_factory=RealDictCursor)                 │
    │   cur.execute(                                                     │
    │       "SELECT id, role, content, created_at "                      │
    │       "FROM messages ORDER BY created_at LIMIT %s",                │
    │       (gioi_han,),                                                 │
    │   )                                                                │
    │   ket_qua = cur.fetchall()                                         │
    │   cur.close()                                                     │
    │   conn.close()                                                    │
    │   return ket_qua                                                   │
    │                                                                    │
    │ (RealDictCursor giúp mỗi dòng trả về ở dạng dict cho dễ đọc/JSON.) │
    └────────────────────────────────────────────────────────────────────┘
    """
    conn = lay_ket_noi()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT id, role, content, created_at "
        "FROM messages ORDER BY created_at LIMIT %s",
        (gioi_han,),
    )
    ket_qua = cur.fetchall()
    cur.close()
    conn.close()
    return ket_qua
