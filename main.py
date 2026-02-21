from utilities.generate_number import generate_number
from utilities.check_phone import check_phone
import asyncio
import config
import json

main_file_path = __file__.replace("main.py", "")
file_name = "database/checked_phones.json"


# Write the all data to the database json file
def write_database(input_object: list[str]):
    with open(main_file_path + file_name, "w") as file:
        file.write(json.dumps(input_object, indent=4, sort_keys=True))

        return True


# Read database json file
def read_database() -> list[str] | None:
    try:
        with open(main_file_path + file_name, "r") as file:
            return json.loads(file.read())

    except:
        return None


write_database(read_database() or [])

if __name__ == "__main__":
    while True:
        gen_phone = generate_number()
        checked_phone_numbers = read_database()

        try:
            checked_username = asyncio.run(check_phone(gen_phone, config.checked_username))
            if checked_username:
                print(f"Shomare telephone peida shod: {checked_username} | {gen_phone}")

                checked_phone_numbers.append(str(checked_username))
                write_database(checked_phone_numbers)

                break

            else:
                checked_phone_numbers.append(gen_phone)
                write_database(checked_phone_numbers)
                continue

        except:
            checked_phone_numbers.append(gen_phone)
            write_database(checked_phone_numbers)
            continue
