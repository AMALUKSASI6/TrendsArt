from flask import *
from database import *
admin=Blueprint('admin',__name__)

@admin.route('/admin_home') 
def admin_home():
	return render_template('admin_home.html')

@admin.route('/complaint')
def complaint():
	data={}
	q="select * from complaint inner join user using(user_id)"
	res=select(q)
	data['complaint']=res
	return render_template('admin_view_complaint.html',data=data)

@admin.route('/replay',methods=['get','post'])
def replay():
	cid=request.args['cid']
	if 'submit' in request.form:
		replay=request.form['replay']
		q="update complaint set reply_description='%s' where complaint_id='%s'"%(replay,cid)
		update(q)
		flash("send reply successfully")

		return redirect(url_for('admin.complaint'))

	return render_template('admin_send_replay.html') 


@admin.route('/admin_view_artist')
def admin_view_artist():
	data={}
	q="select * from artist inner join login using(login_id)"
	res=select(q)
	data['art']=res
	if 'action' in request.args:
		action=request.args['action']
		login_id=request.args['login_id']
	else:
		action=None
	if action=="accept":
		q="update login set user_type='artist' where login_id='%s'"%(login_id)
		update(q)
		return redirect(url_for('admin.admin_view_artist'))
	if action=="reject":
		q="update login set user_type='reject' where login_id='%s'"%(login_id)
		update(q)
		return redirect(url_for('admin.admin_view_artist'))
					
	return render_template('admin_view_artist.html',data=data)


@admin.route('/manage_category',methods=['get','post'])
def manage_category():
	if 'submit' in request.form:
		category=request.form['category']
		q="insert into category values(null,'%s')"%(category)
		insert(q)

	data={}
	q="select * from category"
	res=select(q)
	data['category']=res


	if 'action' in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None
	if action=="delete":
		q="delete from category where category_id='%s'"%(cid)
		delete(q)
		flash("delete successfully")

		return redirect(url_for('admin.manage_category'))

	if action=="update":
		q="select * from category where category_id='%s'" %(cid)
		res=select(q)
		data['cate']=res
	if 'update' in request.form:
		category=request.form['category']
		q="update category set categoryname='%s' where category_id='%s'" %(category,cid)
		update(q)
		flash("updated successfully")

		return redirect(url_for('admin.manage_category'))



	return render_template('admin_managecategory.html',data=data)

		
	


@admin.route('/admin_view_user')
def admin_view_user():
	data={}
	q="select * from user"
	res=select(q)
	data['art']=res
	if 'action' in request.args:
		action=request.args['action']
		login_id=request.args['login_id']
	else:
		action=None
	if action=="accept":
		q="update login set user_type='artist' where login_id='%s'"%(login_id)
		update(q)
	if action=="reject":
		q="update login set user_type='reject' where login_id='%s'"%(login_id)
		update(q)
	return render_template('admin_view_user.html',data=data)




@admin.route('/admin_manage_art',methods=['get','post'])
def admin_manage_art():
	data={}
	# uid=session['uid']
 #    artistid=request.args['artist_id']
	
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
		# art=request.args['art']
		#amt=request.args['amt']
	else:
		action=None

	
	if action=="delete":
		q="delete from arts where art_id='%s' and work_status='pending'"%(aid)
		delete(q)
        #flash("delete successfully")
	

	
		return redirect(url_for('admin.admin_manage_art'))
	return render_template('admin_manage_art.html',data=data)

