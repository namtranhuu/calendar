# Lịch Âm Việt Nam (Vietnamese Lunar Calendar) 📅

Dự án này tự động tạo và cập nhật tệp `.ics` cho Lịch Âm Việt Nam. Bạn có thể sử dụng tệp này để đăng ký (subscribe) lịch âm trực tiếp trên các ứng dụng như Apple Calendar, Google Calendar, Outlook, v.v.

Tệp `.ics` được tự động tạo mới mỗi năm bằng **GitHub Actions** (để luôn bao gồm dữ liệu của năm trước, năm hiện tại và năm sau).

## 🚀 Cách sử dụng (How to subscribe)

Để hiển thị lịch âm trên điện thoại hoặc máy tính của bạn, hãy sao chép đường dẫn (URL) tới tệp `amlich.ics` dạng raw (Raw URL) và thêm vào ứng dụng lịch của bạn dưới dạng **Subscribed Calendar** (Lịch đăng ký/Lịch thêm bằng URL).

**Đường dẫn Lịch (Raw URL):**
*(Hãy thay `<username>` và `<repository>` bằng đường dẫn Git của bạn)*
```
https://raw.githubusercontent.com/<username>/<repository>/main/amlich.ics
```

### Hướng dẫn nhanh cho iOS (Apple Calendar):
1. Mở ứng dụng **Cài đặt (Settings)** > **Lịch (Calendar)** > **Tài khoản (Accounts)** > **Thêm tài khoản (Add Account)**.
2. Chọn **Khác (Other)** > **Thêm Lịch đã đăng ký (Add Subscribed Calendar)**.
3. Dán đường dẫn Lịch ở trên vào và chọn **Tiếp (Next)** > **Lưu (Save)**.

### Hướng dẫn nhanh cho Google Calendar:
1. Mở trang web [Google Calendar](https://calendar.google.com/).
2. Ở menu bên trái, phần **Lịch khác (Other calendars)**, bấm dấu **+** > **Từ URL (From URL)**.
3. Dán đường dẫn Lịch ở trên vào và chọn **Thêm lịch (Add calendar)**.

## 🛠 Cách hoạt động

- **`amlich.py`**: Mã nguồn Python sử dụng thư viện [`lunar-vn`](https://pypi.org/project/lunar-vn/) để chuyển đổi từ Dương lịch sang Âm lịch một cách chính xác. Mã này tự động nhận dạng các ngày mùng 1, ngày rằm, và các dịp lễ tết quan trọng của Việt Nam (Tết Nguyên Đán, Giỗ Tổ Hùng Vương, v.v.).
- **`amlich.ics`**: Tệp lịch đầu ra chuẩn iCalendar (RFC 5545).
- **`GitHub Actions (.github/workflows/amlich.yml)`**: Chạy tự động vào lúc 00:00 ngày 1 tháng 1 hàng năm để tạo tệp `amlich.ics` mới và tự động commit/push vào repo.

## 📦 Phát triển (Development)

Nếu bạn muốn chạy tệp Python tạo lịch trên máy tính của mình:

```bash
# Tạo môi trường ảo (tùy chọn)
python3 -m venv venv
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy mã sinh tệp ICS
python amlich.py
```
