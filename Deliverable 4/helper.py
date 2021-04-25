import json
import sys
import psycopg2
import itertools

db = None

def getEvents(): 
    try:
        db = psycopg2.connect("dbname=seng2021")
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute("Select * From events where id = 2979283185636941")
        db.close()
        rows = cursor.fetchall()
        results = [{'id': col1, 'title': col2, 'time_start': col3, 'time_finish': col4, 'description': col5, 
                    'location': col6, 'host': col7, 'image_url': col8, 'category': col9, } 
                    for (col1, col2, col3, col4, col5, col6, col7, col8, col9) in rows]
        return results
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
        cursor.execute("Select * From societies")
        rows = cursor.fetchall()
        results = [{'id': col1, 'uni': col2, 'name': col3, 'description': col4, 'image_url': col5} for (col1, col2, col3, col4, col5) in rows]
        return results
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
        cursor.execute("Select * From societies where id = %s", (societyID,))
        rows = cursor.fetchall()
        results = [{'id': col1, 'uni': col2, 'name': col3, 'description': col4, 'image_url': col5} for (col1, col2, col3, col4, col5) in rows]
        return results
    except psycopg2.Error as err:
        print("DB error: ", err)
    finally:
        if db:
            db.close() 

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