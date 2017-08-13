import os
import bcrypt

class Locker:
    def __init__(self, filename='locker'):
        self.filename = '%s.txt' % filename
        self.__file_data = {}


    def get_locker_data(self):
        """ Reads a locker file via the given filename instance property """
        if os.path.isfile(self.filename):
            curr_parent = ''

            with open(self.filename, 'r') as locker_file:
                # Get each new line from the file
                for data in locker_file.read().split('\n'):
                    line = data.split('\n')[0]
                    # Check if line is not empty
                    if line:
                        if '\t' in line:
                            metadata = [ metadata.strip() for metadata in line.split(':') ]
                            key, value = metadata[0], metadata[1]
                            self.__file_data[curr_parent][key] = value
                        else:
                            curr_parent = line
                            self.__file_data[curr_parent] = {}
            return self.__file_data
        else:
            # Create the file and try again recursively
            print("No file '%s' found, creating one instead" % self.filename)
            self.save({})
            return self.get_locker_data()


    def save(self, locker_data):
        """
            Writes to the file with the password data and metadata
                locker_data:
                    A dictionary containing all the account password data and metadata for your accounts
                filename:
                    The location/filename where the data is to be stored
        """
        data = ''
        data_content = locker_data.items()

        # Check if data is not empty
        if data_content:
            for app_name, metadata in data_content:
                data += app_name + '\n'
                for key, value in metadata.items():
                    data += '\t%s: %s\n' % (key, str(value))

        with open(self.filename, 'w') as locker_file:
            locker_file.write(data)


    @staticmethod
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


    @staticmethod
    def ask_option_number(text="[Enter Option Number]: "):
        """ Asks for an input printing based on the given parameter text """
        try:
            return int(input(text))
        except:
            return input(text)


    def print_data(self):
        """
            Prints the list of stored password, gives the option to select from said list
            and prints the password details for valid data selections
        """
        data = self.__file_data

        if data:
            data_keys = list(data.keys())

            print("\n\tEnter a number from the list below to show details:\n\tPress 'c' to cancel\n")
            # Print list of stored account passwords
            print('\n'.join('\t%i: %s' % (index, app_name) for index, app_name in enumerate(data_keys)))
            selected_option = input('\n[Select password details for]: ').lower()

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


    def _add_password_data(self, should_encrypt='y'):
        """ Auxiliary Function for add_password that does the true adding work """
        data = self.__file_data
        app_name = input("\n\t[Where is this password used for?]: ").title()

        while len(app_name) < 3:
            print("\n\tUSAGE NAME MUST NOT BE LESS THAN 3 CHARACTERS")
            app_name = input("\n\t[Where is this password used for?]: ").title()

        # Print an error that the application name has already been stored
        if app_name in data:
            print("\n\tAbort: You already have a password stored for '%s'" % app_name)
            return

        data[app_name] = {}
        app = data[app_name]

        def encryptor(should_encrypt):
            def wrapper(func):
                def inner(*args, **kwargs):
                    secret = func(*args, **kwargs)

                    while len(secret) < 3:
                        print("\n\tPASSWORD MUST NOT BE LESS THAN 3 CHARACTERS")
                        secret = func(*args, **kwargs)

                    if should_encrypt == 'y':
                        hint = input("\n\t[Enter Password Hint]: ")

                        while len(hint) < 3:
                            print("\n\tHINT MUST NOT BE LESS THAN 3 CHARACTERS")
                            hint = input("\n\t[Enter Password Hint]: ")

                        # Bcrypt hash encrypt the secret password
                        secret = bcrypt.hashpw(str.encode(secret), bcrypt.gensalt()).decode()
                        app["HINT"] = hint

                    app["SECRET"] = secret
                    print("\n\tPASSWORD_FOR: %s" % app_name)
                    [ print("\t%s: %s" % (key, value)) for key, value in app.items() ]
                    should_store = input("\n\t[Store this password?[Y/N/C]]: ").lower()

                    while should_store not in 'ync':
                        should_store = input("[Store this password?[Y/N/C]]: ").lower()
                    else:
                        # Delete created password detail if canceled or should not be stored
                        if should_store in 'nc':
                            del data[app_name]
                    return should_store
                return inner
            return wrapper

        @encryptor(should_encrypt)
        def pw_details():
            return input("\n\t[Enter desired password]: ")

        should_store = pw_details()

        while should_store == 'n':
            return self._add_password_data(should_encrypt)
        else:
            if should_store == 'y':
                self.save(data)
                print("===SAVE SUCCESS===")
                return
            elif should_store == 'c':
                print('canceled')
                return


    def add_password(self):
        """ Adds a new password data to the locker """
        print("\n\tDo you want the password to be encrypted? [Y/N]\n\tPress 'c' to cancel")
        selected_option = input("\n[Encrypt Password?]: ").lower()

        if selected_option.isalpha():
            if selected_option == 'c':
                return
            elif selected_option not in 'ync':
                print("\n\tInvalid Answer: Must be [Y/N/C]\n")
            else:
                self._add_password_data(selected_option)
        else:
            print("\n\tInvalid Answer: Must be [Y/N/C]\n")
