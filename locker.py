import os

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


    def print_data(self):
        """
            Prints the list of stored password, gives the option to select from said list
            and prints the password details for valid data selections
        """
        data = self.__file_data
        
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
