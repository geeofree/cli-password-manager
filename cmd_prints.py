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
    try:
        return int(input(text))
    except:
        return input(text)
