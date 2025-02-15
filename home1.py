from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        day, month, year = map(int, value.split('.'))
        try:
            datetime(year, month, day)
        except ValueError:
            raise ValueError("Invalid date.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
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
    
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_birthday(self, date):
        self.birthday = Birthday(date)
    
    def show_birthday(self):
        if self.birthday:
            return f"Birthday of {self.name}: {self.birthday}"
        return f"No birthday set for {self.name}"
    
    def __str__(self):
        phone_list = '; '.join(p.value for p in self.phones)
        birthday_info = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_list}{birthday_info}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                day, month, year = map(int, record.birthday.value.split('.'))
                birthday_this_year = datetime(today.year, month, day).date()
                if birthday_this_year < today:
                    birthday_this_year = datetime(today.year + 1, month, day).date()
                
                days_until = (birthday_this_year - today).days
                if days_until <= 7:
                    greeting_day = birthday_this_year
                    if greeting_day.weekday() >= 5:  # Якщо вихідний, переносимо на понеділок
                        greeting_day += timedelta(days=(7 - greeting_day.weekday()))
                    upcoming.append(f"{record.name.value} - {greeting_day.strftime('%d.%m.%Y')}")
        return "\n".join(upcoming) if upcoming else "No upcoming birthdays."
    
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    return record.show_birthday()

@input_error
def birthdays(args, book):
    return book.get_upcoming_birthdays()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            name, phone = args
            record = book.find(name)
            if not record:
                record = Record(name)
                book.add_record(record)
            record.add_phone(phone)
            print("Contact added.")

        elif command == "change":
            name, old_phone, new_phone = args
            record = book.find(name)
            if record:
                record.edit_phone(old_phone, new_phone)
                print("Phone number updated.")
            else:
                print("Contact not found.")

        elif command == "phone":
            name = args[0]
            record = book.find(name)
            print(record.show_phones() if record else "Contact not found.")

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            name, date = args
            record = book.find(name)
            if record:
                record.add_birthday(date)
                print("Birthday added.")
            else:
                print("Contact not found.")

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

   

