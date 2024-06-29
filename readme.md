# Patient Management System (PMS)

This Python script is a comprehensive system for managing a clinic, including functionalities for various roles such as receptionist, nurse, and doctor. It uses the MySQL connector to interact with a MySQL database.

## Features

### Database Setup
- Connects to a MySQL database.
- Creates a database named `clinic` if it doesn't exist.
- Creates necessary tables: `credentials`, `patients`, `doctors`, `waiting`, and `records`.

### Sign Up System
- Allows new users to create an account by providing their name, username, password, and profession.
- Ensures username uniqueness and validates input lengths.
- For doctors, also collects their speciality and initializes their availability status.

### Login System
- Provides options to login, sign up, or exit.
- Validates user credentials and identifies their role (receptionist, nurse, or doctor).

### Receptionist Functions
- Registers new patients by collecting personal and insurance details.
- Updates existing patient information.
- Schedules appointments with available doctors based on their speciality.
- Generates unique tokens for patient consultations.

### Nurse Functions
- Retrieves the next patient using their token.
- Records vital signs such as height, weight, body temperature, and blood pressure.

### Doctor Functions
- Retrieves the next patient using their token.
- Views patient details and previous medical records.
- Records new prescriptions and updates patient records.
- Marks their availability status.


### Data Management
- Commits changes to the database after each operation to ensure data integrity.
- Uses SQL queries to perform insertions, updates, and selections based on user inputs.

---

To use this script, ensure you have MySQL installed and running, and update the connection parameters (`user`, `host`, `passwd`) with your MySQL credentials.

### Developers:
- Abdul Swareeh
- Abdul Hadi
- Abijith Menon 