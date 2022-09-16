
from operator import itemgetter
import random, datetime
import os
import re
import decimal

def main():
    menu_route()

def display_menu():
    print("   MAIN MENU")
    print("-----------------")
    print("1. Car Iventory Menu")
    print("2. Review Menu")
    print("3. Reports Menu")
    print("4. Exit")

#main method that manages process flow
def menu_route():
    #main variable fo keeping track of file data
    cars_data = get_car_data_from_file()
    review_data = get_review_data_from_file()
    keep_going = True
    while keep_going:
        clear_console()
        display_menu()
        item = get_menu_item(4)
        match item:
            case 1:
                #goes into inventory menu
                inventory_module(cars_data)

            case 2:
                #goes into reviews module   
                review_module(review_data, cars_data)
                pass
            case 3:
                #goes into the reports section
                reports_module(cars_data, review_data)
                pass
            case 4:
                #exit
                clear_console()
                print("goodbye")
                keep_going = False



#for main menu
def get_menu_item(item_count):
    item = input("Enter menu item: ")
    
    while not is_valid(item, item_count):
        item = input(f"Enter either an integer 1 to {item_count}: ")

    return int(item)

#utility function, changes based on what OS type
def clear_console():
     os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def return_to_menu():
    print()
    input("Press ENTER to return to the menu....")

def get_car_data_from_file():
    #first check if path exists. Return if it doesn't exist
    if not os.path.exists("./cars.txt"):
        clear_console()
        print("Cars data file not found. Please place the file in the same folder, then restart program")
        input("\n\nPress ENTER to return to the main menu...")
        return

    car_file = open("./cars.txt")
    car_data = []

    line = car_file.readline().replace("\n","")
    while line != "":
        temp = line.split("#")
        #need to convert year and price to a number data type
        car_data.append([temp[0],temp[1],int(temp[2]), float(temp[3])])
        line = car_file.readline().replace("\n","")
    return car_data

def get_review_data_from_file():
    #first check if path exists. Return if it doesn't exist
    if not os.path.exists("./reviews.txt"):
        clear_console()
        print("Review data file not found. Please place the file in the same folder, then restart program")
        input("\n\nPress ENTER to return to the main menu...")
        return
    
    reviews_file = open("./reviews.txt")
    review_data = []

    line = reviews_file.readline().replace("\n","")
    while line != "":
        temp = line.split("#")
        #need to convert year and price to a number data type
        datetime_split_temp = temp[2].split("-")
        datetime_value = datetime.date(int(datetime_split_temp[2]),int(datetime_split_temp[0]),int(datetime_split_temp[1]))
        review_data.append([int(temp[0]),temp[1], datetime_value, int(temp[3]), temp[4]])
        line = reviews_file.readline().replace("\n","")
    reviews_file.close()
    return review_data
    
def display_inventory_menu():
    print("   INVENTORY MENU")
    print("---------------------")
    print("1) Add to the inventory")
    print("2) Edit car's data in inventory")
    print("3) Delete a car from inventory")
    print("4) Exit to main menu")

#main routing method for item 1 in main menu
def inventory_module(cars_data):
    keep_going = True
    while keep_going:
        clear_console()
        display_inventory_menu()
        item = get_menu_item(4)
        match item:
            case 1:
                #goes into inventory menu
                add_inventory(cars_data)
                return_to_menu()
            case 2:
                #goes into reviews module   
                edit_inventory(cars_data)
                return_to_menu()
            case 3:
                #goes into the reports section
                delete_inventory(cars_data)
                return_to_menu()
            case 4:
                #exit
                clear_console()
                keep_going = False

#main method for adding a car to inventory file
def add_inventory(car_data):
    display_cars(car_data)
    print("\nWhat is the name of the car you would like to add to this list? (Enter :qt to return to menu)\n")
    usr_input = input().lower()
    if usr_input == ":qt":
        return
    car_name = get_unique_car_name(car_data, usr_input)
    print("\nWhat is the car's type?\n")
    car_type = get_car_type()
    car_year = get_valid_year()
    car_price = get_valid_price()

    #append the new car
    car_data.append([car_name,car_type,car_year,car_price])
    save_to_file(car_data, "./cars.txt")

