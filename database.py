import mysql.connector

email = "aaltman818@gmailcom".replace("@", "_") # for now no periods, may replace later with other character

db = mysql.connector.connect(
    host="XXX",
    user="XXX",
    passwd="XXX",
    database="userFiles" # Add only after first run
    )
mycursor = db.cursor()

# On first run
mycursor.execute("CREATE DATABASE userFiles")

# On second run
mycursor.execute("CREATE TABLE " + email + " (file TEXT, fileID int PRIMARY KEY AUTO_INCREMENT)")

# To view table
mycursor.execute("DESCRIBE" + email)