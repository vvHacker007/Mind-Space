from flask import Flask,jsonify,request,session,redirect
from passlib.hash import pbkdf2_sha256
import uuid
from app import db
import datetime
from dateutil.relativedelta import relativedelta, MO
import time
from cryptography.fernet import Fernet
from text_summarizer import summarize
import math, random
import smtplib

class User:
    def generate_otp(self) :
        digits = "0123456789"
        OTP = ""
        for i in range(6) :
            OTP += digits[math.floor(random.random()*10)]
        return OTP
    
    def start_session(self,user):
        del user['password']
        del user['birthdate']
        session['logged_in'] = True
        session['user'] = user
        session.permanent = True
        # app.permanent_session_lifetime = timedelta(minutes=5)
        return "success"

    def signup(self,form):
        print(request.form)

        # Create the user object
        user = {
            "_id":uuid.uuid4().hex,
            "name":form.username.data,
            "email":form.email.data,
            "password":form.password.data,
            "phone":form.phone.data,
            "birthdate":str(form.birthdate.data),
            "submitted_blogs":0,
            "saved_blogs":0,
            "followers":0,
            "profile-pic":"",
            "following":0
        }
        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
            
        if db.Login.find_one({'name': form.username.data}):
            return "failed"
        elif db.Login.find_one({'email': form.email.data}):
            return "failed"
        elif len(str(form.phone.data))<=6:
            return "failed"
        elif len(str(form.phone.data))>=12:
            return "failed"
        elif db.Login.find_one({'phone': form.phone.data}):
            return "failed"
        elif form.password.data != form.confirm_pass.data:
            return "failed"
        elif len(form.password.data)<5 and len(form.confirm_pass.data)<5:
            return "failed"
        elif len(form.password.data)>20 and len(form.confirm_pass.data)>20:
            return "failed"
        if db.Login.find_one(str(user["email"]))==None:
            print("PASSSED1")
            today = datetime.date.today()
            date_today = today.strftime("%B %d, %Y")
            time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
            # try:
            print("PASSED OTP0")
            session['otp'] = self.generate_otp()
            session['user_signup'] = user
            print(session['otp'])
            print(session['user_signup'])
            print("OTP Generated")
            server = smtplib.SMTP("smtp.gmail.com" , 587)
            server.ehlo()
            server.starttls()
            print("PASSED OTP1")
            server.login('mindspaceblogging@gmail.com','Mind_Space@007')
            print("PASSED OTP2")
            message = "Dear MindSDpace User,\n Your One Time PIN(OTP) for MindSpace Registration is: "+session["otp"]+"\n\n(Generated at " + date_today + time_now + "\nThis is an auto-generated email. Do not reply to this email."
            print(message)
            print("PASSED OTP3")
            server.sendmail('mindspaceblogging@gmail.com',user["email"],message)
            print("OTP sent succesfully..")
            server.quit()
            return "success"
            # except:
            #     return "failed_otp"
        print("YOU FAILED")
        return "failed"

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self,form,flag):
        print(flag)
        if flag==0:
            print("REACHED SUCCESS1")
            user = db.Login.find_one({"email": form.email.data})
        elif flag==1:
            print("REACHED SUCCESS2")
            user = db.Login.find_one({"name": form.email.data})
        print(user)
        print(pbkdf2_sha256.verify(form.password.data, user['password']))
        if user and pbkdf2_sha256.verify(form.password.data, user['password'])==True:
            print("REACHED SUCCESS3")
            self.start_session(user)
            return "success"    
        return "failed"
    
    def create_post(self,form,user):
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        form.content.data = form.content.data.replace(r"\n", "\t")
        content_summary = summarize(form.content.data) 
        user_posts = {
            "_id":uuid.uuid4().hex,
            "name":str(session['user']['name']),
            "email":str(session['user']['email']),
            "phone":str(session['user']['phone']),
            "date":str(date_today),
            "time":str(time_now),
            "title":str(form.title.data),
            "blog":str(form.content.data),
            "summary":str(content_summary),
            "likes":0,
            "comments":0
        }
        
        db.Posts.insert_one(user_posts)
        nob = db.Login.find_one({'name':session['user']['name']})['submitted_blogs']
        if db.Login.update_many({'name':session['user']['name']},{"$set":{"submitted_blogs": nob+1}}):
            return "success"
        return "failed"
    
    def save_post(self,form,user):
        today = datetime.date.today()
        date_today = today.strftime("%B %d, %Y")
        time_now = str(time.strftime("%I:%M:%S %p,", time.gmtime())) + str(" GMT")
        user_posts_saved = {
            "_id":uuid.uuid4().hex,
            "name":str(session['user']['name']),
            "email":str(session['user']['email']),
            "phone":str(session['user']['phone']),
            "date":str(date_today),
            "time":str(time_now),
            "title":str(form.title.data),
            "blog":str(form.content.data),
        }
        db.Saved_posts.insert_one(user_posts_saved)
        nosb = db.Login.find_one({'name':session['user']['name']})['saved_blogs']
        db.Login.update_many({'name':session['user']['name']},{"$set":{"saved_blogs": nosb+1}})
