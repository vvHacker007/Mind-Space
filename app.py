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
from forms import RegistrationForm, LoginForm, PostForm, OTPForm, ForgotPassForm, ResetPassForm, EditProfileForm
from flask_wtf import FlaskForm
import uuid
import time
from dateutil.relativedelta import relativedelta, MO
from markdownify import markdownify
# from flask_cors import CORS, cross_origin
import cloudinary
import cloudinary.uploader
import json
# import markdown
# from goodreads_quotes import Goodreads
# from profanityfilter import ProfanityFilter
# pf = ProfanityFilter()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
client = pm.MongoClient(os.getenv('MONGO_CLIENT'))
db1 = client.Blogs
# db2 = client.Users Will use this later for login and signup
db3 = client.Cloudinary

from user.models import User




# def calling_func():
# 	return "HELLO"

# @app.context_processor
# def context_processor():
# 	return dict(key='value',some_func_key=calling_func) //using this i can use the variables key and some_func() in any jinja templates to access the variables


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
        print(db1.Login.find_one({'name': form.email.data}))
        if db1.Login.find_one({'name': form.email.data}):
            resp = User().login(form,1)
        elif db1.Login.find_one({'email': form.email.data}):
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
    # user = db1.Login.find_one({"name":user})
    # user_posts = db1.Posts.find_many({"email":user["email"]})
    if session['user']['name']==user:
        posts = db1.Posts.find({})
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
    form = PostForm()
    if session['user']['name']==user:
        if form.validate_on_submit():
            print(form.content.data)
            print(form.title.data)
            print(form.submit.data)
            print(form.save.data)
            if form.submit.data == True:
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = form.file.data
                app.logger.info('%s file_to_upload', img_to_upload)
                if img_to_upload:
                    print("REACHED_HERE first")
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace")
                    app.logger.info(upload_dict_result)
                    print("REACHED_HERE second")
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().create_post(form,user,upload_dict_result)
                else:
                    resp1 = "success"
                    resp2 = User().create_post(form,user,upload_dict_result)
                if resp1=="success" and resp2 == "success":
                    flash("Congrats @"+session['user']['name']+", your blog has been posted successfully!!")
                    return render_template('message.html',user=user)
                else:
                    User().save_post(form,user)
                    flash("Due to some issues the blog wasn't posted. But we have saved the content on your timeline. You can check that using on your profile")
                    return render_template('message.html',user=user)
            elif form.save.data == True:
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = form.file.data
                app.logger.info('%s file_to_upload', img_to_upload)
                if img_to_upload:
                    print("REACHED_HERE first")
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace")
                    app.logger.info(upload_dict_result)
                    print("REACHED_HERE second")
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().save_post(form,user,upload_dict_result)
                else:
                    resp1 = "success"
                    resp2 = User().save_post(form,user)
                if resp1=="success" and resp2 == "success":
                    flash("Congrats @"+session['user']['name']+", your blog has been posted successfully!!")
                    return render_template('message.html',user=user)
                else:
                    flash("Due to some issues the blog wasn't saved. Try again, later")
                    return render_template('message.html',user=user)
        return render_template("write_post.html",user=user,form=form,title="Write")
    elif 'user' in session and session['user']['name']!=user:
        return redirect(url_for('user_write',user=session['user']['name']))
    else:
        session.clear()
        return redirect(url_for('login'))


