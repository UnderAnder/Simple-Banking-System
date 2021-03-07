import random
import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.create_table()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS card('
                    'id INTEGER PRIMARY KEY,'
                    'number TEXT,'
                    'pin TEXT,'
                    'balance INTEGER DEFAULT 0)'
                    ';')
        self.conn.commit()

    def add_new_card(self, card_number, pin):
        pin = f"'{pin}'"  # fix bug when lead zeroes don't save in db, check "Rigid Affinity"
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

    def get_balance(self, card_number):
        cur = self.conn.cursor()
        cur.execute('SELECT balance '
                    'FROM card '
                    f'WHERE number = {card_number};')
        return int(cur.fetchone()[0])

    def add_income(self, card_number, deposit):
        cur = self.conn.cursor()
        cur.execute('UPDATE card '
                    f'SET balance = balance + {deposit} '
                    f'WHERE number = {card_number};')
        self.conn.commit()
        print('Income was added!')

    def transfer(self, card_number, deposit, target):
        cur = self.conn.cursor()
        cur.execute('UPDATE card '
                    f'SET balance = balance - {deposit} '
                    f'WHERE number = {card_number};')

        cur.execute('UPDATE card '
                    f'SET balance = balance + {deposit} '
                    f'WHERE number = {target};')
        self.conn.commit()

    def close_account(self, card_number):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM card '
                    f'WHERE number = {card_number};')
        self.conn.commit()
        print('The account has been closed!')


class Account:
    def __init__(self):
        self.card = None

    @staticmethod
    def new_account():
        card = Card().generate_card()
        print('Your card has been created')
        print('Your card number:')
        print(card.number)
        print('Your card PIN:')
        print(card.pin)

    def auth(self, number, pin):
        if number is None and pin is None:
            self.new_account()
        else:
            self.card = Card().auth(number, pin)

    def transfer_card_checks(self, target):
        if self.card.number == target:
            print("You can't transfer money to the same account!")
            return False

        if not Card().luhn_check(target):
            print('Probably you made a mistake in the card number. Please try again!')
            return False
        if self.card.db.get_card(target) is None:
            print('Such a card does not exist.')
            return False
        return True

    def transfer_balance_check(self, deposit):
        balance = self.card.db.get_balance(self.card.number)
        if balance < deposit:
            print('Not enough money!')
            return False
        return True

    def show_balance(self):
        print('Balance:', self.card.db.get_balance(self.card.number))

    def logout(self):
        self.card = None



class Card:
    card_database = DB()

    def __init__(self):
        self.number = None
        self.pin = None
        self.db = self.card_database

    def generate_card(self):
        card_number_bin = '400000'
        card_number_ain = '{:09d}'.format(random.randrange(999999999))
        card_number_checksum = self.luhn_gen_checksum(card_number_bin + card_number_ain)
        card_number = int(card_number_bin + card_number_ain + card_number_checksum)

        # check for unique card number
        if self.card_database.get_card(card_number) is not None:
            self.generate_card()

        self.number = card_number
        self.pin = '{:04d}'.format(random.randrange(9999))
        self.card_database.add_new_card(self.number, self.pin)
        return self

    @staticmethod
    def luhn(card_number):
        card_number = str(card_number)
        digit_sum = 0
        for index, digit in enumerate(card_number):
            digit = int(digit)
            if index % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            digit_sum += digit
        return digit_sum

    @staticmethod
    def luhn_gen_checksum(card_number_without_checksum):
        digit_sum = Card().luhn(card_number_without_checksum)
        if digit_sum % 10 == 0:
            return str(0)
        return str(10 - (digit_sum % 10))

    @staticmethod
    def luhn_check(card_number):
        digit_sum = Card().luhn(card_number)
        if digit_sum % 10 == 0:
            return True
        return False

    def auth(self, card_number, pin):
        card_in_db = self.card_database.get_card(card_number)
        if card_in_db is not None and str(card_number) in card_in_db and pin in card_in_db:
            print('You have successfully logged in!')
            self.number = card_number
            self.pin = pin
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
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')

        self.choice(input())

    def choice(self, n):
        if self.account.card is None:
            if n == '1':  # Create an account
                self.account.auth(None, None)

            elif n == '2':  # Log into account
                self.login_menu()

            elif n == '0':  # Exit
                self.exit()

            else:
                print('input 1, 2 or 0 for exit')
                self.choice(input())
        else:
            if n == '1':  # Balance
                self.account.show_balance()

            elif n == '2':  # Add income
                deposit = int(input('Enter income:\n'))
                self.account.card.db.add_income(self.account.card.number, deposit)

            elif n == '3':  # Do transfer
                target_number = int(input('Enter card number:\n'))
                if not self.account.transfer_card_checks(target_number):
                    return False
                deposit = int(input('Enter how much money you want to transfer:'))
                if not self.account.transfer_balance_check(deposit):
                    return False
                self.account.card.db.transfer(self.account.card.number, deposit, target_number)

            elif n == '4':  # Close account
                self.account.card.db.close_account(self.account.card.number)
                self.account.logout()

            elif n == '5':  # Log out
                self.account.logout()

            elif n == '0':  # Exit
                self.exit()

            else:
                print('input 1, 2, 3, 4, 5 or 0 for exit')
                self.choice(input())

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
