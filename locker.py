import os
import bcrypt
import copy

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
        self.__file_data = locker_data

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
    def ask_option(data_keys=None, title_text=None, input_text="Enter Option Number"):
        """ Asks for an input printing based on the given parameter text """

        if title_text != None:
            print("\n\t%s:\n\tPress 'c' to cancel\n" % title_text)
        if data_keys:
            print("\n".join("\t%i: %s" % (index, app_name) for index, app_name in enumerate(data_keys)))
            print("\n")

        input_value = input("[%s]: " % input_text)

        try:
            return int(input_value)
        except:
            return input_value.lower()



    def __encryptpass(clsmethod):
        """ Method decorator for validating if a password should be encrypted or not """
        def wrapper(self, *args, **kwargs):
            print("\n\tDo you want the password to be encrypted? [Y/N]\n\tPress 'c' to cancel")
            should_encrypt = input("\n[Encrypt Password?]: ").lower()

            if should_encrypt.isalpha():
                if should_encrypt == 'c':
                    print("\n\t===CANCELED===\n")
                    return
                elif should_encrypt in 'yn':
                    clsmethod(self, should_encrypt, *args, **kwargs)
                else:
                    print("\n\tInvalid Answer: Must be  Y/N/C\n")
            else:
                print("\n\tInvalid Answer: Must be  Y/N/C\n")
        return wrapper



    def __datacheck(error_text):
        """ Method Decorator that validates whether the locker file has data on it """
        def decorator(clsmethod):
            def wrapper(self, *args, **kwargs):
                data = self.__file_data
                if data:
                    data_keys = list(data.keys())
                    clsmethod(self, data, data_keys, *args, **kwargs)
                else:
                    print("\n\t%s\n" % error_text)
            return wrapper
        return decorator



    def __pwdetails(clsmethod):
        """ Method Decorator that handles logic for password detail gathering and saving the data """
        def wrapper(self, should_encrypt, app_name=None, *args, **kwargs):
            data = copy.deepcopy(self.__file_data)
            app_name = app_name or clsmethod(self, data, app_name, *args, **kwargs)

            if app_name != None:
                data[app_name] = {}
                app = data[app_name]
                secret = input("\n\t[Enter desired password]: ")

                while len(secret) < 3:
                    print("\n\tPASSWORD MUST NOT BE LESS THAN 3 CHARACTERS")
                    secret = input("\n\t[Enter desired password]: ")

                if should_encrypt == 'y':
                    hint = input("\n\t[Enter Password Hint]: ")

                    while len(hint) < 3:
                        print("\n\tHINT MUST NOT BE LESS THAN 3 CHARACTERS")
                        hint = input("\n\t[Enter Password Hint]: ")

                    # Bcrypt hash encrypt the secret password
                    secret = bcrypt.hashpw(str.encode(secret), bcrypt.gensalt()).decode()
                    app["HINT"] = '"%s"' % hint

                app["SECRET"] = secret
                print("\n\t%s Details" % app_name)
                [ print("\t===%s: %s" % (key, value)) for key, value in app.items() ]
                should_store = input("\n\t[Store this password? Y/N/C]: ").lower()

                # Repeat should_store input question if invalid answer
                while should_store not in 'ync':
                    should_store = input("\n\t[Store this password? Y/N/C]: ").lower()
                else:
                    # Delete created password detail if canceled or should not be stored
                    if should_store in 'nc':
                        del data[app_name]

                    # Repeat Password Detail gathering if No by recursing
                    if should_store == 'n':
                        return wrapper(self, should_encrypt, app_name)
                    else:
                        # Save data if yes
                        if should_store == 'y':
                            self.save(data)
                            print("\n\t===SAVE SUCCESS===\n")
                        # Exit Password Detail gathering if canceled
                        elif should_store == 'c':
                            print('\n\t===CANCELED===\n')
        return wrapper



    @__datacheck(error_text="No Password stored to show.")
    def print_data(self, data, data_keys):
        """
            Prints the list of stored password, gives the option to select from said list
            and prints the password details for valid data selections
        """

        print("\n\t[[ PASSWORD LIST ]]\n")

        selected_option = self.ask_option(
            data_keys,
            title_text="Enter a number from the list below to SHOW details",
            input_text="Show password details for"
        )

        # Try-Except whether the given selected_option is a valid index on data_keys
        try:
            app_name = data_keys[selected_option]
            app = data[app_name]
            print("\n\t%s Details" % app_name)
            [ print("\t===%s: %s" % (key, value)) for key, value in app.items() ]
            print("\n")
        except Exception as error:
            if str(selected_option).isalpha() and selected_option == 'c':
                print("\n\t===CANCELED===\n")
            else:
                print("\n\tInvalid option number\n")



    @__encryptpass
    @__pwdetails
    def __save_pw_data(self, data, app_name):
        """ Auxiliary Function for add_password that does the true adding work """
        app_name = input("\n\t[Where is this password used on?]: ").title()

        while len(app_name) < 3:
            print("\n\tUSAGE NAME MUST NOT BE LESS THAN 3 CHARACTERS")
            app_name = input("\n\t[Where is this password used on?]: ").title()

        # Print an error and return None when the application name has already been stored
        if app_name in data:
            print("\n\tAbort: You already have a password stored for '%s'" % app_name)
        else:
            return app_name


    @__encryptpass
    @__pwdetails
    def __edit_pw_data(self, data, app_name):
        """ Auxiliary Function for edit_password """
        return app_name



    def add_password(self):
        """ Adds a new password data to the locker """
        print("\n\t[[ ADD A NEW PASSWORD ]]")
        self.__save_pw_data()



    @__datacheck(error_text="No Password stored to edit.")
    def edit_password(self, data, data_keys):
        """ Edit a password selected from the list of available passwords on the locker file """

        print("\n\t[[ EDIT A PASSWORD ]]")

        selected_option = self.ask_option(
            data_keys,
            title_text="Enter a number from the list below to EDIT the details",
            input_text="Edit password details for"
        )

        # Try-Except whether the given selected_option is a valid index on data_keys
        try:
            app_name = data_keys[selected_option]
            self.__edit_pw_data(app_name)
        except Exception as error:
            if str(selected_option).isalpha() and selected_option == 'c':
                print("===CANCELED===")
            else:
                print("\n\tInvalid option number\n")



    @__datacheck(error_text="No Password stored to delete.")
    def delete_password(self, data, data_keys):
        """ Edit a password selected from the list of available passwords on the locker file """

        print("\n\t[[ DELETE A PASSWORD ]]")

        selected_option = self.ask_option(
            data_keys,
            title_text="Enter a number from the list below to DELETE",
            input_text="Delete Password"
        )

        try:
            app_name = data_keys[selected_option]
            confirm = self.ask_option(input_text="Are you sure you want to delete %s? Y/N" % app_name)

            if confirm == 'y':
                del data[app_name]
                self.save(data)
                print("\n\t===DELETE SUCCESS===\n")
            elif confirm == 'n':
                return
            else:
                print("\n\tInvalid Confirmation Answer\n")
        except Exception as error:
            if str(selected_option).isalpha() and selected_option == 'c':
                print("\n\t===CANCELED===\n")
            else:
                print("\n\tInvalid option number\n")