#main method for editing a car
def edit_inventory(car_data):
    display_cars(car_data)
    print("\nWhat is the name of the car you would like to edit (enter :qt to exit)?\n")
    usr_input = input()
    if usr_input == ":qt":
        return
    car_index = get_index_of_car_by_name(car_data, usr_input)

    clear_console()
    print("Would you like to edit the car's type?\n")
    if get_bool():
        print("What would you like to change the type to?\n")
        car_data[car_index][1] = get_car_type()

    clear_console()
    print("Would you like to edit the car's Manufacture Year?\n")
    if get_bool():
        print("What would you like to change the year to?\n")
        car_data[car_index][2] = get_valid_year()

    clear_console()
    print("Would you like to edit the car's price?\n")
    if get_bool():
        print("What would you like to change the price to?\n")
        car_data[car_index][3] = get_valid_price()
    
    save_to_file(car_data, path="./cars.txt")

#No soft deleting, removes directly from list
def delete_inventory(car_data):
    display_cars(car_data)
    print("\nWhat is the name of the car you would like to delete? (:qt to exit)\n")
    #value for user to enter to leave the deleting process
    usr_input = input()
    if usr_input == ":qt":
        return
    car_index = get_index_of_car_by_name(car_data,usr_input)
    #a try/except to catch if the action isn't completed
    try:
        del car_data[car_index]
        save_to_file(car_data, "./cars.txt")
    except:
        print("Could not delete car. Try again")
    
def get_car_type():
    usr_input = input().lower()
    #list of possible usr input value for type
    type_list = ["sedan","hatchback","suv","truck","van","convertible"]
    while usr_input not in type_list:
        usr_input = input("Please insert either sedan, hatchback, suv, truck, van, or convertible: ")
    return usr_input

def get_valid_year():
    from_year = 2010
    to_year = 2020
    usr_int = get_int("\nPlease give a year between 2010 and 2020.\n\n")
    while (usr_int > to_year or usr_int < from_year):
        usr_int = get_int("\nPlease give a year between 2010 and 2020.\n\n")
    return usr_int

#The only error handling her is making sure their input is not less than 0.
def get_valid_price():
    usr_int = get_int("\nPlease enter a Price for the car\n\n")
    if(usr_int <= 0.0000000000000000000000000000001):
        usr_int = get_int("\nPlease enter a Price for the car that is greater than $0.00.\n\n")
    return usr_int

def get_index_of_car_by_name(car_data, car_name):
    
    while is_name_unique(car_data, car_name):
        print("Could not find. Please enter a name of a car on the list\n")
        car_name = input().lower()
    for i in range(0,len(car_data)):
        if car_data[i][0] == car_name:
            return i
    #theoretically, it hsould never get to this point
    return -1

#used for asking user for a car name and checking to make sure that does not exist. This is because the car name must be unique
def get_unique_car_name(car_data, car_name):
    while (not is_name_unique(car_data, car_name) or len(car_name) < 1):
        if len(car_name) < 1:
            print("You need atleast one character to the name")
        else:
            print("Please enter a unique car name")
        car_name = input()
    return car_name

def is_name_unique(car_data, car_name):
    for car in car_data:
        if car[0].lower() == car_name.lower():
            return False
    return True
            
        
#general file that handles cars and reviews file saving
def save_to_file(file_data, path):
    if(path == "./reviews.txt"):
        prep_review_for_saving(file_data)
    #sort the data by name first, alphabetical
    file_data = sorted(file_data,key=itemgetter(0))
    prepped_file_data = []
    #modifies the file_data to be ready for writelines to write to file. 
    for i in range(0,len(file_data)):
        #need to convert every car to a concetenated string with # demilited
        temp = "#".join([str(j) for j in file_data[i]])
        temp += "\n" #a new line to signify a another car
        prepped_file_data.append(temp)
    car_file = open(path,"w")

    car_file.writelines(prepped_file_data)
    car_file.close()

#needed to format the date into a correclty formated string before saving
def prep_review_for_saving(review_data):
    for i in range(0, len(review_data)):
        temp = review_data[i][2].strftime("%m-%d-%Y")
        review_data[i][2] = temp

def review_menu():
    print("  REVIEW MENU")
    print("----------------")
    print("1) Create a Review")
    print("2) Return to main menu")

#main method for item 2 in main menu 
def review_module(review_data, cars_data):
    keep_going = True
    while keep_going:
        clear_console()
        review_menu()
        item = get_menu_item(2)
        match item:
            case 1:
                #goes to creating a new review
                create_review(review_data,cars_data)
                return_to_menu()
            case 2:
                #exits
                return_to_menu()
                keep_going = False

