import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class HospitalManagementSystem:
    def __init__(self, root, host, user, password, database):
        self.root = root
        self.root.title("Hospital Management System")

        # Connect to MySQL database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="h"        )
        self.cursor = self.connection.cursor()

        # Create tables if not exist
        self.create_tables()

        self.create_widgets()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(10) NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                specialization VARCHAR(255) NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT,
                doctor_id INT,
                date DATE NOT NULL,
                time TIME NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')

        self.connection.commit()

    def create_widgets(self):
        # Patient Entry Frame
        patient_frame = ttk.LabelFrame(self.root, text="Patients")
        patient_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(patient_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(patient_frame, text="Age:").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(patient_frame, text="Gender:").grid(row=0, column=2, padx=5, pady=5)

        self.patient_name_entry = ttk.Entry(patient_frame, width=20)
        self.patient_age_entry = ttk.Entry(patient_frame, width=10)
        self.patient_gender_entry = ttk.Entry(patient_frame, width=10)

        self.patient_name_entry.grid(row=1, column=0, padx=5, pady=5)
        self.patient_age_entry.grid(row=1, column=1, padx=5, pady=5)
        self.patient_gender_entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(patient_frame, text="Add Patient", command=self.add_patient).grid(row=2, columnspan=3, pady=10)

        # Doctor Entry Frame
        doctor_frame = ttk.LabelFrame(self.root, text="Doctors")
        doctor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(doctor_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(doctor_frame, text="Specialization:").grid(row=0, column=1, padx=5, pady=5)

        self.doctor_name_entry = ttk.Entry(doctor_frame, width=20)
        self.doctor_specialization_entry = ttk.Entry(doctor_frame, width=20)

        self.doctor_name_entry.grid(row=1, column=0, padx=5, pady=5)
        self.doctor_specialization_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(doctor_frame, text="Add Doctor", command=self.add_doctor).grid(row=2, columnspan=2, pady=10)

        # Appointment Entry Frame
        appointment_frame = ttk.LabelFrame(self.root, text="Appointments")
        appointment_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        ttk.Label(appointment_frame, text="Patient:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(appointment_frame, text="Doctor:").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(appointment_frame, text="Date:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(appointment_frame, text="Time:").grid(row=0, column=3, padx=5, pady=5)

        self.patient_combobox = ttk.Combobox(appointment_frame, values=self.get_patient_names())
        self.doctor_combobox = ttk.Combobox(appointment_frame, values=self.get_doctor_names())
        self.date_entry = ttk.Entry(appointment_frame, width=15)
        self.time_entry = ttk.Entry(appointment_frame, width=10)

        self.patient_combobox.grid(row=1, column=0, padx=5, pady=5)
        self.doctor_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.date_entry.grid(row=1, column=2, padx=5, pady=5)
        self.time_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(appointment_frame, text="Schedule Appointment", command=self.schedule_appointment).grid(row=2, columnspan=4, pady=10)

    def add_patient(self):
        name = self.patient_name_entry.get()
        age = self.patient_age_entry.get()
        gender = self.patient_gender_entry.get()

        if name and age and gender:
            try:
                self.cursor.execute("INSERT INTO patients (name, age, gender) VALUES (%s, %s, %s)", (name, age, gender))
                self.connection.commit()
                self.clear_patient_entries()
                self.update_patient_combobox()
                messagebox.showinfo("Success", "Patient added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding patient: {e}")

    def add_doctor(self):
        name = self.doctor_name_entry.get()
        specialization = self.doctor_specialization_entry.get()

        if name and specialization:
            try:
                self.cursor.execute("INSERT INTO doctors (name, specialization) VALUES (%s, %s)", (name, specialization))
                self.connection.commit()
                self.clear_doctor_entries()
                self.update_doctor_combobox()
                messagebox.showinfo("Success", "Doctor added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding doctor: {e}")

    def schedule_appointment(self):
        patient_name = self.patient_combobox.get()
        doctor_name = self.doctor_combobox.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        if patient_name and doctor_name and date and time:
            try:
                patient_id = self.get_patient_id_by_name(patient_name)
                doctor_id = self.get_doctor_id_by_name(doctor_name)

                self.cursor.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (%s, %s, %s, %s)",
                                    (patient_id, doctor_id, date, time))
                self.connection.commit()
                self.clear_appointment_entries()
                messagebox.showinfo("Success", "Appointment scheduled successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error scheduling appointment: {e}")

    def get_patient_names(self):
        self.cursor.execute("SELECT name FROM patients")
        return [row[0] for row in self.cursor.fetchall()]

    def get_doctor_names(self):
        self.cursor.execute("SELECT name FROM doctors")
        return [row[0] for row in self.cursor.fetchall()]

    def get_patient_id_by_name(self, name):
        self.cursor.execute("SELECT id FROM patients WHERE name=%s", (name,))
        return self.cursor.fetchone()[0]

    def get_doctor_id_by_name(self, name):
        self.cursor.execute("SELECT id FROM doctors WHERE name=%s", (name,))
        return self.cursor.fetchone()[0]

    def clear_patient_entries(self):
        self.patient_name_entry.delete(0, tk.END)
        self.patient_age_entry.delete(0, tk.END)
        self.patient_gender_entry.delete(0, tk.END)

    def clear_doctor_entries(self):
        self.doctor_name_entry.delete(0, tk.END)
        self.doctor_specialization_entry.delete(0, tk.END)

    def clear_appointment_entries(self):
        self.patient_combobox.set("")
        self.doctor_combobox.set("")
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def update_patient_combobox(self):
        self.patient_combobox["values"] = self.get_patient_names()

    def update_doctor_combobox(self):
        self.doctor_combobox["values"] = self.get_doctor_names()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root,host="localhost", user="root", password="root", database="h")
    root.mainloop()
