import mysql.connector as ms

con = ms.connect(user='root',host='localhost',passwd='robo')

cur = con.cursor()

cur.execute('create database if not exists clinic')
cur.execute('use clinic')

cur.execute('create table if not exists credentials(Username varchar(30),Password varchar(40),Profession varchar(20))')

# Everything a receptionist needs to do-------------------------------------------------------
def receptionist():
    cur.execute('create table if not exists patients(Name varchar(30),Age varchar(3),Phone_Number varchar(15),EmailID varchar(254),Insurance varchar(50))')
    while True:
        repeat = input('\nSelect an Option:\n1.Register Patient\n2.Logout\nOption: ')
        if repeat == '2':
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
                    print(data)
                    cur.execute('select * from patients where name="{}" and phone_number="{}"'.format(PTname,PTnumber))
                    data = cur.fetchall()
                    PTage = data[0][1]
                    PTemail = data[0][3]
                    PTinsurance = data[0][4]

                    consult_doctor = input('Which doctor would you like to consult: ')
                    token ='QRTW'
                    consultation_fees = int(input('Enter consulation fees: '))

                    cur.execute('create table if not exists waiting(Token varchar(4),Name varchar(30),Consulting_Doctor varchar(30),Speciality varchar(20),Phone_number varchar(15),EmailID varchar(254),Age varchar(3),Insurance varchar(50),Consultation_Fees int,Height decimal(5,2),Weight decimal(3,1),Blood_Pressure int)')
                    cur.execute('insert into waiting values("{}","{}","{}","{}",{},"{}","{}","{}","{}",NULL,NULL,NULL)'.format(token,PTname,consult_doctor,consult_speciality,PTnumber,PTemail,PTage,PTinsurance,consultation_fees))
                    con.commit()
                    print('Your token number is:',token)
                    break

#---------------------------------------------------------------------------------------


# Login System --------------------------------------------------------------------------
while True:
    login = input('\nSelect an Option:\n1.Login\n2.Sign Up\n3.Exit\nOption: ')

    if login == '1':
        username = input('\nEnter an username: ')
        password = input('Enter an password: ')

        cur.execute('SELECT profession from credentials where username="{}" and password ="{}"'.format(username,password))
        data = cur.fetchall()

        if data == []:
            print('\nInvalid Username or Password!')

        else:
            profession = data[0][0]

            if profession.lower() == 'receptionist':
                receptionist()
            
            elif profession.lower() == 'nurse':
                # nurse()
                print('Nurse things')
            
            elif profession.lower() == 'doctor':
                # doctor()
                print('doctor things')

            else:
                print('Error: Invalid profession found!')
                


    if login == '2':
        cur.execute('SELECT username from credentials')
        data = cur.fetchall()
        duplicate = False

        username = input('\nEnter an username: ')
        password = input('Enter an password: ')
        profession = input('Enter your profession(Receptionist/Nurse/Doctor): ')

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

        cur.execute('insert into credentials values("{}","{}","{}")'.format(username,password,profession))
        print('Your account has been created!')


        cur.execute("create table if not exists doctors(Name varchar(30),Speciality varchar(30),Availability varchar(5))")
        if profession.lower() == 'doctor':
            name = input('Enter your name: ')
            speciality = input('Enter your speciality: ')
            cur.execute('insert into doctors values("{}","{}","False")'.format(name,speciality))
            con.commit()

    if login == '3':
        print('Shutting systems down!')
        break

#------------------------------------------------------------