import os, random


def main():
    menu_route()



def display_menu():
    clear_console()
    print("1) Check if a value entered by a user is an integer, a real number or not a number.")
    print("2) Play a game of dice.")
    print("3) Exit the application.")


def menu_route():

    keep_going = True

    while keep_going:
        display_menu()
        decision = get_menu_item()
        print(decision)
        if (decision == "1"):
            check_number()
            input("press ENTER to go back to the main menu")
            display_menu()
        elif (decision == "2"):
            roll_dice()
            display_menu()
        elif (decision == "3"):
            keep_going = False
        

def get_menu_item():
    user_input = input("Please Enter your menu selection: ")
    while user_input != "1" and user_input != "2" and user_input != "3":
        user_input = input("Not a valid selection; Please input 1,2, or 3: ")
    return user_input

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def check_number():
    clear_console()
    user_input = input("Give me some type of input: ")
    try:
        int(user_input)
        print("Your value is an integer!")
        return
    except:
        pass
    try:
        float(user_input)
    except:
        print("Your value is a non-numeric value!")
        return

    print("Your value is a real number with decimal values")


def roll_dice():
    input("Press ENTER to start the game")
    clear_console()
    usr_dice1 = random.randint(1,6)
    usr_dice2 = random.randint(1,6)
    print(f"You rolled a: {usr_dice1}")
    print(f"You rolled a: {usr_dice2}")
    usr_total = usr_dice2 + usr_dice1
    print(f'Your total is: {usr_total}')
    if(get_usr_roll_decision()):
        usr_dice3 = random.randint(1,6)
        print(f"You rolled a: {usr_dice3}")
        usr_total += usr_dice3
        print(f'Your total is: {usr_total}')
    cpu_dice1 = random.randint(1,6) 
    cpu_dice2 = random.randint(1,6) 
    cpu_dice3 = random.randint(1,6) 
    cpu_total = cpu_dice1 + cpu_dice2 + cpu_dice3
    print(f"The computer rolled a: {cpu_dice1}")
    print(f"The computer rolled a: {cpu_dice2}")
    print(f"The computer rolled a: {cpu_dice3}")
    print(f"The computer has a total of {cpu_total}")
    if(abs(10-cpu_total) == (abs(10-usr_total))):
        print("It is Tie. No winner")
    elif(abs(10-cpu_total) < (abs(10-usr_total))):
        print("The computer wins as it is closer to 10")
    else:
        print("You win! Because you were closer to 10\n")
    input("Press ENTER to return to the Main Menu....")


def get_usr_roll_decision():
    usr_input = input("Would you like to roll again? (yes/no)").lower()
    while usr_input != 'no' and usr_input != 'yes':
        usr_input = input("Please Enter yes or no: ").lower()
    if usr_input == 'yes':
        return True
    else:
        return False









main()

