# extract_images_from_excel.py
import openpyxl
from openpyxl.drawing.image import Image
import os
from PIL import Image as PILImage
import requests
from io import BytesIO

class ExcelImageExtractor:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.images = []
        
    def extract_images(self):
        """Trích xuất hình ảnh từ Excel"""
        wb = openpyxl.load_workbook(self.excel_file)
        
        for sheet in wb.worksheets:
            print(f"Đang xử lý sheet: {sheet.title}")
            
            # Lấy tất cả hình ảnh trong sheet
            if sheet._images:
                for idx, img in enumerate(sheet._images):
                    # Lưu hình ảnh
                    img_data = img._data()
                    filename = f"extracted_image_{sheet.title}_{idx+1}.png"
                    
                    with open(filename, 'wb') as f:
                        f.write(img_data)
                    print(f"  ✅ Đã lưu: {filename}")
                    self.images.append(filename)
            
            # Đọc dữ liệu từ cells
            for row in sheet.iter_rows(min_row=1, max_row=10):
                for cell in row:
                    if cell.value and ('http' in str(cell.value).lower()):
                        print(f"  🔗 Tìm thấy link: {cell.value}")
        
        print(f"\n✅ Tổng cộng: {len(self.images)} hình ảnh")
        return self.images
    
    def create_post_with_images(self):
        """Tạo bài viết kèm hình ảnh"""
        posts = []
        
        for idx, img_path in enumerate(self.images):
            # Tạo nội dung bài viết
            content = f"""
========================================
BÀI VIẾT AFFILIATE {idx+1} KÈM HÌNH ẢNH
========================================

🔥 SHOPEE 6.6 MEGA SALE 🔥

[HÌNH ẢNH: {img_path}]

✨ ƯU ĐÃI ĐẶC BIỆT:
• Giảm giá đến 50%
• Freeship 0Đ toàn quốc
• Voucher Xtra 6 triệu đồng

🛍️ MUA NGAY: https://shorten.asia/cBGVb2kE

#Shopee6_6 #Sale #Affiliate
"""
            post_file = f"post_with_image_{idx+1}.txt"
            with open(post_file, "w", encoding="utf-8") as f:
                f.write(content)
            posts.append(post_file)
            print(f"✅ Đã tạo: {post_file}")
        
        return posts

if __name__ == "__main__":
    # Chỉ định file Excel của bạn
    excel_file = "your_file.xlsx"  # Đổi tên file của bạn
    
    if os.path.exists(excel_file):
        extractor = ExcelImageExtractor(excel_file)
        images = extractor.extract_images()
        posts = extractor.create_post_with_images()
        print(f"\n✅ Hoàn thành! {len(images)} ảnh, {len(posts)} bài viết")
    else:
        print(f"❌ Không tìm thấy file: {excel_file}")
        print("Vui lòng đảm bảo file Excel ở cùng thư mục")