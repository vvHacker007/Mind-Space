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
import cloudinary
import cloudinary.uploader
import json
import requests
from itertools import chain
from iteration_utilities import unique_everseen

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
app.debug = True
client = pm.MongoClient(os.getenv('MONGO_CLIENT'))
db1 = client.Blogs
db2 = client.Users
db3 = client.Cloudinary


from user.models import User




# def calling_func():
# 	return "HELLO"

# @app.context_processor
# def context_processor():
# 	return dict(key='value',some_func_key=calling_func) //using this i can use the variables key and some_func() in any jinja templates to access the variables


ist = pytz.timezone('Asia/Kolkata')

@app.route('/') # Checked 
def redirect_to_home():
    # Redirect to the user homepage if the user is in session
    if 'user' in session:
        return redirect(url_for('user_home',user=session['user']['name']))
    return render_template("home.html")




@app.route('/login/', methods=['GET', 'POST']) # Checked 
def login():
    form = LoginForm()
    # Check if anything is in the session and  clear the session
    if 'user' in session:
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        session['user']['logout_date'] = date_today
        session['user']['time_stamp'] = time_now
        session['user']['_id'] = uuid.uuid4().hex
        db2.Logout_Time.insert_one(session['user'])
        flash(f'Logged out of the session successfully','success')
        print("Cleared the session")  

    if 'otp' in session or 'email' in session or 'forgot_pass' in session:
        session.clear()
        print("Cleared the session")
    
    if form.validate_on_submit():
        print("Submission is validated successfully")
        resp = None        
        checked = form.remember.data
        
        if db2.Login.find_one({'name': form.email.data}):
            resp = User().login(form,1,checked)
        elif db2.Login.find_one({'email': form.email.data}):
            resp = User().login(form,0,checked)
        
        # Checking the response and logging in if there is no two factor authentication
        if resp=="two_factor":
            User().login_two_factor_auth()
            return redirect(url_for('otp_verify'))
        
        # Starting if there two factor auth is disabled
        if resp=="success":
            print("Login in Process if there is no two factor authentication")
            name_user = str(session['user']['name'])
            return redirect(url_for('user_home',user=name_user))
        else:
            flash(f"Invalid login credentials","danger")    
    return render_template('login.html', title='MindSpace-Login', form=form)




@app.route('/signup/',methods=['GET','POST']) # Checked 
def signup():
    form = RegistrationForm()
    
    # Check if anything is in the session and  clear the session
    if 'user' in session:
        
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        session['user']['logout_date'] = date_today
        session['user']['time_stamp'] = time_now
        session['user']['_id'] = uuid.uuid4().hex
        db2.Logout_Time.insert_one(session['user'])
        session.clear()
        flash(f'Logged out of the session successfully','success')
        print("Cleared the session") 
    
    if 'otp' in session or 'email' in session or 'forgot_pass' in session:
        session.clear()
        print("Cleared the session")

    if form.validate_on_submit() == False:
        
        # Flashing errors if submission is failed
        if form.email.errors:
            for i in form.email.errors:
                flash(i,'danger')
        elif form.phone.errors:
            flash(f'Please enter a valid phone number','danger')
    
    
    if form.validate_on_submit():
        
        # Calculating user age
        y,m,d = str(form.birthdate.data).split("-")
        date_today = str(datetime.date.today())
        ty,tm,td = date_today.split("-")
        date1 = datetime.datetime(int(y),int(m),int(d))
        date2 = datetime.datetime(int(ty),int(tm),int(td))
        years = relativedelta(date2,date1).years

        # Signing up and formatting the data
        resp = User().signup(form)

        # Redirectting to enter the session
        if resp=="success":
            return redirect(url_for("otp_verify"))

        elif resp=="failed":
            flash(f"Please enter a valid email address OR check your internet connection!","danger")
            return render_template('signup.html', title='MindSpace-Signup', form=form)        
        
        else:
            flash(resp,'danger')
            return render_template('signup.html', title='MindSpace-Signup', form=form)
    
    return render_template('signup.html', title='MindSpace-Signup', form=form)




@app.route("/forgot-password/",methods=['GET','POST']) #Checked
def forgot_password():
    form = ForgotPassForm()
    
    # Check sessions and clear if any exists
    if 'user' in session or 'otp' in session:
        session.clear()

    # Form Validation
    if form.validate_on_submit():
        resp = None
        print("Data is Validated successfully")
        if db2.Login.find_one({'email': form.email_id.data}):
            resp = User().forgot_pass(form)
        
        else:
            flash(f"Email-id is not registered!","danger")
            return render_template("forgot_password.html",title='MindSpace-Forgot Password', form=form)

        if resp=="success":
            return redirect(url_for('otp_verify'))
        
        else:
            flash(f"Please enter a valid email address","danger")    
    return render_template("forgot_password.html",title='MindSpace-Forgot Password', form=form)




