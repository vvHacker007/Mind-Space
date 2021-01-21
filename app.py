from flask import Flask,redirect,request,url_for,jsonify,session,render_template
import pymongo as pm

app = Flask(__name__)

client = pm.MongoClient("mongodb+srv://Blogger:vedv2002@cluster0.krw6c.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.Blogs
login_col = db.Login
data = None

@app.route('/')
def redirect_to_login():
    return redirect(url_for("login"))
@app.route('/login/',methods=["POST","GET"])
def login():
    if request.method == "POST":
        check_email = request.form["id"]
        check_password = request.form["pass"]
        data = login_col.find_one({ "Email": check_email, "Password": check_password })
        if(data != None):
            return redirect(url_for("user"))
        else:
            return render_template("signup.html")
    else:
        return render_template("login.html")

@app.route('/signup/',methods=["POST","GET"])
def signup():
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
        return render_template("signup.html")
        

@app.route('/user/')
def user():
    return render_template("user.html")




if __name__ == '__main__':
    app.run(debug=True)