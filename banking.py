import random
import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.create_table()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS card('
                    'id INTEGER PRIMARY KEY AUTOINCREMENT,'  # i know it's bad
                    'number TEXT,'
                    'pin TEXT,'
                    'balance INTEGER DEFAULT 0)'
                    ';')
        self.conn.commit()

    def add_new_card(self, card_number, pin):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO card (number, pin)'
                    f'VALUES({card_number},	{pin})'
                    ';')
        self.conn.commit()

    def get_card(self, card_number):
        cur = self.conn.cursor()
        # WARNING very secure -_-, idc
        cur.execute('SELECT number, pin, balance '
                    'FROM card '
                    f'WHERE number = {card_number};')
        return cur.fetchone()


class Account:
    def __init__(self):
        self.balance = 0
        self.card = None

    def auth(self, number, pin):
        if number is None and pin is None:
            self.new_account()
        else:
            if self.card is None:
                self.card = Card().auth(number, pin)

    @staticmethod
    def new_account():
        card = Card().generate_card()
        print('Your card has been created')
        print('Your card number:')
        print(card.number)
        print('Your card PIN:')
        print(card.pin)

    def show_balance(self):
        print('Balance:', self.balance)

    def logout(self):
        self.card = None


class Card:
    card_database = DB()

    def __init__(self):
        self.number = None
        self.pin = None
        self.bd = self.card_database

    def generate_card(self):
        card_number_bin = '400000'
        card_number_ain = '{:09d}'.format(random.randrange(999999999))
        card_number_checksum = self.luhn(card_number_bin + card_number_ain)
        card_number = int(card_number_bin + card_number_ain + card_number_checksum)

        # check for uniq card number
        if self.card_database.get_card(card_number) is not None:
            self.generate_card()

        self.number = card_number
        self.pin = '{:04d}'.format(random.randrange(9999))
        self.card_database.add_new_card(self.number, self.pin)
        return self

    @staticmethod
    def luhn(card_number_without_checksum):
        digit_sum = 0
        for index, digit in enumerate(card_number_without_checksum):
            digit = int(digit)
            if index % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            digit_sum += digit
        if digit_sum % 10 == 0:
            return str(0)
        return str(10 - (digit_sum % 10))

    def auth(self, card_number, pin):
        card_in_db = self.card_database.get_card(card_number)
        print(card_in_db)
        if card_in_db is not None and str(card_number) in card_in_db and pin in card_in_db:
            print('You have successfully logged in!')
            return self

        print('Wrong card number or PIN!')
        return None


class Menu:
    def __init__(self, account):
        self.account = account

    def show(self):
        if self.account.card is None:
            self.main_menu()
        else:
            self.account_menu()

    def main_menu(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')

        self.choice(input())

    def login_menu(self):
        card_number = int(input('Enter your card number:\n'))
        card_pin = input('Enter your PIN:\n')
        self.account.auth(card_number, card_pin)

    def account_menu(self):
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')

        self.choice(input())

    def choice(self, n):
        if self.account.card is None:
            if n == '1':
                self.account.auth(None, None)
            elif n == '2':
                self.login_menu()
            elif n == '0':
                self.exit()
            else:
                print('input 1, 2 or 0 for exit')
                self.choice(input())
        elif self.account.card is not None:
            if n == '1':
                self.account.show_balance()
            elif n == '2':
                self.account.logout()
            elif n == '0':
                self.exit()
            else:
                print('input 1, 2 or 0 for exit')
                self.choice(input())
        else:
            print("Error")
            exit()

    @staticmethod
    def exit():
        print('Bye!')
        exit()


def main():
    account = Account()
    while True:
        Menu(account).show()


if __name__ == '__main__':
    main()
