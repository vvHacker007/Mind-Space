from flask import Flask,jsonify,request,session,redirect
from passlib.hash import pbkdf2_sha256
import uuid
from app import db1, db2, db3, app
import datetime
from dateutil.relativedelta import relativedelta, MO
import time
from cryptography.fernet import Fernet
from text_summarizer import summarize
import math, random
import smtplib
import re
import markdown
import os
import json
from flask_mail import Mail,Message
from dotenv import load_dotenv,find_dotenv
from datetime import timedelta
from better_profanity import profanity
load_dotenv(find_dotenv())

mail = Mail(app)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = os.getenv('EMAIL_ID'),
    MAIL_PASSWORD = os.getenv('EMAIL_PASS'),
))
mail = Mail(app) 

class User:



    def generate_otp(self): # Checked 
        digits = "0123456789"
        OTP = ""
        for i in range(6) :
            OTP += digits[math.floor(random.random()*10)]
        return OTP
    


    def start_session(self,user,checked): # Checked 
        del user['password']
        del user['_id']
        
        # Adding user and logged in to the session
        session['user'] = user
        session['logged_in'] = True
        if checked==True:
            print("31 Days of session")
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=31)
        elif checked==True:
            print("5 Hours of session")
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=300)
        return "success"



    def signup(self,form):  # Checked 
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        
        # Checking the entered data
        if db2.Login.find_one({'name': form.username.data}):
            return "Username already exists!"
        elif db2.Login.find_one({'email': form.email.data}):
            return "Email already registered!"
        elif len(str(form.phone.data))<=6:
            return "Please enter a valid phone number!"
        elif len(str(form.phone.data))>=12:
            return "Please enter a valid phone number!"
        elif db2.Login.find_one({'phone': form.phone.data}):
            return "Phone number already registered!"
        elif form.password.data != form.confirm_pass.data:
            return "Password doesn't match!"
        elif len(form.password.data)<5 and len(form.confirm_pass.data)<5:
            return "Password too small!"
        elif len(form.password.data)>20 and len(form.confirm_pass.data)>20:
            return "Password too long!"

        # user data entered
        user = {
            "_id":uuid.uuid4().hex,
            "name":form.username.data,
            "email":form.email.data,
            "password":form.password.data,
            "phone":form.phone.data,
            "birthdate":str(form.birthdate.data),
            "joined_date": str(date_today),
            "submitted_blogs":0,
            "saved_blogs":0,
            "followers":0,
            "profile_pic":"https://res.cloudinary.com/dq84d1ar3/image/upload/v1620798507/profile-user_xroad2.png",
            "following":0,
            "full_name":form.username.data,
            'two_factor_auth':False,
            'bio':None,
            'age':None
        }

        # Encrypting the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
    

        if db2.Login.find_one(str(user["email"]))==None:
            print("Email Check!")
            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
            
            # Otp generated and added to session along with user_signup
            session['otp'] = self.generate_otp()
            session['user_signup'] = user
            msg = Message('OTP Verification',sender =os.getenv('EMAIL_ID'),recipients = [user["email"]])
            msg.body = "Dear MindSpace User,\n Your One Time PIN(OTP) for MindSpace Verification is: "+session["otp"]+"\n\n" + date_today +"\n"+ time_now + "\nThis is an auto-generated email. Do not reply to this email."
            mail.send(msg)
            return "success"
        print("OTP generation failed")
        return "failed"

    def login(self,form,flag,checked=None):  # Checked 
        
        # Flag chooses between username or email to login
        if flag==0:
            user = db2.Login.find_one({"email": form.email.data})
        elif flag==1:
            user = db2.Login.find_one({"name": form.email.data})

        # Check the entered password and start the session
        if user and pbkdf2_sha256.verify(form.password.data, user['password'])==True:
            self.start_session(user,checked)
            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
            session['user']['login_date'] = date_today
            session['user']['time_stamp'] = time_now
            session['user']['_id'] = uuid.uuid4().hex
            db2.Login_Time.insert_one(session['user'])
            del session['user']['_id']
            if session['user']['two_factor_auth'] == True:
                session.pop('user',None)
                session.pop('logged_in',None)
                session['email'] = user['email']
                return "two_factor"
            return "success"    
        return "failed"
    
    def create_post(self,form,user,image_json=None): #Checked

        # Cleaning and Summarizing the content
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        form.content.data = markdown.markdown(form.content.data)
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', form.content.data)
        cleantext = cleantext.replace(r"\n", "\t")
        cleantext = profanity.censor(cleantext, '@')
        print("THIS IS THE CLEANED FORMAT",cleantext)
        content_summary = summarize(cleantext) 
        if image_json==None:
            user_posts = {
                "_id":uuid.uuid4().hex,
                "name":str(session['user']['name']),
                "email":str(session['user']['email']),
                "phone":str(session['user']['phone']),
                "date":str(date_today),
                "time":str(time_now),
                "title":str(profanity.censor(form.title.data, '@')),
                "blog":str(profanity.censor(form.content.data, '@')),
                "summary":str(content_summary),
                "img":"",
                "likes":0,
                "comments":0        
                }
        elif image_json['secure_url']:
            user_posts = {
                "_id":uuid.uuid4().hex,
                "name":str(session['user']['name']),
                "email":str(session['user']['email']),
                "phone":str(session['user']['phone']),
                "date":str(date_today),
                "time":str(time_now),
                "title":str(profanity.censor(form.title.data, '@')),
                "blog":str(profanity.censor(form.content.data, '@')),
                "summary":str(content_summary),
                "img":str(image_json['secure_url']),
                "likes":0,
                "comments":0        
                }
        
        # Inserting the data in the database
        db1.Posts.insert_one(user_posts)
        nob = db2.Login.find_one({'name':session['user']['name']})['submitted_blogs']
        if db2.Login.update_many({'name':session['user']['name']},{"$set":{"submitted_blogs": nob+1}}):
            return "success"
        return "failed"
    
    def save_post(self,form,user,image_json=None): #Checked
        
        # Cleaning and Summarizing the content
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        form.content.data = markdown.markdown(form.content.data)
        if image_json:
            user_posts_saved = {
                "_id":uuid.uuid4().hex,
                "name":str(session['user']['name']),
                "email":str(session['user']['email']),
                "phone":str(session['user']['phone']),
                "date":str(date_today),
                "time":str(time_now),
                "title":str(profanity.censor(form.title.data, '@')),
                "blog":str(profanity.censor(form.content.data, '@')),
                "img":image_json["secure_url"],
                "likes":0,
                "comments":0        
                }
        else:
            user_posts_saved = {
                "_id":uuid.uuid4().hex,
                "name":str(session['user']['name']),
                "email":str(session['user']['email']),
                "phone":str(session['user']['phone']),
                "date":str(date_today),
                "time":str(time_now),
                "title":str(profanity.censor(form.title.data, '@')),
                "blog":str(profanity.censor(form.content.data, '@')),
                "img":"",
                "likes":0,
                "comments":0        
                }
        
        # Inserting the data in the database
        db1.Saved_posts.insert_one(user_posts_saved)
        nosb = db2.Login.find_one({'name':session['user']['name']})['saved_blogs']
        if db2.Login.update_many({'name':session['user']['name']},{"$set":{"saved_blogs": nosb+1}}):
            return "success"
        return "failed;"

    def forgot_pass(self,form):

        # Checking if the email is registered
        if db2.Login.find_one({'email': form.email_id.data}):

            # Cleared the session
            session.clear()
            print("Email Check!")
            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
            
            # Otp generated and added to session along with forgot_pass
            session['otp'] = self.generate_otp()
            session['email'] = form.email_id.data
            msg = Message('OTP Verification',sender =os.getenv('EMAIL_ID'),recipients = [session["email"]])
            msg.body = "Dear MindSpace User,\n Your One Time PIN(OTP) for Reset Password is: "+session["otp"]+"\n\n" + date_today +"\n"+ time_now + "\nThis is an auto-generated email. Do not reply to this email."
            mail.send(msg)
            session['forgot_pass'] = True
            return "success"
        print("OTP generation failed")
        return "failed"

    def profile_image_upload(self,image_json): #Checked

        # Uploading the image and adding to database
        image_url = image_json['secure_url']
        user_email = db2.Login.find_one({"email": image_json['email']})
        if user_email and db3.Profile.insert_one(image_json):
            if db2.Login.update_many({'email':image_json['email']},{"$set":{"profile_pic": image_url}}):
                return "success"
            else:
                return "failed"
        return "failed"
    
    def blog_image_upload(self,image_json): # Checked

        # Uploading the image and adding to database
        image_url = image_json['secure_url']
        user_email = db2.Login.find_one({"email": image_json['email']})

        if user_email and db3.Blog.insert_one(image_json):
            return "success"
        else:
            return "failed"
        
    def profile_update(self,updated_data):

        # Creating a dictionary to upload the data to the database
        to_update = {}
        user_data = db2.Login.find_one({"name":session["user"]["name"]})
        
        # Check if user name already exists
        if updated_data["name"]:
            
            if db2.Login.find_one({"name":updated_data["name"]})==None:
                to_update["name"] = updated_data["name"]
            
            else:
                return "Username already exists!"
        
        # Check if email id already exists if not then chnage the email
        if updated_data["email"]:
        
            if db2.Login.find_one({"email":updated_data["email"]})==None:
                to_update["email"] = updated_data["email"]
        
            else:
                return "Email already registered!"
        
        # Check if password matches
        if updated_data["password"] and updated_data["confirm_pass"]=="":
            return "Confirm the new password!"
        
        if updated_data["password"] and updated_data["confirm_pass"]:
        
            if updated_data["password"] == updated_data["confirm_pass"]:
                if pbkdf2_sha256.verify(updated_data["password"],user_data["password"])==True:
                    return "New password matches the old password"
                
                to_update["password"] = updated_data["password"]
            
            else:
                return "Password doesn't match!"
        
        # Check if phone number is valid
        if updated_data["phone"]:
        
            if db2.Login.find_one({"phone":updated_data["phone"]}):
        
                if updated_data["phone"] >= 12 and updated_data["phone"]<=6:
                    to_update["phone"] = int(updated_data["phone"])
        
                else:
                    return "Please enter a valid phone number!"
        
            else:
                return "Phone number already registered!"
        
        # Add DOB to the data
        if updated_data["birthdate"]:
            to_update["birthdate"] = str(updated_data["birthdate"])
        
        # Update the full name
        if updated_data["full_name"]:
            to_update["full_name"] = updated_data["full_name"]
        
        # Update the bio
        if updated_data["bio"]:
            to_update["bio"] = updated_data["bio"]
        
        # Updated data to be added in session
        session["user_updated_data"]=to_update
        
        # Send OTP
        if db2.Login.find_one({'email': session['user']['email']}):

            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")

            # Otp generated and added to session along
            session['otp'] = self.generate_otp()
            msg = Message('OTP Verification',sender =os.getenv('EMAIL_ID'),recipients = [session["user"]["email"]])
            msg.body = "Dear MindSpace User,\n Your One Time PIN(OTP) for MindSpace Verification is: "+session["otp"]+"\n\nGenerated at " + date_today + " " + time_now + "\nThis is an auto-generated email. Do not reply to this email."
            mail.send(msg)
            return "success"
        else:
            return "failed"
        
    
    def edit_post(self,user_blog,image_json=None): # Checked

        # Todays date and time
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        
        # Convert markdown Blog into html
        user_blog["blog"] = markdown.markdown(user_blog["blog"])

        # Summarizing the blog
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', user_blog["blog"])
        cleantext = cleantext.replace(r"\n", "\t")
        content_summary = summarize(cleantext) 

        # Data creation if image is added
        if image_json:
            user_posts = {
                "_id":user_blog['_id'],
                "name":str(session['user']['name']),
                "email":str(session['user']['email']),
                "phone":str(session['user']['phone']),
                "date":str(date_today),
                "time":str(time_now),
                "title":user_blog["title"],
                "blog":user_blog["blog"],
                "img":image_json["secure_url"],
                "summary":str(content_summary),
                "likes":0,
                "comments":0        
                }
        
        else:
            user_posts = {
                "_id":user_blog["_id"],
                "name":str(session['user']['name']),
                "email":str(session['user']['email']),
                "phone":str(session['user']['phone']),
                "date":str(date_today),
                "time":str(time_now),
                "title":user_blog["title"],
                "blog":user_blog["blog"],
                "img":user_blog['img'],
                "summary":str(content_summary),
                "likes":0,
                "comments":0        
                }
        
        # Find the published post and update the editted post
        if db1.Posts.find_one({"_id":user_blog["_id"]}):
            
            del user_posts["_id"]
            db1.Posts.update_one({"_id":user_blog["_id"]},{"$set":user_posts })
            return "success"
        
        # Find the saved post and replace with the new post
        elif db1.Saved_posts.find_one({"_id":user_blog["_id"]}):

            db1.Saved_posts.delete_one({"_id":user_blog["_id"]})
            db1.Posts.insert_one(user_posts)
            nosb = db2.Login.find_one({'name':session['user']['name']})['saved_blogs']
            nob = db2.Login.find_one({'name':session['user']['name']})['submitted_blogs']
            if db2.Login.update_many({'name':session['user']['name']},{"$set":{"saved_blogs": nosb-1}}) and db2.Login.update_many({'name':session['user']['name']},{"$set":{"submitted_blogs": nob+1}}):
                return "success"
        
        return "failed"
    
    def edit_save(self,user_blog,image_json=None):

        # Todays Date and Time
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")

        #Convert makdown into HTML
        user_blog["blog"] = markdown.markdown(user_blog["blog"])

        # Summarizing the blog
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', user_blog["blog"])
        cleantext = cleantext.replace(r"\n", "\t")
        content_summary = summarize(cleantext)

        # Data Creation if image is added
        if image_json:
            user_posts_saved = {
                "_id":uuid.uuid4().hex,
                "name":str(session['user']['name']),
                "email":str(session['user']['email']),
                "phone":str(session['user']['phone']),
                "date":str(date_today),
                "time":str(time_now),
                "title":user_blog["title"],
                "blog":user_blog["blog"],
                "img":image_json["secure_url"],
                "likes":0,
                "comments":0        
                }

        else:
            user_posts_saved = {
                "_id":uuid.uuid4().hex,
                "name":str(session['user']['name']),
                "email":str(session['user']['email']),
                "phone":str(session['user']['phone']),
                "date":str(date_today),
                "time":str(time_now),
                "title":user_blog["title"],
                "blog":user_blog["blog"],
                "img":user_blog['img'],
                "likes":0,
                "comments":0        
                }

        # Find the post and save the published post        
        if db1.Posts.find_one({"_id":user_blog["_id"]}):
            db1.Posts.delete_one({"_id":user_blog["_id"]})
            db1.Saved_posts.insert_one(user_posts_saved)
            nosb = db2.Login.find_one({'name':session['user']['name']})['saved_blogs']
            nob = db2.Login.find_one({'name':session['user']['name']})['submitted_blogs']
            if db2.Login.update_many({'name':session['user']['name']},{"$set":{"saved_blogs": nosb+1}}) and db2.Login.update_many({'name':session['user']['name']},{"$set":{"submitted_blogs": nob-1}}):
                return "success"
        
        # Find the saved post and update it
        elif db1.Saved_posts.find_one({"_id":user_blog["_id"]}):
            del user_posts_saved["_id"]
            if db1.Saved_posts.update_one({"_id":user_blog["_id"]},{"$set":user_posts_saved }):
                return "success"
        return "failed"       

        # Save the post if not saved anywhere
        db1.Saved_posts.insert_one(user_posts_saved)
        nosb = db2.Login.find_one({'name':session['user']['name']})['saved_blogs']
        if db2.Login.update_many({'name':session['user']['name']},{"$set":{"saved_blogs": nosb+1}}):
            return "success"
        return "failed;"

    def delete_account(self,user): # Checked

        # Checking if the User exists in the Database
        if db2.Login.find_one({'name':user}):
            
            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")

            # Generate OTP and adding to session
            session['otp'] = self.generate_otp()
            print("OTP Generated")

            # Send the message to the users email
            msg = Message('OTP Verification',sender =os.getenv('EMAIL_ID'),recipients = [session["user"]["email"]])
            msg.body = "Dear MindSpace User,\n Your One Time PIN(OTP) for Account Deletion is: "+session["otp"]+"\n\nGenerated at " + date_today + " " + time_now + "\nThis is an auto-generated email. Do not reply to this email."
            mail.send(msg)
            
            # Delete_acc Added to session for otp verification
            session['delete_acc'] = user
            return "success"
        else:
            return "failed"
    

    def change_password(self,user,new_pass,confirm_new_pass): # Checked

        # Extract data from user
        user_data = db2.Login.find_one({"name":user})
        
        # Check if the new password matches the confirm password
        if new_pass and confirm_new_pass:
            if new_pass == confirm_new_pass:
                if pbkdf2_sha256.verify(new_pass,user_data["password"])==True:
                    return "New password matches the old password"
            else:
                return "Password doesn't match!"
        
        # Check if user exists in the Database
        if db2.Login.find_one({'name': user}):
            
            # Extract current date and time
            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
            
            # Generate OTP and add it to session
            session['otp'] = self.generate_otp()
            print("OTP Generated")

            # Generate message and send it to the email
            msg = Message('OTP Verification',sender =os.getenv('EMAIL_ID'),recipients = [session["user"]["email"]])
            msg.body = "Dear MindSpace User,\n Your One Time PIN(OTP) for MindSpace Verification is: "+session["otp"]+"\n\nGenerated at " + date_today + " " + time_now + "\nThis is an auto-generated email. Do not reply to this email."
            mail.send(msg)

            # Add new_pass in session for otp verification
            session['new_pass'] = pbkdf2_sha256.encrypt(new_pass)            
            return "success"
        else:
            return "failed"

    def two_factor_authenticate(self,user): 

        # Extract User Data from database
        user_data = db2.Login.find_one({"name":user})
        
        if db2.Login.find_one({'name': user}):

            # Todays date and time
            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")

            # Generate otp and add it to the session
            session['otp'] = self.generate_otp()
            print("OTP Generated")
            
            # Generate message and send it to the email
            msg = Message('OTP Verification',sender =os.getenv('EMAIL_ID'),recipients = [session["user"]["email"]])
            msg.body = "Dear MindSpace User,\n Your One Time PIN(OTP) for MindSpace Verification is: "+session["otp"]+"\n\nGenerated at " + date_today + " " + time_now + "\nThis is an auto-generated email. Do not reply to this email."
            mail.send(msg)

            # Add two_factor_auth to session for otp verification
            session['two_factor_auth'] = True
            return "success"
        else:
            return "failed" 

    def login_two_factor_auth(self):
        print("Two Factor Authentication Satrting")
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        # Otp generated and added to session
        session['otp'] = self.generate_otp()
        print(session['otp'])
        msg = Message('OTP Verification',sender =os.getenv('EMAIL_ID'),recipients = [session['email']])
        msg.body = "Dear MindSpace User,\n Your One Time PIN(OTP) for MindSpace Verification is: "+session["otp"]+"\n\n" + date_today +"\n"+ time_now + "\nThis is an auto-generated email. Do not reply to this email."
        mail.send(msg)
        session['login_two_factor'] = True
        return "success"
    
    def disable_two_factor_authenticate(self,user):
        user_data = db2.Login.find_one({"name":user})
        
        if db2.Login.find_one({'name': user}):
            print("PASSSED1")
            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
            # try:
            print("PASSED OTP0")
            session['otp'] = self.generate_otp()
            print(session['otp'])
            print("OTP Generated")
            msg = Message('OTP Verification',sender =os.getenv('EMAIL_ID'),recipients = [session["user"]["email"]])
            msg.body = "Dear MindSpace User,\n Your One Time PIN(OTP) for MindSpace Verification is: "+session["otp"]+"\n\nGenerated at " + date_today + " " + time_now + "\nThis is an auto-generated email. Do not reply to this email."
            mail.send(msg)
            session['two_factor_auth'] = False
            return "success"
        else:
            return "failed" 