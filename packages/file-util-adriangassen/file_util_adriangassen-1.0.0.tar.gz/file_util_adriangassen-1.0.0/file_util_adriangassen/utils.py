
def user_confirms():
    while True:
        answer = input("Would you like to continue with the operation? [y/n]: ")
        if answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        else:
            print("Invalid, please enter y (yes) or n (no): ")


