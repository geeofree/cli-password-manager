def print_options():
    """ Prints the Password Manager Options """
    print("""
    PASSWORD MANAGER
    by Geoffrey

    Options:
    1: Show Passwords         4: Delete Password
    2: Add Password           5: Show Options
    3: Change Password        0: Exit Password Manager
    """)


def ask_option_number(text="Enter Option Number: "):
    """ Asks for an input printing based on the given parameter text """
    return int(input(text))


def print_data(data):
    """
        Prints the list of stored password, gives the option to select from said list
        and returns the data object for valid data selections
    """
    if data:
        data_keys = list(data.keys())

        print("""
        Enter a number from the list below to show details:
        Press 'c' to cancel
        """)
        print('\n'.join('\t%i: %s' % (num, app_name) for num, app_name in enumerate(data_keys)))
        selected_option = input('\nSelect Password Number: ').lower()

        if selected_option == 'c':
            return
        elif int(selected_option) >= len(data_keys):
            print('Invalid option number\n')
        else:
            print(data[data_keys[int(selected_option)]], '\n')
    else:
        print("""
        No Password Stored Yet.
        """)
