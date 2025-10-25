import datetime 
import random 
import mysql.connector as sqltor 
import pandas as pd 
 
con = sqltor.connect(host="localhost", user="root", password="sathana") 
cur = con.cursor(buffered=True) 
cur.execute("CREATE DATABASE IF NOT EXISTS hello") 
cur.execute("USE hello") 
 
cur.execute(""" 
CREATE TABLE IF NOT EXISTS appt ( 
    idno CHAR(12) PRIMARY KEY, 
    name VARCHAR(100), 
    age INT, 
    gender CHAR(1), 
    phone CHAR(10), 
    bg VARCHAR(5) 
) 
""") 
con.commit() 
 
def today_str(): 
    d = datetime.date.today() 
    return d.strftime("%A, %d %B %Y") 
 
def now_time_str(): 
    t = datetime.datetime.now() 
    return t.strftime("%H:%M:%S") 
 
def valid_blood_group(bg): 
    allowed = {"A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"} 
    return bg.upper() in allowed 
 
# --- Patient operations --- 
def register_patient(): 
    while True: 
        idn = input("Enter Aadhaar (12 digits): ").strip() 
        if len(idn) == 12 and idn.isdigit(): 
            cur.execute("SELECT 1 FROM appt WHERE idno = %s", (idn,)) 
            if cur.fetchone(): 
                print("A patient with this Aadhaar already exists.") 
                return 
            break 
        print("Invalid Aadhaar. Must be 12 digits.") 
 
    name = input("Patient name: ").strip() 
    while True: 
        try: 
            age = int(input("Age: ").strip()) 
            break 
        except ValueError: 
            print("Please enter numeric age.") 
    while True: 
        gender = input("Gender (M/F): ").strip().upper() 
        if gender in ("M", "F"): 
            break 
        print("Enter M or F.") 
    while True: 
        phone = input("Phone (10 digits): ").strip() 
        if len(phone) == 10 and phone.isdigit(): 
            break 
        print("Invalid phone.") 
    while True: 
        bg = input("Blood group (A+, B+, O+, AB+, A-, B-, O-, AB-): ").strip().upper() 
        if valid_blood_group(bg): 
            break 
        print("Invalid blood group.") 
 
    cur.execute( 
        "INSERT INTO appt (idno, name, age, gender, phone, bg) VALUES (%s, %s, %s, %s, %s, %s)", 
        (idn, name, age, gender, phone, bg) 
    ) 
    con.commit() 
    print("Registration complete.") 
    print_patient(idn) 
 
 
def print_patient(idn): 
    cur.execute("SELECT idno, name, age, gender, phone, bg FROM appt WHERE idno = %s", (idn,)) 
    row = cur.fetchone() 
    if not row: 
        print("No record found.") 
        return 
    print("Patient details:") 
    print(f"  Aadhaar: {row[0]}") 
    print(f"  Name:    {row[1]}") 
    print(f"  Age:     {row[2]}") 
    print(f"  Gender:  {row[3]}") 
    print(f"  Phone:   {row[4]}") 
    print(f"  Blood:   {row[5]}") 
 
 
def get_patient_by_aadhaar(): 
    idn = input("Enter Aadhaar: ").strip() 
    cur.execute("SELECT idno, name, age, gender, phone, bg FROM appt WHERE idno = %s", (idn,)) 
    rows = cur.fetchall() 
    if not rows: 
        print("No data found for that Aadhaar.") 
        return None 
    return rows[0] 
 
 
def update_patient_field(): 
    row = get_patient_by_aadhaar() 
    if not row: 
        return 
    idn = row[0] 
    print("Current details:") 
    print_patient(idn) 
    print("Which field do you want to update?\n1) Name\n2) Age\n3) Gender\n4) Phone\n5) Blood group\n6) Cancel") 
    choice = input("Choice: ").strip() 
    if choice == "1": 
        new = input("New name: ").strip() 
        cur.execute("UPDATE appt SET name = %s WHERE idno = %s", 
(new, idn)) 
    elif choice == "2": 
        while True: 
            try: 
                new = int(input("New age: ").strip()) 
                break 
            except ValueError: 
                print("Enter numeric age.") 
        cur.execute("UPDATE appt SET age = %s WHERE idno = %s", 
(new, idn)) 
    elif choice == "3": 
        while True: 
            new = input("New gender (M/F): ").strip().upper() 
            if new in ("M", "F"): 
                break 
            print("Enter M or F.") 
        cur.execute("UPDATE appt SET gender = %s WHERE idno = %s", 
(new, idn)) 
    elif choice == "4": 
        while True: 
            new = input("New phone (10 digits): ").strip() 
            if len(new) == 10 and new.isdigit(): 
                break 
            print("Invalid phone.") 
        cur.execute("UPDATE appt SET phone = %s WHERE idno = %s", 
(new, idn)) 
    elif choice == "5": 
        while True: 
            new = input("New blood group: ").strip().upper() 
            if valid_blood_group(new): 
                break 
            print("Invalid blood group.") 
        cur.execute("UPDATE appt SET bg = %s WHERE idno = %s", 
(new, idn)) 
    else: 
        print("Canceled.") 
        return 
    con.commit() 
    print("Updated details:") 
    print_patient(idn) 
 
 
