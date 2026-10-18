"""Script TỰ CHẤM cho bài lab chính (Bước 1 -> 4 trong README).

Chạy:  python kiem_tra.py

Script sẽ kiểm tra lần lượt và in [ĐẠT] / [CHƯA] cho từng tiêu chí.
Khi tất cả đều [ĐẠT] nghĩa là bạn đã hoàn thành phần chính của bài lab.
Script này KHÔNG cần chạy máy chủ web — nó gọi thẳng các hàm trong app/db.py.
"""
from app import db, llm


def in_ket_qua(dat, mo_ta, chi_tiet=""):
    nhan = "[ĐẠT] " if dat else "[CHƯA]"
    print(f"{nhan} {mo_ta}")
    if chi_tiet:
        print(f"        -> {chi_tiet}")
    return dat


def main():
    print("=" * 60)
    print("  TỰ CHẤM BÀI LAB BUỔI 4")
    print("=" * 60)
    tat_ca_dat = True

    # 1) Kết nối được cơ sở dữ liệu
    try:
        conn = db.lay_ket_noi()
        conn.close()
        tat_ca_dat &= in_ket_qua(True, "Tiêu chí 1: Kết nối được PostgreSQL (DATABASE_URL đúng).")
    except Exception as e:
        tat_ca_dat &= in_ket_qua(False, "Tiêu chí 1: Kết nối PostgreSQL.", str(e))
        print("\n>> Chưa kết nối được thì các bước sau chưa kiểm tra được. "
              "Xem README.md - Bước 1 & 2.")
        return

    # 2) Bảng messages đã tồn tại
    try:
        conn = db.lay_ket_noi()
        cur = conn.cursor()
        cur.execute("SELECT to_regclass('public.messages')")
        co_bang = cur.fetchone()[0] is not None
        cur.close()
        conn.close()
        tat_ca_dat &= in_ket_qua(
            co_bang, "Tiêu chí 2: Bảng 'messages' đã được tạo.",
            "" if co_bang else "Chạy: psql ... -f sql/create_table.sql (README Bước 2)")
    except Exception as e:
        tat_ca_dat &= in_ket_qua(False, "Tiêu chí 2: Bảng 'messages'.", str(e))
        return

    # 3) luu_tin_nhan() hoạt động
    da_luu_id = None
    try:
        cau_hoi = "Câu kiểm tra tự động"
        cau_tra_loi = llm.goi_llm(cau_hoi)
        db.luu_tin_nhan("user", cau_hoi)
        da_luu_id = db.luu_tin_nhan("assistant", cau_tra_loi)
        ok = isinstance(da_luu_id, int)
        tat_ca_dat &= in_ket_qua(
            ok, "Tiêu chí 3: luu_tin_nhan() lưu được và trả về id.",
            "" if ok else "Hàm phải return id (số nguyên) sau khi commit.")
    except NotImplementedError:
        tat_ca_dat &= in_ket_qua(False, "Tiêu chí 3: luu_tin_nhan().",
                                 "Hàm chưa được hoàn thiện (còn NotImplementedError).")
    except Exception as e:
        tat_ca_dat &= in_ket_qua(False, "Tiêu chí 3: luu_tin_nhan().", str(e))

    # 4) doc_lich_su() đọc lại đúng dữ liệu vừa lưu
    try:
        lich_su = db.doc_lich_su()
        thay = any(r.get("id") == da_luu_id for r in lich_su) if da_luu_id else False
        tat_ca_dat &= in_ket_qua(
            thay, "Tiêu chí 4: doc_lich_su() đọc lại thấy bản ghi vừa lưu.",
            f"Số bản ghi đang có trong bảng: {len(lich_su)}")
    except NotImplementedError:
        tat_ca_dat &= in_ket_qua(False, "Tiêu chí 4: doc_lich_su().",
                                 "Hàm chưa được hoàn thiện (còn NotImplementedError).")
    except Exception as e:
        tat_ca_dat &= in_ket_qua(False, "Tiêu chí 4: doc_lich_su().", str(e))

    print("-" * 60)
    if tat_ca_dat:
        print("  KẾT QUẢ: TẤT CẢ ĐẠT — hoàn thành phần chính!")
        print("  Tiếp theo: làm BÀI LAB LỖI trong thư mục loi/ (README - Bước 5).")
    else:
        print("  KẾT QUẢ: Còn tiêu chí CHƯA đạt — đọc gợi ý ở trên rồi sửa tiếp.")
    print("=" * 60)


if __name__ == "__main__":
    main()
