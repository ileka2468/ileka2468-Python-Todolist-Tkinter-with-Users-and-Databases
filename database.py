import mysql.connector as sqlc
import bcrypt


def retrieve_content(userID):
    db = sqlc.connect(
        host="localhost", # your server ip or localhost if in development enviro
        user="YourUserNameHere", # database username
        passwd="YourPasswordHere", # database password
        database="YourDataBaseNameHere"
    )
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM content WHERE uid = '{userID}'")
    userPosts = cursor.fetchall()
    return userPosts

def insertPost(uid, post, date, time):
    db = sqlc.connect(
        host="localhost", # your server ip or localhost if in development enviro
        user="YourUserNameHere", # database username
        passwd="YourPasswordHere", # database password
        database="YourDataBaseNameHere"
    )
    cursor = db.cursor()
    cursor.execute("INSERT INTO content (uid, content, date_posted, time_posted) VALUES (%s, %s, %s, %s)", (uid, post, date, time))
    db.commit()
    return cursor.lastrowid


def register(username, password, cursor, db):
    if not username.isspace == True:
        if username and password not in [""]:
            if " " not in username and " " not in password:
                bytes_pw = str.encode(password)
                hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
                cursor.execute("INSERT INTO credentials (username, password) VALUES (%s, %s)", (username, hashed_pw))
                db.commit()
                db.close()
                return "User Registered"
            else:
                return "FORMAT ERROR"
        else:
            return "FORMAT EMPTY"
    else:
        return "FORMAT ERROR"


def login(query, userEntry, passEntry):
    actualUser = query[0][1]
    hashedPW = query[0][2]
    bytesHashedPw = str.encode(hashedPW)
    enteredBytesPw = str.encode(passEntry)
    # print(enteredBytesPw)

    # if bcrypt.checkpw(enteredBytesPw, bytesHashedPw):
    #     print("matches")

    if userEntry == actualUser:
        if bcrypt.checkpw(enteredBytesPw, bytesHashedPw):
            return "STATUS OK", query[0][1], query[0][0]
        else:
            return "STATUS FAILED"
    else:
        return "UNKNOWN ERROR"


def preRegister(username, password):
    db = sqlc.connect(
        host="localhost", # your server ip or localhost if in development enviro
        user="YourUserNameHere", # database username
        passwd="YourPasswordHere", # database password
        database="YourDataBaseNameHere"
    )

    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM credentials WHERE username = '{username}'")
    query_matches = cursor.fetchall()
    # print(query_matches)

    try:
        if username == query_matches[0][1]:
            return "STATUS FAILED USER EXISTS"
    except IndexError:
        reg = register(username, password, cursor, db)
        if reg == "User Registered":
            return "STATUS OK"
        elif reg == "FORMAT EMPTY":
            return "FORMAT EMPTY"
        else:
            return "FORMAT ERROR"


def preLogin(username, password):
    db = sqlc.connect(
        host="localhost", # your server ip or localhost if in development enviro
        user="YourUserNameHere", # database username
        passwd="YourPasswordHere", # database password
        database="YourDataBaseNameHere"
    )

    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM credentials WHERE username = '{username}'")
    matches = cursor.fetchall()
    # print(matches)
    returnedlen = len(matches)

    if returnedlen == 0:
        pass
    else:
        response = login(matches, username, password)
        return response
