# check_phone_username.py
import asyncio
import sys
from telethon import TelegramClient, functions, types
from telethon.errors import FloodWaitError, RPCError
import json

main_file_path = __file__.replace("main.py", "")
file_name = "database/checked_phones.json"

# مقداردهی: مقادیر خود را اینجا قرار دهید
API_ID = 1234567            # جایگزین با api_id شما
API_HASH = 'your_api_hash'  # جایگزین با api_hash شما
SESSION_NAME = 'check_session'  # نام سشن ذخیره‌شده

async def check_phone_matches_username(phone_to_test: str, username_to_check: str):
    """
    phone_to_test: شماره به فرمت بین‌المللی مثل +994501234567 یا 0501234567 (ترجیحاً با +کد)
    username_to_check: بدون @، مثلا: 'someusername'
    """
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    try:
        # یک InputPhoneContact ایجاد می‌کنیم (client_id می‌تواند هر عدد یکتا باشد)
        contact = types.InputPhoneContact(client_id=0, phone=phone_to_test, first_name="Temp", last_name="Temp")
        try:
            result = await client(functions.contacts.ImportContactsRequest([contact]))
        except FloodWaitError as e:
            print(f"Rate limited by Telegram. باید {e.seconds} ثانیه صبر کنید.")
            return None
        except RPCError as e:
            print("خطای RPC از تلگرام:", e)
            return None

        users = result.users  # لیست کاربران برگردانده شده برای контакتی که اضافه شد
        if not users:
            print("این شماره در تلگرام ثبت نشده یا اطلاعات قابل دسترسی نیست.")
            return False

        # معمولاً فقط یک user برمی‌گردد — اما ایمن عمل می‌کنیم و اولین user را بررسی می‌کنیم
        user = users[0]
        found_username = getattr(user, 'username', None)
        found_name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()

        if found_username:
            print(f"شماره مرتبط با یوزر: @{found_username} — نام نمایشی: {found_name}")
            matches = (found_username.lower() == username_to_check.lower().lstrip('@'))
            if matches:
                print("✅ شماره با یوزرنیم مورد نظر مطابقت دارد.")
            else:
                print("❌ شماره با یوزرنیم مورد نظر مطابقت ندارد.")
            return matches
        else:
            # کاربر موجود است ولی یوزرنیم تنظیم نکرده
            print(f"شماره متعلق به کاربری است اما یوزرنیم ندارد. نام نمایشی: {found_name}")
            return False

    finally:
        # تمیزکاری: مخاطب وارد شده را حذف می‌کنیم تا سابقه اضافه کردن نماند
        try:
            await client(functions.contacts.DeleteContactsRequest(id=[types.InputUser(user_id=0, access_hash=0)]))
        except Exception:
            # راهِ امن‌تر: قبل از حذف باید id واقعی کاربر را بسازیم؛ ولی برای جلوگیری از خطا،
            # تلاش می‌کنیم همه مخاطبین موقت با phone پاک شوند با روشی ساده‌تر:
            try:
                # سعی می‌کنیم contact را با شماره حذف کنیم (ابتدا fetch contacts و پیدا کردن آی‌دی)
                contacts = await client.get_contacts()
                for c in contacts:
                    if getattr(c, 'phone', None) and c.phone.replace('+','') == phone_to_test.replace('+',''):
                        await client(functions.contacts.DeleteContactsRequest(id=[c]))
            except Exception:
                # اگر پاک نشد نادیده می‌گیریم (سشن محلی را می‌توان دستی پاک کرد)
                pass
        await client.disconnect()


# Write the all data to the database json file
def write_database(input_object: object):
    with open(main_file_path + file_name, "w") as file:
        file.write(json.dumps(input_object, sort_keys=True))
        
        return True

# Read database json file
def read_database() -> list[str] | None:
    try:
        with open(main_file_path + file_name, "r") as file:
            return json.loads(file.read())
    
    except:
        return None
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_phone_username.py <phone_to_test> <username_to_check>")
        print("Example: python check_phone_username.py +994501234567 someusername")
        sys.exit(1)

    phone = sys.argv[1]
    username = sys.argv[2]

    res = asyncio.run(check_phone_matches_username(phone, username))
    if res is True:
        print("RESULT: MATCH")
    elif res is False:
        print("RESULT: NO MATCH")
    else:
        print("RESULT: ERROR or UNKNOWN")