from flask import Flask,redirect,request,url_for,jsonify,session,render_template,flash,make_response,g
import pymongo as pm
import datetime
from dateutil.relativedelta import relativedelta, MO
import phonenumbers
import pytz
import os
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
from functools import wraps
from forms import RegistrationForm, LoginForm, PostForm, OTPForm, ForgotPassForm, ResetPassForm
from flask_wtf import FlaskForm
import uuid
import time
from dateutil.relativedelta import relativedelta, MO
# from profanityfilter import ProfanityFilter
# pf = ProfanityFilter()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
client = pm.MongoClient(os.getenv('MONGO_CLIENT'))
db = client.Blogs

from user.models import User




# def calling_func():
# 	return "HELLO"

# @app.context_processor
# def context_processor():
# 	return dict(key='value',some_func_key=calling_func) //using this i can use the variables key and some_func() in any jinja templates to access the variables

#tutorial
posts = [
    {
        'author':'Author1',
        'title':'Blog 1',
        'content':'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos sit dolorum similique, unde consequatur repudiandae iusto laborum at nihil quasi non excepturi veritatis impedit tenetur vero nesciunt rem explicabo doloremque.',
        'date_posted':'April 07, 2021'
    },
    {
        'author':'Author2',
        'title':'Blog 2',
        'content':'Blog Content 2',
        'date_posted':'April 09, 2021'
    },
    {
        'author':'Author2',
        'title':'Blog 2',
        'content':'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos sit dolorum similique, unde consequatur repudiandae iusto laborum at nihil quasi non excepturi veritatis impedit tenetur vero nesciunt rem explicabo doloremque.',
        'date_posted':'April 09, 2021'
    },
    {
        'author':'Author2',
        'title':'Blog 2',
        'content':'Blog Content 2',
        'date_posted':'April 09, 2021'
    },
    {
        'author':'Author2',
        'title':'Blog 2',
        'content':'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos sit dolorum similique, unde consequatur repudiandae iusto laborum at nihil quasi non excepturi veritatis impedit tenetur vero nesciunt rem explicabo doloremque.',
        'date_posted':'April 09, 2021'
    },
    {
        'author':'Author2',
        'title':'Blog 2',
        'content':'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos sit dolorum similique, unde consequatur repudiandae iusto laborum at nihil quasi non excepturi veritatis impedit tenetur vero nesciunt rem explicabo doloremque.',
        'date_posted':'April 09, 2021'
    },
    {
        'author':'Author2',
        'title':'Blog 2',
        'content':'Blog Content 2',
        'date_posted':'April 09, 2021'
    },
]

ist = pytz.timezone('Asia/Kolkata')

