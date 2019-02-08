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

donor_totals = {}

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
    clear_screen()
    print('Note: This operation will create a directory in the current working directory')
    if get_user_input(messages['letters_confirmation']).lower() == 'y':
        dir_path = os.getcwd() + '/letters'
        os.mkdir(dir_path)

        clear_screen()
        for donor in donors:
            donor_filename = '_'.join(donor.split(' ')) + '.txt'
            with open(os.path.join(dir_path + donor_filename), 'w+') as new_file:
                new_file.write(messages['donor_letter'].format(
                    donor, '$', int(donors[donor][-1])))
        else:
            print("Letters Created at:\n{}\n\n".format(dir_path))


def send_a_thank_you():
    """ Gives a user the option to list all donors, or else will create a new
        donor using the inputted name and adds their new donation using the
        inputted amount """
    clear_screen()

    # Ask user for the donors name
    thank_you_input = get_user_input(messages['thanks'])

    # If the donor exists in donor list ask for latest donation amount and add it
    if thank_you_input == 'list':
        clear_screen()
        print("All donors:")
        for donor, donations in donors.items():
            print('\t' + donor)

        thank_you_input = get_user_input('\n\n' + messages['thanks'])

    # If donor isn't in donor list ask for their first donation amount and add it
    donation_amount = input(
        'How much did {} contribute?\n---->'.format(thank_you_input))

    if thank_you_input in donors.keys():
        donors[thank_you_input].append(donation_amount)
    else:
        donors[thank_you_input] = []
        donors[thank_you_input].append(donation_amount)

    clear_screen()
    # Print a formatted message with donors name and recent donation amount
    print(messages['thank_you_message'].format('Thank you so much',
                                               thank_you_input, '$', int(donors[thank_you_input][-1])))


def create_a_report():
    """ Prints a formatted report showing donor name, total donations, number of
        donations, and average donation amount. """
    clear_screen()

    # This prints the top of the table
    print("{:25} | {:12} | {:<19} | {:<16}".format(
        'Name', 'Total Given', 'Number of Donations', 'Average Donation'))
    print('-' * 81)

    # Get the sum of a donors donations and add that with their name to a new dict
    for donor, donations in donors.items():
        placeholder = 0
        for donation in donations:
            placeholder += int(donation)

        donor_totals[donor] = placeholder

    # Sort donor_totals dict by their values
    sorted_donor_totals = sorted((value, key)
                                 for (key, value) in donor_totals.items())

    # Print each donor info from most donated to least
    for total_donor in sorted_donor_totals[::-1]:
        print('{:25} | ${:<11,} | {:^19} | ${:<16,}'.format(
            total_donor[1], total_donor[0], len(donations), (total_donor[0] / len(donations))))
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

        if user_input.lower() != 'quit':
            main_menu_answers.get(user_input, 'nothing')()

        # if user_input.lower() == 'thanks':
        #     send_a_thank_you()
        # elif user_input.lower() == 'report':
        #     create_a_report()
        # elif user_input.lower() == 'letters':
        #     letters_for_all()
