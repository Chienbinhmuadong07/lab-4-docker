"""BÀI LAB LỖI 3/3 — SAI KIỂU DỮ LIỆU (invalid input syntax for type integer).

Cách làm:
    1. Chạy:  python loi/loi_3_sai_kieu.py
    2. ĐỌC KỸ thông báo lỗi. Bạn sẽ thấy dạng:
           invalid input syntax for type integer: "một"
       Cột id trong bảng messages có kiểu SỐ NGUYÊN (integer), nhưng câu
       truy vấn lại đưa vào một CHỮ ("một") nên PostgreSQL không hiểu.
    3. Sửa giá trị truyền vào cho ĐÚNG KIỂU (một số nguyên, ví dụ 1),
       rồi chạy lại — không còn báo lỗi nữa.

Gợi ý: so id với một con số, không phải với một từ tiếng Việt.
"""
from app import db

conn = db.lay_ket_noi()
cur = conn.cursor()

# GIÁ TRỊ NÀY SAI KIỂU — cột id là số nguyên, mà đây lại là chữ "một".
id_can_tim = 1

cur.execute("SELECT id, role, content FROM messages WHERE id = %s", (id_can_tim,))
dong = cur.fetchone()

if dong is None:
    print("Truy vấn THÀNH CÔNG (không có dòng nào khớp, nhưng KHÔNG còn lỗi kiểu). "
          "Bạn đã sửa đúng lỗi 3!")
else:
    print(f"Truy vấn THÀNH CÔNG, tìm thấy: {dong}. Bạn đã sửa đúng lỗi 3!")

cur.close()
conn.close()
