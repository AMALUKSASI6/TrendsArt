from flask import *
from database import *
public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
	if 'login' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'"%(username,password)
		res=select(q)
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['user_type']=="admin":
				return redirect(url_for('admin.admin_home'))

			elif res[0]['user_type']=="artist":
				q="select * from artist where login_id='%s'" %(session['lid'])
				res=select(q)
				session['aid']=res[0]['artist_id']
				return redirect(url_for('artist.artist_home'))

			elif res[0]['user_type']=="reject":
				flash("you are a rejected artist.")
				
			
			elif res[0]['user_type']=="user":
				q="select *from user where login_id='%s'" %(session['lid'])
				res=select(q)
				session['uid']=res[0]['user_id']
				return redirect(url_for('user.user_home'))
		else:
			flash("enter correct username and password")

				

	return render_template('login.html')




@public.route('/artistregistration',methods=['get','post'])
def artistregistration():
	if 'submit'	in request.form:
		firstname=request.form['fname']
		Lastname=request.form['lname']
		phone=request.form['phone']
		Email=request.form['email']
		username=request.form['username']
		password=request.form['password']
		q="insert into login values(null,'%s','%s','pending')"%(username,password)
		id=insert(q)
		q="insert into artist values(null,'%s','%s','%s','%s','%s')"%(id,firstname,Lastname,phone,Email)
		insert(q)
		flash("registration successfully")
		
	return render_template('artistregistration.html')



@public.route('/userregistration',methods=['get','post'])
def userregistration():
	if "register" in request.form:
		firstname=request.form['fname']
		Lastname=request.form['lname']
		latitude=request.form['latitude']
		longitude=request.form['longitude']
		phone=request.form['phone']
		Email=request.form['email']
		username=request.form['username']
		password=request.form['password']

		q="insert into login values(null,'%s','%s','user')"%(username,password)
		id=insert(q)
		q="insert into user values(null,'%s','%s','%s','%s','%s','%s','%s')"%(id,firstname,Lastname,latitude,longitude,phone,Email)
		insert(q)
		flash("registration successfully")	
	return render_template('user_registration.html')

@public.route('/public_view_art',methods=['get','post'])
def public_view_art():
	data={}
	# uid=session['uid']
	# artistid=request.args['artist_id']
	
	q="select * from category"
	res=select(q)
	data['cat']=res
	print(res)
     
	q="SELECT * FROM arts INNER JOIN artist USING(artist_id)"
	res=select(q)
	data['art']=res
	print(res)
	

	if 'search' in request.form:
		cat=request.form['cat']
		q="SELECT * FROM arts INNER JOIN artist USING(artist_id) where category_id='%s'"%(cat)
		res=select(q)
		data['search']=select(q)
		

	
	if'action' in request.args:
		action=request.args['action']
		aid=request.args['aid']
		art=request.args['art']
		amt=request.args['amt']
	else:
		action=None

	if action=="add_to_cart":
		q="SELECT * FROM `order`  WHERE user_id='%s' AND artist_id='%s' and order_status='pending' "%(uid,aid)
		res=select(q)
		if res:
			ids=res[0]['order_id']
			q="update `order` set amount=amount+'%s' where order_id='%s'"%(amt,ids)
			update(q)
			flash("updated")
		else:
			q="insert into `order` values(null,'%s','%s',curdate(),'pending','%s')"%(uid,aid,amt)
			ids=insert(q)
		q="SELECT * FROM `orderdetails`  WHERE order_id='%s' AND art_id='%s' "%(ids,art)
		res=select(q)
		if res:
			flash("updated")
		else:
			q="insert into orderdetails values(null,'%s','%s')"%(ids,art)
			insert(q)
			flash("added")
		return redirect(url_for('public.public_view_art'))
	return render_template('public_view_art.html',data=data)

