import mysql.connector
import datetime

# ANSI escape codes for formatting
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"
print(f"{BOLD}{UNDERLINE}LIBRARY MANAGEMENT SYSTEM{RESET}")


# Function to establish a connection to the MySQL database
def connect_to_database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Santanu@123",
        database="library_db"
    )
    return db


# Establishing a connection to the MySQL database
# db = connect_to_database()


# Create Admins table

def create_database_tables():
    # Establishing a connection to the MySQL database
    db = connect_to_database()

    # Create Admins table
    create_admins_table_query = """
    CREATE TABLE IF NOT EXISTS admins (
        admin_name VARCHAR(50) NOT NULL,
        gender VARCHAR(15) NOT NULL,
        age VARCHAR(3) NOT NULL,
        phone_no VARCHAR(10) NOT NULL, 
        email VARCHAR(50) NOT NULL,
        password VARCHAR(250) NOT NULL,
        admin_id INT PRIMARY KEY
    )
    """

    # Create Library Staff table
    create_library_staff_table_query = """
    CREATE TABLE IF NOT EXISTS library_staff (
        staff_id INT PRIMARY KEY,
        staff_name VARCHAR(50) NOT NULL,
        gender VARCHAR(15) NOT NULL,
        age VARCHAR(3) NOT NULL,
        phone_no VARCHAR(10) NOT NULL, 
        email VARCHAR(50) NOT NULL,
        password VARCHAR(100) NOT NULL,
        date_of_joining DATE
    )
    """
    # Create Books table
    create_books_table_query = """
    CREATE TABLE IF NOT EXISTS books (
        book_id INT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(100),
        category VARCHAR(50),
        isbn VARCHAR(50) NOT NULL,
        availability_status VARCHAR(10)
    )
    """

    # Create Students table
    create_students_table_query = """
    CREATE TABLE IF NOT EXISTS students (
        roll_id INT PRIMARY KEY,
        student_name VARCHAR(50) NOT NULL,
        gender VARCHAR(15) NOT NULL,
        age VARCHAR(3) NOT NULL,
        phone_no VARCHAR(10) NOT NULL, 
        email VARCHAR(50) NOT NULL,
        password VARCHAR(250) NOT NULL
    )
    """

    # Create Issue Log table
    create_issue_log_table_query = """
    CREATE TABLE IF NOT EXISTS issue_log (
        issue_id INT AUTO_INCREMENT PRIMARY KEY,
        book_id INT,
        roll_id INT,
        issued_date DATE,
        to_be_return_date DATE,
        returned_date DATE,
        fine_id INT,
        FOREIGN KEY (book_id) REFERENCES books(book_id),
        FOREIGN KEY (roll_id) REFERENCES students(roll_id),
        FOREIGN KEY (fine_id) REFERENCES late_fine(fine_id)
    )
    """

    # Create late-fine-Log table
    create_late_fine_table_query = """
    CREATE TABLE IF NOT EXISTS late_fine (
    fine_id INT PRIMARY KEY,
    roll_id INT,
    fine_amount INT,
    fine_duration INT,
    status VARCHAR(10),
    FOREIGN KEY (roll_id) REFERENCES students(roll_id)
    )
    """

    # Execute the CREATE TABLE queries
    cursor = db.cursor()
    cursor.execute(create_admins_table_query)
    cursor.execute(create_library_staff_table_query)
    cursor.execute(create_books_table_query)
    cursor.execute(create_students_table_query)
    cursor.execute(create_late_fine_table_query)
    cursor.execute(create_issue_log_table_query)
    db.commit()
    db.close()


try:
    create_database_tables()
except Exception as e:
    print("Error occurred while inserting data:", e)


# Function to check if admin credentials are valid
def validate_admin(admin_id, password):
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM admins WHERE admin_id = %s AND password = %s"
    cursor.execute(query, (admin_id, password))
    admin_data = cursor.fetchone()
    db.close()
    return admin_data is not None


