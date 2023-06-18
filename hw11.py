from datetime import datetime, date
from collections import UserDict
class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 5  # Розмір сторінки за замовчуванням

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self):
        records = list(self.data.values())
        num_pages = len(records) // self.page_size + 1

        for page in range(num_pages):
            start = page * self.page_size
            end = start + self.page_size
            yield records[start:end]

class Record:
    def __init__(self, name, *fields):
        self.name = name
        self.fields = list(fields)

    def add_field(self, field):
        self.fields.append(field)

    def delete_fields(self, field):
        if field in self.fields:
            self.fields.remove(field)

    def edit_fields(self, old_field, new_field):
        if old_field in self.fields:
            index = self.fields.index(old_field)
            self.fields[index] = new_field

    def days_to_birthday(self):
        birthday_field = self.get_birthday_field()
        if birthday_field:
            today = date.today()
            next_birthday = date(today.year, birthday_field.value.month, birthday_field.value.day)

            if next_birthday < today:
                next_birthday = date(today.year + 1, birthday_field.value.month, birthday_field.value.day)

            days_left = (next_birthday - today).days
            return days_left

    def get_birthday_field(self):
        for field in self.fields:
            if isinstance(field, Birthday):
                return field
        return None

class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

class Name(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if not isinstance(value, str) or not value.isdigit():
            raise ValueError("Phone number must be a string of digits only.")

class Birthday(Field):
    def validate(self, value):
        if not isinstance(value, date):
            raise ValueError("Birthday must be a date object.")

        today = date.today()
        if value < today:
            raise ValueError("Birthday must be a future date.")

