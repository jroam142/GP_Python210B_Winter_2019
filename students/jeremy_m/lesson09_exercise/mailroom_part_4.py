#!/usr/bin/env python3

# lesson 03 Exercise - String Formatting Lab
# Jeremy Monroe

import os
import pathlib
import time

donors = {'Charlize Theron': [134000],
          'Charlie Boorman': [15, 5],
          'James Franco': [25, 250, 2, 500],
          'Nike': [22000],
          'Count Chocula': [1257633, 2532790]
          }

# donor_totals = {}

user_input = ''

messages = {'start': ("What would you like to do?\n"
                      "1: to Send a Thank You\n"
                      "2: Create a Report\n"
                      "3 to create letters for all donors\n"
                      "quit: to Quit"
                      ),
            'thanks': ("Please input the donors name "),
            'thank_you_message': ("{:^42}\n"
                                  "{:^42}\n"
                                  "For your incredibly generous donation of:\n"
                                  "{:>19}{:<23,}\n\n"),
            'donor_letter': ("{:^41}\n"
                             "Thank you so much for your generous donation of:\n"
                             "{:>21}{:,}\n"
                             "We will always remember your money fondly."),
            'letters_confirmation': 'Is this ok?\nType y or n:'
            }


def letters_for_all():
    """ This function creates a directory in the cwd and fills that with an
        individual file (letter) for each donor.
    """

    clear_screen()
    dir_path = os.getcwd() + '/letters'
    os.mkdir(dir_path)

    clear_screen()
    for donor in donors:
        letter_text = get_letter_text(donor)
        donor_filename = get_donor_filename(donor)
        with open(dir_path + '/' + donor_filename, 'w+') as new_file:
            new_file.write(letter_text)
    else:
        print("Letters Created at:\n{}\n\n".format(dir_path))


def get_donor_filename(donor_name):
    donor_filename = '_'.join(donor_name.split(' ')) + '.txt'
    return donor_filename


def get_letter_text(donor_name):
    letter_text = messages['donor_letter'].format(
        donor_name, '$', int(donors[donor_name][-1]))
    return letter_text


def send_a_thank_you():
    """ Gives a user the option to list all donors, or else will create a new
        donor using the inputted name and adds their new donation using the
        inputted amount """
    clear_screen()

    donor_name_input, donation_amount = send_a_thank_you_inputs()
    add_donor(donor_name_input, donation_amount)

    clear_screen()
    print_thank_you_message(donor_name_input)


def send_a_thank_you_inputs():
    """ Returns donors name and their recent donation amount after getting both
        as input from the user.
    """
    donor_name_input = get_user_input(messages['thanks'])

    if donor_name_input == 'list':
        clear_screen()
        print("All donors:")
        for donor in donors:
            print(donor)

        donor_name_input = get_user_input('\n\n' + messages['thanks'])

    # Keep asking for donation_amount until user enters a number.
    while True:
        try:
            donation_amount = int(get_user_input(
                'How much did {} contribute?'.format(donor_name_input)))
            break
        except ValueError:
            print('Please enter a number.')

    return (donor_name_input, donation_amount)


def print_thank_you_message(donor_name_input):
    """ Print a formatted message with donors name and recent donation amount """
    print(messages['thank_you_message'].format('Thank you so much',
                                               donor_name_input, '$', int(donors[donor_name_input][-1])))


def add_donor(donor_name_input, donation_amount):
    """ Adds a donor and their donation to the donors dict.
        Called in send_a_thank_you()
    """
    if donor_name_input in donors.keys():
        donors[donor_name_input].append(donation_amount)
    else:
        donors[donor_name_input] = [donation_amount]


def create_a_report():
    """ Prints a formatted report showing donor name, total donations, number of
        donations, and average donation amount. """
    clear_screen()

    sorted_donor_sums = sum_donors_donations()

    print_report(sorted_donor_sums)


def sum_donors_donations():
    """ Returns a dict sorted by values. The values are the sums of a donors 
        donations
    """
    donor_sums = {donor: sum(donations)
                  for donor, donations in donors.items()}

    sorted_by_values = sorted((value, key)
                              for (key, value) in donor_sums.items())

    return sorted_by_values    


def print_report(sorted_donor_totals):
    """ Prints a formatted report showing info for each donor in order from
        highest total donations to least.
    """
    # This prints the top of the table
    print("{:25} | {:12} | {:<19} | {:<16}".format(
        'Name', 'Total Given', 'Number of Donations', 'Average Donation'))
    print('-' * 81)

    for total_donor in sorted_donor_totals[::-1]:
        print('{:25} | ${:<11,} | {:^19} | ${:<16,}'.format(
            total_donor[1], total_donor[0], len(donors[total_donor[1]]), (total_donor[0] / len(donors[total_donor[1]]))))
    print('\n\n')


def get_user_input(msg):
    """ Gets a users input using msg as the prompt """
    return input(msg + '\n\n---->')


def clear_screen():
    """ Clears the terminal screen """
    os.system('cls') if os.name == 'nt' else os.system('clear')


main_menu_answers = {'1': send_a_thank_you,
                     '2': create_a_report, '3': letters_for_all}

if __name__ == "__main__":
    clear_screen()

    # Continue getting input until user types quit
    while user_input.lower() != 'quit':
        user_input = get_user_input(messages['start'])

        try:
            main_menu_answers.get(user_input, 'nothing')()
        except TypeError:
            clear_screen()
            continue
