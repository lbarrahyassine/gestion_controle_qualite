#import mysql.connector
from connexion import *
from mysql.connector import Error


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            print(result)
    except Error as e:
        print(f"The error '{e}' occurred")
        return results

"""ajout_cat ="INSERT INTO categorie (id_cat, libele) VALUES (1, 'voitures');"
execute_query(connection, ajout_cat)"""
def show_tables():
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(table)

def fetch_categories():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Categorie")
    categories = cursor.fetchall()
    cursor.close()
    for category in categories:
        print(category)
    return categories

def fetch_sous_categories():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Sous_Categorie")
    sous_categories = cursor.fetchall()
    cursor.close()
    for sous_cat in categories:
        print(sous_cat)
    return sous_categories

def fetch_equipements():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Equipement")
    equipements = cursor.fetchall()
    cursor.close()
    for equip in equipements:
        print(equip)
    return equipements

#print(execute_read_query(connection,"SELECT * FROM sous_Categorie"))

fetch_categories()
print(fetch_sous_categories())