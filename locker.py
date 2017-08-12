import os

class Locker:
    def __init__(self, filename='locker'):
        self.filename = '%s.txt' % filename


    def get_locker_data(self):
        """ Reads a locker file via the given filename instance property """
        if os.path.isfile(self.filename):
            file_data = {}
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
                            file_data[curr_parent][key] = value
                        else:
                            curr_parent = line
                            file_data[curr_parent] = {}
            return file_data
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

        # Check if data is empty
        if data_content:
            for app_name, metadata in data_content:
                data += app_name + '\n'
                for key, value in metadata.items():
                    data += '\t%s: %s\n' % (key, str(value))

        with open(self.filename, 'w') as locker_file:
            locker_file.write(data)
