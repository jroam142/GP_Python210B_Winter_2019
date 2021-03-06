import cli_main as mp
import os




def test_add_donor():
    """ Testing whether new donors are added to donors dict when user selects
        send_a_thank_you option
    """
    mp.don_col.add_donor("Chomson", 1234)
    assert 'Chomson' in mp.don_col.donors


def test_add_donor_new_donation():
    """ Testing whether an exitisting donors old donations will be overwritten
        by new ones.
    """
    mp.don_col.add_donor('Lemon Grass', 2020)
    mp.don_col.add_donor('Lemon Grass', 3030)
    assert mp.don_col.donors['Lemon Grass'].donations[-1] == 3030


def test_sum_donors_donations():
    """ Testing whether a donors donations are summed correctly and if donor sums
        dict is sorted properly.
    """
    mp.don_col.add_donor('James', -5)
    mp.don_col.add_donor('James', -3)
    sorted_test_dict = mp.don_col.sum_donors_donations()
    assert sorted_test_dict[0][1] == 'James'
    assert sorted_test_dict[0][0] == -8


def test_get_donor_filename():
    """ Checks to make sure donor filenames are generated as expected """
    test_filename = mp.donor_letters.get_donor_filename("Seat Cushion")
    assert test_filename == 'Seat_Cushion.txt'


def test_get_letter_text():
    """ Checks to see if 'letter_text' from get_letter_text is accurate """
    mp.don_col.add_donor('Sean Hannity', 400)
    test_letter_text = mp.donor_letters.get_letter_text('Sean Hannity')
    correct_letter_text = ("{:^41}\n"
                           "Thank you so much for your generous donation of:\n"
                           "{:>21}{:,}\n"
                           "We will always remember your money fondly.").format('Sean Hannity', '$', 400)
    assert test_letter_text == correct_letter_text


def test_letters_for_all():
    """ First tests whether the 'letters' dir was created, then checks if a file
        was created for each donor
    """
    if not os.path.isdir('letters'):
        mp.donor_letters.letters_for_all()
    assert os.path.isdir('letters')
    for donor in mp.don_col.donors:
        donor_filename = mp.donor_letters.get_donor_filename(donor)
        assert os.path.isfile('./letters/{}'.format(donor_filename))
