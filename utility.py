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