@app.route('/reset-password/',methods=['GET','POST']) #Checked
def reset_pass():
    form = ResetPassForm()

    # Check if the forgot_pass is in session
    if 'forgot_pass' in session and 'otp' not in session:

        # Checking Validation
        if form.validate_on_submit():

            # Checking Data
            if form.password.data != form.confirm_pass.data:
                flash(f"Password doesn't match!","danger")
            
            elif len(form.password.data)<5 and len(form.confirm_pass.data)<5:
                flash(f"Password too small!","danger")
            
            elif len(form.password.data)>20 and len(form.confirm_pass.data)>20:
                flash(f"Password too long!","danger")
            
            # Redirects to login after reseting the password
            else:
                user = db2.Login.find_one(session["email"])
                form.password.data = pbkdf2_sha256.encrypt(form.password.data)
                db2.Login.update_one({"email":session["email"]},{"$set":{"password":form.password.data}})
                session.pop('user_signup',None)
                session.pop('forgot_pass',None)
                flash(f'Password changed successfully!', 'success')
                return redirect(url_for('login'))
    else:
        session.clear()
        return redirect(url_for('login'))
    return render_template("reset_password.html", title='MindSpace-Reset Password',form=form)




@app.route('/<user>/home') # Checked 
def user_home(user):
    
    # Check if the user is in session if any other user is in session then redirect to their homepage if noone is in the session then redirect to login page
    if 'user' in session and session['user']['name']==user:
        posts = db1.Posts.find({}).sort("_id",-1)
        return render_template("user_home.html",posts=posts,user=user)
    elif 'user' in session and session['user']['name']!=user:
        return redirect(url_for('user_home',user=session['user']['name']))
    else:
        session.clear()
        return redirect(url_for('login'))



@app.route('/<user>/write/',methods=['GET','POST']) #Checked
def user_write(user):
    form = PostForm()
    
    # If user is the same in the session
    if 'user' in session and session['user']['name']==user:
        if form.validate_on_submit():
            print('Submission is successful')
            if form.submit.data == True:
                
                # Uploading the image
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = form.file.data
                app.logger.info('%s file_to_upload', img_to_upload)
                
                if img_to_upload:
                    
                    # Image is selected now time to upload
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace/Blogs")
                    app.logger.info(upload_dict_result)
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
                    flash("Due to some issues the blog wasn't posted. But we tried to save the content on your timeline.")
                    return render_template('message.html',user=user)
                
            elif form.save.data == True:

                # Uploading the image
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = form.file.data
                app.logger.info('%s file_to_upload', img_to_upload)

                if img_to_upload:

                    # Image is selected now time to upload
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace/Blogs")
                    app.logger.info(upload_dict_result)
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().save_post(form,user,upload_dict_result)

                else:
                    # No image was selected
                    resp1 = "success"
                    resp2 = User().save_post(form,user)

                if resp1=="success" and resp2 == "success":
                    flash("Congrats @"+session['user']['name']+", your blog has been saved successfully!!")
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




@app.route('/logout/') # Checked 
def logout():
    if 'user' in session:
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        session['user']['logout_date'] = date_today
        session['user']['time_stamp'] = time_now
        session['user']['_id'] = uuid.uuid4().hex
        db2.Logout_Time.insert_one(session['user'])
        session.clear()
    return redirect(url_for('login'))




