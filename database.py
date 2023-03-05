import mysql.connector

db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="rootpassword",
        database="userfiles"
    )
def userInfo(email):
    email = email.replace("@", "_").replace(".", "_")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="rootpassword",
        database="userfiles"
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS " + email + " (fileName TEXT, file LONGBLOB, fileID int PRIMARY KEY AUTO_INCREMENT)")
    mycursor.close
    db.close()

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def insertBLOB(email, biodataFile):
    email = email.replace("@", "_").replace(".", "_")
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="rootpassword",
            database="userfiles"
        )
        mycursor = db.cursor()
        sql_insert_blob_query = "INSERT INTO " + email  + " (fileName, file) VALUES (%s, %s)"

        file = convertToBinaryData(biodataFile)

        # Convert data into tuple format
        insert_blob_tuple = (biodataFile, file)
        result = mycursor.execute(sql_insert_blob_query, insert_blob_tuple)
        db.commit()

    except mysql.connector.Error as error:
        print("Failed to upload and save file. {}".format(error))

    finally:
        if db.is_connected():
            mycursor.close()
            db.close()
            print("MySQL connection is closed")

def readBLOB(email, fileName, fileLocation):
    email = email.replace("@", "_").replace(".", "_")
    print("Reading BLOB data from user table")
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="rootpassword",
            database="userfiles"
        )
        mycursor = db.cursor()
        sql_fetch_blob_query = "SELECT * from " + email + " where fileName = %s"
        insert_blob_tuple = (fileName, )
        mycursor.execute(sql_fetch_blob_query, insert_blob_tuple)
        record = mycursor.fetchall()
        for row in record:
            print("File Name = ", row[0])
            file = row[1]
            print("Storing employee image and bio-data on disk \n")
            write_file(file, fileLocation)

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if db.is_connected():
            mycursor.close()
            db.close()
            print("MySQL connection is closed")

def checkCredentialExistance(email):
    email = email.replace("@", "_").replace(".", "_")
    returnBool = False
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="rootpassword",
            database="userLogin"
        )
        mycursor = db.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS Credentials(email TEXT, password BLOB, userID int PRIMARY KEY AUTO_INCREMENT)")
        mycursor.execute("SELECT email, COUNT(*) FROM Credentials WHERE email = %s GROUP BY email", (email,))
        results = mycursor.fetchall()
        for row in results:
            if row[0] == email:
                returnBool = True
                print("Exists")
        if returnBool == False:
            print("Doesn't Exist")
        if db.is_connected():
            mycursor.close()
            db.close()                
            print("MySQL connection is closed")
    except mysql.connector.Error as error:
        print("Failed to check. {}".format(error))
        return False

    return returnBool
        

def createCredentials(email, password):
    email = email.replace("@", "_").replace(".", "_")
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="rootpassword",
            database="userLogin"
        )
        mycursor = db.cursor()
        result = mycursor.execute("INSERT INTO Credentials(email, password) VALUES (%s, %s)", (email, password))
        db.commit()

    except mysql.connector.Error as error:
        print("Failed to save login credentials. {}".format(error))

    finally:
        if db.is_connected():
            mycursor.close()
            db.close()
            print("MySQL connection is closed")

def getCredentials(email):
    email = email.replace("@", "_").replace(".", "_")
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="rootpassword",
            database="userLogin"
        )
        mycursor = db.cursor()
        mycursor.execute("SELECT * from Credentials")
        record = mycursor.fetchall()
        #for row in record:
            #password = row[1]
        return record

    except mysql.connector.Error as error:
        print("Failed to get login credentials. {}".format(error))

    finally:
        if db.is_connected():
            mycursor.close()
            db.close()
            print("MySQL connection is closed")