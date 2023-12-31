from datetime import datetime as dt, timedelta
from collections import UserList
import pickle
import os
from abc import ABC, abstractmethod

class User(ABC):
    @abstractmethod
    def __init__(self, value):
        pass

    @property
    @abstractmethod
    def value(self):
        pass

class Name(User):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

class Phone(User):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

class Birthday(User):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

class Email(User):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

class Status(User):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

class Note(User):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

class Record:
    def __init__(self, name, phones, birthday, email, status, note):
        self.name = Name(name).value
        self.phones = [Phone(phone).value for phone in phones]
        self.birthday = Birthday(birthday).value
        self.email = Email(email).value
        self.status = Status(status).value
        self.note = Note(note).value

class AddressBook(UserList):
    def __init__(self):
        super().__init__()
        self.counter = -1

    def __setitem__(self, index, record):
        self.data[index] = {
            'name': record.name,
            'phones': record.phones,
            'birthday': record.birthday,
            'email': record.email,
            'status': record.status,
            'note': record.note
        }

    def log(self, action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')

    def edit(self, contact_name, parameter, new_value):
        names = []
        try:
            for account in self.data:
                names.append(account['name'])
                if account['name'] == contact_name:
                    if parameter == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parameter == 'email':
                        new_value = Email(new_value).value
                    elif parameter == 'status':
                        new_value = Status(new_value).value
                    elif parameter == 'phones':
                        new_contact = new_value.split(' ')
                        new_value = []
                        for number in new_contact:
                             new_value.append(Phone(number).value)
                    if parameter in account.keys():
                        account[parameter] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:
                raise NameError
        except ValueError:
            print('Incorrect parameter! Please provide correct parameter')
        except NameError:
            print('There is no such contact in address book!')
        else:
            self.log(f"Contact {contact_name} has been edited!")
            return True
        return False


    def save(self, file_name):
        with open(file_name + '.bin', 'wb') as file:
            pickle.dump(self.data, file)
        self.log("Addressbook has been saved!")

    def load(self, file_name):
        emptyness = os.stat(file_name + '.bin')
        if emptyness.st_size != 0:
            with open(file_name + '.bin', 'rb') as file:
                self.data = pickle.load(file)
            self.log("Addressbook has been loaded!")
        else:
            self.log('Adressbook has been created!')
        return self.data

    def add(self, record):
        account = {
            'name': record.name,
            'phones': record.phones,
            'birthday': record.birthday,
            'email': record.email,
            'status': record.status,
            'note': record.note
        }


        self.data.append(account)
        self.log(f"Contact {record.name} has been added.")

    def search(self, pattern: str, category: str):
        result = []
        category_new = category.strip().lower().replace(' ', '')
        pattern_new = pattern.strip().lower().replace(' ', '')

        for account in self.data:
            if category_new == 'phones':
                for phone in account['phones']:
                    if phone.lower().startswith(pattern_new):
                        result.append(account)
            elif account[category_new].lower().replace(' ', '') == pattern_new:
                result.append(account)
        if not result:
            return 'There is no such contact in address book!'
        return result

if __name__ == "__main__":
    address_book = AddressBook()

    record1 = Record(name="John Doe", phones=["123456789"], birthday="1990-01-01", email="john@example.com", status="Active", note="Some note")
    record2 = Record(name="Jane Doe", phones=["987654321"], birthday="1985-05-05", email="jane@example.com", status="Inactive", note="Another note")

    address_book.add(record1)
    address_book.add(record2)

    print("Address Book:")
    print(address_book)

    search_result = address_book.search("John Doe", "name")
    print("Search Result:")
    print(search_result)

    edit_result = address_book.edit("John Doe", "status", "Inactive")
    print("Edit Result:", edit_result)

    address_book.save("address_book_file")

    address_book.load("address_book_file")

    print("Address Book After Loading:")
    print(address_book)