@app.route("/<user>/profile/",methods=['GET','POST']) #Checked
def user_profile(user):

    
    if 'user' in session and user == session['user']["name"]:

        print("Profile page opened by the owner")

        # Extracting User Data and Posts
        user_data = db2.Login.find_one({"name":user})
        user_posts = db1.Posts.find({"email" : user_data["email"]})
        saved_user_posts = db1.Saved_posts.find({"email" : session["user"]["email"]})

        app.logger.info('in upload route')
        cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
        upload_result = None

        if request.method == 'POST':

            # Uploading the image
            print("POST request")
            file_to_upload = request.files['profile_image']
            app.logger.info('%s file_to_upload', file_to_upload)
            
            if file_to_upload:
                
                # Image is selected now time to upload
                upload_result = cloudinary.uploader.upload(file_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace/Profiles")
                app.logger.info(upload_result)
                print("REACHED_HERE last")
                upload_result["username"] = session['user']['name']
                upload_result["email"] = session['user']['email']
                upload_result["phone"] = session['user']['phone']
                upload_result["_id"] = uuid.uuid4().hex
                resp = User().profile_image_upload(upload_result)
                
                # Image uploaded successfully
                if resp=="success":
                    flash(session['user']['name']+", your profile picture has been uploaded successfully!!")

                # No image was selected
                elif resp=="failed":
                    flash(session['user']['name']+", due to some issues your image did not upload, Try again later!")
                return render_template('message.html',user=session['user']['name'])
            else:
                flash(session['user']['name']+", due to some issues your image did not upload, Try again later!")
                return render_template('message.html',user=session['user']['name'])
        return render_template("profile.html",user=user_data,posts=user_posts,saved_posts=saved_user_posts)
    
    # User opens others profile
    elif 'user' in session and user != session['user']["name"]:

        # Extracting User Data and Posts
        user_data = db2.Login.find_one({"name":user})
        user_posts = db1.Posts.find({"email" : user_data["email"]})
        session_user_data = db2.Login.find_one({"name":session['user']['name']})

        if db2.Follow.find_one({"user_followed":user_data['_id'],"user":session_user_data['_id']}):
            followed=True
        
        else:
            followed=False

        return render_template("others_profile.html",user=user_data,posts=user_posts,followed=followed)

    # Anonymous opens others profile
    elif 'user' not in session:

        # Extracting User Data and Posts
        user_data = db2.Login.find_one({"name":user})
        user_posts = db1.Posts.find({"email" : user_data["email"]})
        
        return render_template("no_user_profile.html",user=user_data,posts=user_posts)
        # return redirect(url_for('login'))





@app.route('/<user>/edit/',methods=['GET','POST']) # Checked (The Email id if changed would not be checked if its valid, alternate feature can be added to check if the email updated exists.)
def edit_profile(user):

    # Check if the owner opened the profile page or not
    if 'user' in session and user == session['user']['name']:
        print("Owner Opened his profile page")
        form = EditProfileForm()
        user = db2.Login.find_one({"name":session['user']['name']})

        # Adding Cloudinary configurations
        app.logger.info('in upload route')
        cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
        upload_result = None
        
        if form.validate_on_submit():

            # Extracting user data
            print("Submission Validated")
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
            resp1="not_failed" # For profile pic upload
            resp2="success"    # For user profile update 
            resp3="failed"     # To check if the user profile is updated for otp verify

            # Checking for profile image upload
            if new_pic:

                print("Uploading the image to cloudinary")
                upload_result = cloudinary.uploader.upload(new_pic, api_secret=os.getenv('API_SECRET'), folder="MindSpace/Profiles")
                app.logger.info(upload_result)

                upload_result["username"] = session['user']['name']
                upload_result["email"] = session['user']['email']
                upload_result["phone"] = session['user']['phone']
                upload_result["_id"] = uuid.uuid4().hex
                resp1 = User().profile_image_upload(upload_result)

            # Checking if there is any change in the enteries
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
                resp3 = "success"
            
            # Checking if the response is successful
            if resp2=="success" and resp3=="success":
                return redirect(url_for('otp_verify'))
            
            #  Checking if there is any error in the update profile
            elif resp2!="success" and resp3=="success":
                flash(resp2,'danger')
                return render_template("edit_profile.html",user=user,form=form)
            
            # Checking if the profile picture is canceled
            elif resp1=="failed":
                flash(session['user']['name']+", due to some issues your image did not upload, Try again later!",'danger')
                return render_template("edit_profile.html",user=user,form=form)
            
            # Check if the profile picture is successful
            elif resp1=="success":
                flash(session['user']['name']+", your image has been uploaded successfully!",'success')
                return render_template("edit_profile.html",user=user,form=form)
            
            # Check if the profile picture is unsuccessful
            elif resp1=="not_failed":
                return render_template("edit_profile.html",user=user,form=form)
            
            return render_template("edit_profile.html",user=user,form=form)
        return render_template("edit_profile.html",user=user,form=form)
    
    elif 'user' in session and user != session['user']['name']:
        return redirect(url_for('edit_profile',user=session['user']['name']))

    elif 'user' not in session:
        return redirect(url_for('login'))




@app.route("/<user>/settings",methods=['GET','POST']) # Checked
def user_settings(user):
    
    # Checking if user is in session
    if 'user' in session and user == session['user']['name']:

        # Collecting the data form the user
        user_data = db2.Login.find_one({'name': user})

        # Todays Date and Time
        date_today = str(datetime.date.today())
        ty,tm,td = date_today.split("-")
        y,m,d = user_data['birthdate'].split("-")
        date1 = datetime.datetime(int(y),int(m),int(d))
        date2 = datetime.datetime(int(ty),int(tm),int(td))
        years = relativedelta(date2,date1).years
        months = relativedelta(date2,date1).months
        days = relativedelta(date2,date1).days
        
        # Post request 
        if request.method == 'POST':
            
            if request.form.get('update'): # Checked

                print("Profile Information Updated")
                
                full_name = request.form.get('fullName')                
                bio = request.form.get('bio')
                age = request.form.get('age')
                
                db2.Login.update({"name":session["user"]["name"]},{"$set":{"full_name":full_name,"age":age,"bio":bio}})
            
            elif request.form.get('update_acc'): # Checked
                
                print("Account Username Update")

                user_name = request.form.get('username')
                
                # Check if the username already exists
                if db2.Login.find_one({'name':user_name}):
                    
                    flash('Username already taken!','danger')
                    return render_template("settings.html",user=user_data,years=years,months=months,days=days)
                
                else:

                    db2.Login.update({"name":session["user"]["name"]},{"$set":{"name":user_name}})
                    db1.Posts.update_many({"email":session["user"]["email"]},{"$set":{"name":user_name}})
                    db1.Saved_posts.update_many({"email":session["user"]["email"]},{"$set":{"name":user_name}})
                    flash('Username has been updated successfully!','success')
                    return redirect(url_for('login'))
            
            elif request.form.get('deleteacc'): # Checked
                
                print("Delete Account")

                resp = User().delete_account(session['user']['name'])
                
                # Check if the response is successful that is otp is sent to the email
                if resp=="success":
                    return redirect(url_for('otp_verify'))
                
                elif resp=="failed":
                    flash(f"Check your internet connection!","danger")   
            
            elif request.form.get('update_pass'): # Checked

                print("Secure Settings Change password")

                # Check if the changed password is valid
                if request.form.get('new_pass') and not request.form.get('confirm_new_pass'):
                    flash(f"Confirm the New Password!","danger")
                
                elif not request.form.get('new_pass') and request.form.get('confirm_new_pass'):
                    flash(f"Enter the New Password!","danger")
                
                elif not request.form.get('new_pass') and not request.form.get('confirm_new_pass'):
                    flash(f"Enter the New Password!","danger")

                elif request.form.get('new_pass') != request.form.get('confirm_new_pass'):
                    flash(f"Password doesn't match!","danger")

                elif len(request.form.get('new_pass'))<5 and len(request.form.get('confirm_new_pass'))<5:
                    flash(f"Password too small!","danger")

                elif len(request.form.get('new_pass'))>20 and len(request.form.get('confirm_new_pass'))>20:
                    flash(f"Password too long!","danger")

                else:
                    
                    # If password is valid then change password
                    new_pass = request.form.get('new_pass')
                    confirm_new_pass = request.form.get('confirm_new_pass')
                    resp = User().change_password(user,new_pass,confirm_new_pass)

                    # Check if the response is success
                    if resp == "success":
                        return redirect(url_for('otp_verify'))

                    elif resp=="failed":
                        flash('Check your internet connection!','danger')
                        return render_template("settings.html",user=user_data,years=years,months=months,days=days)
                   
                    else:
                        flash(resp,'danger')
                        return render_template("settings.html",user=user_data,years=years,months=months,days=days)

            elif request.form.get('two_factor_auth'): # Checked

                print("Secure Settings Enable Two Factor Authentication")
                resp = User().two_factor_authenticate(user)

                # Check if the response is success
                if resp == "success":
                    return redirect(url_for('otp_verify'))
                
                elif resp=="failed":
                    flash('Check your internet connection!','danger')
                    return render_template("settings.html",user=user_data,years=years,months=months,days=days)
                
                else:
                    flash(resp,'danger')
                    return render_template("settings.html",user=user_data,years=years,months=months,days=days)

            elif request.form.get('disable_two_factor_auth'): # Checked

                print("Secure Settings Disable Two Factor Authentication")
                resp = User().disable_two_factor_authenticate(user)

                # Check if the response is success
                if resp == "success":
                    return redirect(url_for('otp_verify'))
                
                elif resp=="failed":
                    flash('Check your internet connection!','danger')
                    return render_template("settings.html",user=user_data,years=years,months=months,days=days)
                
                else:
                    flash(resp,'danger')
                    return render_template("settings.html",user=user_data,years=years,months=months,days=days)
        return render_template("settings.html",user=user_data,years=years,months=months,days=days)

    # If user not in session then redirect to the user page
    elif 'user' in session and user != session['user']['name']: # Checked
        return redirect(url_for('user_settings',user=session['user']['name']))
    
    elif 'user' not in session:
        return redirect(url_for('login'))




@app.route("/blog/<_id>/") # Checked
def user_blog_redirect(_id):

    # Extract Blog data from database
    user_post = db1.Posts.find_one({"_id":_id})
    
    # Check if the blog belongs to user in session
    if 'user' in session and user_post["name"] == session["user"]["name"]:
        
        # Extract user Data from database
        user = db2.Login.find_one({"name":session["user"]["name"]})
        return render_template("blog.html",user_post=user_post,user=user)

    # If the blog doesnot belong to the user in session then render other_blog
    elif 'user' in session and user_post["name"] != session["user"]["name"]:
        
        # Extract user Data from database
        user = db2.Login.find_one({"name":user_post["name"]})
        return render_template("others_blog.html",user_post=user_post,user=user)
    
    # If noone is in the session then redirect to login
    elif 'user' not in session:
        
        # Extract user Data from database
        user = db2.Login.find_one({"name":user_post["name"]})
        return render_template("no_user_blog.html",user_post=user_post,user=user)




@app.route("/verification/",methods=['GET','POST'])
def otp_verify():
    form = OTPForm()
    
    # Checks if user or otp is in session if not redirect to signup
    if 'otp' not in session and 'user' not in session:
        return redirect(url_for('signup'))

    # Checks if user is in session and otp is not in session if not redirect to user home page
    if 'otp' not in session and 'user' in session:
        return redirect(url_for('user_home',user=session['user']['name']))

    print("OTP Verification Needed!")
    
    # Checks if otp and user_signup are in session
    if 'otp' in session and 'user_signup' in session and form.validate_on_submit():
        print("Signup Verification")
    
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
    
            if db2.Login.insert_one(session["user_signup"]):
                session.pop('user_signup',None)
                flash(f'Account created successfully!', 'success')
                return redirect(url_for('login'))
    
        else:
            session.clear()
            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return redirect(url_for('signup'))
    
    elif 'otp' in session and 'forgot_pass' in session and form.validate_on_submit():
        print("Forgot Password Verification")
    
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
            return redirect(url_for('reset_pass'))
    
        else:
            session.clear()
            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return redirect(url_for('login'))
    
    elif 'otp' in session and 'user_updated_data' in session and form.validate_on_submit():
        print("Updating User Information Verification")
    
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
            db2.Login.update_one({"email":session["user"]["email"]},{"$set":session["user_updated_data"] })
            db1.Posts.update_many({"email":session["user"]["email"]},{"$set":session["user_updated_data"] })
            db1.Saved_posts.update_many({"email":session["user"]["email"]},{"$set":session["user_updated_data"] })
            session.clear()
            return redirect(url_for('login'))
    
        else:
            session.pop('otp',None)
            session.pop('user_updated_data',None)
            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return redirect(url_for('user_profile',user=session['user']['name']))
    
    elif 'otp' in session and 'delete_acc' in session and form.validate_on_submit():
        print("Delete Account Verification")
    
        if(form.otp.data==session['otp']):

            db1.Posts.delete_many({'name':session['delete_acc'] })
            db1.Saved_posts.delete_many({'name':session['delete_acc'] })
            db2.Login.delete_many({'name':session['delete_acc'] })
            db2.Login_Time.delete_many({'name':session['delete_acc'] })
            db3.Blog.delete_many({'name':session['delete_acc'] })
            db3.Profile.delete_many({'name':session['delete_acc'] })
            session.clear()
            return redirect(url_for('login'))
    
        else:

            session.pop('otp',None)
            session.pop('delete_acc',None)
            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return redirect(url_for('user_profile',user=session['user']['name']))
    
    elif 'otp' in session and 'new_pass' in session and form.validate_on_submit():
        print("Change Password Verification")
    
        if(form.otp.data==session['otp']):

            session.pop('otp',None)
            db2.Login.update_one({"email":session['user']["email"]},{"$set":{"password":session['new_pass']}})
            session.clear()
            flash(f'Password Changed Successfully', 'success')
            return redirect(url_for('login'))
    
        else:

            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return render_template("otp_verification.html", title='MindSpace-Verification',form=form)
    
    elif 'otp' in session and 'two_factor_auth' in session and form.validate_on_submit():
        print("Activate Two Factor Authentication Confirmation")
    
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
            db2.Login.update_one({"email":session['user']["email"]},{"$set":{'two_factor_auth':session['two_factor_auth']}})
            session.clear()
            return redirect(url_for('login')) 
    
        else:
            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return render_template("otp_verification.html", title='MindSpace-Verification',form=form)
    
    elif 'otp' in session and 'login_two_factor' in session and form.validate_on_submit():
        print("Two factor Auth Login")
    
        if(form.otp.data==session['otp']):
            session.pop('otp',None)
            session.pop('login_two_factor',None)
            session['user'] = db2.Login.find_one({"email":session['email']})
            session['logged_in'] = True
            name_user = str(session['user']['name'])
            return redirect(url_for('user_home',user=name_user))
    
        else:
            session.pop('otp',None)
            session.pop('login_two_factor',None)
            flash(f'OTP you have entered is incorrect, Try Again!', 'danger')
            return redirect(url_for('login'))
    return render_template("otp_verification.html", title='MindSpace-Verification',form=form)




@app.route("/blog/<_id>/edit/",methods=['GET','POST']) # Checked
def edit_blog(_id):

    # Extract Blog Data from Database
    user_post = db1.Posts.find_one({"_id":_id})

    # Check if the user is in session and blog belongs to the user in session
    if 'user' in session and user_post["name"] == session["user"]["name"]:

        # Convert HTML Post into markdown
        user_post["blog"] = markdownify(user_post["blog"])

        # Check for POST Request
        if request.method == "POST":

            # Check which button was pressed
            if request.form.get("post_blog"):

                print("Blog is being published...")

                # Add configuration for blog image if added
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = request.files["blog_file"]
                app.logger.info('%s file_to_upload', img_to_upload)

                # Blog title and content
                user_post["blog"] = request.form["blog_text"]
                user_post["title"] = request.form["title_text"]

                # Check if image is uploaded
                if img_to_upload:
                    
                    print("Image is being uploaded...")
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace/Blogs")
                    app.logger.info(upload_dict_result)

                    # Add image data and user data from session  
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    user_post["img"] = upload_dict_result["secure_url"]

                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().edit_post(user_post,upload_dict_result)
                
                # If image is not uploaded then resp1 is set to succes as default
                else:

                    resp1 = "success"
                    resp2 = User().edit_post(user_post,upload_dict_result)
                
                # If responses are success then redirect
                if resp1=="success" and resp2 == "success":

                    flash("Congrats @"+session['user']['name']+", your blog has been posted successfully!!")
                    return render_template('message.html',user=session["user"]["name"])
                
                # else display the error
                else:

                    User().edit_save(user_post,upload_dict_result)
                    flash("Due to some issues the blog wasn't posted. But we have saved the content on your timeline. You can check that using on your profile")
                    return render_template('message.html',user=session["user"]["name"])
            
            elif request.form.get("save_blog"):
                print("Blog is being saved...")

                # Add configuration for blog image if added
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = request.files["blog_file"]
                app.logger.info('%s file_to_upload', img_to_upload)

                # Blog title and content
                user_post["blog"] = request.form["blog_text"]
                user_post["title"] = request.form["title_text"]

                # Check if image is uploaded
                if img_to_upload:
                    
                    print("Image is being uploaded...")
                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace/Blogs")
                    app.logger.info(upload_dict_result)

                    # Add image data and user data from session
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    user_post["img"] = upload_dict_result["secure_url"]
                    
                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().edit_post(user_post,upload_dict_result)

                # If image is not uploaded then resp1 is set to succes as default
                else:

                    resp1 = "success"
                    resp2 = User().edit_save(user_post,upload_dict_result)

                # If responses are success then redirect
                if resp1=="success" and resp2 == "success":

                    flash("@"+session['user']['name']+" your blogs has been saved on your timeline successfully")
                return render_template('message.html',user=session["user"]["name"])  
    
    # If user is not present in the session then redirect to user_blog_redirected
    else:
        return redirect(url_for('user_blog_redirect',_id=user_post["_id"]))
    return render_template("edit_blog.html",user_post=user_post)




@app.route("/blog/<_id>/delete/") # Checked
def delete_blog(_id):

    # Find the blog in the database
    user_post = db1.Posts.find_one({"_id":_id})

    # If post belongs to the user in session then delete the post from database
    if 'user' in session and user_post["name"] == session["user"]["name"]:

        db1.Posts.delete_one({"_id":_id})
        nob = db2.Login.find_one({'name':session['user']['name']})['submitted_blogs']

        if db2.Login.update_many({'name':session['user']['name']},{"$set":{"submitted_blogs": nob-1}}):
        
            flash(session["user"]["name"]+",your blog has been removed successfully!")
        
        else:
        
            flash(session["user"]["name"]+", due to some issues we were not able to remove your blog. Try again later!")
        return render_template("message.html",user=session["user"]["name"])
    
    # If user is not present in the session then redirect to user_blog_redirected
    else:
        return redirect(url_for('user_blog_redirect',_id=user_post["_id"]))




@app.route("/saved/<_id>/") # Checked
def user_saved_blog_redirect(_id):

    # Extract the Blog Data and user data if present from the Database
    user_post = db1.Saved_posts.find_one({"_id":_id})
    user = db2.Login.find_one({"name":user_post["name"]})

    if 'user' in session and user_post["name"] == session["user"]["name"]:
        return render_template("saved_blog.html",user_post=user_post,user=user)

    elif 'user' in session and user_post["name"] != session["user"]["name"]:
        return redirect(url_for('user_home',user=session["user"]["name"]))
    
    elif 'user' not in session:
        return redirect(url_for('login'))




@app.route("/saved/<_id>/edit/",methods=['GET','POST']) # Checked
def edit_saved_blog(_id):

    # Extract Saved Blog Data from Database
    user_post = db1.Saved_posts.find_one({"_id":_id})   

    # Check if the blog belongs to user in session   
    if 'user' in session and user_post["name"] == session["user"]["name"]:

        # Convert HTML Text into Markdown
        user_post["blog"] = markdownify(user_post["blog"])

        # Check the POST Request
        if request.method == "POST":
            
            # Check which button is pressed
            if request.form.get("post_blog"):

                print("Blog is being Published...")
                
                # Image upload configuration
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = request.files["blog_file"]
                app.logger.info('%s file_to_upload', img_to_upload)

                # Extract Blog data and user data from Database
                user_post["blog"] = request.form["blog_text"]
                user_post["title"] = request.form["title_text"]

                # Check if Image is uploaded
                if img_to_upload:

                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace/Blogs")
                    app.logger.info(upload_dict_result)

                    # Add user data and image data from the session
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    user_post["img"] = upload_dict_result["secure_url"]

                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().edit_post(user_post,upload_dict_result)

                # If image is not uploaded then resp1 is set to succes as default 
                else:
                
                    resp1 = "success"
                    resp2 = User().edit_post(user_post,upload_dict_result)

                # Check if both the responses are success
                if resp1=="success" and resp2 == "success":

                    flash("Congrats @"+session['user']['name']+", your blog has been posted successfully!!")
                    return render_template('message.html',user=session["user"]["name"])
                
                # if not then provide the error message
                else:
                    User().edit_save(user_post,upload_dict_result)
                    flash("Due to some issues the blog wasn't posted. But we have saved the content on your timeline. You can check that using on your profile")
                    return render_template('message.html',user=session["user"]["name"])

            elif request.form.get("save_blog"):

                print("Blog is being saved...")
                
                #Image Upload configurations
                app.logger.info('in upload route')
                cloudinary.config(cloud_name=os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))
                upload_dict_result = None
                img_to_upload = request.files["blog_file"]
                app.logger.info('%s file_to_upload', img_to_upload)

                # Extract Blog Data and User Data from Database
                user_post["blog"] = request.form["blog_text"]
                user_post["title"] = request.form["title_text"]

                # Check if image is uploaded
                if img_to_upload:

                    upload_dict_result = cloudinary.uploader.upload(img_to_upload, api_secret=os.getenv('API_SECRET'), folder="MindSpace/Blogs")
                    app.logger.info(upload_dict_result)

                    # Add user Data and image data from session
                    upload_dict_result["username"] = session['user']['name']
                    upload_dict_result["email"] = session['user']['email']
                    upload_dict_result["phone"] = session['user']['phone']
                    user_post["img"] = upload_dict_result["secure_url"]

                    resp1 = User().blog_image_upload(upload_dict_result)
                    resp2 = User().edit_save(user_post,upload_dict_result)
                
                # If image is not uploaded then resp1 is set to succes as default 
                else:
                    resp1 = "success"
                    resp2 = User().edit_save(user_post)

                # Check if both the responses are success
                if resp1=="success" and resp2 == "success":
                    flash("@"+session['user']['name']+" your blogs has been saved on your timeline successfully")

                else:
                    return render_template("edit_saved_blog.html",user_post=user_post)

                return render_template('message.html',user=session["user"]["name"])  
    else:
        return redirect(url_for('user_home',user=session["user"]["name"]))

    return render_template("edit_saved_blog.html",user_post=user_post)




