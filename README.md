# 📱 check-username-find-number

> **Disclaimer:** This project is intended for learning purposes only. Do not use it for malicious activities.
> The algorithm can find Iranian phone numbers associated with a Telegram username.

---

## 🗂 Project Structure

```text
check-username-find-number/
│
├─ main.py                  # Main script to generate and check phone numbers
├─ config.py                # Configuration file for API_ID, API_HASH, SESSION_NAME
├─ example.env              # Example environment variables
├─ LICENSE                  # BSD 3-Clause License
├─ README.md                # Project readme
├─ .gitignore               # Git ignore rules
├─ .gitattributes           # Git attributes
│
├─ database/
│   └─ checked_phones.json  # Stores checked phone numbers
│
└─ utilities/
    ├─ generate_number.py   # Function to generate Iranian phone numbers
    └─ check_phone.py       # Async function to check phone number via Telegram API
```

---

## ⚙️ Configuration

* **config.py** reads your `.env` file:

| Variable           | Description                                      |
| ------------------ | ------------------------------------------------ |
| `API_ID`           | Telegram API ID (integer)                        |
| `API_HASH`         | Telegram API hash (string)                       |
| `SESSION_NAME`     | Name of the Telegram session file (string)       |
| `checked_username` | Username to search for (default: `@Sobhan_SRZA`) |

* **example.env** provides a template for `.env`:

```env
API_ID='your_api_id'
API_HASH='your_api_hash'
SESSION_NAME='check_session'
```

---

## 🧩 Main Components

### 1️⃣ `utilities/generate_number.py`

Generates Iranian phone numbers randomly, with optional region bias.

**Function:** `generate_number(region_bias: Optional[List[str]] = None, bias_strength: int = 30) -> str`

* **Parameters:**

  * `region_bias`: List of prefix strings to favor specific regions.
  * `bias_strength`: Weight for the biased prefixes.

* **Returns:** Phone number in international format, e.g., `+989133334567`.

* **Example:**

```python
from utilities.generate_number import generate_number

phone = generate_number(region_bias=['912', '935'], bias_strength=50)
print(phone)  # Output: +989123456789
```

---

### 2️⃣ `utilities/check_phone.py`

Asynchronously checks if a generated phone number belongs to a given Telegram username.

**Function:** `async def check_phone(phone_to_test: str, username_to_check: str) -> bool | None`

* **Parameters:**

  * `phone_to_test`: Phone number in international format (`+989xxxxxxxxx`).
  * `username_to_check`: Telegram username **without** `@`.

* **Returns:**

  * `True` if the phone matches the username.
  * `False` if it does not match or user has no username.
  * `None` in case of Telegram rate limiting or RPC errors.

* **Key Features:**

  * Adds the phone as a temporary Telegram contact.
  * Checks if the returned user matches the target username.
  * Deletes the temporary contact after checking.
  * Handles Telegram API rate limits (`FloodWaitError`) and RPC errors gracefully.

* **Example:**

```python
from utilities.check_phone import check_phone
import asyncio

result = asyncio.run(check_phone("+989123456789", "Sobhan_SRZA"))
print(result)  # True or False
```

---

### 3️⃣ `main.py`

Orchestrates phone number generation, checking, and database updates.

**Key Functions:**

#### `write_database(input_object: list[str]) -> bool`

* Writes the checked phone numbers list to `database/checked_phones.json`.
* Returns `True` after successful write.

#### `read_database() -> list[str] | None`

* Reads `database/checked_phones.json`.
* Returns the list of stored phone numbers or `None` if the file doesn't exist.

**Main Logic (simplified):**

```python
from utilities.generate_number import generate_number
from utilities.check_phone import check_phone
import asyncio
import config

gen_phone = generate_number()
checked_username = asyncio.run(check_phone(gen_phone, config.checked_username))
print(checked_username)
```

* ✅ Generates a phone number.
* ✅ Checks the number against a target username.
* ✅ Stores or prints the result.

---

## 💾 Database

**File:** `database/checked_phones.json`
**Type:** JSON array of strings

* **Purpose:** Stores all checked phone numbers to avoid rechecking.
* **Sample Content:**

```json
[
    "+989933776869",
    "+989917915906",
    "+989937241629",
    "+989905209473"
]
```

> ⚠️ Previous entries like `<coroutine object check_phone ...>` are invalid — they were added due to a previous bug. Only store actual phone numbers.

---

## 🛠 How to Use

1. Clone the repository:

```bash
git clone https://github.com/yourusername/check-username-find-number.git
cd check-username-find-number
```

2. Install dependencies:

```bash
pip install telethon python-dotenv
```

3. Set your `.env` file based on `example.env`.

4. Run the main script:

```bash
python main.py
```

* The script will generate a phone number and check it against the target Telegram username.

---

## ⚡ Features

* 🔹 Generate valid Iranian phone numbers with realistic region distribution.
* 🔹 Check if a phone number belongs to a Telegram username.
* 🔹 Async handling of Telegram API with error management.
* 🔹 Persistent storage of checked numbers to `checked_phones.json`.
* 🔹 Configurable via `.env` file.

---

## 🧩 Functions Summary

| Module                         | Function            | Description                                |
| ------------------------------ | ------------------- | ------------------------------------------ |
| `utilities/generate_number.py` | `generate_number()` | Generate random Iranian phone numbers.     |
| `utilities/check_phone.py`     | `check_phone()`     | Async check if phone belongs to username.  |
| `main.py`                      | `write_database()`  | Write checked numbers to JSON file.        |
| `main.py`                      | `read_database()`   | Read JSON file containing checked numbers. |

---

## 🎨 Design Notes

* Uses **Telethon** for Telegram API.
* JSON database is lightweight and easy to extend.
* All core logic is modular, making it easy to integrate into other scripts or bots.
* Emojis are used in logs to provide clarity for matching results ✅❌.

---

## 📄 License

BSD 3-Clause License — see `LICENSE` file.
© 2025 Sobhan.SRZA (mr.sinre)