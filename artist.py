from flask import *
from database import *
import uuid
artist=Blueprint('artist',__name__)

@artist.route('/artist_home') 
def artist_home():
	return render_template('artist_home.html')

@artist.route('/art_upload')
def art_upload():
	return render_template('art_upload.html')

@artist.route('/artupload',methods=['get','post'])
def artupload():
	id=session['aid']
	data={}
	q="select * from arts inner join category using(category_id) where artist_id='%s'" %(id)
	res=select(q)
	data['art']=res
	
	q="select * from category"
	res=select(q)
	data['cat']=res

	if "submit" in request.form:
		workname=request.form['workname']
		workdescription=request.form['description']
		images=request.files['img']
		path="static/uploads/"+str(uuid.uuid4())+images.filename
		images.save(path)
		price=request.form['price']
		catname=request.form['cat']		
		q="insert into arts values(null,'%s','%s','%s','%s',curdate(),'%s','pending','%s')"%(id,workname,workdescription,path,price,catname)
		insert(q)
		flash("upload successfully")
		return redirect(url_for('artist.artupload'))


	if 'action' in request.args:
		action=request.args['action']
		art_id=request.args['art_id']
	else:
		action=None

	if action=="delete":
		q="delete from arts where art_id='%s'"%(art_id)
		delete(q)
		flash("delete successfully")
		return redirect(url_for('artist.artupload'))	
	return render_template('art_upload.html',data=data)



@artist.route('/artist_view_cutomiseddesign',methods=['get','post'])
def artist_view_cutomiseddesign():
	data={}
	aid=session['aid']
	q="select * from customiseddesign inner join user using(user_id) where artist_id='%s'"%(aid)
	res=select(q)
	data['art']=res
	if 'action' in request.args:
		action=request.args['action']
		did=request.args['did']
	else:
		action=None
	if action=="accept":
		q="update customiseddesign set status='accept' where cdesign_id='%s'"%(did)
		update(q)
	if action=="reject":
		q="update customiseddesign set status='reject' where cdesign_id='%s'"%(did)
		update(q)
		return redirect(url_for('artist.artist_view_cutomiseddesign'))
	return render_template('artist_view_customiseddesign.html',data=data)

@artist.route('/artist_view_order',methods=['get','post'])
def artist_view_order():
	data={}
	aid=session['aid']
	q="SELECT * FROM `order` INNER JOIN `user` USING(user_id) INNER JOIN `orderdetails` USING(`order_id`) where artist_id='%s' and order_status='paid'"%(aid)
	print(q)	
	res=select(q)
	data['order']=res
	return render_template('artist_view_order.html',data=data)	

@artist.route('/artist_view_payment',methods=['get','post'])
def artist_view_payment():
	data={}
	q="SELECT * FROM `payment` INNER JOIN `user` USING(user_id)"	
	res=select(q)
	data['payment']=res
	return render_template('artist_view_payment.html',data=data)	

@artist.route('/artist_view_art',methods=['get','post'])
def artist_view_art():
	oid=request.args['oid']
	aid=request.args['aid']
	data={}
	q="SELECT * from arts inner join orderdetails using(art_id) where order_id='%s' and art_id='%s'"%(oid,aid)	
	res=select(q)
	data['art']=res
	print(res)
	return render_template('artist_view_art.html',data=data)



@artist.route('/artist_custom_payment',methods=['get','post'])
def artist_custom_payment():
	cid=request.args['cid']
	data={}
	if 'submit' in request.form:
		payment=request.form['payment']
		q="update customiseddesign set amt='%s' where cdesign_id='%s'"%(payment,cid)
		update(q)
		flash("AMOUNT ADDED")
		return redirect(url_for('artist.artist_view_cutomiseddesign'))
	return render_template('artist_custom_payment.html',data=data)


