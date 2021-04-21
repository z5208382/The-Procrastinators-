import json
import sys
import psycopg2
db = None

try:
    db = psycopg2.connect("dbname=seng2021")
    db.autocommit = True
    cursor = db.cursor()
    categories = []
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
            category = (event["categories"][0])
            if(category not in categories):
              categories.append(category)

            try: 
              host = (event["hosts"][0]["id"])
            except: 
              host = None

            try: 
              cursor.execute("INSERT INTO Events(id, eventTitle, startDate, endDate, description, location, eventImage, category, host) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",(id,title,start,finish,description, location, eventImage, category, host))
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

    for category in categories: 
      cursor.execute("Insert into Categories(id) values (%s)", (category,))

except psycopg2.Error as err:
  print("DB error: ", err)
finally:
  if db:
    db.close()