import mysql.connector as ms
import random

con = ms.connect(user='root',host='localhost',passwd='yourpassword')

cur = con.cursor()

cur.execute('create database if not exists clinic')
cur.execute('use clinic')

cur.execute('create table if not exists credentials(Name varchar(30),Username varchar(30),Password varchar(40),Profession varchar(20))')

# Everything a receptionist needs to do-------------------------------------------------------
def receptionist():
    cur.execute('SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED')

    cur.execute('create table if not exists patients(Name varchar(30),Age varchar(3),Phone_Number varchar(15),EmailID varchar(254),Insurance varchar(50))')
    while True:
        repeat = input('\nSelect an Option:\n1.Register Patient\n2.Logout\nOption: ')
        if repeat == '2':
            print('\nLogging out...')
            break
        else:
            PTname = input('Enter patient name: ')

            if len(PTname)>30:
                print('Name excceded character limit: 30')
                continue

            PTnumber = input('Enter patient phone number: ')

            if len(PTnumber)>15:
                print('Invalid phone number!')
                continue
            
            cur.execute('select * from patients where name="{}" and phone_number="{}"'.format(PTname,PTnumber))
            data = cur.fetchall()
             
            if data == []:
                    PTemail = input('Enter patient Email ID: ')
                    if len(PTemail)>254:
                        print('Email ID excceded character limit: 254')
                        continue

                    PTage = input('Enter patient age: ')
                    
                    if len(PTage)>3:
                        print('Invalid Age!')
                        continue

                    PTinsurance = input('Enter patient insurance (None, if does not have any): ')

                    if len(PTinsurance)>50:
                        print('Insurance company name is too large!')
                        continue

                    cur.execute('insert into patients values("{}","{}","{}","{}","{}")'.format(PTname,PTage,PTnumber,PTemail,PTinsurance))
                    con.commit()
                    cur.execute('select * from patients where name="{}" and phone_number="{}"'.format(PTname,PTnumber))
                    data = cur.fetchall()
                    print(data)

            else:
                print(data)
                
            while True:
                wnt2update = input('Would you like to update the above data (y/n): ')

                if wnt2update == 'y':
                    toUpdate = input('What would you like to update? (Name,Age,Phone_number,Email id,Insurance): ')
                    updatedInfo = input('What is the correct information?: ')
                    cur.execute('update patients set {}="{}" where name="{}" and phone_number="{}"'.format(toUpdate,updatedInfo,PTname,PTnumber))
                    con.commit()
                    cur.execute('select * from patients where name="{}" and phone_number="{}"'.format(PTname,PTnumber))
                    data = cur.fetchall()
                    print(data)
                else:
                    break

            while True:
                consult_speciality = input('Which speciality would you like to consult: ')
                cur.execute('select * from doctors where speciality="{}" and Availability="True"'.format(consult_speciality))
                data = cur.fetchall()

                if data == []:
                    print('Sorry! No doctors of this speciality are available at this time.')
                    rptsearch = input('Would you like to consult another speciality? (y/n): ')
                    if rptsearch == 'n':
                        break

                else:
                    print(data,'To cancel the process input: ->["Cancel"]')
                    cur.execute('select * from patients where name="{}" and phone_number="{}"'.format(PTname,PTnumber))
                    data = cur.fetchall()
                    PTage = data[0][1]
                    PTemail = data[0][3]
                    PTinsurance = data[0][4]

                    consult_doctor = input('Which doctor would you like to consult: ')

                    if consult_doctor.lower() == 'cancel':
                        break

                    cur.execute('create table if not exists waiting(Token varchar(4),Name varchar(30),Consulting_Doctor varchar(30),Speciality varchar(20),Phone_number varchar(15),EmailID varchar(254),Age varchar(3),Insurance varchar(50),Consultation_Fees int,Height decimal(5,2),Weight decimal(3,1),Body_Temperature decimal(3,1),Blood_Pressure int)')

                    def generateToken():
                        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                        generatedToken = ''

                        for i in range(4):
                            random_chr = random.choice(characters)
                            generatedToken+= random_chr
                        return generatedToken

                    Token = generateToken()

                    cur.execute('select token from waiting')
                    data = cur.fetchall()


                    while True:
                        for i in data:
                            for j in i:
                                if j == Token:
                                    Token = generateToken()
                                    break
                        break
                    
                    consultation_fees = int(input('Enter consulation fees: '))

                    cur.execute('insert into waiting values("{}","{}","{}","{}",{},"{}","{}","{}","{}",NULL,NULL,NULL,NULL)'.format(Token,PTname,consult_doctor,consult_speciality,PTnumber,PTemail,PTage,PTinsurance,consultation_fees))
                    con.commit()
                    print('Your token is:',Token)
                    break

# Things nurse do-----------------------------------------------

