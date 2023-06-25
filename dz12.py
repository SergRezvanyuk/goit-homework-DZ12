from collections import UserDict
from datetime import datetime, timedelta
import re
import pickle


class Field:
    def __init__(self, value=None):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.__p_value = None
        self.value = value

    @property
    def value(self):
        return self.__p_value
    
    @value.setter
    def value(self, value):
        pattern = r'^[\(\)\-\d]+$'
        if re.match(pattern, value):
            self.__p_value = value
        else:
            raise ValueError("Wrong phone")



class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.__p_value = None
        self.value = value
    
    @property
    def value(self, value):
        return self.__p_value
    
    @value.setter
    def value(self, value):
        if isinstance(value, datetime) and value < datetime.now():
            self.__p_value = value
        else:
            raise Exception("Wrong date")


class Record:
    def __init__(self, name, phone = None, birthday = None):
        self.name = name
        self.birthday = birthday
        if phone:
            self.phones = []
            self.phones.append(phone)
        else:
            self.phones = []

    def days_to_birthday(self):
        if self.birthday._Birthday__p_value:
            b = self.birthday._Birthday__p_value
            month = b.month
            days = b.day
            year = datetime.now().year
            nb = datetime(year = year, month = month, day = days)
            if nb < datetime.now():
                nb = datetime(year = year+1, month = month, day = days)
            return f'{(nb - datetime.now()).days} days until the birthday'


    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone


class AddressBook(UserDict):
    STOP_ITER = 3
    def __iter__(self):
        self._index = 0
        self._keys = list(self.data.keys())
        return self

    def __next__(self):
        if self._index >= len(self._keys):
            raise StopIteration
        else:
            start = self._index
            end = min(self._index + self.STOP_ITER, len(self._keys))
            self._index += self.STOP_ITER
            return [self.data[key] for key in self._keys[start:end]]


    def add_record(self, record):
        key = record.name.value
        self.data[key] = record
        write_data()

    def search_name(self, name):
        f=''
        for k,v in self.data.items():
            if name in k:          
                f = f + k + ' \n' 
                if v.phones:
                    f = f + ' ' * len(k)+ ' Phone: '
                    l = len(v.phones)
                    for tel in range(l):
                        f += v.phones[tel].value +' '
                    f += '\n'    
                if v.birthday:
                    f = f + ' ' * len(k) + ' birthday: ' + str(v.birthday._Birthday__p_value.date())   
                    f += '\n'     
        return f
    
    def search_phone(self, phone):
        f=''
        for k,v in self.data.items():
            for n in range(len(v.phones)):
                if phone in v.phones[n].value:
                    f = f + k + ' Phone : ' + v.phones[n].value+'\n'
            
        return f




def write_data():
    with open(file_name, "wb") as fh:
        pickle.dump(address_book, fh)

file_name = 'AddressBook.bin'
address_book = AddressBook()
with open(file_name, "rb") as fh:
    address_book = pickle.load(fh)
    
    






