from flask import Flask,render_template,request,session,redirect
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

#Admin

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/admin_login.html')




#Companies

@app.route('/company/register', methods=["GET","POST"])
def company_register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        hr_contact = request.form["hr_contact"]
        website = request.form["website"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        
        cur.execute("SELECT * FROM company WHERE email=?", (email,))
        existing = cur.fetchone()

        if existing:
            conn.close()
            return """This email is already registered.<br><br>Please use another email.<br><br><a href="/company/register">Back</a>"""

        cur.execute("INSERT INTO company(name,email,password,hr_contact,website,status) VALUES(?,?,?,?,?,?)",(name,email,password,hr_contact,website,"Pending"))

        conn.commit()
        conn.close()

        return """Registration successful.<br><br>Admin approval pending.<br><br>After admin approval you can login.<br><br><a href="/company/login">Go to Login</a>"""

    return render_template('company/company_register.html')
    


@app.route('/company/login',methods=["GET","POST"])
def company_login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        conn=sqlite3.connect("database.db")
        cur=conn.cursor()

        cur.execute("SELECT * FROM company WHERE email=? AND password=?", (email,password))
        company=cur.fetchone()

        conn.close()

        if company:

            if company[7] == "Pending":
                return """
                Your company registration is waiting for admin approval.<br><br>
                <a href="/company/login">Back</a>
                """

            if company[7] == "Rejected":
                return """
                Your company registration has been rejected by admin.<br><br>
                <a href="/company/login">Back</a>
                """
            
            if company[7] == "Deleted":
                return """
                Your company account has been deleted by admin.<br><br>
                <a href="/company/login">Back</a>
                """

            session["company_id"]=company[0]
            return redirect('/company/dashboard')

        else:
            return """
            Incorrect username or password.<br><br>
            <a href="/company/login">Try Again</a>
            """

    return render_template('company/company_login.html')



#student

@app.route('/student/login',methods=["GET","POST"])
def student_login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        conn=sqlite3.connect("database.db")
        cur=conn.cursor()

        cur.execute("SELECT * FROM student WHERE email=? AND password=?", (email,password))
        student=cur.fetchone()

        conn.close()

        if student:

            if student[6] == "Pending":
                return "Waiting for admin approval"

            if student[6] == "Rejected":
                return "Your registration rejected"

            if student[6] == "Deleted":
                return "Your account deleted by admin"

            session["student_id"]=student[0]
            return redirect('/student/dashboard')
        else:
            return """
            Incorrect email or password.<br><br>
            <a href="/student/login">Try Again</a>
            """

    return render_template('students/student_login.html')

@app.route('/student/registers', methods=["GET","POST"])
def student_register():

    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        phone=request.form["phone"]
        resume=request.form["resume"]

        conn=sqlite3.connect("database.db")
        cur=conn.cursor()

        cur.execute(
        "INSERT INTO student(name,email,password,phone,resume,status) VALUES(?,?,?,?,?,?)",
        (name,email,password,phone,resume,"Pending")
        )

        conn.commit()
        conn.close()

        return """
        Registration Successful.<br><br>
        Admin approval pending.<br>
        After admin approval you can login.<br><br>
        <a href="/student/login">Go to Login</a>
        """

    return render_template('students/student_register.html')


if __name__=='__main__':
    app.run(debug=True)
