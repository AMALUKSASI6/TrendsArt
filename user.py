from flask import *
from database import *
import uuid
user=Blueprint('user',__name__)

@user.route('/user_home') 
def user_home():
	return render_template('user_home.html')


@user.route('/user_view_art',methods=['get','post'])
def user_view_art():
	data={}
	uid=session['uid']
	# artistid=request.args['artist_id']
	
	q="select * from category"
	res=select(q)
	data['cat']=res
	print(res)
     
	q="SELECT * FROM arts INNER JOIN artist USING(artist_id) INNER JOIN login USING(login_id) WHERE user_type='artist' and work_status='pending'"
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
		return redirect(url_for('user.user_view_art'))
	return render_template('user_view_art.html',data=data)


@user.route('/user_complaint',methods=['get','post'])
def user_complaint():
	uid=session['uid']
	if 'submit' in request.form:
		complaint=request.form['complaint']
		q="insert into complaint values(null,'%s','%s','pending',now())"%(uid,complaint)
		insert(q)
		flash("send complaint successfully")
	data={}
	q="select * from complaint where user_id='%s'"%(uid)
	res=select(q)
	data['replay']=res
	return render_template('complaint.html',data=data)

@user.route('/customiseddesign',methods=['get','post'])
def customiseddesign():
	data={}
	q="select * from artist INNER JOIN login USING(login_id) WHERE user_type='artist'"
	res=select(q)
	data['artist']=res
	print(res)

	uid=session['uid']
	if 'booking' in request.form:
		a=request.form['a_id']
		design=request.form['design']
		description=request.form['description']
		images=request.files['img']
		path="static/upload/"+str(uuid.uuid4())+images.filename
		images.save(path)
		q="insert into customiseddesign values(null,'%s','%s','%s','%s',curdate(),'pending','%s','pending')"%(uid,a,design,description,path)
		insert(q)
		# q="select * from customiseddesign where user_id='%s'"%(uid)
		# res=select(q)
	
	q="select * from customiseddesign where user_id='%s'"%(uid)
	res=select(q)
	data['art']=res
	return render_template('customiseddesign.html',data=data)


@user.route('/user_make_payment',methods=['get','post'])
def user_make_payment():
	data={}
	aid=request.args['aid']
	art=request.args['art']
	uid=session['uid']
	q="select * from  arts where art_id='%s'"%(art)
	res=select(q)
	data['pay']=res

	if 'pay' in request.form:
		amt=request.form['amt']
		q="insert into `order` values(null,'%s','%s',curdate(),'paid','%s')"%(uid,aid,amt)
		ids=insert(q)
		q="insert into orderdetails values(null,'%s','%s')"%(ids,art)
		insert(q)
		q="insert into payment values(null,'%s','%s','Order','%s',curdate())"%(ids,uid,amt)
		insert(q)
		q="update arts set work_status='selled' where art_id='%s' "%(art)
		update(q)
		flash("payment successfully")
		
		return redirect(url_for('user.user_view_art'))
	return render_template("user_make_payment.html",data=data)



@user.route('/user_view_addtoart',methods=['get','post'])
def user_view_addtoart():
	data={}
	uid=session['uid']
	q="SELECT * FROM `order` INNER JOIN orderdetails USING(order_id) INNER JOIN arts USING (art_id)  WHERE user_id='%s' and work_status='pending' "%(uid)
	print(q)
	res=select(q)
	data['cart']=res

	return render_template("user_view_addtoart.html",data=data)







@user.route('/custom_payment',methods=['get','post'])
def custom_payment():
	data={}
	uid=session['uid']
	aid=request.args['aid']
	art=request.args['art']
	amt=request.args['amt']
	data['amt']=amt
	cdesign_id=request.args['cdesign_id']
	if 'pay' in request.form:
		q="INSERT INTO `payment` VALUES(NULL,'%s','%s','Custom','%s',CURDATE())"%(cdesign_id,uid,amt)
		insert(q)
		q="UPDATE `customiseddesign` SET `status`='Paid' WHERE `cdesign_id`='%s'"%(cdesign_id)
		update(q)
		return redirect(url_for("user.customiseddesign"))
		flash("payment successfully")
		# return redirect(url_for('user.customiseddesign'))
	return render_template("custom_payment.html",data=data)

