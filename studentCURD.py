import mysql.connector
conn=mysql.connector.connect (
    host="localhost",
    port=3306,
    user="root",
    password="sathana",
    database="sathana"
)
def get_connection():
    try:
        conn=mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="sathana",
            database="sathana"
        )
        return conn
    except mysql.connector.Error as e:
        print("Couldn't connect ot Mysql.Please")
        print("Error: ", e)
        return None
    

def create_stud(): 
    name = input("Enter student name: ").strip() 
    age_text = input("Enter age (number): ").strip() 
    if not name or not age_text.isdigit(): 
        print("Please provide a name and a number for age.") 
        return 
    age = int(age_text) 
 
    conn = get_connection () 
 
    if not conn: return 
    cur = conn.cursor() 
    cur.execute("INSERT INTO stud (name, age) VALUES (%s, %s)", (name, age)) 
    conn.commit() 
    print("Stud added!") 
    cur.close() 
    conn.close() 
 
 
def read_stud(): 
    conn = get_connection() 
    if not conn: return 
    cur = conn.cursor() 
    cur.execute("SELECT id, name, age FROM stud ORDER BY id") 
    rows = cur.fetchall() 
    if not rows: 
        print("No stud yet. Try option 1 to add one.") 
    else: 
        print("\n--- Stud ---") 
        for row in rows: 
            print(f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]}") 
    cur.close() 
    conn.close() 
 
def update_stud(): 
    id_text = input("Enter the ID of the stud to update: ").strip() 
    if not id_text.isdigit(): 
        print("Please enter a valid ID number.") 
        return 
    new_name = input("New name: ").strip() 
    new_age_text = input("New age (number): ").strip() 
    if not new_name or not new_age_text.isdigit(): 
        print("Please provide a name and a number for age.") 
        return 
    new_age = int(new_age_text) 
 
    conn = get_connection() 
    if not conn: return 
    cur = conn.cursor() 
    cur.execute("UPDATE stud SET name=%s, age=%s WHERE id=%s", (new_name, new_age, id_text)) 
    conn.commit() 
    if cur.rowcount == 0: 
        print("No stud with that ID was found.") 
    else: 
        print("Stud updated!") 
    cur.close() 
    conn.close() 
 
def delete_stud(): 
    id_text = input("Enter the ID of the stud to delete: ").strip() 
    if not id_text.isdigit(): 
        print("Please enter a valid ID number.") 
        return 
 
    conn = get_connection() 
    if not conn: return 
    cur = conn.cursor() 
    cur.execute("DELETE FROM stud WHERE id=%s", (id_text,)) 
    conn.commit() 
    if cur.rowcount == 0: 
        print("No stud with that ID was found.") 
    else: 
        print("Stud deleted!") 
    cur.close() 
    conn.close() 
 
def main(): 
    print("Python MySQL CRUD demo!\n") 
    while True: 
        print("Choose an option:") 
        print("1) Create (add a stud)") 
        print("2) Read (show all stud)") 
        print("3) Update (edit a stud)") 
        print("4) Delete (remove a stud)") 
        print("5) Exit")
        
        choice = input("Your choice (1-5): ").strip() 
 
        if choice == "1": 
            create_stud() 
        elif choice == "2": 
            read_stud() 
        elif choice == "3": 
            update_stud() 
        elif choice == "4": 
            delete_stud() 
        elif choice == "5": 
            print("Goodbye!") 
            break 
        else: 
            print("Please choose 1, 2, 3, 4, or 5.\n") 
 
if __name__ == "__main__": 
    main() 
