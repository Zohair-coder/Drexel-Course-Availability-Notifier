def inputIndex(max=float('inf')):
    """
    Function that prompts the user to input the index from the list printed.
    If the input is not a number, the user is prompted to enter it again.

    Arguments: maximum index allowed (integer)

    Returns: index (integer)
    """
    isValid = False

    while not isValid:
        index = input("Please select the index: ")
        if index.isnumeric():
            if int(index) >= 0 and int(index) <= max:
                isValid = True
            else:
                print("Invalid input.")
        else:
            print("Invalid input.")
    return int(index)


def inputCourse():
    """
    Function that prommpts the user to input the course code in the format: "EXMPL 101".
    If the input is not valid(two words, first word composed of alphabet and second word composed of numbers), the user is asked to enter the code again.
    If the first word is in lower-case, it is converted to uppercase.

    Arguments: None

    Returns: List of two elements, with the first element being EXMPL and second element being 101.
    """

    isValid = False
    while not isValid:
        course = input("Please enter the course code (EXMPL 101): ")
        course = course.split()
        if len(course) == 2 and course[0].isalpha() and course[1].isnumeric():
            isValid = True
        else:
            print("Invalid input.")

    if course[0].islower():
        course[0] = course[0].upper()
    return course
