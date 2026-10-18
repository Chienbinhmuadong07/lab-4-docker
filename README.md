# Bài lab buổi 4 — Cho ứng dụng "nhớ" được lịch sử hội thoại

> **Mục tiêu:** Gắn cơ sở dữ liệu PostgreSQL vào ứng dụng chat để nó **lưu** và **đọc lại** được lịch sử hội thoại, kể cả sau khi tắt/bật.
> **Thời lượng:** 1 giờ 30 phút · Làm **cá nhân** · **Không cần AI, không cần API key, không cần Internet.**

Trước khi bắt đầu, hãy đọc file **`DE-BAI.txt`** để hiểu bối cảnh và nhiệm vụ. File `README.md` này là hướng dẫn **từng bước**.

---

## Bảng phân bổ thời gian (tổng 90 phút)

| Bước | Nội dung | Thời gian |
|------|----------|-----------|
| 0 | Chuẩn bị: cài thư viện, dựng PostgreSQL, tạo CSDL `chatdb` | 10 phút |
| 1 | Cấu hình kết nối (`.env` → `DATABASE_URL`) | 10 phút |
| 2 | Tạo bảng `messages` | 10 phút |
| 3 | Hoàn thiện **lưu** hội thoại (`luu_tin_nhan` + `/chat`) | 25 phút |
| 4 | Hoàn thiện **đọc** lịch sử (`doc_lich_su` + `/history`) + tự chấm | 20 phút |
| 5 | **Bài lab lỗi**: đọc log SQL, sửa 3 lỗi | 15 phút |

---

## Bước 0 — Chuẩn bị (10 phút)

**a) Cài thư viện Python** (nên dùng môi trường ảo như các buổi trước):

```bash
pip install -r requirements.txt
```

**b) Có một PostgreSQL đang chạy.** Chọn 1 trong 2 cách:

- **Đã cài PostgreSQL trên máy** (khuyến nghị cho buổi này): bảo đảm dịch vụ đang chạy ở cổng `5432`.
- **Có Docker sẵn** (không bắt buộc, module Docker học sau): 
  ```bash
  docker run --name pg-lab4 -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
  ```

**c) Tạo cơ sở dữ liệu tên `chatdb`:**

```bash
# Cách 1 — dùng lệnh createdb:
createdb -U postgres chatdb

# Cách 2 — trong psql:
psql -U postgres -c "CREATE DATABASE chatdb;"
```

> Nếu mật khẩu `postgres` của bạn khác, hãy nhớ nó — bước 1 sẽ cần.

---

## Bước 1 — Cấu hình kết nối (10 phút)

`connection string` là chuỗi cho ứng dụng biết **kết nối tới đâu, bằng tài khoản gì**. Nó chứa **mật khẩu** nên **không ghi thẳng vào mã nguồn** mà đặt trong tập tin `.env` (đúng nguyên tắc đã dùng cho API key ở buổi 3).

**a) Tạo `.env` từ mẫu:**

```bash
# Windows (PowerShell)
Copy-Item .env.example .env
# macOS / Linux
cp .env.example .env
```

**b) Mở `.env`, kiểm tra `DATABASE_URL` khớp máy bạn:**

```
postgresql://postgres:postgres@localhost:5432/chatdb
```

Từng phần: `postgresql` (loại CSDL) · `postgres:postgres` (user:mật khẩu) · `localhost:5432` (địa chỉ:cổng) · `chatdb` (tên CSDL). Sai **một** phần là không kết nối được — hãy sửa cho đúng máy bạn.

---

## Bước 2 — Tạo bảng `messages` (10 phút)

Ứng dụng cần một cái bảng để lưu hội thoại. Chạy sẵn file SQL:

```bash
psql "postgresql://postgres:postgres@localhost:5432/chatdb" -f sql/create_table.sql
```

Kiểm tra nhanh trong psql:

```sql
\d messages      -- xem cấu trúc bảng
```

Bảng gồm 4 cột: `id` (số tự tăng), `role` (`user`/`assistant`), `content` (nội dung), `created_at` (thời điểm lưu).

---

## Bước 3 — Hoàn thiện phần LƯU hội thoại (25 phút)

**a) Mở `app/db.py`, hoàn thiện hàm `luu_tin_nhan()`** (tìm chữ `TODO`). Hàm này chạy một câu `INSERT` và **phải `conn.commit()`** thì dữ liệu mới được ghi thật.

**b) Mở `app/main.py`, ở endpoint `/chat`** thêm **hai** lời gọi lưu — một cho câu hỏi (`"user"`), một cho câu trả lời (`"assistant"`).

> **Vì sao lưu cả hai?** Một lượt hội thoại gồm 2 câu. Muốn xem lại đúng mạch chuyện thì phải lưu đủ cả hỏi lẫn đáp.

**Kiểm tra thử** (chạy máy chủ):

```bash
uvicorn app.main:app --reload
```

Mở `http://127.0.0.1:8000/docs`, bấm **POST /chat**, gửi thử:

```json
{ "message": "Xin chào" }
```

---

## Bước 4 — Hoàn thiện phần ĐỌC lịch sử + tự chấm (20 phút)

**a) Trong `app/db.py`, hoàn thiện `doc_lich_su()`** — chạy `SELECT ... ORDER BY created_at`.

**b) Trong `app/main.py`, ở endpoint `/history`** trả về `db.doc_lich_su()`.