@app.route("/saved/<_id>/delete/") # Checked
def delete_saved_blog(_id):
    
    # Extract Blog data from database
    user_post = db1.Saved_posts.find_one({"_id":_id})

    # Check if the blog belongs to user in session
    if 'user' in session and user_post["name"] == session["user"]["name"]:
        db1.Saved_posts.delete_one({"_id":_id})
        nosb = db2.Login.find_one({'name':session['user']['name']})['saved_blogs']
        if db2.Login.update_many({'name':session['user']['name']},{"$set":{"saved_blogs": nosb-1}}):
            flash(session["user"]["name"]+",your blog has been removed successfully!")
        else:
            flash(session["user"]["name"]+", due to some issues we were not able to remove your blog. Try again later!")
        return render_template("message.html",user=session["user"]["name"])
    else:
        return redirect(url_for('user_home',user=session["user"]["name"]))



@app.route('/search/<data>')# Checked
def search_data(data):
    
    if 'user' in session:
    
        # Extracting posts related to entered keyword
        posts_title_data = db1.Posts.find({'title':{"$regex": data,'$options' : 'i'}})
        posts_content_data = db1.Posts.find({'summary':{"$regex": data,'$options' : 'i'}})

        # Extracting users with related keywords
        users_name_data = db2.Login.find({'name':{"$regex": data,'$options' : 'i'}})
        users_email_data = db2.Login.find({'email':{"$regex": data,'$options' : 'i'}})
        user_full_name_data = db2.Login.find({'full_name':{"$regex": data,'$options' : 'i'}})

        # Concating the data extracted 
        posts_data = [x for x in chain(posts_title_data,posts_content_data)]
        users_data = [i for i in chain(users_name_data,users_email_data,user_full_name_data)]

        # Selecting the unique data
        posts_data = list(unique_everseen(posts_data))
        users_data = list(unique_everseen(users_data))

        return render_template('search.html',data=data,users_data=users_data,posts_data=posts_data,len_users=len(users_data),len_posts=len(posts_data))
    
    elif 'user' not in session:
        
        # Extracting posts related to entered keyword
        posts_title_data = db1.Posts.find({'title':{"$regex": data,'$options' : 'i'}})
        posts_content_data = db1.Posts.find({'summary':{"$regex": data,'$options' : 'i'}})

        # Extracting users with related keywords
        users_name_data = db2.Login.find({'name':{"$regex": data,'$options' : 'i'}})
        users_email_data = db2.Login.find({'email':{"$regex": data,'$options' : 'i'}})
        user_full_name_data = db2.Login.find({'full_name':{"$regex": data,'$options' : 'i'}})

        # Concating the data extracted 
        posts_data = [x for x in chain(posts_title_data,posts_content_data)]
        users_data = [i for i in chain(users_name_data,users_email_data,user_full_name_data)]

        # Selecting the unique data
        posts_data = list(unique_everseen(posts_data))
        users_data = list(unique_everseen(users_data))

        return render_template('anonymous_search.html',data=data,users_data=users_data,posts_data=posts_data,len_users=len(users_data),len_posts=len(posts_data))





