from flask import Flask
import sqlite3

app=Flask(__name__)
app.secret_key = "mysecret123"

#database connection
conn = sqlite3.connect("database.db", timeout=10)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS student(id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, phone TEXT, resume TEXT, status TEXT );")
cur.execute("CREATE TABLE IF NOT EXISTS company(id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, hr_contact TEXT, website TEXT, approval_status TEXT, status TEXT );")
cur.execute("CREATE TABLE IF NOT EXISTS drive(id INTEGER PRIMARY KEY, company_id INTEGER, job_title TEXT, description TEXT, eligibility TEXT, deadline TEXT, status TEXT );")
cur.execute("CREATE TABLE IF NOT EXISTS application(id INTEGER PRIMARY KEY, student_id INTEGER, drive_id INTEGER, application_date TEXT, status TEXT );")
cur.execute("CREATE TABLE IF NOT EXISTS placement(id INTEGER PRIMARY KEY,application_id INTEGER,placement_status TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS admin(id INTEGER PRIMARY KEY,email TEXT UNIQUE,password TEXT)")


conn.commit()
conn.close()