def nurse():
    while True:
        repeat = input("\nSelect an Option:\n1.Next patient\n2.Logout\nOption: ")

        if repeat == "2":
            print("\nLogging out...")
            break  

        else:
            token = input('Enter the token: ')


            cur.execute("SELECT Name, age FROM waiting WHERE Token = %s", (token,))    
            result = cur.fetchone()
            
            if result:
                print(f"Patient Name: {result[0]}, Age: {result[1]}")

            height = int(input('Enter the height: '))
            weight = int(input('Enter the weight: '))
            body_temperature = int(input('Enter the body temperature: '))
            blood_pressure = int(input('Enter the blood pressure: '))
            
            cur.execute("UPDATE waiting SET Height = %s, Weight = %s,body_temperature = %s, blood_Pressure = %s WHERE Token = %s", (height, weight,body_temperature, blood_pressure, token))
            con.commit()

# Things docotors do----------------------------------------------------------------------

def doctor():
    while True:
        repeat =input('\nSelect an option:\n1.Next Patient\n2.Logout\nOption: ')

        if repeat == '2':
            print('Logging out...')
            cur.execute('update doctors set availability="False" where name="{}"'.format(drname))
            con.commit()
            break
        else:
           token = input('Enter patient token: ')
           cur.execute('select * from waiting where token="{}"'.format(token))
           data = cur.fetchall()
           if data ==[]:
               print('Invalid Token!')
               continue
           
           else:
            print('\nName:',data[0][1])
            print('Phone number:',data[0][4])
            print('EmailID:',data[0][5])
            print('Age:',data[0][6])
            print('Height:',data[0][9])
            print('Weight:',data[0][10])
            print('Body Temperature:',data[0][11])
            print('Blood Pressure:',data[0][12])
            print('\nPrevious Records:')

            cur.execute('create table if not exists records(Name varchar(30),Consulting_Doctor varchar(30),Speciality varchar(20),Prescription varchar(200),Phone_number varchar(15),EmailID varchar(254),Age varchar(3),Insurance varchar(50),Consultation_Fees int,Height decimal(5,2),Weight decimal(3,1),Body_Temperature decimal(3,1),Blood_Pressure int)')
            cur.execute('select * from records where name="{}" and phone_number="{}"'.format(data[0][1],data[0][4]))
            data = cur.fetchall()
            print(data)

            prescription = input('\nEnter prescription: ')

            cur.execute('select * from waiting where token="{}"'.format(token))
            data = cur.fetchall()

            cur.execute('insert into records values("{}","{}","{}","{}",{},"{}","{}","{}","{}","{}","{}","{}","{}")'.format(data[0][1],data[0][2],data[0][3],prescription,data[0][4],data[0][5],data[0][6],data[0][7],data[0][8],data[0][9],data[0][10],data[0][11],data[0][12]))
            con.commit()
            cur.execute('delete from waiting where token="{}"'.format(token))
            con.commit()
            print('Patient Record Saved!')

# Login System --------------------------------------------------------------------------
print('\nAll Systems Online!')
while True:
    login = input('\nSelect an Option:\n1.Login\n2.Sign Up\n3.Exit\nOption: ')

    if login == '1':
        username = input('\nEnter an username: ')
        password = input('Enter an password: ')

        cur.execute('SELECT profession,name from credentials where username="{}" and password ="{}"'.format(username,password))
        data = cur.fetchall()

        if data == []:
            print('\nInvalid Username or Password!')

        else:
            profession = data[0][0]
            name = data[0][1]

            if profession.lower() == 'receptionist':
                print('\nWelcome back {}!'.format(name))
                receptionist()
            
            elif profession.lower() == 'nurse':
                print('\nWelcome back {}!'.format(name))
                nurse()
            
            elif profession.lower() == 'doctor':
                print('\nWelcome back {}!'.format(name))
                cur.execute('select * from credentials where username="{}" and password="{}" and profession="Doctor"'.format(username,password))
                data = cur.fetchall()
                drname = data[0][0]
                cur.execute('update doctors set availability="True" where name="{}"'.format(drname))
                con.commit()

                doctor()

            else:
                print('Error: Invalid profession found!')
                
    if login == '2':
        cur.execute('SELECT username from credentials')
        data = cur.fetchall()
        duplicate = False

        name = input('\nEnter your name: ')
        username = input('\nEnter an username: ')
        password = input('Enter an password: ')
        profession = input('\nEnter your profession(Receptionist/Nurse/Doctor): ')

        if len(name)>30:
            print('Name is too long!')
            continue

        if len(username)>30 or len(password)>40:
            print('Username or password excceded the character count 30 and 40 respectively!')
            continue

        for i in range(len(data)):
            if username in data[i]:
                duplicate = True

        if duplicate == True:
            print('Duplicate account!')
            continue

        if profession.lower() not in ['doctor','nurse','receptionist']:
            print('Invalid Profession!')
            continue

        cur.execute('insert into credentials values("{}","{}","{}","{}")'.format(name,username,password,profession))

        cur.execute("create table if not exists doctors(Name varchar(30),Speciality varchar(30),Availability varchar(5))")
        if profession.lower() == 'doctor':
            speciality = input('Enter your speciality: ')
            cur.execute('insert into doctors values("{}","{}","False")'.format(name,speciality))
            con.commit()
        
        print('Your account has been created!')

    if login == '3':
        print('Shutting systems down!')
        break
