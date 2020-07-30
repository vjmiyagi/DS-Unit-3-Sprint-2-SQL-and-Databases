import os
import sqlite3
import pandas as pd 
from sqlalchemy import create_engine

# Read csv into pandas DataFrame
df = pd.read_csv('buddymove_holidayiq.csv')
print(df.shape)
print(df.head())
df.rename(columns={"User Id":"UserID"}, inplace=True)
print(df.head())


# Create a connection to sqlite DB

conn = sqlite3.connect("buddy.db")
curs = conn.cursor()



query = """CREATE TABLE IF NOT EXISTS users (UserID text, Sports number, 
            Religious number, Nature number,
            Theatre number, Shopping number,
            Picnic number)"""
curs.execute(query)
conn.commit()

df.to_sql('users', conn, if_exists='replace', index = False)

query = """
        SELECT
            count(distinct UserID)
        FROM
            users;"""
result = curs.execute(query)
conn.commit()
print(result)

# Function for queries
def askme(query):
    r = curs.execute(query).fetchall()
    r = r[0]
    return r
print()


# Get row count from new sqlite3 table
t1 = "Table rows number: "
q1 = """
        SELECT
            count(distinct UserID)
        FROM
            users;"""
r1 = askme(q1)
conn.commit()
print(t1, r1[0])

''' How many users who reviewed at least 100 Nature 
    in the category also reviewed at least 100 in the 
    Shopping category?'''

t2 = "Users that reviewed at least 100 Nature and Shopping: "
q2 = """
        SELECT
            count(distinct UserID)
        FROM
            users
        WHERE Nature > 99
        AND Shopping > 99;"""
r2 = askme(q2)
print(t2, r2[0])


t3 = "Genre averages are: "
q3 = """
        SELECT
            round(AVG(Sports),2) as Sports
            ,round(AVG(Religious),2) as Religious
            ,round(AVG(Nature),2) as Nature
            ,round(AVG(Theatre),2) as Theatre
            ,round(AVG(Shopping),2) as Shopping
            ,round(AVG(Picnic),2) as Picnic
        FROM
            users;"""
r3 = curs.execute(q3).fetchall()
r3 = r3[0]
print()
print("Average reviews per category:")
print("Sports:                ", r3[0])
print("Religious:            ", r3[1])
print("Nature                ", r3[2])
print("Theatre               ", r3[3])
print("Shopping              ", r3[4])
print("Picnic                ", r3[5])


# Tidy up
curs.close()
conn.close()