**c) Kiểm chứng "dữ liệu còn lại sau khi tắt":**
1. Gọi `/chat` vài lần.
2. **Tắt** máy chủ (Ctrl+C) rồi **bật lại** (`uvicorn ...`).
3. Gọi **GET /history** — lịch sử vẫn còn. Đây chính là điều buổi 3 chưa làm được!

**d) Tự chấm bằng script** (không cần máy chủ):

```bash
python kiem_tra.py
```

Khi thấy **tất cả `[ĐẠT]`** là bạn đã hoàn thành phần chính. ✅

---

## Bước 5 — Bài lab lỗi: đọc log SQL và sửa (15 phút)

Trong thư mục `loi/` có **3 chương trình chạy bị lỗi** — đúng 3 lỗi SQL hay gặp nhất (slide 15). Với **mỗi** file: chạy nó → **đọc kỹ** thông báo lỗi → tìm chỗ sai → sửa → chạy lại tới khi in "THÀNH CÔNG".

```bash
python loi/loi_1_ket_noi.py            # gợi ý log: connection refused
python loi/loi_2_bang_chua_ton_tai.py  # gợi ý log: relation "..." does not exist
python loi/loi_3_sai_kieu.py           # gợi ý log: invalid input syntax for type integer
```

| Log báo | Nghĩa là | Hướng sửa |
|---------|----------|-----------|
| `connection refused` | Sai địa chỉ/cổng, hoặc CSDL chưa chạy | Sửa lại cổng/địa chỉ trong chuỗi kết nối |
| `relation "..." does not exist` | Sai tên bảng, hoặc chưa tạo bảng | Sửa tên bảng cho khớp / tạo bảng |
| `invalid input syntax for type integer` | Đưa sai kiểu vào cột số | Truyền đúng kiểu (số nguyên) |

> **Trọng tâm:** đừng đoán mò. Hãy **đọc đúng từng dòng** thông báo lỗi — nó nói thẳng ra chỗ sai. Đây là kỹ năng quan trọng nhất của buổi 4.

---

## Checkpoint cuối buổi (điều kiện ĐẠT)

- [ ] Ứng dụng kết nối được PostgreSQL qua `DATABASE_URL` trong `.env`.
- [ ] `/chat` lưu được cả câu hỏi và câu trả lời vào bảng `messages`.
- [ ] `/history` (hoặc `kiem_tra.py`) đọc lại thấy lịch sử đã lưu đúng.
- [ ] Sửa xong cả 3 lỗi trong `loi/`.

Đạt checkpoint này là **đủ điều kiện vào module Docker**.

---

## Cấu trúc thư mục

```
lab-4/
├── DE-BAI.txt            # Bối cảnh + đề bài (đọc trước tiên)
├── README.md             # Hướng dẫn từng bước (file này)
├── requirements.txt      # Thư viện cần cài
├── .env.example          # Mẫu cấu hình — sao thành .env
├── kiem_tra.py           # Script TỰ CHẤM phần chính
├── sql/
│   └── create_table.sql  # Câu lệnh tạo bảng messages
├── app/
│   ├── main.py           # FastAPI /chat, /history (có TODO)
│   ├── db.py             # Lớp kết nối CSDL (có TODO)
│   └── llm.py            # LLM giả lập (không cần sửa)
├── loi/                  # Bài lab lỗi — 3 file chạy bị lỗi
│   ├── loi_1_ket_noi.py
│   ├── loi_2_bang_chua_ton_tai.py
│   └── loi_3_sai_kieu.py
└── giai/                 # ĐÁP ÁN — chỉ mở khi đã tự làm xong
    ├── DAP-AN.txt
    └── db_giai.py
```

## Nếu bị kẹt

- Đọc lại đúng dòng thông báo lỗi — 90% câu trả lời nằm ở đó.
- `python kiem_tra.py` chỉ ra tiêu chí nào chưa đạt.
- Cùng đường thì mở `giai/DAP-AN.txt` để đối chiếu — nhưng hãy tự làm trước.


## Lab 5 — Docker hóa ứng dụng

### 1. Yêu cầu

- Docker Engine hoặc Docker Desktop.
- Mã nguồn ứng dụng và file `requirements.txt`.

### 2. Build Docker image

Chạy tại thư mục gốc của dự án, nơi chứa `Dockerfile`:

```bash
docker build -t chat-lab5 .
```

### 3. Chạy container

```bash
docker run -d --name chat-lab5 -p 8000:8000 chat-lab5
```

### 4. Kiểm tra ứng dụng

Mở trình duyệt tại:

http://localhost:8000/health

Kết quả mong đợi:

```json
{
  "status": "ok"
}
```

HTTP status code mong đợi: `200`.

Có thể kiểm tra bằng lệnh:

```bash
curl -i http://localhost:8000/health
```

### 5. Xem trạng thái container

```bash
docker ps
```

Xem log nếu ứng dụng không khởi động:

```bash
docker logs chat-lab5
```

Dừng và xóa container:

```bash
docker stop chat-lab5
docker rm chat-lab5
```

### 6. Cấu trúc Docker

Dockerfile sử dụng multi-stage build với hai giai đoạn:

- `builder`: cài các thư viện Python vào `/install`.
- `runner`: sao chép thư viện từ giai đoạn `builder`, sao chép mã nguồn ứng dụng và chạy Uvicorn.

File `.dockerignore` loại trừ file môi trường và các file không cần thiết khỏi ngữ cảnh build.
