import os
import sqlite3
import pandas as pd 


# Connect to the sqlite3 database
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")
conn = sqlite3.connect(DB_FILEPATH)
curs = conn.cursor()

def askme(query):
    r = curs.execute(query).fetchall()
    r = r[0]
    return r
print()


# - How many total Characters are there?
q1 = """SELECT
            count(distinct character_id)
        FROM
            charactercreator_character;"""
r1 = askme(q1)


#  - How many of each specific subclass?
# CLERICS:
q2 = """SELECT
            count(distinct character_ptr_id)
        FROM
            charactercreator_cleric;"""

r2 = askme(q2)


# FIGHTERS:
q3 = """SELECT
            count(distinct character_ptr_id)
        FROM
            charactercreator_fighter;"""
r3 = askme(q3)


# MAGE:
q4 = """SELECT
            count(distinct character_ptr_id)
        FROM
            charactercreator_mage;"""
r4 = askme(q4)


# NECROMANCER:
q5 = """SELECT
            count(distinct mage_ptr_id)
        FROM
            charactercreator_necromancer;"""
r5 = askme(q5)


# THIEF:
q6 = """SELECT
            count(distinct character_ptr_id)
        FROM
            charactercreator_thief;"""
r6 = askme(q6)

# - How many total Items?
q7 = """SELECT
            count(distinct item_id)
        FROM
            armory_item;"""
r7 = askme(q7)


# - How many of the Items are weapons? How many are not?
q8a = """SELECT
            count(distinct item_ptr_id)
        FROM
            armory_weapon;"""
r8a = askme(q8a)


# - How many of the Items are weapons? How many are not?
q8b = """SELECT
            count(distinct item_id)
        FROM
            armory_item
        WHERE item_id < 138;"""
r8b = askme(q8b)



t1 = "Total number of   characters are: "
t2 = "Total number of      clerics are: "
t3 = "Total number of     fighters are: "
t4 = "Total number of        mages are: "
t5 = "Total number of necromancers are: "
t6 = "Total number of      thieves are: "
t7 = "Total number           items are: "
t8a = "Total number of      weapons are: "
t8b = "Total number of  non-weapons are: "

print(t1, r1[0])
print(t2, r2[0])
print(t3, r3[0])
print(t4, r4[0])
print(t5, r5[0])
print(t6, r6[0])
print(t7, r7[0])
print(t8a, r8a[0])
print(t8b, r8b[0])
print()


# How many Items does each character have? (Return first 20 rows)
t9 = "Items carried by each character: "
q9 = """
    SELECT name as Name
    ,item_id as ID
    ,COUNT(item_id) as Weapons
    FROM charactercreator_character c, charactercreator_character_inventory i
    WHERE c.character_id = i.character_id
    GROUP BY c.character_id;"""
r9 = curs.execute(q9).fetchmany(20)
print(t9)
print(r9)
df = pd.DataFrame(r9, columns={"Character","ID", "Items"})
print(df)
print()


# How many Weapons does each character have? (Return first 20 rows)
t9 = "Items carried by each character: "
q9 = """
    SELECT name as Name
    ,item_id as ID
    ,COUNT(item_id) as Weapons
    FROM charactercreator_character c, charactercreator_character_inventory i
    WHERE c.character_id = i.character_id
    AND item_id > 137
    GROUP BY c.character_id;"""
r9 = curs.execute(q9).fetchmany(20)
print(t9)
print(r9)
df = pd.DataFrame(r9, columns={"Character","ID", "Items"})
print(df)


# - On average, how many Items does each Character have?
q11 = """
SELECT
    count(DISTINCT item_id)
FROM
    charactercreator_character_inventory
Group BY
    character_id;"""
r11 = askme(q11)


# - On average, how many Weapons does each character have?
q12 = """
SELECT
    count(DISTINCT item_id)
FROM
    charactercreator_character_inventory
WHERE
    item_id > 137
Group BY
    character_id;"""
r12 = askme(q12)


t11 = "The average # of   items per character carries is: "
t12 = "The average # of weapons per character carries is: "
print()
print(t11, r11[0])
print(t12, r12[0])

# Tidy up
curs.close()
conn.close()