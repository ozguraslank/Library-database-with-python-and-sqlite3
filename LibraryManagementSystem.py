import sqlite3
import time


class Book():
    def __init__(self, book_name, writer, page_amount, price, edition, situation):
        self.book_name = book_name
        self.writer = writer
        self.page_amount = int(page_amount)
        self.price = float(price)
        self.edition = int(edition)
        self.situation = situation


class Database():
    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect("The_Library.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("Create table if not exists Books (Name TEXT, Writer TEXT, PageAmount INT, Price FLOAT, Edition INT, Situation TEXT)")
        self.cursor.execute("Create table if not exists Students (Name TEXT, Surname TEXT, Age INT, Balance FLOAT, Borrowed INT, Password TEXT)")
        self.cursor.execute("Create table if not exists Managers (Name TEXT, Surname TEXT, Age INT, Password TEXT)")
        self.connection.commit()

    def disconnect(self):
        self.connection.close()
        print("DISCONNECTED!")

    def add_manager(self, the_manager):
        self.cursor.execute("Insert into Managers Values(?,?,?,?)",(the_manager.name, the_manager.surname, the_manager.age, the_manager.password))
        self.connection.commit()

    def add_student(self, the_student):
        self.cursor.execute("Insert into Students Values(?,?,?,?,?,?)", (the_student.name, the_student.surname, the_student.age, the_student.balance, the_student.borrowed,the_student.password))
        self.connection.commit()

    def show_books(self):
        self.cursor.execute("Select * from Books")
        books = self.cursor.fetchall()

        if (len(books) == 0):
            print("There is no book!")

        else:
            print("***************************************\n")
            for i in books:
                a_book = Book(i[0], i[1], i[2], i[3], i[4], i[5])
                print(i)
            print("\n***************************************\n")

    def query_book(self, the_book):
        self.cursor.execute("Select * from Books where Name = ?", [the_book.book_name])
        books = self.cursor.fetchall()

        if (len(books) == 0):
            print("This book is not exists!")

        else:
            for i in books:
                print(i)


class Student():
    def __init__(self, name, surname, age, balance, borrowed, password):
        self.connect()
        self.name = name
        self.surname = surname
        self.age = int(age)
        self.balance = float(balance)
        self.borrowed = int(borrowed)
        self.password = password

    def show_info(self):
        self.cursor.execute("Select * from Students where Name = ? and Surname = ?", (self.name, self.surname))
        students = self.cursor.fetchall()

        print("*********************************************")
        for i in students:
            print(i)
        print("*********************************************\n")

    def connect(self):
        self.connection = sqlite3.connect("The_Library.db")
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()
        print("DISCONNECTED!")

    def deposit_money(self, quantity):
        self.cursor.execute("Select * from Students where Name = ? and Surname = ?", (self.name, self.surname))
        students = self.cursor.fetchall()

        if (len(students) == 0):
            print("This student is not exists!")

        else:
            for i in students:
                the_balance = i[3]
                the_balance += float(quantity)
                self.cursor.execute("Update Students set Balance = ? where Name = ? and Surname = ?", (the_balance, self.name, self.surname))
                self.connection.commit()

    def borrow(self, the_book):
        if (self.borrowed >= 3):
            print("You are already took 3 books, you cant take more...")

        else:
            self.cursor.execute("Select * from Books where Name = ?", [the_book.book_name])
            books = self.cursor.fetchall()

            if (len(books) == 0):
                print("This book is not exists!")

            else:
                for i in books:
                    if (i[5] == "SOLD"):
                        print("This book is sold...")

                    elif (i[5] == "TAKEN"):
                        print("This book is already taken...")

                    else:
                        decision2 = input("The book is avaiable, will you take it? (Y/N)")

                        if (decision2 == "Y" or decision2 == "y"):
                            self.cursor.execute("Update Books set Situation = ? where Name = ? ",("TAKEN", the_book.book_name))
                            self.borrowed += 1
                            self.cursor.execute("Update Students set Borrowed = ? where Name = ? and Surname = ?",(self.borrowed, self.name, self.surname))
                            self.connection.commit()
                            print("You succesfully took the book!")

                        elif (decision2 == "N" or decision2 == "n"):
                            print("Operation is canceled!...")

                        else:
                            print("Invalid Operation!")

    def buy(self, the_book):
        self.cursor.execute("Select * from Books where Name = ?", [the_book.book_name])
        books = self.cursor.fetchall()

        if (len(books) == 0):
            print("This Book is not exists!")

        else:
            for i in books:
                if (self.balance < i[3]):
                    print("You don't have enough balance to buy this book!")

                else:
                        if (i[5] == "AVAIABLE"):
                            decision3 = input("The Book is avaiable, will you buy it? (Y/N): ")

                            if (decision3 == "Y" or decision3 == "y"):
                                self.cursor.execute("Update Books set Situation = ? where name = ?", ("SOLD", the_book.book_name))
                                self.balance -= i[3]
                                self.cursor.execute("Update Students set Balance = ? where name = ?",(self.balance, self.name))
                                print("You bought the book!")
                                self.connection.commit()

                            elif (decision3 == "N" or decision3 == "n"):
                                print("You didnt buy the book")

                            else:
                                print("Invalid operation")

    def give_back(self, the_book):
        self.cursor.execute("Select * from Books where Name = ?", [the_book.book_name])
        books = self.cursor.fetchall()

        if (len(books) == 0):
            print("This Book is not exists!")

        else:
            self.cursor.execute("Update Books set Situation = ? where Name = ? ", ("AVAIABLE", the_book.book_name))
            self.borrowed = ((self.borrowed) - 1)
            self.cursor.execute("Update Students set Borrowed = ? where Name = ? and Surname = ?",(self.borrowed, self.name, self.surname))
            self.connection.commit()
            print("You gave the book back! ")


class Manager():
    def __init__(self, name, surname, age, password):
        self.connect()
        self.name = name
        self.surname = surname
        self.age = int(age)
        self.password = password

    def connect(self):
        self.connection = sqlite3.connect("The_Library.db")
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()
        print("DISCONNECTED!")

    def add_book(self, the_book):
        self.cursor.execute("Insert into Books Values(?,?,?,?,?,?)", (the_book.book_name, the_book.writer, the_book.page_amount, the_book.price, the_book.edition,the_book.situation))
        self.connection.commit()

    def delete_book(self, the_book):
        self.cursor.execute("Delete from Books where Name = ?", [the_book.book_name])
        self.connection.commit()

    def add_student(self, the_student):
        self.cursor.execute("Insert into Students Values(?,?,?,?,?,?)", (the_student.name, the_student.surname, the_student.age, the_student.balance, the_student.borrowed,the_student.password))
        self.connection.commit()

    def show_info(self):
        self.cursor.execute("Select * from Managers where Name = ? and Surname = ?", (self.name, self.surname))
        managers = self.cursor.fetchall()

        print("*********************************************")
        for i in managers:
            print(i)
        print("*********************************************\n")


database = Database()

while True:
    print("""
    *******************************************
    Press 1 for Student Login
    Press 2 for Manager Login
    Press 3 for sign-up as Student
    Press 4 for quit
    *******************************************
    """)
    new_decision = input("Decision: ")

    if (new_decision == "4"):
        print("Disconnected!\n")
        break

    else:
            if (new_decision == "1"):
                try_name = input("Enter Your Name: ")
                try_surname = input("Enter Your Surname: ")
                try_password = input("Enter your Password: ")
                database.cursor.execute("Select * from Students where Name = ? and Surname = ? and Password = ?",(try_name, try_surname, try_password))
                students = database.cursor.fetchall()

                if (len(students) == 0):
                    print("This student is not exists!\nYou are going back to menu...\n")
                    time.sleep(2)
                    continue

                else:
                    for i in students:
                        if (((i[0] == try_name) and (i[1] == try_surname) and (i[5] == try_password))):
                            print("You succesfully signed in!\nPlease wait...")
                            new_student = Student(i[0], i[1], i[2], i[3], i[4], i[5])
                            time.sleep(2)

                            while True:
                                print("""
                                 *******************************************
                                 Press 1 for see the books in the library
                                 Press 2 for query a book
                                 Press 3 for deposit money into your account
                                 Press 4 for borrow a book
                                 Press 5 for buy a book
                                 Press 6 for give a book back
                                 Press 7 for see the account information
                                 Press 8 for go back to main menu
                                 *******************************************
                                 """)
                                new_decision2 = input("Decision: ")

                                if (new_decision2 == "8"):
                                    print("You are going back to menu...\n")
                                    time.sleep(2)
                                    break


                                else:
                                    while True:
                                        if (new_decision2 == "1"):
                                            print("Please wait...")
                                            time.sleep(2)
                                            database.show_books()
                                            new_decision3 = input("Please enter something to go back to menu\n")
                                            break

                                        elif (new_decision2 == "2"):
                                            name = input("Enter the book's name: ")
                                            database.cursor.execute("Select * from Books where Name = ?", [name])
                                            books = database.cursor.fetchall()

                                            if (len(books) == 0):
                                                print("This book is not exists!\nYou are going back to menu...")
                                                time.sleep(2)
                                                break

                                            else:
                                                for i in books:
                                                    print(i)
                                                    new_decision3 = input("Please enter something to go back to menu\n")
                                            break

                                        elif (new_decision2 == "3"):
                                            quantity = float(input("How much money?: "))
                                            print("Please wait...")
                                            time.sleep(2)
                                            new_student.deposit_money(quantity)
                                            print("Done!\n")
                                            new_decision3 = input("Please enter something to go back to menu\n")
                                            break

                                        elif (new_decision2 == "4"):
                                            name = input("Enter the book's name: ")
                                            new_student.cursor.execute("Select * from Books where Name = ?", [name])
                                            books = new_student.cursor.fetchall()

                                            if (len(books) == 0):
                                                print("This book is not exists!")

                                            else:
                                                for i in books:
                                                    new_book = Book(i[0], i[1], i[2], i[3], i[4], i[5])
                                                    print("Please wait...")
                                                    time.sleep(2)
                                                    new_student.borrow(new_book)
                                                    new_decision3 = input("Please enter something to go back to menu\n")
                                                break

                                        elif (new_decision2 == "5"):
                                            name = input("Enter the book's name: ")
                                            new_student.cursor.execute("Select * from Books where Name = ?", [name])
                                            books = new_student.cursor.fetchall()

                                            if (len(books) == 0):
                                                print("This book is not exists!")

                                            else:
                                                for i in books:
                                                    new_book = Book(i[0], i[1], i[2], i[3], i[4], i[5])
                                                    new_student.buy(new_book)
                                                new_decision3 = input("Please enter something to go back to menu\n")
                                            break



                                        elif (new_decision2 == "6"):
                                            name = input("Enter the book's name: ")
                                            new_student.cursor.execute("Select * from Books where Name = ?", [name])
                                            books = new_student.cursor.fetchall()

                                            if (len(books) == 0):
                                                print("This book is not exists!")

                                            else:
                                                for i in books:
                                                    new_book = Book(i[0], i[1], i[2], i[3], i[4], i[5])
                                                    new_student.give_back(new_book)
                                                new_decision3 = input("Please enter something to go back to menu\n")
                                            break

                                        elif (new_decision2 == "7"):
                                            new_student.show_info()
                                            new_decision3 = input("Please enter something to go back to menu\n")
                                            break


            elif (new_decision == "2"):
                try_name = input("Enter Your Name: ")
                try_surname = input("Enter Your Surname: ")
                try_password = input("Enter your Password: ")
                database.cursor.execute("Select * from Managers where Name = ? and Surname = ? and Password = ?", (try_name, try_surname, try_password))
                managers = database.cursor.fetchall()

                if (len(managers) == 0):
                    print("This Manager is not exists!\nYou are going back to menu...\n")
                    time.sleep(2)
                    continue

                else:
                    for i in managers:
                        if (((i[0] == try_name) and (i[1] == try_surname) and (i[3] == try_password))):
                            print("You succesfully signed in!\nPlease wait...")
                            new_manager = Manager(i[0], i[1], i[2], i[3])
                            time.sleep(2)

                            while True:
                                print("""
                                *******************************************
                                Press 1 for see the books in the library
                                Press 2 for query a book
                                Press 3 for add a book
                                Press 4 for delete a book
                                Press 5 for add a student
                                Press 6 for see the account information
                                Press 7 for go back to menu
                                *******************************************
                                """)

                                new_decision2 = input("Decision: ")

                                if (new_decision2 == "7"):
                                    print("You are going back to menu...\n")
                                    time.sleep(2)
                                    break

                                else:
                                    while True:
                                        if (new_decision2 == "1"):
                                            print("Please wait...")
                                            time.sleep(2)
                                            database.show_books()
                                            new_decision3 = input("Please enter something to go back to menu\n")
                                            break


                                        elif (new_decision2 == "2"):
                                            name = input("Enter the book's name: ")
                                            database.cursor.execute("Select * from Books where Name = ?", [name])
                                            books = database.cursor.fetchall()

                                            if (len(books) == 0):
                                                print("This book is not exists!\nYou are going back to menu...")
                                                time.sleep(2)
                                                break

                                            else:
                                                for i in books:
                                                    print(i)
                                                    new_decision3 = input("Please enter something to go back to menu\n")
                                                break

                                        elif (new_decision2 == "3"):
                                            print("PLEASE ENTER THE INFORMATİONS CORRECTLY,BY ONE BY!")
                                            new_name = input("Book Name: ")
                                            new_writer = input("Writer Name: ")
                                            new_page_amount = int(input("Page Amount: "))
                                            new_price = float(input("Book's Price: "))
                                            new_edition = int(input("Book's Edition: "))
                                            new_situation = "AVAIABLE"
                                            print("Adding...")
                                            time.sleep(2)
                                            new_book = Book(new_name, new_writer, new_page_amount, new_price,new_edition, new_situation)
                                            new_manager.add_book(new_book)
                                            print("Added!")
                                            new_decision3 = input("Please enter something to go back to menu\n")
                                            break

                                        elif (new_decision2 == "4"):
                                            name = input("Enter the book's name: ")
                                            database.cursor.execute("Select * from Books where Name = ?", [name])
                                            books = database.cursor.fetchall()

                                            if (len(books) == 0):
                                                print("This book is not exists!\nYou are going back to menu...")
                                                time.sleep(2)
                                                break

                                            else:
                                                for i in books:
                                                    new_book = Book(i[0], i[1], i[2], i[3], i[4], i[5])

                                                print("Deleting...")
                                                time.sleep(2)
                                                new_manager.delete_book(new_book)
                                                print("Deleted!")
                                                new_decision3 = input("Please enter something to go back to menu\n")
                                                break

                                        elif (new_decision2 == "5"):
                                            print("PLEASE ENTER THE INFORMATİONS CORRECTLY,BY ONE BY!")
                                            new_name = input("Name: ")
                                            new_surname = input("Surname: ")
                                            new_age = int(input("Age: "))
                                            new_balance = int(0)
                                            new_borrowed = int(0)
                                            new_password = input("Password: ")
                                            print("Adding...")
                                            time.sleep(2)
                                            new_student = Student(new_name, new_surname, new_age, new_balance,new_borrowed, new_password)
                                            new_manager.add_student(new_student)
                                            print("Added!")
                                            new_decision3 = input("Please enter something to go back to menu\n")
                                            break

                                        elif (new_decision2 == "6"):
                                            new_manager.show_info()
                                            new_decision3 = input("Please enter something to go back to menu\n")
                                            break

            elif (new_decision == "3"):
                print("PLEASE ENTER THE INFORMATİONS CORRECTLY,BY ONE BY!")
                new_name = input("Name: ")
                new_surname = input("Surname: ")
                new_age = int(input("Age: "))
                new_balance = float(0)
                new_borrowed = int(0)
                new_password = input("Password: ")
                print("Adding...")
                time.sleep(2)
                new_student = Student(new_name, new_surname, new_age, new_balance, new_borrowed, new_password)
                database.add_student(new_student)
                print("Added!")
                new_decision3 = input("Please enter something to go back to menu\n")
                continue

