@app.route('/')
def redirect_to_home():
    if 'user' in session:
        return redirect(url_for('user_home',user=session['user']['name']))
    return render_template("home.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if 'user' in session or 'otp' in session:
        session.clear()
        print("REACHED THE POINT")
    if form.validate_on_submit():
        resp = None
        print("REACHED THE POINT BEYOND")
        print(db.Login.find_one({'name': form.email.data}))
        if db.Login.find_one({'name': form.email.data}):
            resp = User().login(form,1)
        elif db.Login.find_one({'email': form.email.data}):
            resp = User().login(form,0)
        print("RESP IS",resp)
        if resp=="success":
            print("REACHED SUCCESS MAIN")
            name_user = str(session['user']['name'])
            print(name_user)
            return redirect(url_for('user_home',user=name_user))
        else:
            flash(f"Invalid login credentials","danger")    
    return render_template('login.html', title='MindSpace-Login', form=form)

@app.route('/signup/',methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    if 'user' in session:
        session.clear()
    if form.validate_on_submit() == False:
        if form.email.errors:
            for i in form.email.errors:
                flash(i,'danger')
        elif form.phone.errors:
            flash(f'Please enter a valid phone number','danger')
    if form.validate_on_submit():
        y,m,d = str(form.birthdate.data).split("-")
        date_today = str(datetime.date.today())
        ty,tm,td = date_today.split("-")
        date1 = datetime.datetime(int(y),int(m),int(d))
        date2 = datetime.datetime(int(ty),int(tm),int(td))
        years = relativedelta(date2,date1).years

        resp2 = User().signup(form)
        # print("THIS IS IMPORTANT!!!!!!!")
        # print(resp2)
        if resp2=="success":
            return redirect(url_for("otp_verify"))
            # if db.Login.insert_one(session["user_signup"]):
            #     print("PASSSED2")
            # flash(f'Account created successfully!', 'success')
            # return redirect(url_for('login'))
        elif resp2=="failed_otp":
            flash(f"Please enter the valid email address OR check your internet connection!","danger")
            return render_template('signup.html', title='MindSpace-Signup', form=form)        
        else:
            # print("THIS IS VERY IMPORTANT!!!!")
            flash(resp2,'danger')
            return render_template('signup.html', title='MindSpace-Signup', form=form)
    return render_template('signup.html', title='MindSpace-Signup', form=form)

@app.route('/<user>/home')
def user_home(user):
    if session['user']['name']==user:
        return render_template("user_home.html",posts=posts,user=user) #user['name'] not working for signin session
    elif 'user' in session and session['user']['name']!=user:
        return redirect(url_for('user_home',user=session['user']['name']))
    else:
        session.clear()
        return redirect(url_for('login'))


@app.route('/logout/') # logout completed
def logout():
    if 'user' in session:
        session.clear()
    return redirect(url_for('login'))


@app.route('/<user>/write/',methods=['GET','POST'])
def user_write(user):
    if session['user']['name']==user:
        form = PostForm()
        if form.validate_on_submit():
            print(form.content.data)
            print(form.title.data)
            print(form.submit.data)
            print(form.save.data)
            if form.submit.data == True:
                resp = User().create_post(form,user)
                if resp == "success":
                    flash("Congrats @"+session['user']['name']+", your blog has been posted successfully!!")
                    return render_template('message.html',user=user)
                else:
                    User().save_post(form,user)
                    flash("Due to some issues the blog wasn't posted. But we have saved the content on your timeline. You can check that using on your profile")
                    return render_template('message.html',user=user)
            elif form.save.data == True:
                User().save_post(form,user)
                flash("@"+session['user']['name']+" your blogs has been saved on your timeline successfully")
                return render_template('message.html',user=user)
        return render_template("write_post.html",user=user,form=form,title="Write")
    elif 'user' in session and session['user']['name']!=user:
        return redirect(url_for('user_write',user=session['user']['name']))
    else:
        session.clear()
        return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']


@app.route("/<user>/profile/")
def user_profile(user):
    user_posts = db.Posts.find({"name" : user})
    return render_template("profile.html",user=user,posts=user_posts)

@app.route("/forgot-password/",methods=['GET','POST'])
def forgot_password():
    form = ForgotPassForm()
    print("REACHER HERE 999")
    if 'user' in session or 'otp' in session:
        session.clear()
        print("REACHED THE POINT")
    if form.validate_on_submit():
        resp = None
        print("REACHED THE POINT BEYOND")
        print(db.Login.find_one({'name': form.email_id.data}))
        if db.Login.find_one({'email': form.email_id.data}):
            resp = User().forgot_pass(form)
        print("RESP IS",resp)
        if resp=="success":
            return redirect(url_for('otp_verify'))
        else:
            flash(f"Please enter a valid email address","danger")    
    return render_template("forgot_password.html",title='MindSpace-Forgot Password', form=form)

@app.route("/verification/",methods=['GET','POST'])
def otp_verify():
    form = OTPForm()
    if 'otp' not in session:
        return redirect(url_for('signup'))
    print("OTP Verification Needed!")
    if 'otp' in session and 'user_signup' in session and form.validate_on_submit():
        print("OTP Verification 1")
        print(form.otp.data)
        print(form.submit.data)
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
            if db.Login.insert_one(session["user_signup"]):
                session.pop('user_signup',None)
                print("PASSSED2")
                flash(f'Account created successfully!', 'success')
                return redirect(url_for('login'))
        else:
            session.clear()
            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return redirect(url_for('signup'))
        session.clear()
    if 'otp' in session and 'user_signup' not in session and form.validate_on_submit():
        print("OTP Verification 1")
        print(form.otp.data)
        print(form.submit.data)
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
            return redirect(url_for('reset_pass'))
    return render_template("otp_verification.html", title='MindSpace-Verification',form=form)


@app.route('/reset-password/',methods=['GET','POST'])
def reset_pass():
    form = ResetPassForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_pass.data:
            flash(f"Password doesn't match!","danger")
        elif len(form.password.data)<5 and len(form.confirm_pass.data)<5:
            flash(f"Password too small!","danger")
        elif len(form.password.data)>20 and len(form.confirm_pass.data)>20:
            flash(f"Password too long!","danger")
        else:
            user = db.Login.find_one(session["email"])
            form.password.data = pbkdf2_sha256.encrypt(form.password.data)
            db.Login.update_one({"email":session["email"]},{"$set":{"password":form.password.data}})
            session.pop('user_signup',None)
            print("PASSSED2")
            flash(f'Password changed successfully!', 'success')
            return redirect(url_for('login'))
    return render_template("reset_password.html", title='MindSpace-Reset Password',form=form)
















# if __name__ == '__main__':
#     app.secret_key = "only20dollarsinmypocket"
#     app.jinja_env.auto_reload = True
#     app.run(debug=True)


# @app.route('/<name_u>/')
# def user(name_u):
#     return render_template("user_home.html", name_u=name_u)



# class data_handling:
#     #GET
#     def __get_data(self):
#         return "youcantseemeget"
#     def get_data(self):
#         self.__get_data_handling()
#     def __get_data_handling(self):
#         self.__get_data()
    
#     #POST
#     def __post_data(self):
#         return "youcantseemepost"
#     def post_data(self):
#         self.__post_data_handling()
#     def __post_data_handling(self):
#         self.__get_data()

# @app.route('/login/',methods=["POST","GET"])
# def login():
#     if request.method == "POST":
#         user_name = request.form["user_name"]
#         password = request.form["pass"]
#         if db.Login.find_one({'name': user_name,'Password': password}):
#             return redirect(url_for("user", name_u = user_name))
#         else:
#             if (db.Login.find_one({'name': user_name})):
#                 flash(f"Invalid Password!")
#             else:
#                 flash(f"Enter a valid Username!")
#             return render_template("login.html")
#     else:
#         return render_template("login.html")
    
# @app.route('/forgot_password/',methods=["POST","GET"])
# def forgot_pass():
#     return render_template("forgot_password.html")


# @app.route('/signup/',methods=["POST","GET"])
# def signup():
#     if request.method == "POST":
#         user_name = request.form["username"]
#         email = request.form["emailid"]
#         phone = request.form["phone"]
#         password = request.form["pass"]
#         check_password = request.form["confirm_pass"]
#         birthdate = request.form["birthdate"]
#         y,m,d = birthdate.split("-")
        
#         if (db.Login.find_one({'name': user_name})):
#             flash(f"Username already exists")
#             return render_template("signup.html")
        
#         if(password!=check_password):
#             flash(f"Password doesn't match!")
#             return render_template("signup.html")
        
#         if (db.Login.find_one({'email': email})):
#             flash(f"Account with same Email-id already exists!")
#             return render_template("signup.html")
        
#         name = user_name

#         date_today = str(datetime.date.today())
#         ty,tm,td = date_today.split("-")
#         date1 = datetime.datetime(int(y),int(m),int(d))
#         date2 = datetime.datetime(int(ty),int(tm),int(td))
#         years = relativedelta(date2,date1).years

#         mydict = {"Name":name,"User Name":user_name,"Email":email,"Password":password,"Age":years,"Phone":phone}
#         db.Login.insert_one(mydict)
#         return render_template("login.html")
#     else:
#         return render_template("signup.html")