def create_review(review_data,cars_data):
    car_to_review = get_car_name_to_review(cars_data)
    #if the user inputs :qt, it will return the string "exit" in the function above, so we need to leave
    if car_to_review == "exit":
        return
    this_id = get_next_id(review_data)
    review = get_review()
    rating = get_rating()
    todate = datetime.date.today()
    review_data.append([this_id, car_to_review, todate, rating, review])
    save_to_file(review_data, "./reviews.txt")
    
#getting the textual review
def get_review():
    clear_console()
    print(f"Please type in your textual review:\n\n")
    usr_input = input()
    while usr_input == "":
        usr_input = input("\nPlease enter atleast one character:\n\n")
    return usr_input
#get numerical rating 0-10
def get_rating():
    clear_console()
    usr_input = get_int(f"Please type in your numerical rating 0-10:\n\n")
    while usr_input > 10 or usr_input < 0:
        usr_input = get_int("\nPlease enter an integer 0-10:\n\n")
    return usr_input

#need to implement auto-incrementing ID's
def get_next_id(review_data):
    review_data = sorted(review_data, reverse=True, key=itemgetter(0))
    return int(review_data[0][0]) + 1

#need to make sure the car name exists
def get_car_name_to_review(cars_data):
    display_cars(cars_data)
    car_to_review = input("\n type in the name of the car you would like to review (:qt to exit)\n\n")
    if car_to_review == ":qt":
        return "exit"
    while is_name_unique(cars_data, car_to_review):
        car_to_review = input("\n Please input an existing car name.\n\n")
    return car_to_review

def report_menu():
    print("  REPORT MENU")
    print("----------------")
    print("1) Rating Statistics For a Given Year")
    print("2) Reviews and Average Rating by Car Name")
    print("3) Get all positive reviews")

#Main routing method for the report menu
def reports_module(car_data, review_data):
    keep_going = True
    while keep_going:
        clear_console()
        report_menu()
        item = get_menu_item(4)
        match item:
            case 1:
                rating_stats_by_year(review_data)
                return_to_menu()
            case 2:
                #goes into reviews module   
                review_and_ratings_by_car(review_data)
                return_to_menu()
            case 3:
                #goes into the reports section
                reviews_with_positive_words(review_data)
                return_to_menu()
            case 4:
                #exit
                clear_console()
                keep_going = False

#outputs text to console and a file in the ./reports folder of the average, min, and max rating for a given year 
def rating_stats_by_year(review_data):
    usr_input_year = get_year("What year would you like to pull the review statistics for?\n")
    output_file = open(f"./reports/rating_statistic_{usr_input_year}.txt", "w")
    output_text = calc_rating_stats_by_year(review_data, usr_input_year)

    clear_console()
    print(output_text)

    output_file.write(output_text)
    output_file.close()

#processing method for the statistics report
def calc_rating_stats_by_year(review_data, usr_input_year):
    year_review_list = [review for review in review_data if usr_input_year == review[2].year]
    list_of_ratings = list(map(itemgetter(3), year_review_list))
    try:
        return f"In the year {usr_input_year}, the average rating is {sum(list_of_ratings)/len(list_of_ratings)}, the maximum is {max(list_of_ratings)}, and the minimum is {min(list_of_ratings)}"
    except:
        return f"There were no reviews in {usr_input_year}"

#dedicated method to run for report menu item 2
#it is supposed to list the car, the average rating, and each review with the rating
def review_and_ratings_by_car(review_data):
    review_data_sorted_by_name = sorted(review_data, key=itemgetter(1), reverse=False)
    #intial seeting values for control break
    car_review_report_list = []
    count = 1
    total_rating_count = review_data_sorted_by_name[0][3]
    current_car_name = review_data_sorted_by_name[0][1]
    #this variable will hold all of the reviews and rating for the car we are focusing on 
    current_car_reviews = [{"text_review": review_data_sorted_by_name[0][4], "rating":review_data_sorted_by_name[0][3]}]
    for review in review_data_sorted_by_name[1:]:
        if current_car_name == review[1]:
            count += 1
            total_rating_count += review[3]
            current_car_reviews.append({"text_review": review[4], "rating": review[3]})
        else:
            total_rating_count, count, current_car_reviews, current_car_name = break_review_and_ratings_by_car(total_rating_count, count, current_car_reviews, current_car_name, review, car_review_report_list)
    #must run again to avoid fence post error
    break_review_and_ratings_by_car(total_rating_count, count, current_car_reviews, current_car_name, review, car_review_report_list)
    save_and_print_review_and_ratings_by_car_to_file(car_review_report_list)

