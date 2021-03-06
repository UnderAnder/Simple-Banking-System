import random


class Account:
    def __init__(self, number, pin):
        self.balance = 0
        if number is None and pin is None:
            self.card = self.new_account()
        else:
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


class Card:
    card_database = {}

    def __init__(self):
        self.number = None
        self.pin = None

    def generate_card(self):
        card_number_bin = '400000'
        card_number_checksum = '8'
        card_number_ain = random.randint(100000000, 999999999)
        card_number = card_number_bin + str(card_number_ain) + card_number_checksum

        if card_number in self.card_database:
            self.generate_card()
        card_pin = random.randint(1000, 9999)
        self.card_database[card_number] = card_pin
        self.number = card_number
        self.pin = card_pin
        return self

    def auth(self, number, pin):
        if number in self.card_database:
            if pin == self.card_database[number]:
                print('You have successfully logged in!')
                Menu('account_menu')
                return self
        else:
            print('Wrong card number or PIN!')
        return None


class Menu:
    def __init__(self, state):
        self.state = state
        self.account = None
        if state == 'main_menu':
            self.main_menu()
        if state == 'account_menu':
            self.account_menu()

    def main_menu(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')

        self.choice(input(), 'main_menu')

    def login_menu(self):
        card_number = input('Enter your card number:\n')
        card_pin = input('Enter your PIN:\n')
        Account(card_number, card_pin)

    def account_menu(self):
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')

        self.choice(input(), 'account_menu')

    def choice(self, n, state):
        if state == 'main_menu':
            if n == '1':
                self.account = Account(None, None)
            elif n == '2':
                self.login_menu()
            elif n == '0':
                self.exit()
            else:
                print('input 1, 2 or 0 for exit')
                self.choice(input(), 'main_menu')
        elif state == 'account_menu':
            if n == '1':
                self.account.show_balance()
            elif n == '2':
                self.login_menu()
            elif n == '0':
                self.exit()
            else:
                print('input 1, 2 or 0 for exit')
                self.choice(input(), 'account_menu')

    def exit(self):
        print('Bye!')
        exit()


def main():
    Menu('main_menu')


if __name__ == '__main__':
    main()