@app.route("/<user>/follow/")# Checked
def follow_user(user):

    # Check if user is in session and the user is not the same as the user in session
    if 'user' in session and user!=session['user']['name']:

        # Todays date and time
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")

        # Extracting both user data 
        other_user_data = db2.Login.find_one({'name':user})
        session_user_data = db2.Login.find_one({'name':session['user']['name']})

        user_follow_check = {
            "user":session_user_data['_id'],
            "user_followed":other_user_data['_id'],
        }

        if not db2.Follow.find_one(user_follow_check):
        
            # Updating the follower and following data on database
            db2.Login.update_one({"name":user},{"$set":{"followers":other_user_data['followers']+1}})
            db2.Login.update_one({"name":session['user']['name']},{"$set":{"following":session_user_data['following']+1}})

            # Creating a dictonary containing the user followed and the user following data
            user_follow = {
                "_id":uuid.uuid4().hex,
                "user":session_user_data['_id'],
                "user_followed":other_user_data['_id'],
                "date":date_today,
                "time_stamp":time_now
            }

            # Inserting the dictonary to the database
            db2.Follow.insert_one(user_follow)

    return redirect(url_for("user_profile",user=user))




@app.route("/<user>/unfollow/")# Checked
def unfollow_user(user):
    
    # Check if user is in session and the user is not the same as the user in session
    if 'user' in session and user!=session['user']['name']:

        # Extracting both user data 
        other_user_data = db2.Login.find_one({'name':user})
        session_user_data = db2.Login.find_one({'name':session['user']['name']})
        
        user_unfollow_check = {
            "user":session_user_data['_id'],
            "user_followed":other_user_data['_id'],
        }
        
        if db2.Follow.find_one(user_unfollow_check):
        
            # Updating the follower and following data on database
            db2.Login.update_one({"name":user},{"$set":{"followers":other_user_data['followers']-1}})
            db2.Login.update_one({"name":session['user']['name']},{"$set":{"following":session_user_data['following']-1}})

            # Creating a dictonary containing the user followed and the user following data
            user_unfollow = {
                "user":session_user_data['_id'],
                "user_followed":other_user_data['_id'],
            }

            # Searching the database and deleting any existing entry
            db2.Follow.delete_one(user_unfollow)
    return redirect(url_for("user_profile",user=user))



if __name__ == '__main__':
    app.run(threaded=True)