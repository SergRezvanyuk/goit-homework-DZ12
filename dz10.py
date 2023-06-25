from collections import UserDict


class Field:
    def __init__(self, value=None):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name, phone):
        self.name = name
        if phone:
            self.phones = []
            self.phones.append(phone)
        else:
            self.phones = []
    
    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone


class AddressBook(UserDict):
    def add_record(self, record):
        key = record.name.value
        self.data[key] = record



