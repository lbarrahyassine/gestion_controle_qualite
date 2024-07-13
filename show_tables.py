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
    #for category in categories:
        #print(category)
    return categories

def fetch_sous_categories():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Sous_Categorie")
    sous_categories = cursor.fetchall()
    cursor.close()
    #for sous_cat in sous_categories:
        #print(sous_cat)
    return sous_categories

def fetch_equipements():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Equipement")
    equipements = cursor.fetchall()
    cursor.close()
    #for equip in equipements:
        #print(equip)
    return equipements

#print(execute_read_query(connection,"SELECT * FROM sous_Categorie"))

#fetch_equipements()
#print(fetch_sous_categories())

def fetch_equipements_combo():
    cursor = connection.cursor()
    cursor.execute("SELECT libele FROM Equipement")
    equipements = cursor.fetchall()
    cursor.close()
    return equipements

def fetch_type_combo():
    cursor = connection.cursor()
    cursor.execute("SELECT libelle FROM type_ctrl")
    types = cursor.fetchall()
    cursor.close()
    return types
def id_type(type):
    cursor = connection.cursor()
    cursor.execute("SELECT id_type FROM type_ctrl where Libelle = \'"+type+"\'")
    #cursor.execute("SELECT id_type FROM type_ctrl WHERE libelle = ?", (type,))
    types = cursor.fetchall()
    cursor.close()
    return types[0][0] if types else None

def id_freq(freq, per):
    cursor = connection.cursor()
    cursor.execute("SELECT id_freq FROM frequence where frequence=\'" + freq +"\'AND periode=\'"+per+"\'")
    #cursor.execute("SELECT id_freq FROM frequence WHERE frequence = ? AND periode = ?", (freq, per))
    types = cursor.fetchall()
    cursor.close()
    return types[0][0]

def id_equip(equip):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM equipement where libele=\'" + equip + "\'")
    equipe = cursor.fetchall()
    cursor.close()
    return equipe[0][0]

def id_org(org):
    cursor = connection.cursor()
    cursor.execute("SELECT id_org FROM organisme where nom=\'" + org + "\'")
    orgs = cursor.fetchall()
    cursor.close()
    return orgs[0][0]

def fetch_frequence_combo():
    cursor = connection.cursor()
    cursor.execute("SELECT frequence, periode FROM frequence")
    freqs = cursor.fetchall()
    cursor.close()
    return freqs

def fetch_frequence2_combo(type):
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT frequence, periode FROM frequence JOIN assoc1 ON frequence.id_freq=assoc1.id_freq WHERE id_type=\'"+type+"\'")
    freqs = cursor.fetchall()
    cursor.close()
    return freqs

def fetch_equipement2_combo(type, freq):
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT libele FROM equipement JOIN assoc1 ON equipement.id=assoc1.id WHERE id_type=\'"+type+"\' AND id_freq=\'"+freq+"\'")
    freqs = cursor.fetchall()
    cursor.close()
    return freqs

def fetch_auditeur():
    cursor = connection.cursor()
    cursor.execute("SELECT nom FROM organisme")
    org = cursor.fetchall()
    cursor.close()
    return org
