-- ============================================================
--  Tạo bảng messages để lưu lịch sử hội thoại.
--  Chạy TRƯỚC KHI dùng ứng dụng (xem README.md - Bước 2).
--
--  Cách chạy (chọn 1):
--    psql "postgresql://postgres:postgres@localhost:5432/chatdb" -f sql/create_table.sql
--  hoặc mở psql rồi dán toàn bộ nội dung dưới đây.
-- ============================================================

CREATE TABLE IF NOT EXISTS messages (
    id          SERIAL PRIMARY KEY,        -- số thứ tự tự tăng, định danh mỗi bản ghi
    role        VARCHAR(20),               -- 'user' hay 'assistant'
    content     TEXT,                      -- nội dung câu nói
    created_at  TIMESTAMP DEFAULT now()    -- thời điểm lưu, mặc định là lúc tạo
);
