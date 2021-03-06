from dataBase import userDB
from UserClass import User
import pyperclip
from ctypes import windll
import time
import threading
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

curr_user = "placeholder"
user_database = userDB("test_DB")
def user_login():
    """
    login process - verifying the user - username & password.
    :return: if the login was successful
    :rtype: boolean
    """
    global curr_user, user_database
    curr_user = ""
    username_input = input("\nenter your username: ")
    password_input = getpass(prompt="enter your password: ", stream = None)
    if(not user_database.user_in_DB(username_input)): # checking if the user in the databse
        user_database.register_user(username_input, password_input)
    curr_user = User(username_input, password_input, user_database.getID(username_input)) # creating a User object with its credentials
    return user_database.confirm_User(username_input, password_input)

def copy_creds(str):
    """
    copies data to the clipboard and deletes it after 30s
    :param str: information to copy
    :type str: String
    :return: None
    """
    pyperclip.copy(str)
    time.sleep(15) # waiting 15 seceonds
    if windll.user32.OpenClipboard(None): # clearing the clipboard
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()

def auto_login(acc_creds):
    """
    automaticly opens the url and fills the account's credentials
    :param acc_creds: the account's url and credentials
    :type acc_creds: List
    :return: None
    """
    print("opening website")
    driver = webdriver.Chrome(r"D:\chromedriver.exe")
    driver.get(acc_creds[0])
    time.sleep(0.5)
    password = driver.find_element_by_css_selector("input[type='password']") # locating password input box
    try: # locating username/email input box
        user = driver.find_element_by_css_selector("input[type='email']")
    except Exception:
        user = driver.find_element_by_css_selector("input[type='text']")
    password.send_keys(acc_creds[2])
    user.send_keys(acc_creds[1])

def copy_menu(cred_list):
    """
    the menu to copy the account credentials
    :param cred_list: a list of all accounts retrieved with their information in tuples
    :type cred_list: list
    :return: None
    """
    print("\nhere are the accounts we found:")
    if len(cred_list) == 0: # checking if any accounts were found
        print("no accounts were found\n")
        return None
    for i in range(len(cred_list)):
        acc = cred_list[i]
        print("\t" + str(i) + ". url: " + acc[0]) # displaying the retrieved accounts to the user
    chosen_account = int(input("insert the number of the desired account: "))
    if chosen_account > len(cred_list): # checking if the chosen account exists in the list
        print("invalid number, please try again")
        return None
    print("""what would you like to do?
            1. copy the url
            2. copy the username
            3. copy the password
            4. auto login
            5. nothing""")
    copy_info = input("enter the number of what you want to do: ") # the user enters what information to copy
    while copy_info != "5":
        if copy_info == "1":
            t = threading.Thread(target=copy_creds, args=(cred_list[chosen_account][0],)) # copying the url and clearing the clipboard afterwards
        elif copy_info == "2":
            t = threading.Thread(target=copy_creds, args=(cred_list[chosen_account][1],)) # copying the username and clearing the clipboard afterwards
        elif copy_info == "3":
            t = threading.Thread(target=copy_creds, args=(cred_list[chosen_account][2],)) # copying the password and clearing the clipboard afterwards
        elif copy_info == "4":
            t = threading.Thread(target=auto_login, args=(cred_list[chosen_account],)) # automaticly login in to the website
        t.start()
        time.sleep(1)
        copy_info = input("\nenter the number of what else you want to do: ")

def accountDB_menu():
    """
    the menu to control the database
    :return: True or False - logging out or exiting completely
    :rtype: boolean
    """
    global curr_user, user_database
    print("hello " + curr_user.getUsername() + " please choose an action to perform:")
    welcome = """
             1: Enter a new Account to the database
             2: Remove an Account from the database
             3: Get an Account url, username and password
             4: log out
             5: exit the program"""
    print(welcome)
    action = input("what would you like to do? enter the corresponding number: ")
    while action != "5":
        if action == "1": # inserting an account to the database
            acc_url = input("enter the account's url: ")
            acc_name = input("enter the account's name: ")
            acc_username = input("enter the account's username: ")
            acc_password = getpass(prompt="enter the account's password: ", stream = None)
            user_database.inset_account(curr_user, acc_url, acc_name, acc_username, acc_password)
        elif action == "2": # removing an account to the databse
            acc_name = input("enter the account's name you desire to delete: ")
            acc_username = input("enter the account's username you desire to delete: ")
            user_database.remove_account(curr_user, acc_name, acc_username)
        elif action == "3": # retrieving an account from the database
            acc_name = input("enter the account's name: ")
            copy_menu(user_database.get_account(curr_user, acc_name))
        elif action == "4":
            print("\nyou are logged out :)")
            return True
        else:
            print("invalid input, please try again")
        print(welcome)
        action = input("what else would you like to do? enter the corresponding number: ")
    print("\n thank you and goodbye :)")
    return False

def main():
    keepgoin = True # whether the program will continue with a new user
    while keepgoin:
        if(user_login()):
            print("logged in successfully")
            keepgoin = accountDB_menu() # the program will continue with a new user if returned True
        else:
            print("login failed")


if __name__ == '__main__':
    main()
