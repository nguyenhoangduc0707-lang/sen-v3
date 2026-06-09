import csv

# Đọc file CSV hiện tại
with open('posts_schedule.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Sửa giờ đăng cho đa dạng
time_slots = ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00']

for i, row in enumerate(rows):
    row['Time'] = time_slots[i % len(time_slots)]
    row['Status'] = 'PENDING'

# Ghi lại file CSV
with open('posts_schedule.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print('✅ Updated CSV with different times:')
for row in rows:
    print(f'   {row["Time"]} - {row["Content"][:30]}...')
