from flask import Flask,redirect,request,url_for,jsonify,session,render_template,flash
import pymongo as pm

app = Flask(__name__)
client = pm.MongoClient("mongodb+srv://Blogger:vedv2002@cluster0.krw6c.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.Blogs
login_col = db.Login
data = None

@app.route('/')
def redirect_to_home():
    return render_template("home.html")

@app.route('/login/',methods=["POST","GET"])
def login():
    if request.method == "POST":
        user_name = request.form["user_name"]
        password = request.form["pass"]
        if login_col.find_one({'User Name': user_name}):
            print("Found USER!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for("user", name_u = user_name))
        else:
            print("NOT Found USER!!!!!!!!!!!!!!!!!!!!!!!!")
            flash(f"Login Unsuccessfull")
            return render_template("login.html")
    
    else:
        return render_template("login.html")
    """
    if request.method == "POST":
        check_email = request.form["id"]
        check_password = request.form["pass"]
        data = login_col.find_one({ "Email": check_email, "Password": check_password })
        if(data != None):
            return redirect(url_for("user"))
        else:
            return render_template("signup.html")
    else:
        """
    

@app.route('/signup/',methods=["POST","GET"])
def signup():
    """
    if request.method == "POST":
        name = request.form["name"]
        user_name = request.form["username"]
        email = request.form["id"]
        password = request.form["pass"]
        age = request.form["age"]
        phone = request.form["phone"]
        mydict = {"Name":name,"User Name":user_name,"Email":email,"Password":password,"Age":age,"Phone":phone}
        login_col.insert_one(mydict)
        return render_template("user.html")
    else:
        """
    return render_template("signup.html")
        

@app.route('/<name_u>/')
def user(name_u):
    return render_template("user.html", name_u=name_u)

if __name__ == '__main__':
    app.secret_key = "hsagfgfahg"
    app.run(debug=True)