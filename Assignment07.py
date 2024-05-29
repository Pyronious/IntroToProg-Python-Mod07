# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates managing data using classes
# Change Log:
#   Patrick Moynihan: 2024-04-10 Created script
#   Patrick Moynihan: 2024-04-08 Added ability to save data to CSV file
#   Patrick Moynihan: 2024-04-25 Added menu functionality
#   Patrick Moynihan: 2024-05-02 Added ability to read data from CSV file
#   Patrick Moynihan: 2024-05-10 Refactored to use dictionaries and JSON file format
#   Patrick Moynihan: 2024-05-18 Refactored to use functions and classes
#   Patrick Moynihan: 2024-05-22 Refactored to use classes for data management
# ------------------------------------------------------------------------------------------ #
import json
from typing import IO

# Define the Data Constants

MENU: str = '''
------ Course Registration Program ------
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"
KEYS: list = ["FirstName", "LastName", "CourseName"]

# Define the global data variables
menu_choice: str = ''  # Hold the choice made by the user.
students: list = []  # List of data for all students
saved: bool = True  # Tracks whether newly added data has been saved


# Define the classes
class Person:
    """
    Class for storing information about a person

    ChangeLog:
        Patrick Moynihan, 2024-05-22: Created class
    """

    def __init__(self, first_name: str = "", last_name: str = ""):
        """
        Initialise a new Person object

        :param first_name: First name of the person
        :param last_name: Last name of the person
        """
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def validate_name(name: str):
        """
        Validates a name to ensure it contains only alpha or space characters.

        :param name: Name to be validated
        :return: Returns True if the name is valid, otherwise False
        """
        # If the name contains only alpha characters (ignoring spaces), or is empty, validate it as good.
        if name.replace(' ', '').isalpha() or name == '':
            return True
        else:
            return False  # Data validation failed

    @property
    def first_name(self) -> str:
        """
        Gets the person's first name

        Returns:
            A string containing the first name of the person
        """
        return self.__first_name  # Returns the private attribute

    @first_name.setter
    def first_name(self, value: str):
        """
        Sets the person's first name
        """
        # Validate incoming data
        try:
            if Student.validate_name(value):  # Use our custom validation method to check the name
                self.__first_name = value.title()  # Store private attribute
            else:
                raise ValueError(f">>> First name must use only letters.\n")
        except ValueError as e:
            IO.output_error_messages(e)

    @property
    def last_name(self) -> str:
        """
        Gets the person's last name

        Returns:
            A string containing the last name of the person
        """
        return self.__last_name  # Returns the private attribute

    @last_name.setter
    def last_name(self, value: str):
        """
        Sets the person's last name
        """
        # Validate incoming data
        try:
            if Student.validate_name(value):  # Use our custom validation method to check the name
                self.__last_name = value.title()  # Store private attribute
            else:
                raise ValueError(f">>> Last name must use only letters.\n")
        except ValueError as e:
            IO.output_error_messages(e)

    def __str__(self):
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """
        Subclass of Person for storing information about a student

        ChangeLog:
            Patrick Moynihan, 2024-05-22: Created class
    """

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        """
        Initialize a new Student object
        :param first_name: First name of the student
        :param last_name: Last name of the student
        :param course_name: Course name the student is registered for
        """
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        """
        Gets the student's registered course name

        Returns:
            A string containing the course name the student is registered for
        """
        return self.__course_name  # Returns the private attribute

    @course_name.setter
    def course_name(self, value: str):
        """
        Sets the student's registered course name
        """
        # Validate incoming data
        try:
            if len(value) > 25:
                raise ValueError(f">>> Course name must not exceed 25 characters.\n")
            else:
                self.__course_name = value.title()  # Store private attribute
        except ValueError as e:
            IO.output_error_messages(e)

    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.course_name}"


class FileProcessor:
    """
    Functions for reading and writing JSON files.

    ChangeLog:
        Patrick Moynihan, 2024-05-18: Created class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) -> list:
        """
        Reads the specified JSON file and stores it in a list of Student objects.

        :param file_name: string representing the name of the JSON file
        :param student_data: list to which student data will be stored
        :return: list of data loaded from file
        """
        file: IO  # Holds a reference to an opened file.

        IO.print_info(f">>> Loading data from {file_name}")
        try:
            file = open(file_name, "r")
            json_data = json.load(file)
            file.close()
            IO.print_info(f">>> Loaded {len(json_data)} records.")

            # Validate file data to see if it contains the dictionary keys we expect.
            for i, record in enumerate(json_data, start=1):  # Loop through all records in JSON data
                for key in KEYS:  # Loop through all keys we expect to find
                    if not key in record:  # If key doesn't exist, throw error
                        raise ValueError(
                            f'>>> Missing dictionary key "{key}" in record {i}. Please check {file_name} for errors.')

                # Create a new Student object and add it to the list
                student_data.append(
                    Student(record["FirstName"], record["LastName"], record["CourseName"]))

            return student_data  # Send the list of Student objects back to the statement that called us


        # Let the user know we couldn't find the file
        except FileNotFoundError:
            IO.output_error_messages(f">>> {file_name} not found. A new file will be created.")
            file = open(file_name, "w")
            file.close()

        # Let the user know some other problem occurred when loading the file
        except Exception as e:
            IO.output_error_messages(
                f">>> There was an error while loading {file_name}. Please check {file_name} and try again.")
            IO.output_error_messages(e, e.__doc__)
            exit()

        # If the file is still open for some reason, close it
        finally:
            if not file.closed:
                IO.print_info(">>> Closing file.")
                file.close()

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list) -> bool:
        # In the assignment 6 review, Kelly recommended returning student_data from this method, but I don't understand
        # why that would be desirable. We don't change the value of student_data in this method, so why return it?
        # Nothing in the main code is expecting it to be returned, and all we use student_data for is to save the
        # data to a file. Any clarification would be appreciated.
        """
                Writes the provided list to a JSON file.

                :param file_name: string representing the name of the JSON file
                :param student_data: list from which student data will be saved
                :return: bool representing whether the data was saved
                """
        file: IO = None
        registrant: Student = None  # For iterating through the student_data list
        json_data: list = []  # For holding JSON compatible data

        # Loop through the Students in student_data and convert to JSON
        for registrant in student_data:
            record: dict = {"FirstName": registrant.first_name, "LastName": registrant.last_name,
                            "CourseName": registrant.course_name}  # Format the data as a dict
            json_data.append(record)  # Append the dict to json_data

        try:
            # Save JSON to file
            file = open(file_name, 'w')
            json.dump(json_data, file, indent=4)
            file.close()
            IO.print_info(f">>> Wrote registration data to {file_name}\n")

            return True  # Let the caller know we saved successfully

        except Exception as e:
            IO.output_error_messages(">>> There was an error writing the registration data. Is the file read-only?")
            IO.output_error_messages(f">>> {e}", e.__doc__)
            return False  # Let the caller know we failed to save the file
        finally:
            # Does file have a value other than None? If so, is the file open? If so, close the file.
            if file and not file.closed:
                file.close()


class IO:
    """
        Functions for handling user input and output.

        ChangeLog:
            Patrick Moynihan, 2024-05-18: Created class
        """

    @staticmethod
    def print_info(message: str) -> None:
        """
        Prints an informational message to the console in green.

        :param message: The message to be printed
        """
        print(f"\033[0;32;49m{message}\033[39m")

    @staticmethod
    def print_warning(message: str, newline: bool = True) -> None:
        """
        Prints a warning message to the console in red.

        :param message: The warning to be printed
        :param newline: Boolean indicating whether to add a new line at the end of the message
        """
        if newline:
            print(f"\033[0;31;49m{message}\033[39m")
        else:
            print(f"\033[0;31;49m{message}\033[39m", end="")

    @staticmethod
    def output_menu(menu: str) -> None:
        """
        Displays the menu options

        :param menu: string to be printed as the menu
        """
        print(menu)

    @staticmethod
    def input_menu_choice() -> str:
        """
        Retrieves user input from the menu

        :return: string representing the user input
        """
        choice = input("\033[1;33;49mEnter your choice: \033[0;39m")
        return choice

    @staticmethod
    def output_student_courses(student_data: list) -> None:
        """
        Prints out the student registration data in human-readable format.

        :param student_data: list from which student data will be presented
        """
        IO.print_info(">>> The current data is:\n")
        IO.print_info("First Name          Last Name           Course Name         ")
        IO.print_info("-----------------------------------------------------------------")
        for registrant in student_data:
            # Print each row of the table inside fixed width columns
            print(f"{registrant.first_name[:20]:<20}{registrant.last_name[:20]:<20}{registrant.course_name[:25]:<25}")
        IO.print_info("-----------------------------------------------------------------")

    @staticmethod
    def input_student_data(student_data: list) -> list:
        """
        Reads the student registration data from the user and appends it to a list

        :param student_data: list to which student data will be appended
        """

        # Input user data for new student registration
        IO.print_info(">>> Register a student for a course\n")
        registrant = Student()  # Creates a new Student object named registrant
        while not registrant.first_name:  # Keep trying until we get a validated input
            registrant.first_name = input("Enter student's first name: ")

        while not registrant.last_name:  # Keep trying until we get a validated input
            registrant.last_name = input("Enter student's last name: ")

        while not registrant.course_name:  # Keep trying until we get a validated input
            registrant.course_name = input("Enter the course name: ")

        student_data.append(registrant)  # Append the entered data to the passed-in list
        IO.print_info(f">>> Registered {registrant.first_name} {registrant.last_name} for {registrant.course_name}.")
        return student_data

    @staticmethod
    def output_error_messages(message: str, error: Exception = None) -> None:
        """
        Presents custom error message to user, along with Python's technical error.

        :param message: The custom error message to present to the user
        :param error: The technical error message from Python
        """
        # if we get two arguments, print the custom error and the Python technical error
        if error:
            IO.print_warning(f"{message}")
            IO.print_warning(f">>> Python technical error: {error}")
        # otherwise just print the custom error message
        else:
            IO.print_warning(f"{message}")


# Load data from enrollment JSON file into students
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Main program loop

while True:
    # Present the menu of choices
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == '1':
        # Ingest student registration data from user
        students = IO.input_student_data(student_data=students)
        saved = False  # Set the saved flag to false, so we can remind user to save
        continue

    elif menu_choice == '2':
        # Display the data in a human-friendly format
        IO.output_student_courses(students)
        continue

    elif menu_choice == '3':
        # Save the data to a file and set saved flag to True if save was successful
        if FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students) == True:
            saved = True
            IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == '4':
        # Exit if data has already been saved or was unmodified (i.e. saved = undefined)
        if saved is False:
            IO.print_warning(">>> New registration data not saved. Save it now? (Y/N): ", False)
            save_confirm = input()
            if save_confirm.capitalize() == 'Y':
                if FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students) == True:
                    IO.print_info(">>> Have a nice day!\n")
                    exit()
                else:
                    continue  # File was not successfully saved, so return to main menu
            elif save_confirm.capitalize() == 'N':
                IO.print_warning(">>> Newly entered data not saved.")
                IO.print_info(">>> Have a nice day!\n")
                exit()
        else:
            IO.print_info(">>> Have a nice day!\n")
            exit()

    else:
        IO.print_warning(">>> Please choose option 1, 2, 3, or 4.")