# Function for admin functions
def admin_functions():
    while True:
        print("Admin Menu:")
        print("1. Change/Update Admin Details")
        print("2. Add Admins")
        print("3. Add Staff")
        print("4. Add Student")
        print("5. Add Book")
        print("6. Show Staff List")
        print("7. Show Student List")
        print("8. Show Book List")
        print("9. Delete Staff")
        print("10. Delete Book")
        print("11. Delete Student")
        print("12. Logout to Main Menu")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                # Function to update admin details
                update_admin_details()
            elif choice == 2:
                # Function to add admins
                add_admin()
            elif choice == 3:
                # Function to add staff
                add_staff()
            elif choice == 4:
                # Function to add student
                add_student()
            elif choice == 5:
                # Function to add book
                add_book()
            elif choice == 6:
                # Function to show staff list
                show_staff_list()
            elif choice == 7:
                # Function to show student list
                show_student_list()
            elif choice == 8:
                # Function to show book list
                show_book_list()
            elif choice == 9:
                # Function to delete staff
                delete_staff()
            elif choice == 10:
                # Function to delete book
                delete_book()
            elif choice == 11:
                # Function to delete student
                delete_student()
            elif choice == 12:
                # Logout to main menu
                main_menu()
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Function to update admin details
def update_admin_details():
    db = connect_to_database()
    cursor = db.cursor()

    admin_id = input("Enter Admin ID: ")
    new_name = input("Enter New Admin Name: ")
    new_gender = input("Enter New Gender: ")
    new_age = input("Enter New Age: ")
    new_phone_no = input("Enter New Phone Number: ")
    new_email = input("Enter New Email: ")
    new_password = input("Enter New Password: ")

    query = "UPDATE admins SET admin_name=%s, gender=%s, age=%s, phone_no=%s, email=%s, password=%s WHERE admin_id=%s"
    data = (new_name, new_gender, new_age, new_phone_no, new_email, new_password, admin_id)

    cursor.execute(query, data)
    db.commit()
    db.close()

    print("Admin details updated successfully.")


