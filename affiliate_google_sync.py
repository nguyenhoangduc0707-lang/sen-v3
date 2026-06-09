import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
import json
import requests
from datetime import datetime
import time
import os
import csv

class AffiliateGoogleSync:
    def __init__(self):
        self.credentials_file = 'google_credentials.json'
        self.sheet_name = 'DYT01_Affiliate_Data_Hub'
        self.use_csv_fallback = False
        
        if not os.path.exists(self.credentials_file):
            print(f'⚠️  {self.credentials_file} not found! Using CSV fallback')
            self.use_csv_fallback = True
        else:
            self.connect_to_google_sheets()
    
    def connect_to_google_sheets(self):
        try:
            scope = ['https://spreadsheets.google.com/feeds', 
                    'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, scope)
            self.client = gspread.authorize(creds)
            
            try:
                self.sheet = self.client.open(self.sheet_name).sheet1
            except:
                self.sheet = self.client.create(self.sheet_name).sheet1
                print(f'✅ Created new sheet: {self.sheet_name}')
            
            print('✅ Connected to Google Sheets!')
        except Exception as e:
            print(f'❌ Google Sheets connection failed: {e}')
            self.use_csv_fallback = True
    
    def fetch_from_accesstrade(self):
        print('📡 Fetching data from Accesstrade...')
        
        # Dữ liệu mẫu
        sample_data = [
            {
                'campaign_id': 'CAM001',
                'product_name': 'Tai nghe Bluetooth Sony WH-1000XM5',
                'price': 6990000,
                'commission': 12,
                'affiliate_link': 'https://accesstrade.vn/link/001',
                'end_date': '2026-07-01',
                'image_url': 'https://example.com/sony.jpg'
            },
            {
                'campaign_id': 'CAM002',
                'product_name': 'Mỹ phẩm chính hãng Olay',
                'price': 450000,
                'commission': 15,
                'affiliate_link': 'https://accesstrade.vn/link/002',
                'end_date': '2026-06-30',
                'image_url': 'https://example.com/olay.jpg'
            },
            {
                'campaign_id': 'CAM003',
                'product_name': 'Khóa học Marketing Online',
                'price': 1990000,
                'commission': 20,
                'affiliate_link': 'https://accesstrade.vn/link/003',
                'end_date': '2026-08-01',
                'image_url': 'https://example.com/course.jpg'
            }
        ]
        return sample_data
    
    def update_google_sheet(self, data):
        if self.use_csv_fallback:
            return self.update_csv_file(data)
        
        print('📤 Updating Google Sheet...')
        self.sheet.clear()
        
        headers = ['Campaign ID', 'Product Name', 'Price (VND)', 'Commission (%)', 
                   'Affiliate Link', 'End Date', 'Status', 'Image URL', 'Synced At']
        self.sheet.append_row(headers)
        
        for item in data:
            row = [
                item.get('campaign_id', ''),
                item.get('product_name', ''),
                item.get('price', 0),
                item.get('commission', 0),
                item.get('affiliate_link', ''),
                item.get('end_date', ''),
                'PENDING',
                item.get('image_url', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
            self.sheet.append_row(row)
        
        print(f'✅ Updated {len(data)} campaigns to Google Sheet')
        return True
    
    def update_csv_file(self, data):
        """Lưu vào CSV với fieldnames động"""
        if not data:
            print('No data to save')
            return False
        
        # Lấy tất cả keys từ dữ liệu
        fieldnames = list(data[0].keys())
        
        with open('affiliate_data_backup.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f'✅ Saved {len(data)} campaigns to affiliate_data_backup.csv')
        return True
    
    def read_from_sheet_and_create_tasks(self):
        if self.use_csv_fallback:
            return self.read_from_csv_and_create_tasks()
        
        print('📥 Reading from Google Sheet...')
        try:
            records = self.sheet.get_all_records()
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()
            
            created_tasks = 0
            for i, record in enumerate(records, start=2):
                if record.get('Status') == 'PENDING':
                    content = f"""🔥 AFFILIATE DEAL 🔥

📦 {record.get('Product Name', 'Sản phẩm')}
💰 Giá: {record.get('Price (VND)', 0):,}đ
💸 Hoa hồng: {record.get('Commission (%)', 0)}%

🔗 Link: {record.get('Affiliate Link', '')}
⏰ Đến: {record.get('End Date', '')}

👉 Click ngay!"""
                    
                    cursor.execute('''
                        INSERT INTO tasks (title, description, task_type, worker_name, 
                                          status, priority, payload, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        f"Affiliate: {record.get('Product Name', '')[:50]}",
                        f"Auto affiliate post",
                        'affiliate_post',
                        'shopee_affiliate',
                        'PENDING',
                        8,
                        json.dumps({
                            'content': content,
                            'campaign_id': record.get('Campaign ID', ''),
                            'product_name': record.get('Product Name', ''),
                            'affiliate_link': record.get('Affiliate Link', ''),
                            'image_url': record.get('Image URL', ''),
                            'platform': 'facebook'
                        }),
                        datetime.now().isoformat()
                    ))
                    
                    if not self.use_csv_fallback:
                        self.sheet.update(f'G{i}', 'TASK_CREATED')
                    
                    created_tasks += 1
                    print(f'✅ Created task for: {record.get("Product Name", "")[:30]}')
            
            conn.commit()
            conn.close()
            print(f'📊 Created {created_tasks} affiliate tasks!')
        except Exception as e:
            print(f'❌ Error: {e}')
    
    def read_from_csv_and_create_tasks(self):
        if not os.path.exists('affiliate_data_backup.csv'):
            print('No CSV data found')
            return
        
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        with open('affiliate_data_backup.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                content = f"""🔥 AFFILIATE DEAL 🔥

📦 {row.get('product_name', 'Sản phẩm')}
🔗 Link: {row.get('affiliate_link', '')}"""
                
                cursor.execute('''
                    INSERT INTO tasks (title, task_type, worker_name, status, priority, payload, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    f"Affiliate: {row.get('product_name', '')[:50]}",
                    'affiliate_post',
                    'shopee_affiliate',
                    'PENDING',
                    8,
                    json.dumps({'content': content, 'affiliate_link': row.get('affiliate_link', '')}),
                    datetime.now().isoformat()
                ))
                print(f'✅ Created task for: {row.get("product_name", "")[:30]}')
        
        conn.commit()
        conn.close()
    
    def run_sync(self):
        print('\n' + '='*50)
        print(' AFFILIATE SYNC STARTED')
        print(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print('='*50)
        
        data = self.fetch_from_accesstrade()
        print(f'📡 Fetched {len(data)} campaigns')
        
        self.update_google_sheet(data)
        self.read_from_sheet_and_create_tasks()
        
        print('='*50)
        print(' AFFILIATE SYNC COMPLETED')
        print('='*50 + '\n')

if __name__ == '__main__':
    import sys
    sync = AffiliateGoogleSync()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        sync.run_sync()
    else:
        print('🚀 Starting Affiliate Sync Service...')
        print('Will sync every 60 minutes')
        print('Press Ctrl+C to stop\n')
        try:
            while True:
                sync.run_sync()
                print('⏰ Waiting 60 minutes for next sync...\n')
                time.sleep(3600)
        except KeyboardInterrupt:
            print('\n👋 Sync service stopped')
