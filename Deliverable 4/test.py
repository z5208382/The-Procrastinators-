import json
import sys
import psycopg2
db = None

try:
    db = psycopg2.connect("dbname=seng2021")
    db.autocommit = True
    cursor = db.cursor()
    with open("events.json") as f: 
        events = json.load(f)
        for event in events:
            id = (event["id"])
            title = (event["title"])
            start = (event["time_start"])
            finish = (event["time_finish"])
            description = (event["description"])
            location = (event["location"])
            eventImage = (event["image_url"])
            try: 
              cursor.execute("INSERT INTO Events(id, eventTitle, startDate, endDate, description, location, eventImage) VALUES(%s, %s, %s, %s, %s, %s, %s)",(id,title,start,finish,description, location, eventImage))
            except psycopg2.IntegrityError:
              db.rollback()
            else:
              db.commit()

    with open("societies.json") as g: 
        societies = json.load(g)
        for society in societies: 
            id = (society["id"])
            name = (society["name"])
            description = (society["description"])
            societyImage = (society["image_url"])
            uni = (society["uni"])
            try: 
              cursor.execute("INSERT INTO Societies(id, uni, name, description, societyImage) VALUES(%s, %s, %s, %s, %s)",(id, uni, name, description, societyImage))
            except psycopg2.IntegrityError:
              db.rollback()
            else:
              db.commit()

except psycopg2.Error as err:
  print("DB error: ", err)
finally:
  if db:
    db.close()