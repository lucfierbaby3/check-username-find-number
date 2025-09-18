from typing import List, Optional
import random

"""
تابع پیشرفته برای تولید شماره تلفن ایرانی با پشتیبانی از تمام مناطق

پارامترها:
region_bias: لیست پیش‌شماره‌های مناطق مورد نظر برای افزایش وزن (پیش‌فرض: None)
bias_strength: میزان افزایش وزن برای مناطق مورد نظر (پیش‌فرض: 30)

بازگشت:
شماره تلفن ایرانی در فرمت بین‌المللی
"""
def generate_number(region_bias: Optional[List[str]] = None, bias_strength: int = 30) -> str:
    
    # پیش‌شماره‌های معتبر ایران با وزن‌های پیش‌فرض بر اساس توزیع جمعیتی
    prefixes = {
        # همراه اول (بر اساس تقسیم‌بندی استانی)
        '910': 12,  # کشوری
        '911': 10,  # مازندران، گلستان، گیلان
        '912': 15,  # تهران، البرز، قم، سمنان، زنجان، قزوین
        '913': 10,  # اصفهان، یزد، کرمان، چهارمحال و بختیاری
        '914': 10,  # آذربایجان شرقی، آذربایجان غربی، اردبیل
        '915': 10,  # خراسان رضوی، شمالی، جنوبی، سیستان و بلوچستان
        '916': 10,  # خوزستان، لرستان
        '917': 10,  # فارس، بوشهر، هرمزگان، کهگیلویه و بویراحمد
        '918': 10,  # کردستان، ایلام، مرکزی، کرمانشاه، همدان
        '919': 12,  # اعتباری کشوری
        
        # ایرانسل
        '930': 12, '933': 12, '935': 15, '936': 12, 
        '937': 12, '938': 12, '939': 12,
        '901': 8, '902': 8, '903': 8, '904': 5, '905': 8,
        
        # رایتل
        '920': 10, '921': 10, '922': 12,
        
        # همراه اول نسل جدید
        '990': 8, '991': 8, '992': 8, '993': 8, '994': 5,
        
        # اپراتورهای مجازی
        '931': 3, '932': 3, '934': 3,  # اسپادان، تالیا، کیش
        '998': 2, '999': 2,  # شاتل موبایل
    }
    
    # Set bias for custom region.
    if region_bias:
        for prefix in region_bias:
            if prefix in prefixes:
                prefixes[prefix] += bias_strength
    
    # Chooise best or random prefix of first three numbers of phone num.
    prefix = random.choices(
        population=list(prefixes.keys()),
        weights=list(prefixes.values()),
        k=1
    )[0]
    
    # Generate other 6 letter of phone number.
    remaining = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    return f"+989{prefix}{remaining}"