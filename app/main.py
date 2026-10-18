"""Ứng dụng chat FastAPI — bản DANG DỞ của bài lab buổi 4.

Nhiệm vụ của bạn: nối 2 endpoint dưới đây vào cơ sở dữ liệu (tìm chữ TODO).

Chạy ứng dụng:
    uvicorn app.main:app --reload
Rồi mở trình duyệt tại  http://127.0.0.1:8000/docs  để thử /chat và /history.
"""
from fastapi import FastAPI
from pydantic import BaseModel

from app import db, llm

app = FastAPI(title="Chat có lưu lịch sử — Lab buổi 4")


class ChatIn(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(body: ChatIn):
    cau_hoi = body.message
    cau_tra_loi = llm.goi_llm(cau_hoi)

    # ┌── TODO (BẠN LÀM) ───────────────────────────────────────────────┐
    # │ Lưu CẢ HAI vào bảng messages (có ĐÚNG hai lời gọi):              │
    # │     db.luu_tin_nhan("user", cau_hoi)                            │
    # │     db.luu_tin_nhan("assistant", cau_tra_loi)                   │
    # │ Đặt hai dòng đó vào NGAY DƯỚI đây, trước câu lệnh return.        │
    # └──────────────────────────────────────────────────────────────────┘
    db.luu_tin_nhan("user", cau_hoi)
    db.luu_tin_nhan("assistant", cau_tra_loi)
    return {"answer": cau_tra_loi}


@app.get("/history")
def history():
    # ┌── TODO (BẠN LÀM) ───────────────────────────────────────────────┐
    # │ Trả về lịch sử thật thay vì danh sách rỗng:                     │
    # │     return {"messages": db.doc_lich_su()}                       │
    # └──────────────────────────────────────────────────────────────────┘
    return {"messages": db.doc_lich_su()}
