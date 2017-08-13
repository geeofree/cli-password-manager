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
        # Print list of stored account passwords
        print('\n'.join('\t%i: %s' % (index, app_name) for index, app_name in enumerate(data_keys)))
        selected_option = input('\nSelect Password Number: ').lower()

        # Try-Except whether the given selected_option is a valid index on data_keys
        try:
            index = int(selected_option)
            pw_account = data_keys[index]
            pw_details = data[pw_account]
            print("\n\tPASSWORD_FOR: %s" % pw_account)
            [ print("\t%s: %s" % (key, value)) for key, value in pw_details.items() ]
            print("\n")
        except:
            if selected_option.isalpha() and selected_option == 'c':
                return
            else:
                print("\n\tInvalid option number\n")
    else:
        print("\n\tNo passwords currently stored.\n")
