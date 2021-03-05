import random


class Account:
    def __init__(self, number, pin):
        self.card = None
        if number is None and pin is None:
            self.new_account()
        else:
            self.login(number, pin)

    def new_account(self):
        self.card = Card()
        print('Your card has been created')
        print('Your card number:')
        print(self.card.number)
        print('Your card PIN:')
        print(Card.card_database[self.card.number])

    def login(self, number, pin):
        card_database = Card.card_database
        if number in card_database:
            if pin == card_database[number]:
                print('You have successfully logged in!')
                Menu('account_menu')
        else:
            print('Wrong card number or PIN!')


class Card:
    card_database = {}

    def __init__(self):
        self.number = self.generate_card()

    def generate_card(self):
        card_number_bin = '400000'
        card_number_checksum = '8'
        card_number_ain = random.randint(100000000, 999999999)
        card_number = card_number_bin + str(card_number_ain) + card_number_checksum

        if card_number in self.card_database:
            self.generate_card()
        card_pin = random.randint(1000, 9999)
        self.card_database[card_number] = card_pin
        return card_number


class Menu:
    def __init__(self, state):
        self.state = state
        if state == 'main_menu':
            self.main_menu()
        if state == 'account_menu':
            self.account_menu()

    def main_menu(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')

        self.choice(input(), self.state)

    def login_menu(self):
        card_number = input('Enter your card number:\n')
        card_pin = input('Enter your PIN:\n')
        Account(card_number, card_pin)

    def account_menu(self):
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')

    def choice(self, n, state):
        if state == 'main_menu':
            if n == '1':
                Account(None, None)
            elif n == '2':
                self.login_menu()
            elif n == '0':
                self.exit()
            else:
                print('input 1, 2 or 0 for exit')
                self.choice(input(), self.state)
        elif state == 'login_menu':
            self.account_menu()

    def exit(self):
        print('Bye!')
        return


def main():
    Menu('main_menu')


if __name__ == '__main__':
    main()