@app.route("/<user>/profile/",methods=['GET','POST'])
def user_profile(user):
    user_data = db1.Login.find_one({"name":user})
    user_posts = db1.Posts.find({"email" : user_data["email"]})
    # print(Goodreads.get_daily_quote())
    if 'user' in session and user_data['email'] == session['user']["email"]:
        print("REACHED_HERE first")
        saved_user_posts = db1.Saved_posts.find({"email" : session["user"]["email"]})
        app.logger.info('in upload route')
        cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
        upload_result = None
        print("REACHED_HERE 2nd")
        if request.method == 'POST':
            print("REACHED_HERE 3rd")
            file_to_upload = request.files['profile_image']
            app.logger.info('%s file_to_upload', file_to_upload)
            if file_to_upload:
                print("REACHED_HERE fourth")
                upload_result = cloudinary.uploader.upload(file_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace")
                app.logger.info(upload_result)
                print("REACHED_HERE last")
                upload_result["username"] = session['user']['name']
                upload_result["email"] = session['user']['email']
                upload_result["phone"] = session['user']['phone']
                upload_result["_id"] = uuid.uuid4().hex
                resp = User().profile_image_upload(upload_result)
                if resp=="success":
                    flash(session['user']['name']+", your profile picture has been uploaded successfully!!")
                elif resp=="failed":
                    flash(session['user']['name']+", due to some issues your image did not upload, Try again later!")
                return render_template('message.html',user=session['user']['name'])
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!File Not Uploaded!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        return render_template("others_profile.html",user=user_data,posts=user_posts)
    return render_template("profile.html",user=user_data,posts=user_posts,saved_posts=saved_user_posts)


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
        print(db1.Login.find_one({'name': form.email_id.data}))
        if db1.Login.find_one({'email': form.email_id.data}):
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
            if db1.Login.insert_one(session["user_signup"]):
                session.pop('user_signup',None)
                print("PASSSED2")
                flash(f'Account created successfully!', 'success')
                return redirect(url_for('login'))
        else:
            session.clear()
            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return redirect(url_for('signup'))
        session.clear()
    if 'otp' in session and 'user_signup' not in session and 'user_updated_data' not in session and form.validate_on_submit():
        print("OTP Verification 1")
        print(form.otp.data)
        print(form.submit.data)
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
            return redirect(url_for('reset_pass'))
    if 'otp' in session and 'user_signup' not in session and 'user_updated_data' in session and form.validate_on_submit():
        print("OTP Verification 1")
        print(form.otp.data)
        print(form.submit.data)
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
            db1.Login.update_one({"email":session["user"]["email"]},{"$set":session["user_updated_data"] })
            session.clear()
            return redirect(url_for('login'))
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
            user = db1.Login.find_one(session["email"])
            form.password.data = pbkdf2_sha256.encrypt(form.password.data)
            db1.Login.update_one({"email":session["email"]},{"$set":{"password":form.password.data}})
            session.pop('user_signup',None)
            print("PASSSED2")
            flash(f'Password changed successfully!', 'success')
            return redirect(url_for('login'))
    return render_template("reset_password.html", title='MindSpace-Reset Password',form=form)


@app.route('/<user>/edit/',methods=['GET','POST'])
def edit_profile(user):
    if user == session['user']['name']:
        form = EditProfileForm()
        user = db1.Login.find_one({"name":session['user']['name']})
        app.logger.info('in upload route')
        cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
        upload_result = None
        if form.validate_on_submit():
            print("REACHED HERE!")
            user_fullname = form.user_fullname.data
            new_user_email = form.new_email.data
            new_user_phone = form.new_phone.data
            new_user_dob = form.new_birthdate.data
            new_user_name = form.new_username.data
            new_bio = form.new_about_me.data
            new_pass = form.new_password.data
            new_re_pass = form.re_new_password.data
            new_pic = form.file.data
            app.logger.info('%s file_to_upload', new_pic)
            resp1="not_failed"
            resp2="success"
            resp3="failed"
            if new_pic:
                print("REACHED_HERE fourth")
                upload_result = cloudinary.uploader.upload(new_pic, api_secret=os.getenv('API_SECRET'), folder="MindSpace")
                app.logger.info(upload_result)
                print("REACHED_HERE last")
                upload_result["username"] = session['user']['name']
                upload_result["email"] = session['user']['email']
                upload_result["phone"] = session['user']['phone']
                upload_result["_id"] = uuid.uuid4().hex
                resp1 = User().profile_image_upload(upload_result)

            if user_fullname or new_user_email or new_user_phone or new_user_dob or new_user_name or new_bio or new_pass or new_re_pass:
                user_update = {
                        "name":new_user_name,
                        "email":new_user_email,
                        "password":new_pass,
                        "confirm_pass":new_re_pass,
                        "phone":new_user_phone,
                        "birthdate":new_user_dob,
                        "full_name":user_fullname,
                        "bio":new_bio
                    }
                resp2 = User().profile_update(user_update)
                resp3="success"
            if resp2=="success" and resp3=="success":
                return redirect(url_for('otp_verify'))
            elif resp2!="success":
                flash(resp2,'danger')
                return render_template("edit_profile.html",user=user,form=form)
            elif resp1=="failed":
                flash(session['user']['name']+", due to some issues your image did not upload, Try again later!",'danger')
                return render_template("edit_profile.html",user=user,form=form)
            elif resp1=="success":
                flash(session['user']['name']+", your image has been uploaded successfully!",'success')
                return render_template("edit_profile.html",user=user,form=form)
            elif resp1=="not_failed":
                return render_template("edit_profile.html",user=user,form=form)
            return render_template("edit_profile.html",user=user,form=form)
        return render_template("edit_profile.html",user=user,form=form)
    else:
        return redirect(url_for('edit_profile',user=session['user']['name']))

@app.route("/blog/<_id>/")
def user_blog_redirect(_id):
    user_post = db1.Posts.find_one({"_id":_id})
    user = db1.Login.find_one({"name":user_post["name"]})
    if user_post["name"] == session["user"]["name"]:
        return render_template("blog.html",user_post=user_post,user=user)
    elif user_post["name"] != session["user"]["name"]:
        return render_template("others_blog.html",user_post=user_post,user=user)

@app.route("/blog/<_id>/edit/",methods=['GET','POST'])
def edit_blog(_id):
    user_post = db1.Posts.find_one({"_id":_id})
    if user_post["name"] == session["user"]["name"]:
        user_post["blog"] = markdownify(user_post["blog"])
        if request.method == "POST":
            if request.form.get("post_blog"):
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = request.files["blog_file"]
                app.logger.info('%s file_to_upload', img_to_upload)
                user_post["blog"] = request.form["blog_text"]
                user_post["title"] = request.form["title_text"]
                if img_to_upload:
                    print("REACHED_HERE first")
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace")
                    app.logger.info(upload_dict_result)
                    print("REACHED_HERE second")
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    user_post["img"] = upload_dict_result["secure_url"]
                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().edit_post(user_post,upload_dict_result)
                else:
                    resp1 = "success"
                    resp2 = User().edit_post(user_post,upload_dict_result)
                if resp1=="success" and resp2 == "success":
                    flash("Congrats @"+session['user']['name']+", your blog has been posted successfully!!")
                    return render_template('message.html',user=session["user"]["name"])
                else:
                    User().edit_save(user_post,upload_dict_result)
                    flash("Due to some issues the blog wasn't posted. But we have saved the content on your timeline. You can check that using on your profile")
                    return render_template('message.html',user=session["user"]["name"])
            elif request.form.get("save_blog"):
                    app.logger.info('in upload route')
                    cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                    upload_dict_result = None
                    img_to_upload = request.files["blog_file"]
                    app.logger.info('%s file_to_upload', img_to_upload)
                    user_post["blog"] = request.form["blog_text"]
                    user_post["title"] = request.form["title_text"]
                    if img_to_upload:
                        print("REACHED_HERE first")
                        upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace")
                        app.logger.info(upload_dict_result)
                        print("REACHED_HERE second")
                        upload_dict_result["username"] = session['user']['name']
                        upload_dict_result["email"] = session['user']['email']
                        upload_dict_result["phone"] = session['user']['phone']
                        user_post["img"] = upload_dict_result["secure_url"]
                        resp1 = User().blog_image_upload(upload_dict_result)
                        resp2 = User().edit_post(user_post,upload_dict_result)
                    else:
                        resp1 = "success"
                        resp2 = User().edit_save(user_post,upload_dict_result)
                    if resp1=="success" and resp2 == "success":
                        flash("@"+session['user']['name']+" your blogs has been saved on your timeline successfully")
                    return render_template('message.html',user=session["user"]["name"])   
    else:
        return redirect(url_for('user_blog_redirect',_id=user_post["_id"]))
    return render_template("edit_blog.html",user_post=user_post)



@app.route("/blog/<_id>/delete/")
def delete_blog(_id):
    user_post = db1.Posts.find_one({"_id":_id})
    if user_post["name"] == session["user"]["name"]:
        db1.Posts.delete_one({"_id":_id})
        nob = db1.Login.find_one({'name':session['user']['name']})['submitted_blogs']
        if db1.Login.update_many({'name':session['user']['name']},{"$set":{"submitted_blogs": nob-1}}):
            flash(session["user"]["name"]+",your blog has been removed successfully!")
        else:
            flash(session["user"]["name"]+", due to some issues we were not able to remove your blog. Try again later!")
        return render_template("message.html",user=session["user"]["name"])
    else:
        return redirect(url_for('user_blog_redirect',_id=user_post["_id"]))




@app.route("/saved/<_id>/")
def user_saved_blog_redirect(_id):
    user_post = db1.Saved_posts.find_one({"_id":_id})
    user = db1.Login.find_one({"name":user_post["name"]})
    if user_post["name"] == session["user"]["name"]:
        return render_template("saved_blog.html",user_post=user_post,user=user)
    elif user_post["name"] != session["user"]["name"]:
        return redirect(url_for('user_home',user=session["user"]["name"]))


@app.route("/saved/<_id>/edit/",methods=['GET','POST'])
def edit_saved_blog(_id):
    user_post = db1.Saved_posts.find_one({"_id":_id})      
    if user_post["name"] == session["user"]["name"]:
        user_post["blog"] = markdownify(user_post["blog"])
        print("THIS IS THE TITLE",user_post['title'])
        if request.method == "POST":
            if request.form.get("post_blog"):
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = request.files["blog_file"]
                app.logger.info('%s file_to_upload', img_to_upload)
                user_post["blog"] = request.form["blog_text"]
                user_post["title"] = request.form["title_text"]
                if img_to_upload:
                    print("REACHED_HERE first")
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace")
                    app.logger.info(upload_dict_result)
                    print("REACHED_HERE second")
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    user_post["img"] = upload_dict_result["secure_url"]
                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().edit_post(user_post,upload_dict_result)
                else:
                    resp1 = "success"
                    resp2 = User().edit_post(user_post,upload_dict_result)
                if resp1=="success" and resp2 == "success":
                    flash("Congrats @"+session['user']['name']+", your blog has been posted successfully!!")
                    return render_template('message.html',user=session["user"]["name"])
                else:
                    User().edit_save(user_post,upload_dict_result)
                    flash("Due to some issues the blog wasn't posted. But we have saved the content on your timeline. You can check that using on your profile")
                    return render_template('message.html',user=session["user"]["name"])
            elif request.form.get("save_blog"):
                print("REACHED THIS SUCCESSFULLY")
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = request.files["blog_file"]
                app.logger.info('%s file_to_upload', img_to_upload)
                user_post["blog"] = request.form["blog_text"]
                user_post["title"] = request.form["title_text"]
                if img_to_upload:
                    print("REACHED_HERE first")
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace")
                    app.logger.info(upload_dict_result)
                    print("REACHED_HERE second")
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    user_post["img"] = upload_dict_result["secure_url"]
                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().edit_save(user_post,upload_dict_result)
                else:
                    resp1 = "success"
                    resp2 = User().edit_save(user_post)
                if resp1=="success" and resp2 == "success":
                    flash("@"+session['user']['name']+" your blogs has been saved on your timeline successfully")
                else:
                    return render_template("edit_saved_blog.html",user_post=user_post)
                return render_template('message.html',user=session["user"]["name"])  
    else:
        return redirect(url_for('user_home',user=session["user"]["name"]))
    return render_template("edit_saved_blog.html",user_post=user_post)



@app.route("/saved/<_id>/delete/")
def delete_saved_blog(_id):
    user_post = db1.Saved_posts.find_one({"_id":_id})
    print("THIS IS THE BLOG YOU WANT TO DELETE",user_post)
    if user_post["name"] == session["user"]["name"]:
        db1.Saved_posts.delete_one({"_id":_id})
        nob = db1.Login.find_one({'name':session['user']['name']})['submitted_blogs']
        if db1.Login.update_many({'name':session['user']['name']},{"$set":{"submitted_blogs": nob-1}}):
            flash(session["user"]["name"]+",your blog has been removed successfully!")
        else:
            flash(session["user"]["name"]+", due to some issues we were not able to remove your blog. Try again later!")
        return render_template("message.html",user=session["user"]["name"])
    else:
        return redirect(url_for('user_home',user=session["user"]["name"]))


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