#break for the method above
def break_review_and_ratings_by_car(total_rating_count, count, current_car_reviews, current_car_name, review, car_review_report_list):
    #because lists are passed as reference, changes in here will change the value in parent method
    car_review_report_list.append({"car_name": current_car_name, "reviews": current_car_reviews, "average_rating":total_rating_count/count})
    #reset values for next car
    count = 1
    total_rating_count = review[3]
    current_car_name = review[1]
    current_car_reviews = [{"text_review": review[4], "rating":review[3]}]
    return total_rating_count, count, current_car_reviews, current_car_name

#both saves the rated from the review_and_ratings_by_car_to_file report to file and prints on console
def save_and_print_review_and_ratings_by_car_to_file(car_review_report_list):
    output_file = open("./reports/avg_rating_by_car.txt", "w")
    for group in car_review_report_list:
        output_file.write(f"Car Name: {group['car_name']}\n")
        output_file.write(f"Average Rating: {group['average_rating']}\n")
        output_file.write(f"Reviews:\n")
        print(f"Car Name: {group['car_name']}")
        print(f"Average Rating: {group['average_rating']}")
        print(f"Reviews:")
        for review in group["reviews"]:
            output_file.write(f"\t{review['text_review']}\n")
            output_file.write(f"\tRating: {review['rating']}\n\n")
            print(f"\t{review['text_review']}")
            print(f"\tRating: {review['rating']}\n")
    output_file.close()
    print("\nSaved to file: ./reports/avg_rating_by_car.txt")

#prints and saves to file all reviews that have positive words located in ./positive_word_dictionary.txt
def reviews_with_positive_words(review_data):
    postive_words_file = open("./positive_word_dictionary.txt")
    postive_words_list = postive_words_file.readlines()
    postive_words_file.close()
    postive_words_string =""
    postive_reviews = []
    #the regular expression "re.search" wants a format of words like "great|good|etc"
    for word in postive_words_list:
        postive_words_string += word.lower().replace("\n", "") + "|"
    #to get rid of the last "|" in the string
    postive_words_string = postive_words_string[:-1]
    for review in review_data:
        #this regular expression searches the review for the positive words
        if re.search(postive_words_string, review[4].lower()):
            postive_reviews.append(review)
    print_and_save_positive_reviews(postive_reviews)

def print_and_save_positive_reviews(postive_reviews):
    output_file = open("./reports/comments_with_positive_words.txt", "w")
    for review in postive_reviews:
        output_file.write(f"Car Name: {review[1]}\n")
        output_file.write(f"Average Rating: {review[3]}\n")
        output_file.write(f"Review: {review[4]}\n")
        print(f"Car Name: {review[1]}")
        print(f"Average Rating: {review[3]}")
        print(f"Review: {review[4]}\n")
    output_file.close()

def get_year(message):
    usr_input = input(message)
    while not is_year_valid(usr_input):
        usr_input = input("Please input a valid year: ")
    return int(usr_input)

def is_year_valid(usr_input):
    try:
        usr_input = int(usr_input)
        if 2020 < usr_input or usr_input < 2015:
            return False
    except:
        return False
    return True



def get_int(message):
    usr_input = input(message)
    valid = False
    while not valid:
        try:
            usr_input = int(usr_input)
            valid = True
        except:
            valid = False
            usr_input = input('Please input a valid integer: ')
    return usr_input

def get_bool():
    usr_input = input().lower()
    valid = False
    while not yes_no_valid(usr_input):
        usr_input = input("Please  input either yes/no: ").lower()
    if usr_input == 'yes':
        return True
    else:
        return False


def display_cars(car_data):
    clear_console()
    column_names = ["NAME", "TYPE","MANUFACTURE YEAR", "PRICE"]
    print(f"{column_names[0]: <20} {column_names[1]: <20} {column_names[2]: <20} {column_names[3]: <20}\n")
    for car in car_data:
        print(f"{car[0]: <20} {car[1]: <20} {car[2]: <20} {car[3]: <20}")

##ERROR HANDLING
#specifically check if the main menu input is valid; error handling
def is_valid(user_input, item_count):
    try:
        user_input = int(user_input)
        for i in range(1,item_count+1):
            if(user_input == i):
                return True 
    except ValueError:
        return False

    return False

def yes_no_valid(usr_input):
    if usr_input == 'yes' or usr_input == 'no':
        return True
    return False        
    
    


main()