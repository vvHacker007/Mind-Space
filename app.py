from flask import Flask,redirect,request,url_for,jsonify,session,render_template,flash
import pymongo as pm
import datetime
from dateutil.relativedelta import relativedelta, MO
import phonenumbers
import pytz

app = Flask(__name__)
client = pm.MongoClient("mongodb+srv://Blogger:vedv2002@cluster0.krw6c.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.Blogs
login_col = db.Login
data = None
name=None
phone=None

ist = pytz.timezone('Asia/Kolkata')

@app.route('/')
def redirect_to_home():
    return render_template("home.html")

@app.route('/login/',methods=["POST","GET"])
def login():
    if request.method == "POST":
        user_name = request.form["user_name"]
        password = request.form["pass"]
        if login_col.find_one({'User Name': user_name,'Password': password}):
            return redirect(url_for("user", name_u = user_name))
        else:
            if (login_col.find_one({'User Name': user_name})):
                flash(f"Invalid Password!")
            else:
                flash(f"Enter a valid Username!")
            return render_template("login_2.html")
    else:
        return render_template("login_2.html")
    
@app.route('/forgot_password/',methods=["POST","GET"])
def forgot_pass():
    return render_template("forgot_password.html")

@app.route('/signup/',methods=["POST","GET"])
def signup():
    if request.method == "POST":
        user_name = request.form["username"]
        email = request.form["emailid"]
        phone = request.form["phone"]
        password = request.form["pass"]
        check_password = request.form["confirm_pass"]
        birthdate = request.form["birthdate"]
        y,m,d = birthdate.split("-")
        
        if (login_col.find_one({'User Name': user_name})):
            flash(f"Username already exists")
            return render_template("signup.html")
        
        if(password!=check_password):
            flash(f"Password doesn't match!")
            return render_template("signup.html")
        
        if (login_col.find_one({'Email': email})):
            flash(f"Account with same Email-id already exists!")
            return render_template("signup.html")
        
        name = user_name

        date_today = str(datetime.date.today())
        ty,tm,td = date_today.split("-")
        date1 = datetime.datetime(int(y),int(m),int(d))
        date2 = datetime.datetime(int(ty),int(tm),int(td))
        years = relativedelta(date2,date1).years

        mydict = {"Name":name,"User Name":user_name,"Email":email,"Password":password,"Age":years,"Phone":phone}
        login_col.insert_one(mydict)
        return render_template("login_2.html")
    else:
        return render_template("signup.html")
        

@app.route('/<name_u>/')
def user(name_u):
    return render_template("user_home.html", name_u=name_u)

if __name__ == '__main__':
    app.secret_key = "hsagfgfahg"
    app.jinja_env.auto_reload = True
    app.run(debug=True)