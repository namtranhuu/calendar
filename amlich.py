import datetime as dt
from lunar_vn import solar_to_lunar
import sys

CAN = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"]
CHI = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"]

def get_year_can_chi(year):
    return f"{CAN[year % 10]} {CHI[year % 12]}"

LUNAR_HOLIDAYS = {
    (1, 1): ("Mùng 1 Tết", "Tết Nguyên Đán."),
    (2, 1): ("Mùng 2 Tết", "Tết Nguyên Đán."),
    (3, 1): ("Mùng 3 Tết", "Tết Nguyên Đán."),
    (10, 1): ("Vía Thần Tài", "Ngày vía Thần Tài (Mùng 10 tháng Giêng)."),
    (15, 1): ("Rằm Tháng Giêng (Tết Nguyên Tiêu)", "Tết Nguyên Tiêu — Rằm đầu năm."),
    (3, 3): ("Tết Hàn Thực", "Tết Hàn Thực (Mùng 3 tháng 3)."),
    (10, 3): ("Giỗ Tổ Hùng Vương", "Giỗ Tổ Hùng Vương (10 tháng 3)."),
    (15, 4): ("Lễ Phật Đản", "Lễ Phật Đản (15 tháng 4)."),
    (5, 5): ("Tết Đoan Ngọ", "Tết Đoan Ngọ (Mùng 5 tháng 5)."),
    (15, 7): ("Lễ Vu Lan", "Lễ Vu Lan báo hiếu (Rằm tháng Bảy)."),
    (15, 8): ("Tết Trung Thu", "Tết Trung Thu (Rằm tháng Tám)."),
    (23, 12): ("Cúng Ông Táo", "Lễ cúng tiễn Táo Quân về trời (23 tháng Chạp)."),
}

SOLAR_HOLIDAYS = {
    (1, 1): ("Tết Dương Lịch", "Nghỉ Tết Dương Lịch."),
    (14, 2): ("Lễ Tình Nhân", "Valentine's Day."),
    (8, 3): ("Quốc Tế Phụ Nữ", "Ngày Quốc tế Phụ nữ 8/3."),
    (30, 4): ("Giải Phóng Miền Nam", "Ngày Giải phóng miền Nam, thống nhất đất nước."),
    (1, 5): ("Quốc Tế Lao Động", "Ngày Quốc tế Lao động."),
    (1, 6): ("Quốc Tế Thiếu Nhi", "Ngày Quốc tế Thiếu nhi."),
    (2, 9): ("Quốc Khánh", "Lễ Quốc Khánh nước CHXHCN Việt Nam."),
    (20, 10): ("Ngày Phụ Nữ Việt Nam", "Ngày Phụ nữ Việt Nam 20/10."),
    (20, 11): ("Ngày Nhà Giáo Việt Nam", "Ngày Nhà giáo Việt Nam 20/11."),
    (24, 12): ("Đêm Giáng Sinh", "Đêm Giáng Sinh."),
    (25, 12): ("Lễ Giáng Sinh", "Lễ Giáng Sinh."),
}

def fold_line(line):
    encoded = line.encode('utf-8')
    if len(encoded) <= 75:
        return line + "\r\n"

    res = ""
    current = encoded
    while len(current) > 75:
        split_idx = 75
        while split_idx > 0 and (current[split_idx] & 0xC0) == 0x80:
            split_idx -= 1
        if split_idx == 0:
            split_idx = 75
        res += current[:split_idx].decode('utf-8') + "\r\n "
        current = current[split_idx:]
    res += current.decode('utf-8') + "\r\n"
    return res

def generate_ics():
    now = dt.datetime.now()
    current_year = now.year
    start_year = current_year - 1
    end_year = current_year + 1

    start_date = dt.date(start_year, 1, 1)
    end_date = dt.date(end_year, 12, 31)

    dtstamp = now.strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VCALENDAR",
        f"VERSION:{current_year}",
        "PRODID:-//namth587@gmail.com//Lịch Âm Việt Nam//VI",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALDESC:Lịch Âm Việt Nam",
        "X-WR-CALNAME:Lịch Âm Việt Nam",
        "X-APPLE-CALENDAR-COLOR:#1E88E5",
        "X-WR-TIMEZONE:Asia/Ho_Chi_Minh"
    ]

    curr = start_date
    while curr <= end_date:
        next_day = curr + dt.timedelta(days=1)

        lunar_date = solar_to_lunar(curr)
        next_lunar_date = solar_to_lunar(next_day)

        lday = lunar_date.day
        lmonth = lunar_date.month
        lyear = lunar_date.year
        leap_str = " (Nhuận)" if lunar_date.leap else ""
        can_chi = get_year_can_chi(lyear)

        is_giao_thua = False
        if next_lunar_date.day == 1 and next_lunar_date.month == 1:
            is_giao_thua = True

        solar_tuple = (curr.day, curr.month)
        lunar_tuple = (lday, lmonth) if not lunar_date.leap else None

        summary = f"{lday}/{lmonth}"
        description_lines = [f"Ngày {lday} tháng {lmonth}{leap_str} âm lịch ({can_chi})"]
        importance = None

        holiday_names = []

        if is_giao_thua:
            holiday_names.append("Đêm Giao Thừa")
            description_lines.append("Đêm Giao Thừa: Đêm Giao Thừa đón năm mới âm lịch.")
            importance = "2"
        elif lunar_tuple in LUNAR_HOLIDAYS:
            h_name, h_desc = LUNAR_HOLIDAYS[lunar_tuple]
            holiday_names.append(h_name)
            description_lines.append(f"{h_name}: {h_desc}")
            importance = "2"
        elif lday == 1:
            holiday_names.append("Mùng 1")
        elif lday == 15:
            holiday_names.append("Rằm")

        if solar_tuple in SOLAR_HOLIDAYS:
            s_name, s_desc = SOLAR_HOLIDAYS[solar_tuple]
            holiday_names.append(s_name)
            description_lines.append(f"{s_name}: {s_desc}")
            importance = "2"

        if holiday_names:
            summary += " • " + " • ".join(holiday_names)

        desc_str = "\\n".join(description_lines)

        uid = f"vnlunar-{curr.strftime('%Y%m%d')}@amlich"

        lines.append("BEGIN:VEVENT")
        lines.append(f"SUMMARY:{summary}")
        lines.append(f"DTSTART;VALUE=DATE:{curr.strftime('%Y%m%d')}")
        lines.append(f"DTEND;VALUE=DATE:{next_day.strftime('%Y%m%d')}")
        lines.append(f"DTSTAMP:{dtstamp}")
        lines.append(f"UID:{uid}")
        lines.append(f"DESCRIPTION:{desc_str}")
        if importance:
            lines.append(f"X-MICROSOFT-CDO-IMPORTANCE:{importance}")
        lines.append("END:VEVENT")

        curr = next_day

    lines.append("END:VCALENDAR")

    with open("amlich.ics", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(fold_line(line))

if __name__ == "__main__":
    generate_ics()
