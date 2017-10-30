from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import User, Job
from flask_bcrypt import generate_password_hash, check_password_hash
# pip install
app = Flask(__name__)

app.secret_key = "jshikjduyfdfgsghfsrefatklaeueegegg"


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        names = request.form["names"]
        email = request.form["email"]
        password = request.form["password"]
        password=generate_password_hash(password)
        print(names, email, password)
        User.create(names=names, email=email, password=password)
        flash("Account created successfully")

    return render_template('registration.html')


@app.route('/', methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('display'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = User.get(User.email==email)
            hashed_password = user.password
            if check_password_hash(hashed_password, password):
                flash("Logged in Successfully")
                session['logged_in']=True
                session['names']=user.names
                session['id']=user.id
                return redirect(url_for('display'))
        except User.DoesNotExist:
            flash("Wrong username or password")

    return render_template('login.html')

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id=session['id']
    Job.delete().where(Job.id==id, Job.owner == owner_id).execute()
    flash("Task Deleted Successfully")
    return render_template('display.html')


@app.route('/update/<int:id>')
def update(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id=session['id']
    if id>0:
        Job.update(status="Complete").where(Job.id==id, Job.owner == owner_id).execute()
        flash("Task Updated Successfully")
        return  redirect(url_for("display"))
    return render_template('display.html')

@app.route('/add', methods=['GET','POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id = session['id']
    if request.method =="POST":
        task = request.form["task"]
        Job.create(task=task, owner=owner_id)
        flash("Task added successfully")

    return render_template("add.html")


@app.route('/display')
def display():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    jobs = Job.select().where(Job.owner==id)
    print(jobs)
    return render_template('display.html', jobs=jobs)


if __name__ == '__main__':
    app.run(debug=True)
