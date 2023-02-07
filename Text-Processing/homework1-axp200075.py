# Alan Perez
# axp200075
# Homework 1
# CS 4395.001

# Program will read data from a csv file, will format correctly based off the helper function and display the employees data

import pathlib  # get current working dir
import pickle
import sys  # to get system param
import csv  # read csv file
import re  # regex for the checks


class Person:
    def __init__(self, last, first, middle, empID, phone):
        self.last = last
        self.first = first
        self.middle = middle
        self.empID = empID
        self.phone = phone

    def display(self):
        print("Employee id: ", self.empID)
        print(self.first, self.middle, self.last)
        print(self.phone)


# Formatting the phone number based off the screenshot from the requirements.
# Without properly formatting the program would immediately ask to input a valid phone number instead of asking for the ID first.
def format_phone(phone):
    #  replace if there are spaces
    pattern = re.compile("^\d{0,10}$")
    # 2 periods, will be replacing it with dashes
    pattern2 = re.compile("^\d{3}\.\d{3}\.\d{4}$")
    # add a dash after the first 3 digits, from 3-6 add one after, append the last 4 digits
    if re.search(pattern, phone):
        phone = phone[:3] + "-" + phone[3:6] + "-" + phone[6:]
    #     replace consecutive periods with a dash
    elif re.search(pattern2, phone):
        phone = re.sub("\.", "-", phone)
    #     replace spaces inbetween digits ex: 123 456 7890 with a dash
    else:
        phone = re.sub(" ", "-", phone)
    return phone


def txt_process(file_path):
    results = {}

    # Last,First,Middle Initial,ID,Office phone <-- data.csv header fields, will be targeting by index

    # a. split on comma using csv module
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # skip header
        next(reader)
        # loop through the file
        for row in reader:

            # lName = row['Last'].capitalize()
            # fName = row['First'].capitalize()
            # mName = row['Middle']

            # b. modify lname and fname to be capital
            # extract and assign to variables
            l_name = row[0].capitalize()
            f_name = row[1].capitalize()
            m_name = row[2]
            emp_id = row[3]
            phone = row[4]

            phone = format_phone(phone)
            # c. if middle name is empty, replace with X, otherwise uppercase char
            if not m_name:
                m_name = 'X'
            else:
                m_name = m_name.upper()

            # regex pattern set up for empID and phone

            emp_id_pattern = re.compile("^[A-Z]{2}[0-9]{4}$")
            phone_pattern = re.compile("^\d{3}-\d{3}-\d{4}$")

            # d. modify id
            while not re.match(emp_id_pattern, emp_id):
                print("ID Invalid: {}".format(emp_id))
                print("ID is two letters followed by 4 digits")
                emp_id = input("Please enter a valid id: ")
                # Check for duplicate id, if dup then print error

            # e. modify phone number
            while not re.match(phone_pattern, phone):
                print("Phone {} is invalid".format(phone))
                print("Enter phone number in form 123-456-7890")
                phone = input("Enter phone number: ", )

            # create object with the attribute for our main function to iterate through keys
            if emp_id in results:
                print("{} id already exists", emp_id)
            else:
                results[emp_id] = Person(l_name, f_name, m_name, emp_id, phone)
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')

    rel_path = sys.argv[1]
    file_path = pathlib.Path.cwd().joinpath(rel_path)
    data = txt_process(file_path)
    # with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
    #     text_in = f.read.splitlines()
    # employees = txt_process(text_in[1:])    # ignore heading line
    pickle.dump(data, open('employees.pickle', 'wb'))

    # read the pickle bback in
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    # output employees
    print('\n\nEmployee list:')

    for emp_id in employees_in.keys():
        employees_in[emp_id].display()
