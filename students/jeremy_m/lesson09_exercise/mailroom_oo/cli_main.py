""" This is the main module for mailroom_oo and handles the user interaction. """

#!/usr/bin/env python3

# lesson 03 Exercise - String Formatting Lab
# Jeremy Monroe

import os
import pathlib
import time
from donor_models import Donor, DonorCollection

# This dict is just used to populate don_col.donors dict.
donors = {'Charlize Theron': [134000],
          'Charlie Boorman': [15, 5],
          'James Franco': [25, 250, 2, 500],
          'Nike': [22000],
          'Count Chocula': [1257633, 2532790]
          }

user_input = ''
input_prompt = '\n\n---->'


class DonorLetters():
    """ 
    Handles the creation of txt files formatted as thank you letters for each
    donor in the donors dict.
    """

    def __init__(self):
        pass

    def letters_for_all(self):
        """ 
        This function creates a directory in the cwd and fills that with an
        individual file (letter) for each donor.
        """
        clear_screen()
        dir_path = os.getcwd() + '/letters'
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        clear_screen()
        for donor in don_col.donors:
            letter_text = self.get_letter_text(donor)
            donor_filename = self.get_donor_filename(donor)
            with open(dir_path + '/' + donor_filename, 'w+') as new_file:
                new_file.write(letter_text)
        else:
            print("Letters Created at:\n{}\n\n".format(dir_path))

    def get_donor_filename(self, donor_name):
        """ Formats the supplied donor_name to use as a filename. """
        donor_filename = '_'.join(donor_name.split(' ')) + '.txt'
        return donor_filename

    def get_letter_text(self, donor_name):
        """ Formats the text for the donor letters. """
        letter_text = ("{:^41}\n"
                       "Thank you so much for your generous donation of:\n"
                       "{:>21}{:,}\n"
                       "We will always remember your money fondly.").format(
            donor_name, '$', int(don_col.donors[donor_name].donations[-1]))
        return letter_text


class ThankYou():
    """ 
    Handles creating a thank you letter for a donor.
    This includes adding a new donor if it does not exist, adding a new donation
    to a donors donations list, and printing the formatted thank you letter.
    """

    def __init__(self):
        pass

    def send_a_thank_you(self):
        """ 
        Gives a user the option to list all donors, or else will create a new
        donor using the inputted name and adds their new donation using the
        inputted amount.
        """
        clear_screen()

        donor_name_input, donation_amount = self.send_a_thank_you_inputs()
        don_col.add_donor(donor_name_input, donation_amount)

        clear_screen()
        self.print_thank_you_message(donor_name_input)

    def send_a_thank_you_inputs(self):
        """ 
        Returns donors name and their recent donation amount after getting both
        as input from the user.
        """
        donor_name_confirmation = False

        while not donor_name_confirmation:
            donor_name_input = input(
                "Please input the donors name" + input_prompt)

            if donor_name_input in don_col.donors:
                donor_name_confirmation = True
            else:
                donor_name_confirmation_input = input(('\nIs {} correct?\n'
                                                       'Type yes or no{}').format(donor_name_input, input_prompt))

                if donor_name_confirmation_input.lower() == 'yes':
                    donor_name_confirmation = True
                else:
                    print('\n')

        if donor_name_input == 'list':
            clear_screen()
            print("All donors:")
            for donor in donors:
                print(donor)

            donor_name_input = input(
                "\n\nPlease input the donors name" + input_prompt)

        # Keep asking for donation_amount until user enters a number.
        while True:
            try:
                donation_amount = int(input(
                    'How much did {} contribute?{}'.format(donor_name_input, input_prompt)))
                break
            except ValueError:
                print('Please enter a number.')

        return (donor_name_input, donation_amount)

    def print_thank_you_message(self, donor_name_input):
        """ Print a formatted message with donors name and recent donation amount """
        print(("{:^42}\n"
               "{:^42}\n"
               "For your incredibly generous donation of:\n"
               "{:>19}{:<23,}\n\n").format('Thank you so much',
                                           donor_name_input, '$',
                                           int(don_col.donors[donor_name_input].donations[-1])))


def clear_screen():
    """ Clears the terminal screen """
    os.system('cls') if os.name == 'nt' else os.system('clear')


don_col = DonorCollection()
donor_letters = DonorLetters()
thank_you = ThankYou()

main_menu_answers = {'1': thank_you.send_a_thank_you,
                     '2': don_col.generate_report, '3': donor_letters.letters_for_all}

if __name__ == "__main__":
    clear_screen()

    # This is just to populate the don_col.donors dict with some info to play with
    for donor, donations in donors.items():
        don_col.add_donor(donor, donations[0])
        if len(donations) > 1:
            for donation in donations[1:]:
                don_col.donors[donor].add_donation(donation)

    # Continue getting input until user types quit
    while user_input.lower() != 'quit':
        user_input = input(("What would you like to do?\n"
                            "1: to Send a Thank You\n"
                            "2: Create a Report\n"
                            "3 to create letters for all donors\n"
                            "quit: to Quit{}"
                            ).format(input_prompt))

        try:
            main_menu_answers.get(user_input, 'nothing')()
        except TypeError:
            clear_screen()
            continue
