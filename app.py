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

@app.route('/admin/dashboard', methods=["GET","POST"])
def admin_dashboard():

    email="abc@gmail.com"
    password="123"

    if request.method=="POST":

        if email==request.form["email"] and password==request.form["password"]:

            session["admin"] = "admin"

        else:
            return 'incorrect password or username. click <a href="/admin/login">here</a> to go back'

    if "admin" not in session:
        return redirect("/admin/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM student")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM company")
    total_companies = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM drive")
    total_drives = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM application")
    total_applications = cur.fetchone()[0]

    conn.close()

    return render_template(
        "admin/admin_dashboard.html",
        total_students=total_students,
        total_companies=total_companies,
        total_drives=total_drives,
        total_applications=total_applications
    )

@app.route('/admin/manages')
def manage_students():

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("SELECT * FROM student WHERE status!='Deleted'")
    students = cur.fetchall()

    conn.close()

    return render_template('admin/manage_student.html', students=students)

@app.route('/admin/managec')
def manage_companies():

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("SELECT * FROM company WHERE status!='Deleted'")
    companies = cur.fetchall()

    conn.close()

    return render_template('admin/manage_companies.html', companies=companies)

@app.route('/admin/managed')
def manage_drives():

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("SELECT * FROM drive")
    drives = cur.fetchall()

    conn.close()

    return render_template('admin/manage_Drive.html', drives=drives)

@app.route('/admin/view')
def view_application():

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("""
    SELECT student.name, company.name, drive.job_title, application.status
    FROM application
    JOIN student ON application.student_id = student.id
    JOIN drive ON application.drive_id = drive.id
    JOIN company ON drive.company_id = company.id
    """)

    applications = cur.fetchall()

    conn.close()

    return render_template('admin/view_applications.html', applications=applications)

@app.route('/admin/search', methods=["GET"])
def admin_search():

    query = request.args.get("query")

    students = []
    companies = []

    if query:

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM student WHERE name LIKE ?", ('%'+query+'%',))
        students = cur.fetchall()

        cur.execute("SELECT * FROM company WHERE name LIKE ?", ('%'+query+'%',))
        companies = cur.fetchall()

        conn.close()

    return render_template(
        "admin/admin_Search.html",
        students=students,
        companies=companies
    )

@app.route('/admin/approve_company/<int:company_id>')
def approve_company(company_id):

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("UPDATE company SET status='Approved' WHERE id=?", (company_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/managec')

@app.route('/admin/approve_student/<int:student_id>')
def approve_student(student_id):

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("UPDATE student SET status='Approved' WHERE id=?", (student_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/manages')

@app.route('/admin/approve_drive/<int:drive_id>')
def approve_drive(drive_id):

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("UPDATE drive SET status='Approved' WHERE id=?", (drive_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/managed')

@app.route('/admin/reject_student/<int:student_id>')
def reject_student(student_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("UPDATE student SET status='Rejected' WHERE id=?", (student_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/manages')

@app.route('/admin/reject_company/<int:company_id>')
def reject_company(company_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("UPDATE company SET status='Rejected' WHERE id=?", (company_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/managec')

@app.route('/admin/reject_drive/<int:drive_id>')
def reject_drive(drive_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("UPDATE drive SET status='Rejected' WHERE id=?", (drive_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/managed')

@app.route('/admin/delete_student/<int:student_id>')
def delete_student(student_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("UPDATE student SET status='Deleted' WHERE id=?", (student_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/manages')

@app.route('/admin/delete_company/<int:company_id>')
def delete_company(company_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("UPDATE company SET status='Deleted' WHERE id=?", (company_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/managec')

@app.route('/admin/delete_drive/<int:drive_id>')
def delete_drive(drive_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM drive WHERE id=?", (drive_id,))

    conn.commit()
    conn.close()

    return redirect('/admin/managed')


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

@app.route('/company/dashboard',methods=["GET","POST"])
def company_dashboard ():
    company_id = session["company_id"]

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("SELECT * FROM company WHERE id=?", (company_id,))
    company = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM drive WHERE company_id=?", (company_id,))
    total_drives = cur.fetchone()[0]

    conn.close()
    #email="abc@gmail.com"
    #password="123"
    #if email==request.form["email"] and password==request.form["password"]:
    return render_template('company/company_dashboard.html', company_name=company[1], total_drives=total_drives)
    #else:
     #   return 'incorrect password or username. click <a href="/company/login">here</a> to go back'
        


@app.route('/company/createdrive',methods=["GET","POST"])
def create_drive ():
    if request.method=="POST":
        job_title=request.form["job_title"]
        description=request.form["description"]
        eligibility=request.form["eligibility"]
        deadline=request.form["deadline"]

        company_id = session["company_id"]

        conn=sqlite3.connect("database.db", timeout=10)
        cur=conn.cursor()
        cur.execute( "INSERT INTO drive(company_id,job_title,description,eligibility,deadline,status) VALUES(?,?,?,?,?,?)", (company_id,job_title,description,eligibility,deadline,"Pending")
)
        conn.commit()
        conn.close()
        return 'Your Drive created successfully. please, click <a href="/company/dashboard">here</a> to go your dashboard.'
        
    return render_template('company/create_drive.html')

@app.route('/company/managedrive')
def company_manage_drives():
    company_id=session["company_id"]
    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("SELECT * FROM drive WHERE company_id=?", (company_id)) 
    drives = cur.fetchall()
    conn.close()

    return render_template("company/manage_drives.html", drives=drives)


@app.route('/company/view')
def view_applications():
    company_id = session["company_id"]

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("""
    SELECT application.id, student.name, drive.job_title, application.status
    FROM application
    JOIN student ON application.student_id = student.id
    JOIN drive ON application.drive_id = drive.id
    WHERE drive.company_id = ?
    """, (company_id,))

    applications = cur.fetchall()

    conn.close()
    return render_template('company/view_applications.html', applications=applications)

@app.route('/company/shortlist/<int:app_id>')
def shortlist_student(app_id):

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("UPDATE application SET status=? WHERE id=?", ("Shortlisted", app_id))

    conn.commit()
    conn.close()

    return redirect('/company/view')

@app.route('/company/select/<int:app_id>')
def select_student(app_id):

    conn = sqlite3.connect("database.db", timeout=10)
    cur = conn.cursor()

    cur.execute("UPDATE application SET status=? WHERE id=?", ("Selected", app_id))

    conn.commit()
    conn.close()

    return redirect('/company/view')

@app.route('/company/reject/<int:app_id>')
def company_reject_application(app_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("UPDATE application SET status=? WHERE id=?", ("Rejected", app_id))

    conn.commit()
    conn.close()

    return redirect('/company/view')

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
