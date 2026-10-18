"""BÀI LAB LỖI 2/3 — BẢNG CHƯA TỒN TẠI (relation does not exist).

Cách làm:
    1. Bảo đảm đã tạo bảng messages (README - Bước 2).
    2. Chạy:  python loi/loi_2_bang_chua_ton_tai.py
    3. ĐỌC KỸ thông báo lỗi. Bạn sẽ thấy dạng:
           relation "message" does not exist
       PostgreSQL đang than phiền về một bảng tên KHÔNG khớp với bảng thật.
    4. Tìm chỗ sai trong câu SQL dưới đây và sửa cho khớp tên bảng thật,
       rồi chạy lại — phải in ra số dòng đang có.

Gợi ý: bảng thật của chúng ta tên là "messages" (chú ý chữ cuối).
"""
from app import db

conn = db.lay_ket_noi()
cur = conn.cursor()

# CÂU SQL NÀY ĐANG SAI TÊN BẢNG — hãy sửa.
cur.execute("SELECT COUNT(*) FROM messages")

so_dong = cur.fetchone()[0]
print(f"Truy vấn THÀNH CÔNG. Bảng đang có {so_dong} dòng. Bạn đã sửa đúng lỗi 2!")

cur.close()
conn.close()
