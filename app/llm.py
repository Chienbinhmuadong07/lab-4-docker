"""LLM GIẢ LẬP cho bài lab buổi 4.

Ở buổi 3 các bạn gọi LLM thật qua API key. Trong bài lab này ta CỐ Ý không
dùng LLM thật: hàm dưới đây chỉ "vọng lại" câu hỏi. Nhờ vậy:
  - Không cần API key, không cần Internet.
  - Ai cũng chạy được, kể cả khi không có AI.
  - Cả buổi tập trung 100% vào phần CƠ SỞ DỮ LIỆU (mục tiêu thật của buổi 4).

Bạn KHÔNG cần sửa file này.
"""


def goi_llm(cau_hoi: str) -> str:
    """Nhận câu hỏi, trả về câu trả lời (giả lập)."""
    cau_hoi = (cau_hoi or "").strip()
    if not cau_hoi:
        return "(LLM giả lập) Bạn chưa nhập gì cả."
    return f"(LLM giả lập) Mình đã nhận được câu hỏi: {cau_hoi}"
