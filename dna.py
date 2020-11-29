import csv
from sys import argv, exit
import re


class DnaTest(object):
    """CLASS HELP: the DNA test, simply give DNA sequence to the program, and it searches in the database to
       determine the person who owns the sample.

    type the following in cmd to run the program:
    python dna.py databases/small.csv sequences/1.txt """

    def __init__(self):
        # get filename from the command line without directory names "database" and "sequence"
        self.input_argv = str(argv[1][10:])
        self.sequence_argv = str(argv[2][10:])    

        # Automatically open and close the database file
        with open(f"databases/{self.input_argv}", 'r') as input_file:
            self.input_file = input_file.readlines()

        # Automatically open and close the sequence file
        with open(f"sequences/{self.sequence_argv}", 'r') as sequence_file:
            self.sequence_file = sequence_file.readline()

        # Read CSV file as a dictionary, function: compare_database_with_sequence()
        self.csv_database_dictionary = csv.DictReader(self.input_file)
        # Read CSV file to take the first row, function: get_str_list()
        self.reader = csv.reader(self.input_file)
        # computed dictionary from the sequence file
        self.dict_from_sequence = {}
        self.select_max = {}

    # returns the first row of the CSV file (database file)
    def get_str_list(self):
        # get first row from CSV file by casting it as a list
        keys = next(self.reader)

        # remove 'name' from list, to get STR(i.e 'AGATC', 'AATG', 'TATC') only.
        keys.remove("name")
        return keys

    # returns dictionary of computed STRs from the sequence file (key(STR): value(count))
    def get_str_count_from_sequence(self):  
        for str_key in self.get_str_list():
            regex = rf"({str_key})+"
            matches = re.finditer(regex, self.sequence_file, re.MULTILINE)
            
            for match in matches:
                match_len = len(match.group())
                key_len = len(str_key)
                self.select_max[match] = match_len
                #  select max value from results dictionary (select_max)
                max_values = max(self.select_max.values())

                if max_values >= key_len:
                    result = int(max_values / key_len)
                    self.select_max[str_key] = result
                    self.dict_from_sequence[str_key] = result
                    
                
            # clear compare dictionary to select new key
            self.select_max.clear()

    # compare computed dictionary with the database dictionaries and get the person name
    def compare_database_with_sequence(self):
        # comparison function between database dictionary and sequence computed dictionary
        def dicts_equal(from_sequence, from_database):
            """ return True if all keys and values are the same """
            return all(k in from_database and int(from_sequence[k]) == int(from_database[k]) for k in from_sequence) \
                and all(k in from_sequence and int(from_sequence[k]) == int(from_database[k]) for k in from_database)

        def check_result():
            for dictionary in self.csv_database_dictionary:
                dict_from_database = dict(dictionary)
                dict_from_database.pop('name')

                if dicts_equal(self.dict_from_sequence, dict_from_database):
                    dict_from_database = dict(dictionary)
                    print(dict_from_database['name'])
                    return True

        if check_result():
            pass
        else:
            print("No match")


# run the class and its functions (Program control)
if __name__ == '__main__':
    RunTest = DnaTest()
    RunTest.get_str_count_from_sequence()
    RunTest.compare_database_with_sequence()