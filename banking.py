import random


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

    def new_account(self):
        card = Card().generate_card()
        print('Your card has been created')
        print('Your card number:')
        print(card.number)
        print('Your card PIN:')
        print(card.pin)
        return card

    def show_balance(self):
        print('Balance:', self.balance)

    def logout(self):
        self.card = None


class Card:
    card_database = {}

    def __init__(self):
        self.number = None
        self.pin = None

    def generate_card(self):
        card_number_bin = '400000'
        card_number_checksum = '8'
        card_number_ain = random.randint(100000000, 999999999)
        card_number = int(card_number_bin + str(card_number_ain) + card_number_checksum)

        if card_number in self.card_database:
            self.generate_card()
        card_pin = random.randint(1000, 9999)
        self.card_database[card_number] = card_pin
        self.number = card_number
        self.pin = card_pin
        return self

    def auth(self, number, pin):
        if number in self.card_database and pin == self.card_database[number]:
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
        card_pin = int(input('Enter your PIN:\n'))
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

    def exit(self):
        print('Bye!')
        exit()


def main():
    account = Account()
    while True:
        Menu(account).show()


if __name__ == '__main__':
    main()
