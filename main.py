#!/usr/bin/python
import pymongo
from bson.objectid import ObjectId
import datetime
from flask import Flask, request, render_template, url_for, flash, redirect, session,make_response,jsonify
from functools import wraps,update_wrapper
from pymongo import MongoClient
from wsgiref.handlers import format_date_time

client = MongoClient()
db = client.test


app = Flask(__name__, static_url_path='')
app.secret_key="secret"

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)



def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged' in session:
			return f(*args,**kwargs)
		else:
			flash('Please Login first')
			return redirect(url_for('login'))		
	return wrap

def admin_login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'admin_logged' in session:
			return f(*args,**kwargs)
		else:
			flash('Please Login first')
			return redirect(url_for('admin'))		
	return wrap


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")		#Why some functions are called without being called. Just Calling them *************************************************
def home():
	title="Abhinav's Creation"
	people=db.people
	data=db.data
	admin=db.admin
	admin.insert({'name':'tanmay','password':'aha3d'})
	#Can Insert here for more admins.
	#SHOULD BE UNIQUE
	#people.insert({'name':'Abhinav','place':'YoYo'})
	return render_template('index.html',title=title)		#make a home page

@app.route("/login", methods=['GET','POST'])
def login():
	error=None;
	
	if (request.method=='POST'):
		name=request.form['username']
		password=request.form['password']
		if(db.people.find({'name':name,'password':password}).count()>=1):
			session['logged']=True
			session['name'] = name
			#flash('Logged in')
			return redirect(url_for('user',name=name))#********************************name by POST
		else:
			flash('Invalid Credentials')
			error="Invalid Credentials"
			render_template('login.html',title='login',error=error)
	return render_template('login.html',title='login',error=error)
		

@app.route("/admin",methods=['GET','POST'])
def admin():
	error=None;
	if (request.method=='POST'):
		name=request.form['username']
		password=request.form['password']
		if(db.admin.find({'name':name,'password':password}).count()>=1):#************************WORKS ONLY FOR ONE USER
			session['admin_logged']=True
			return redirect(url_for('admin_main'))
		else:
			flash('Invalid Credentials')
			error="Invalid Credentials"
			return render_template('admin.html',title='Admin',error=error)
	return render_template('admin.html',title='Admin',error=error)

@app.route("/admin_main",methods=['GET','POST'])
@admin_login_required
@nocache
def admin_main():
	dlr=db.people.find()
	ans=None
	detail=None
	if (request.method=='POST'):
		dealer=request.form['dealers']
		ans=db.data.find({'name':dealer})
		detail=db.people.find({'name':dealer})
		return render_template('admin_main.html',title='Admin',ans=ans,dlr=dlr,detail=detail[0])
	return render_template('admin_main.html',title='Admin',ans=ans,dlr=dlr)
	

@app.route("/user",methods=['GET','POST'])
@login_required
@nocache
def user():
	name=request.args['name']
	name=session['name']
	#name=request.args.get('name')
	#import pdb; pdb.set_trace()
	a=db.people.find({'name':name})
	#pwd=a.password
	#See how to submit two forms. Change in Arguments..***************************************************
	if (request.method=='POST'):
		name_user=request.form['name_user']
		mob=request.form['mob']
		email=request.form['email']
		deal=request.form['deal']
		comments=request.form['comments']
		#k=name_user+mob+name+email
		db.data.insert({'name':name,'name_user':name_user,'mob':mob,'email':email,'deal':deal,'comments':comments})#**********************************Id how to use default one/////////////////////////////
	rows=db.data.find({'name':name})
	return render_template('user.html',rows=rows,user=a[0],title="User "+name)
	


@app.route("/logout")
@login_required
#@nocache
def logout():
	
	session.pop('logged',None)
	#response.headers['Cache-Control'] = 'no-cache'
	flash("Logged out")
	return redirect(url_for('home'))	#Displaying Messages - HOW ***************************************************Best by Flash??

@app.route("/admin_logout")
@admin_login_required
#@nocache
def admin_logout():
	
	session.pop('admin_logged',None)
	#response.headers['Cache-Control'] = 'no-cache'
	flash("Logged out")
	return redirect(url_for('home'))

@app.route("/signup", methods=['GET','POST'])
def signup():
	session.pop('logged',None)
	flash1=None
	error=None
	if(request.method=='POST'):
		name=request.form['username']
		if(db.people.find({'name':name}).count()>=1):
			#flash1=""
			flash('Choose other name, Name Already Taken')
			return render_template('signup.html',title='signup',error=error,flash=flash1)
		else:
			flash('User signed up')
			db.people.insert({'name':name,'password':request.form['password'],'full_name':request.form['full_name'],'email':request.form['dlr_email'],'mob':request.form['mob']})
			return redirect(url_for('home'))
	return render_template('signup.html',title='signup',error=error,flash=flash1)

@app.route("/update_comment")
def update_comment():
	comments1 = request.args.get('comment', type=str)
	comments1=comments1.replace('&nbsp;',' ')
	comments1=comments1.replace('<br>','   ')
	print comments1
	id1=request.args.get('id')
	db.data.update(
   	{ '_id': ObjectId(id1) },
   	{ '$set':
      	{
        	'comments': comments1
      	}
    })
	data={"comments":comments1,"id1":id1}
	return jsonify(data)

@app.route("/update_deal")
def  update_deal():
	deal = request.args.get('deal')
	id1=request.args.get('id')
	db.data.update(
		
   	{ '_id': ObjectId(id1)  },
   	{ '$set':
      	{
        	'deal': deal
      	}})
	data={"deal":deal,"id1":id1}
	return jsonify(data)


if __name__ == "__main__":
	app.run(debug=True)