# --- Appointment booking & lists --- 
DOCTORS = [ 
    ("Dr. Varun", "Cardiologist", 201), 
    ("Dr. sathana", "Cardiologist", 202), 
    ("Dr. Salman", "Psychiatrist", 203), 
    ("Dr. Shahrukh", "Psychiatrist", 204), 
    ("Dr. Akshay", "Otolaryngologist", 205), 
    ("Dr. Amir", "Otolaryngologist", 206), 
    ("Dr. Sidharth", "Rheumatologist", 207), 
    ("Dr. Abhishek", "Rheumatologist", 208), 
    ("Dr. Ajay", "Neurologist", 209), 
    ("Dr. Ranveer", "Neurologist", 200), 
] 
SERVICES = [ 
    ("X-Ray", 101), 
    ("MRI", 102), 
    ("CT Scan", 103), 
    ("Endoscopy", 104), 
    ("Dialysis", 105), 
    ("Ultrasound", 301), 
    ("EEG", 302), 
    ("ENMG", 303), 
    ("ECG", 304), 
] 
 
 
def list_doctors(): 
    df = pd.DataFrame(DOCTORS, columns=["Name", "Department", 
"Room"]) 
    print(df.to_string(index=False)) 
 
 
def list_services(): 
    df = pd.DataFrame(SERVICES, columns=["Service", "Room"]) 
    print(df.to_string(index=False)) 
 
 
def book_appointment(): 
    row = get_patient_by_aadhaar() 
    if not row: 
        return 
    print("Select department:") 
    depts = sorted(set(d[1] for d in DOCTORS)) 
    for i, d in enumerate(depts, start=1): 
        print(f"{i}) {d}") 
    try: 
        choice = int(input("Choice number: ").strip()) 
        if not (1 <= choice <= len(depts)): 
            print("Invalid choice.") 
            return 
    except ValueError: 
        print("Invalid input.") 
        return 
    selected_dept = depts[choice - 1] 
    candidates = [d for d in DOCTORS if d[1] == selected_dept] 
    chosen = random.choice(candidates) 
    appointment_date = datetime.date.today() + datetime.timedelta(days=random.choice([1,3,4,5,6])) 
    appointment_no = random.randint(10, 99) 
    print("Appointment confirmed:") 
    print(f"  Patient Aadhaar: {row[0]}") 
    print(f"  Doctor: {chosen[0]} ({chosen[1]})") 
    print(f"  Room: {chosen[2]}") 
    print(f"  Date: {appointment_date.isoformat()}") 
    print(f"  Appointment no.: {appointment_no}") 
 
 
# --- Doctor login (view today's patients random sample) --- 
DOCTOR_PASSWORDS = {str(i+1): 7001 + i for i in 
range(len(DOCTORS))}  # '1' -> 7001 etc. 
 
 
def doctor_login(): 
    doc_id = input("Enter your doctor ID (1..{}), or press Enter to go back: ".format(len(DOCTORS))).strip() 
    if not doc_id: 
        return 
    if doc_id not in DOCTOR_PASSWORDS: 
        print("Unknown doctor ID.") 
        return 
    try: 
        pswd = int(input("Enter password: ").strip()) 
    except ValueError: 
        print("Invalid password format.") 
        return 
    if pswd != DOCTOR_PASSWORDS[doc_id]: 
        print("Wrong password.") 
        return 
    idx = int(doc_id) - 1 
    doc = DOCTORS[idx] 
    now = datetime.datetime.now() 
    ampm = now.strftime("%p") 
    print(f"Hello {doc[0]}. Current time: {now_time_str()} ({ampm})") 
    # For demo: randomly show a few sample patients (or all from DB if you prefer) 
    cur.execute("SELECT idno, name, age FROM appt LIMIT 10") 
    sample = cur.fetchall() 
    if not sample: 
        print("No patients found in database.") 
        return 
    df = pd.DataFrame(sample, columns=["Aadhaar", "Name", "Age"]) 
    print("Today's / sample appointments:") 
    print(df.to_string(index=False)) 
 
 
# --- Main menu --- 
def main(): 
    print("Simple Hospital Appointment System") 
    print("Date:", today_str()) 
    print("Time:", now_time_str()) 
    while True: 
        print("\nMain menu:") 
        print("1) Patient") 
        print("2) Doctor") 
        print("3) Exit") 
        choice = input("Select option: ").strip() 
        if choice == "1": 
            while True: 
                print("\nPatient menu:") 
                print("1) Register") 
                print("2) Book appointment") 
                print("3) List doctors") 
                print("4) List services") 
                print("5) Modify patient data") 
                print("6) Back") 
                c = input("Choice: ").strip() 
                if c == "1": 
                    register_patient() 
                elif c == "2": 
                    book_appointment() 
                elif c == "3": 
                    list_doctors() 
                elif c == "4": 
                    list_services() 
                elif c == "5": 
                    update_patient_field() 
                elif c == "6": 
                    break 
                else: 
                    print("Invalid choice.") 
        elif choice == "2": 
            doctor_login() 
        elif choice == "3": 
            print("Goodbye.") 
            break 
        else: 
            print("Invalid choice.") 
 
 
if __name__ == "__main__": 
    try: 
        main() 
    finally: 
        con.close()  
 
