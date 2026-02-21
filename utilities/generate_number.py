from typing import List, Optional
from config import prefixes
import random

"""
تابع پیشرفته برای تولید شماره تلفن ایرانی با پشتیبانی از تمام مناطق

پارامترها:
region_bias: لیست پیش‌شماره‌های مناطق مورد نظر برای افزایش وزن (پیش‌فرض: None)
bias_strength: میزان افزایش وزن برای مناطق مورد نظر (پیش‌فرض: 30)

بازگشت:
شماره تلفن ایرانی در فرمت بین‌المللی
"""


def generate_number(
    region_bias: Optional[List[str]] = None, bias_strength: int = 30
) -> str:
    # Set bias for custom region.
    if region_bias:
        for prefix in region_bias:
            if prefix in prefixes:
                prefixes[prefix] += bias_strength

    # Chooise best or random prefix of first three numbers of phone num.
    prefix = random.choices(
        population=list(prefixes.keys()), weights=list(prefixes.values()), k=1
    )[0]

    # Generate other 6 letter of phone number.
    remaining = "".join([str(random.randint(0, 9)) for _ in range(6)])

    return f"+989{prefix}{remaining}"
