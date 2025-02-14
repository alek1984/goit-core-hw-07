
from collections import UserDict
from datetime import datetime, timedelta
import re


# Base class for fields
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Name field
class Name(Field):
    pass


# Phone field with validation
class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)


# Birthday field with validation (stored as a string)
class Birthday(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")
        super().__init__(value)


# Contact record class
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None  # Optional birthday field

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = Phone(new_number).value
                return
        raise ValueError("Phone number not found.")

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def show_birthday(self):
        if self.birthday:
            return f"Birthday: {self.birthday}"
        return "No birthday set."

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = f", {self.show_birthday()}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"


# Address book class
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        now = datetime.now()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                # Adjust the year to the current year for comparison
                birthday_this_year = birthday.replace(year=now.year)
                if 0 <= (birthday_this_year - now).days < days:
                    upcoming.append(f"{record.name.value}: {record.birthday.value}")
        return "\n".join(upcoming) if upcoming else "No upcoming birthdays."

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


# Decorator for error handling
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper


# Command functions
@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    record.add_phone(phone)
    return message


@input_error
def change_phone(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return f"Phone number updated for {name}."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    return ", ".join(p.value for p in record.phones)


@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(date)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    return record.show_birthday()


@input_error
def birthdays(_, book):
    return book.get_upcoming_birthdays()


@input_error
def show_all(_, book):
    return str(book) or "No contacts in the address book."


# Main loop
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if user_input in ["close", "exit"]:
            print("Good bye!")
            break

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "hello":
            print("How can I help you?")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

