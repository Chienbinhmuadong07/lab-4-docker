"""BÀI LAB LỖI 1/3 — LỖI KẾT NỐI (sai connection string).

Cách làm:
    1. Chạy:  python loi/loi_1_ket_noi.py
    2. ĐỌC KỸ thông báo lỗi in ra. Bạn sẽ thấy dạng "connection refused"
       (không kết nối được tới máy chủ cơ sở dữ liệu).
    3. Nguyên nhân nằm ngay trong chuỗi DSN dưới đây: có MỘT phần bị sai.
       So với DATABASE_URL đúng trong .env của bạn để tìm ra chỗ sai.
    4. SỬA chuỗi DSN cho đúng rồi chạy lại — phải in "Kết nối THÀNH CÔNG".

Gợi ý: PostgreSQL thường lắng nghe ở cổng 5432.
"""
import psycopg2

# CHUỖI NÀY ĐANG SAI — hãy tìm và sửa (chỉ sai đúng một phần).
DSN = "postgresql://postgres:duong612007@localhost:5432/chatdb"

try:
    conn = psycopg2.connect(DSN)
    conn.close()
    print("Kết nối THÀNH CÔNG. Bạn đã sửa đúng lỗi 1!")
except Exception as e:
    print("LỖI KẾT NỐI:")
    print(e)