# Function to add admins
def add_admin():
    db = connect_to_database()
    cursor = db.cursor()

    admin_name = input("Enter Admin Name: ")
    gender = input("Enter Gender: ")
    age = input("Enter Age: ")
    phone_no = input("Enter Phone Number: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    admin_id = input("Enter Admin ID: ")

    query = """
    INSERT INTO admins (admin_name, gender, age, phone_no, email, password, admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data = (admin_name, gender, age, phone_no, email, password, admin_id)

    try:
        cursor.execute(query, data)
        db.commit()
        print("Admin added successfully.")
    except mysql.connector.IntegrityError:
        print("Admin with the same admin_id already exists.")
    finally:
        db.close()


# Function to add staff
def add_staff():
    db = connect_to_database()
    cursor = db.cursor()

    staff_id = input("Enter Staff ID: ")
    staff_name = input("Enter Staff Name: ")
    gender = input("Enter Gender: ")
    age = input("Enter Age: ")
    phone_no = input("Enter Phone Number: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    date_of_joining = input("Enter Date of Joining (YYYY-MM-DD): ")

    query = "INSERT INTO library_staff (staff_id, staff_name, gender, age, phone_no, email, password, date_of_joining) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (staff_id, staff_name, gender, age, phone_no, email, password, date_of_joining)

    try:
        cursor.execute(query, data)
        db.commit()
        print("Staff added successfully.")
    except mysql.connector.IntegrityError:
        print("Staff with the same staff_id already exists.")
    finally:
        db.close()


# Function to add student
def add_student():
    db = connect_to_database()
    cursor = db.cursor()

    roll_id = input("Enter Roll ID: ")
    student_name = input("Enter Student Name: ")
    gender = input("Enter Gender: ")
    age = input("Enter Age: ")
    phone_no = input("Enter Phone Number: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    query = "INSERT INTO students (roll_id, student_name, gender, age, phone_no, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (roll_id, student_name, gender, age, phone_no, email, password)

    try:
        cursor.execute(query, data)
        db.commit()
        print("Student added successfully.")
    except mysql.connector.IntegrityError:
        print("Student with the same roll_id already exists.")
    finally:
        db.close()


# Function to add book
def add_book():
    db = connect_to_database()
    cursor = db.cursor()

    book_id = input("Enter Book ID: ")
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    category = input("Enter Category: ")
    isbn = input("Enter ISBN: ")
    availability_status = input("Enter Availability Status: ")

    query = "INSERT INTO books (book_id, title, author, category, isbn, availability_status) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (book_id, title, author, category, isbn, availability_status)

    try:
        cursor.execute(query, data)
        db.commit()
        print("Book added successfully.")
    except mysql.connector.IntegrityError:
        print("Book with the same book_id already exists.")
    finally:
        db.close()


# Function to show staff list
def show_staff_list():
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM library_staff"
    cursor.execute(query)
    staff_list = cursor.fetchall()
    db.close()

    if not staff_list:
        print("No staff records found.")
    else:
        print("Staff List:")
        for staff in staff_list:
            print(staff)


# Function to show student list
def show_student_list():
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM students"
    cursor.execute(query)
    student_list = cursor.fetchall()
    db.close()

    if not student_list:
        print("No student records found.")
    else:
        print("Student List:")
        for student in student_list:
            print(student)


# Function to show book list
def show_book_list():
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM books"
    cursor.execute(query)
    book_list = cursor.fetchall()
    db.close()

    if not book_list:
        print("No book records found.")
    else:
        print("Book List:")
        for book in book_list:
            print(book)


# Function to delete staff
def delete_staff():
    db = connect_to_database()
    cursor = db.cursor()

    staff_id = input("Enter Staff ID to delete: ")
    query = "DELETE FROM library_staff WHERE staff_id = %s"

    try:
        cursor.execute(query, (staff_id,))
        db.commit()
        if cursor.rowcount > 0:
            print("Staff deleted successfully.")
        else:
            print("Staff not found.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        db.close()


# Function to delete book
def delete_book():
    db = connect_to_database()
    cursor = db.cursor()

    book_id = input("Enter Book ID to delete: ")
    query = "DELETE FROM books WHERE book_id = %s"

    try:
        cursor.execute(query, (book_id,))
        db.commit()
        if cursor.rowcount > 0:
            print("Book deleted successfully.")
        else:
            print("Book not found.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        db.close()


# Function to delete student
def delete_student():
    db = connect_to_database()
    cursor = db.cursor()

    roll_id = input("Enter Roll ID to delete: ")
    query = "DELETE FROM students WHERE roll_id = %s"

    try:
        cursor.execute(query, (roll_id,))
        db.commit()
        if cursor.rowcount > 0:
            print("Student deleted successfully.")
        else:
            print("Student not found.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        db.close()


# Function to check if a given staff_id and password match
def validate_staff(staff_id, password):
    db = connect_to_database()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM library_staff")
        rs = cursor.fetchall()
        for row in rs:
            print(row)
    except Exception as e:
        print("Error occurred while inserting data:", e)

    query = "SELECT * FROM library_staff WHERE staff_id = %s AND password = %s"
    cursor.execute(query, (staff_id, password))
    staff_data = cursor.fetchone()
    db.close()
    return staff_data is not None


# Function for staff functions
def staff_functions():
    while True:
        print("Staff Menu:")
        print("1. Change/Update Staff Details")
        print("2. Change/Update Student Details")
        print("3. Change/Update Book Details")
        print("4. Add Student")
        print("5. Add Book")
        print("6. Show Student List")
        print("7. Show Books List")
        print("8. Show Issue Log List")
        print("9. Show Late Fine List")
        print("10. Search for a Book (by Book ID)")
        print("11. See Availability Status of a Book (by Book ID)")
        print("12. Issue a Book to Student")
        print("13. Return a Book")
        print("14. Late Fine Submission")
        print("15. See Who Borrowed Books")
        print("16. See Students with Late Fine Due")
        print("17. Logout to Main Menu")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                # Function to change/update staff details
                change_staff_details()
            elif choice == 2:
                # Function to change/update student details
                change_student_details()
            elif choice == 3:
                # Function to change/update book details
                change_book_details()
            elif choice == 4:
                # Function to add a new student
                add_student()
            elif choice == 5:
                # Function to add a new book
                add_book()
            elif choice == 6:
                # Function to show the list of students
                show_student_list()
            elif choice == 7:
                # Function to show the list of books
                show_books_list()
            elif choice == 8:
                # Function to show the list of issue log
                show_issue_log_list()
            elif choice == 9:
                # Function to show the list of late fine
                show_late_fine_list()
            elif choice == 10:
                # Function to search for a book by Book ID
                search_book_by_id()
            elif choice == 11:
                # Function to see the availability status of a book by Book ID
                availability_status_by_id()
            elif choice == 12:
                # Function to issue a book to a student
                issue_book_to_student()
            elif choice == 13:
                # Function for student to return a book
                return_book_by_student()
            elif choice == 14:
                # Function for late fine submission by a student
                late_fine_submission()
            elif choice == 15:
                # Function to see who borrowed books
                see_borrowed_books()
            elif choice == 16:
                # Function to see students with late fine due
                see_students_with_late_fine_due()
            elif choice == 17:
                # Logout to main menu
                main_menu()
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Function to change/update staff details
def change_staff_details():
    db = connect_to_database()
    cursor = db.cursor()

    staff_id = input("Enter Staff ID: ")
    new_staff_name = input("Enter New Staff Name: ")
    new_gender = input("Enter New Gender: ")
    new_age = input("Enter New Age: ")
    new_phone_no = input("Enter New Phone Number: ")
    new_email = input("Enter New Email: ")
    new_password = input("Enter New Password: ")
    new_date_of_joining = input("Enter New Date of Joining (YYYY-MM-DD): ")

    update_query = """
    UPDATE library_staff SET
    staff_name = %s,
    gender = %s,
    age = %s,
    phone_no = %s,
    email = %s,
    password = %s,
    date_of_joining = %s
    WHERE staff_id = %s
    """
    data = (new_staff_name, new_gender, new_age, new_phone_no, new_email, new_password, new_date_of_joining, staff_id)
    cursor.execute(update_query, data)

    db.commit()
    db.close()
    print("Staff details updated successfully.")


# Function to change/update student details
def change_student_details():
    db = connect_to_database()
    cursor = db.cursor()

    roll_id = input("Enter Student Roll ID: ")
    new_student_name = input("Enter New Student Name: ")
    new_gender = input("Enter New Gender: ")
    new_age = input("Enter New Age: ")
    new_phone_no = input("Enter New Phone Number: ")
    new_email = input("Enter New Email: ")
    new_password = input("Enter New Password: ")

    update_query = """
    UPDATE students SET
    student_name = %s,
    gender = %s,
    age = %s,
    phone_no = %s,
    email = %s,
    password = %s
    WHERE roll_id = %s
    """
    data = (new_student_name, new_gender, new_age, new_phone_no, new_email, new_password, roll_id)
    cursor.execute(update_query, data)

    db.commit()
    db.close()
    print("Student details updated successfully.")


# Function to change/update book details
def change_book_details():
    db = connect_to_database()
    cursor = db.cursor()

    book_id = input("Enter Book ID: ")

    # Check if the book ID exists in the database
    check_query = "SELECT COUNT(*) FROM books WHERE book_id = %s"
    cursor.execute(check_query, (book_id,))
    result = cursor.fetchone()

    if result[0] == 0:
        print("Book ID not found. No updates were made.")
        db.close()
        return

    new_title = input("Enter New Title: ")
    new_author = input("Enter New Author: ")
    new_category = input("Enter New Category: ")
    new_isbn = input("Enter New ISBN: ")
    new_availability_status = input("Enter New Availability Status (Available/Issued): ")

    update_query = """
    UPDATE books SET
    title = %s,
    author = %s,
    category = %s,
    isbn = %s,
    availability_status = %s
    WHERE book_id = %s
    """
    data = (new_title, new_author, new_category, new_isbn, new_availability_status, book_id)
    cursor.execute(update_query, data)

    db.commit()
    db.close()
    print("Book details updated successfully.")


# Function to add a new book
def add_book():
    db = connect_to_database()
    cursor = db.cursor()

    book_id = input("Enter Book ID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    category = input("Enter Category: ")
    isbn = input("Enter ISBN: ")
    availability_status = input("Enter Availability Status (Available/Issued): ")

    # Check if the book with the given book_id already exists
    check_query = "SELECT * FROM books WHERE book_id = %s"
    cursor.execute(check_query, (book_id,))
    existing_book = cursor.fetchone()

    if existing_book:
        print("Book with the same Book ID already exists.")
    else:
        insert_query = "INSERT INTO books (book_id, title, author, category, isbn, availability_status) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (book_id, title, author, category, isbn, availability_status)
        cursor.execute(insert_query, data)
        db.commit()
        print("Book added successfully.")

    db.close()


# Function to show books list
def show_books_list():
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM books"
    cursor.execute(query)
    books_list = cursor.fetchall()
    db.close()

    if not books_list:
        print("No books found.")
    else:
        for book in books_list:
            print(book)


# Function to show issue_log list
def show_issue_log_list():
    db = connect_to_database()
    cursor = db.cursor()

    query = "SELECT * FROM issue_log"
    cursor.execute(query)
    issue_log_list = cursor.fetchall()

    db.close()

    if not issue_log_list:
        print("No issue logs found.")
    else:
        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        for issue_log in issue_log_list:
            # Print each column name and its corresponding value
            for i in range(len(column_names)):
                print(f"{column_names[i]} : {issue_log[i]}")
            print()  # Print an empty line between rows


# Function to show late_fine list
def show_late_fine_list():
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM late_fine"
    cursor.execute(query)
    late_fine_list = cursor.fetchall()
    db.close()

    if not late_fine_list:
        print("No late fines found.")
    else:
        # Fetch the column names from the cursor's description
        column_names = [desc[0] for desc in cursor.description]

        for late_fine in late_fine_list:
            # Print column names and their corresponding values
            for i in range(len(column_names)):
                print(f"{column_names[i]}: {late_fine[i]}")
            print()  # Add an empty line between rows for better readability


# Function to search for a book by Book ID
def search_book_by_id():
    db = connect_to_database()
    cursor = db.cursor()

    book_id = input("Enter Book ID to search: ")
    query = "SELECT * FROM books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    book_data = cursor.fetchone()

    db.close()

    if book_data:
        print("Book Details:")
        print("Book ID:", book_data[0])
        print("Title:", book_data[1])
        print("Author:", book_data[2])
        print("Category:", book_data[3])
        print("ISBN:", book_data[4])
        print("Availability Status:", book_data[5])
    else:
        print("Book not available.")


# Function to see the availability status of a book by Book ID
def availability_status_by_id():
    db = connect_to_database()
    cursor = db.cursor()

    book_id = input("Enter Book ID to check availability status: ")
    query = "SELECT availability_status FROM books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    availability_status = cursor.fetchone()

    db.close()

    if availability_status:
        print("Availability Status:", availability_status[0])
    else:
        print("Book not available.")


# Function to issue a book to a student
def issue_book_to_student():
    db = connect_to_database()
    cursor = db.cursor()

    book_id = input("Enter Book ID to issue: ")
    roll_id = input("Enter Student Roll ID: ")

    # Get the current date and calculate the to_be_return_date
    current_date = datetime.date.today()
    to_be_return_date = current_date + datetime.timedelta(days=15)
    print(current_date, to_be_return_date)

    # Check if the book exists and available for issuing
    check_query = "SELECT * FROM books WHERE book_id = %s AND availability_status = 'Available'"
    cursor.execute(check_query, (book_id,))
    book_data = cursor.fetchone()

    if not book_data:
        print("Book not available for issuing.")
    else:
        # Insert the issue_log record
        insert_query = """
        INSERT INTO issue_log (book_id, roll_id, issued_date, to_be_return_date) VALUES (%s, %s, %s, %s)
        """
        data = (book_id, roll_id, current_date, to_be_return_date)
        cursor.execute(insert_query, data)

        # Update the book's availability status
        update_query = "UPDATE books SET availability_status = 'Issued' WHERE book_id = %s"
        cursor.execute(update_query, (book_id,))

        db.commit()
        print("Book issued successfully.")

    db.close()


# Function for student to return a book
def return_book_by_student():
    db = connect_to_database()
    cursor = db.cursor()

    roll_id = input("Enter Student Roll ID: ")
    current_date = datetime.date.today()
    fine_id = None  # Initialize fine_id to None

    # Check if the student has borrowed any book
    check_query = "SELECT * FROM issue_log WHERE roll_id = %s AND returned_date IS NULL"
    cursor.execute(check_query, (roll_id,))
    issued_books = cursor.fetchall()

    if not issued_books:
        print("No books to return.")
    else:
        for book in issued_books:
            # Calculate the fine amount and update the issue_log and late_fine tables
            to_be_return_date = book[4]
            if current_date > to_be_return_date:
                fine_duration = (current_date - to_be_return_date).days
                fine_amount = fine_duration * 5

                # Generate a new fine_id
                check_query = "SELECT MAX(fine_id) FROM late_fine"
                cursor.execute(check_query)
                max_fine_id = cursor.fetchone()[0]
                if max_fine_id is not None:
                    fine_id = max_fine_id + 1
                else:
                    fine_id = 1

                # Insert into late_fine table
                insert_query = """
            INSERT INTO late_fine (fine_id, roll_id, fine_duration, fine_amount, status) VALUES (%s, %s, %s, %s, %s)
            """
                data = (fine_id, roll_id, fine_duration, fine_amount, "due")
                cursor.execute(insert_query, data)

            # Update the issue_log table with returned_date and fine_id
            update_query = "UPDATE issue_log SET returned_date = %s, fine_id = %s WHERE roll_id = %s AND book_id = %s AND returned_date IS NULL"
            data = (current_date, fine_id, roll_id, book[1])
            cursor.execute(update_query, data)

            # Update the books table with availability_status
            update_query = "UPDATE books SET availability_status = 'Available' WHERE book_id = %s"
            cursor.execute(update_query, (book[1],))

        db.commit()
        print("Books returned successfully.")

    db.close()


# Function to see who borrowed books
def see_borrowed_books():
    db = connect_to_database()
    cursor = db.cursor()

    roll_id = input("Enter Student Roll ID: ")
    query = "SELECT * FROM issue_log WHERE roll_id = %s AND returned_date IS NULL"
    cursor.execute(query, (roll_id,))
    borrowed_books = cursor.fetchall()
    db.close()

    if not borrowed_books:
        print("No books borrowed by the student.")
    else:
        print("Books Borrowed by the Student:")
        for book in borrowed_books:
            print("Issue ID:", book[0])
            print("Book ID:", book[1])
            print("Roll ID:", book[2])
            print("Issued Date:", book[3])
            print("To Be Returned Date:", book[6])
            print("Returned Date:", book[5])
            print("Fine ID:", book[4])
            print("--------------------------")


# Function to see students with late fine due
def see_students_with_late_fine_due():
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM late_fine WHERE status = 'due'"
    cursor.execute(query)
    late_fine_due = cursor.fetchall()
    db.close()

    if not late_fine_due:
        print("No late fine due for the student.")
    else:
        print("Students with Late Fine Due:")
        for late_fine in late_fine_due:
            print("Fine ID:", late_fine[0])
            print("Roll ID:", late_fine[1])
            print("Fine Duration (days):", late_fine[2])
            print("Fine Amount:", late_fine[3])
            print("Status:", late_fine[4])
            print("--------------------------")


# Function for late fine submission by a student
def late_fine_submission():
    db = connect_to_database()
    cursor = db.cursor()

    roll_id = input("Enter Student Roll ID: ")

    # Check if the student has any late fine due
    check_query = "SELECT * FROM late_fine WHERE roll_id = %s AND status = 'due'"
    cursor.execute(check_query, (roll_id,))
    late_fine_due = cursor.fetchall()

    if not late_fine_due:
        print("No late fine due for the student.")
    else:
        # Update the status of late fine to "paid"
        update_query = "UPDATE late_fine SET status = 'paid' WHERE roll_id = %s AND status = 'due'"
        cursor.execute(update_query, (roll_id,))
        db.commit()
        print("Late fine submission successful. Late fine status changed to 'paid'.")

    db.close()


# Function to check if a given student_roll_id and password match
def validate_student(student_roll_id, password):
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM students WHERE roll_id = %s AND password = %s"
    cursor.execute(query, (student_roll_id, password))
    student_data = cursor.fetchone()
    db.close()
    return student_data is not None


# Function for student functions
def student_functions():
    while True:
        print("Student Menu:")
        print("1. Change/Update Student Details")
        print("2. See Book List")
        print("3. See Books Borrowed")
        print("4. Can See Their Late Fine")
        print("5. Logout to Main Menu")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                # Function to change/update student details
                change_student_details()
            elif choice == 2:
                # Function to see the list of books
                show_books_list()
            elif choice == 3:
                # Function to see the list of books borrowed by the student
                see_books_borrowed()
            elif choice == 4:
                # Function to see the late fine details of the student
                see_late_fine()
            elif choice == 5:
                main_menu()
                # Logout to main menu
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Function to see the list of books borrowed by the student
def see_books_borrowed():
    db = connect_to_database()
    cursor = db.cursor()

    roll_id = input("Enter Student Roll ID: ")

    query = "SELECT * FROM issue_log WHERE roll_id = %s"
    cursor.execute(query, (roll_id,))
    books_borrowed = cursor.fetchall()

    if books_borrowed:
        print("Books Borrowed by Student:")
        for book in books_borrowed:
            print("Issue ID:", book[0])
            print("Book ID:", book[1])
            print("Issued Date:", book[3])
            print("To Be Returned Date:", book[4])
            print("Returned Date:", book[5] if book[5] else "Not Returned Yet")
            print("-----------------------")
    else:
        print("No books borrowed by the student.")

    db.close()


# Function to see the late fine details of the student
def see_late_fine():
    db = connect_to_database()
    cursor = db.cursor()

    roll_id = input("Enter Student Roll ID: ")

    query = "SELECT * FROM late_fine WHERE roll_id = %s"
    cursor.execute(query, (roll_id,))
    late_fines = cursor.fetchall()

    if late_fines:
        print("Late Fine Details:")
        for fine in late_fines:
            print("Fine ID:", fine[0])
            print("Fine Amount:", fine[2])
            print("Fine Duration:", fine[3])
            print("Status:", fine[4])
            print("-----------------------")
    else:
        print("No late fine for the student.")

    db.close()


# Function to display main menu and get user choice
def main_menu():
    while True:
        print("MAIN MENU")
        print("Enter 1 for ADMIN")
        print("Enter 2 for STAFF")
        print("Enter 3 for STUDENT")
        print("Enter 4 to EXIT")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                admin_id = input("Enter Admin ID: ")
                password = input("Enter Password: ")
                if validate_admin(admin_id, password):
                    admin_functions()
                else:
                    print("Invalid Admin ID or Password.")
            elif choice == 2:
                staff_id = input("Enter Staff ID: ")
                password = input("Enter Password: ")
                if validate_staff(staff_id, password):
                    staff_functions()
                else:
                    print("Invalid Staff ID or Password.")
            elif choice == 3:
                student_roll_id = input("Enter Student Roll ID: ")
                password = input("Enter Password: ")
                if validate_student(student_roll_id, password):
                    student_functions()
                else:
                    print("Invalid Student Roll ID or Password.")
            elif choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


main_menu()
