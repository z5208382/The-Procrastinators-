import json
import sys
import psycopg2

db = None

def getEvents(): 
    try:
        db = psycopg2.connect("dbname=seng2021")
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute("Select * From Events where id = 2979283185636941")
        return cursor.fetchall()
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def getSocieties(): 
    try:
        db = psycopg2.connect("dbname=seng2021")
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute("Select * From Societies")
        return cursor.fetchall()
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def getSociety(societyID):
    try:
        db = psycopg2.connect("dbname=seng2021")
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute("Select * From Societies where id = %s", (societyID,))
        return cursor.fetchall()
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close() 

#instead of user can probably use a token instead. 
def getProfile(userID): 
    try:
        db = psycopg2.connect("dbname=seng2021")
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute("Select * From Profile where id = %s", (userID,))
        return cursor.fetchall()
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()

def getFilterEvents(filter):
    try:
        db = psycopg2.connect("dbname=seng2021")
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute("Select eventId from EventCategories where categoryId = %s ", (filter,))
        return cursor.fetchall()
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close()