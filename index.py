from flask import Flask,render_template,session,url_for,redirect,request,jsonify,session,make_response
from flask_socketio import SocketIO
import pymysql
import os
import datetime
from random import randint
from werkzeug.utils import secure_filename
from summarize_text import first_class
from recomandation_engine import recomandation_engine
import nltk
import hashlib,binascii
import datetime
from bs4 import BeautifulSoup
from knn_recomand import classifier
from modify_html_content import get_modify,tokenization,dictionary_word
from dockfile import print_code_results
from pdf_class import pdf_class
from question_ans import QandA


app=Flask(__name__)
connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif','obj','mtl'])
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app.config['UPLOAD_FOLDER'] = "static/stuff_to_update/user_image"
app.config['MAX_CONTENT_PATH']=2028



##create the projects on the site an vote when you have problem to get helpet by comunity and to put question
the_dbs=[["users",10],["projects",23]]


@app.route("/sumar_create",methods=['POST','GET'])
def test_sumar():

    sumar_how_big=request.form['type']
    text=str(request.form['text'])
    i=0
    ##while i<=2:
    ##soup = BeautifulSoup(text,"html.parser")
##    text=soup.get_text()
        ##i+=1

    var=first_class()
    text=var.summar(text,int(sumar_how_big))
    ##print(text)
    return text


@app.route('/',methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/admin',methods=["POST","GET"])
def admin():
    return render_template("admin/admin.html")

@app.route('/login',methods=['POST','GET'])
def login():
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
       with connection.cursor() as con: 
	    sql="SELECT * FROM user_data"
	    con.execute(sql)
       connection.commit()
    finally:
       connection.close()   
    error=""
    global uname_general_user

    if request.method=='POST' :
        uname_pass = hashlib.sha256(request.form['pass']).hexdigest()

        for i in con.fetchall():          
            if request.form['uname']==i[1] and str(uname_pass)==str(i[2]):
                 uname_user=request.form['uname']
                 uname_pass=hashlib.sha256(request.form['pass']).hexdigest()              
		 connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
		 try:
		    with connection.cursor() as con: 
			 sqkl1="SELECT * FROM user_data WHERE uname=%(uname)s AND pass=%(pass)s"			      
		         con.execute(sqkl1, {'uname': uname_user,'pass':uname_pass})		
		         rewq=con.fetchall()
		    connection.commit()
		 finally:
		    connection.close()   
		 print(rewq)
                 session['connect']='connect'
                 connect=session['connect']
                 session['id']=i[0]
                 session['review']=i[10]
                 id12=session['id']
                 session['time']=datetime.datetime.now()
                 session.permanent=True
                 for i in rewq:
                    admin=i[9]
                    if admin==1:
                        return redirect(url_for("admin",id=session['id'],connect=connect,page='1'))
                    else:
                        id12=session['id']
                        uname_general_user=uname_user
                        return redirect(url_for('profile2',id=id12,connect=connect))
            else:
                       error="wrong name or password"
       
    return render_template('login.html',error=error)

@app.route("/logout",methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route('/register',methods=['POST','GET'])
def register():
    return render_template("register.html")

@app.route('/tutorials_out',methods=['POST','GET'])
def tutorials_out():
    return render_template("all_files_b_login/show_the_tutorials.html")

@app.route('/tutorials_to_see',methods=['POST','GET'])
def tutorials_to_see():
    id1=request.args['id_page']
    id_articol=request.args['id_articol']
##    the_tutorials=[[1,"An introduction in html","An introduction in html werewrwerew"],[2,"An introduction in html","An introduction in html werewrwerew"]]
    return render_template("all_files_b_login/tutorials.html",id1=id1,id_articol=id_articol)






@app.route('/profile',methods=['POST','GET'])
def profile():
    return render_template("profile_page/index.html")




@app.route('/masterpiece',methods=['POST','GET'])
def masterpiece():
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
       with connection.cursor() as con: 
	    select="SELECT * FROM masterpiece "
	    con.execute(select)  
            select_masterpiece=con.fetchall()
       connection.commit()
    finally:
       connection.close()  
    return render_template("masterpiece/masterpiece.html",select_masterpiece=select_masterpiece)


@app.route('/article_masterpiece_page',methods=['POST','GET'])
def article_masterpiece_page():
    id=request.args['id']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
       with connection.cursor() as con:
	    select="SELECT * FROM masterpiece_menu_id WHERE article_masterpiece_id="+str(id)
	    con.execute(select)
	    select_masterpiece=con.fetchall()
       connection.commit()
    finally:
       connection.close()  
    return render_template("masterpiece/article_masterpiece_page.html",select_masterpiece=select_masterpiece,id_article=id)

asd=recomandation_engine()
global new_asd
##new_asd=asd.get_data_mysql()
@app.route('/show_data_masterpiece',methods=['POST','GET'])
def show_data_masterpiece():
    article=request.args['article']
    masterpiece=request.args['masterpiece']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
       with connection.cursor() as con:
	    select="SELECT * FROM article_masterpiece_page WHERE id_masterpiece="+str(masterpiece)+" AND menu_id="+str(article)	 
	    con.execute(select)	    
	    select_masterpiece_data=con.fetchall()
       connection.commit()
       with connection.cursor() as con:
	    ##print(select_masterpiece_data[0][2])
	    select="SELECT * FROM masterpiece_menu_id WHERE article_masterpiece_id ="+str(masterpiece)+" AND article_id_to_show_data="+str(article)	     
	    con.execute(select)	  
	    select_title=con.fetchall()
       connection.commit()
       with connection.cursor() as con:
	    sql="SELECT * FROM recomand_engine_text_masterpiece WHERE id_user='"+str(session['id'])+"'"    
	    con.execute(sql)
	    sql=con.fetchall()
       connection.commit()
    finally:
       connection.close()   
    l=[]
    result=""
    for i in sql:
        l.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[9],i[10],i[11],i[12],i[14],i[15]])
    for i in select_masterpiece_data:
        cls_2=get_modify(i[2],l)
        result=cls_2.delete_tags_from_string()

    #for i in select_masterpiece_data:
        #for j in new_asd:
    #        if j[2]==session['id']:
        #        text__=i[2]
        #        soup = BeautifulSoup(text__)
        #        text__=soup.get_text()
                ##https://www.crummy.com/software/BeautifulSoup/bs4/doc/
            #    print(str(text__))
##                if int(j[3])==0:
##                    text__=text__.replace('<p>','')
##                    text__=text__.replace('</p>','')
##                if int(j[4])==0:
##                    text__=text__.replace('<hr/>','')
##                if int(j[5])==0:
##                    text__=text__.replace('<ul>','')
##                    text__=text__.replace('<ul/>','')
##                    text__=text__.replace('<li>','')
##                    text__=text__.replace('<li/>','')
##                if int(j[6])==0:
##                    text__=text__.replace('<ol>','')
##                    text__=text__.replace('<ol/>','')
##                    text__=text__.replace('<li>','')
##                    text__=text__.replace('<li/>','')
##                print(text__)




    return jsonify(select_masterpiece_data,result,select_title)






@app.route('/profile2',methods=['POST','GET'])
def profile2():
     id=request.args['id']
     id13=session['id']
     connect=session['connect']
     print_options=0
     if id13=="":
         return redirect(url_for('logout'))
##     if url=="":
##         return redirect(url_for('logout'))
     if id13==None :
         return redirect(url_for('logout'))
     if id==id13:
         return redirect(url_for('logout'))
     if request.args['connect'] != 'connect':
         return redirect(url_for('login'))
     if request.args['connect'] == '':
         return redirect(url_for('login'))
     if request.args['connect']=="" and request.args['id']=="" and session['connect']=="connect" and session['id']:
        return redirect(url_for('index'))
     if datetime.date.today()==session['time'].date():
         print_options=1
        ##https://bootsnipp.com/snippets/yNKEE
     return render_template("profile_page/index2.html",print_options=print_options)

@app.route('/popup',methods=['POST','GET'])
def popup():
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
       with connection.cursor() as con:
	    sql="SELECT * FROM tags"
	    con.execute(sql)
	    sql1=con.fetchall()
       connection.commit()
    finally:
       connection.close()    
    return render_template("popup/popup.html",sql1=sql1)

@app.route('/review_popup',methods=['POST','GET'])
def review_popup():
    var_4=request.get_json()

    var_1=var_4['color1']
    var_2=var_4['color2']
    var_3=var_4['knowledge']
    var_5=var_4['aligment'] ##sa nu convertesc culorile in decimal le pun asa si evaluez in functie de restul
    ##print(var_1,var_2,var_3,var_5)
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
       with connection.cursor() as con:
    		sql="UPDATE recomand_engine_text_masterpiece SET aligment='"+str(var_5)+"',background_text='"+var_1+"',text_color='"+str(var_2)+"' WHERE id_user='"+str(session['id'])+"'"      
                con.execute(sql)
       connection.commit()
    finally:
       connection.close()    
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
       with connection.cursor() as con:
    		sql_2="SELECT * FROM recomand_engine_text_masterpiece WHERE id_user='"+str(session['id'])+"'"
    		con.execute(sql_2)
    		sql_2=con.fetchall()
       connection.commit()
    finally:
       connection.close() 
    x=[]
    for i in sql_2:
        x.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[9],i[10],i[11],i[12],i[14],i[15]])
    cls__=classifier()
    user_predict=cls__.class_KNN([x])
    ##print(user_predict)
    for i in user_predict:
    ##    print(i[2])
	    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
	    try:
		with connection.cursor() as con:
			sql="UPDATE recomand_engine_text_masterpiece SET p="+str(i[2])+",hr="+str(i[3])+",ul="+str(i[4])+",ol="+str(i[5])+",table1="+str(i[6])+",tip_font="+str(i[7])+",img="+str(i[8])+",aligment="+str(i[9])+",font_size="+str(i[10])+",code_view="+str(i[11])+",video="+str(i[12])+",link="+str(i[13])+" WHERE id_user="+str(session['id'])+""	       
			con.execute(sql)
		connection.commit()
	    finally:
	    	connection.close()  
    ##cls__.replace_data_predicted(session['id'])
    return "this"


@app.route('/data_comunity_upload',methods=['POST','GET'])
def data_comunity_upload():
    var_1=request.form['title']
    var_2=request.form['descrep']
    var_3=request.form['require']
    var_4=request.form['price']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
		 sqkl1="INSERT INTO comunity VALUES('0',%(var_4)s,'//placeimg.com/280/180/tech',%(var_1)s,%(var_2)s,'','0',%(seseid)s,'0','0',%(var_3)s)"			      
		 con.execute(sqkl1, {'var_1': var_1,'var_2':var_2,'seseid':session['id'],'var_3':var_3,'var_4':var_4})	
   		## sql="INSERT INTO comunity VALUES('0','"+str(var_4)+"','//placeimg.com/280/180/tech','"+str(var_1)+"','"+str(var_2)+"','','0','"+str(session['id'])+"','0','0','"+str(var_3)+"')"       
    		## con.execute(sql)
        connection.commit()
    finally:
    	connection.close()  
    return "connected"

@app.route('/tutorials',methods=['POST','GET'])
def tutorials():
    id_page=request.args['id_page']
    id_articol=request.args['id_articol']
    return render_template("profile_page/tutorials.html",id_page=id_page,id_articol=id_articol)

@app.route('/code_editor',methods=['POST','GET'])
def code_editor():
##    code=request.args['code']
##    sql="SELECT * FROM code_editor WHERE code='"+str(code)+"'"
##    con.execute(sql)
##    code_fecth=con.fetchall()
    return render_template("profile_page/code_editor.html")


@app.route('/community',methods=['POST','GET'])
def community():
    return render_template("community/community.html")



@app.route('/update_data_from_masterpiece',methods=['POST','GET'])
def update_data_from_masterpiece():
    id_article=request.form['id_article']
    id_page=request.form['id_page']
    html_data=request.form['html']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
	    sql="UPDATE article_masterpiece_page SET data=%s WHERE id_masterpiece=%s AND menu_id=%s"
	    args=(html_data,id_page,id_article)	  
    	    con.execute(sql,args)
	connection.commit()
    finally:
    	connection.close()   
    ##get_data=request.args["text"]
##    sel="UPDATE  FROM article_masterpiece_page SET "
##    con.execute(sel)
    return id_article,id_page




@app.route("/select_from_community",methods=['GET','POST'])
def select_from_community():
    limit1=request.args['limit1']
    limit2=request.args['limit2']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
		sel="SELECT * FROM comunity WHERE user_id='"+str(session['id'])+"' LIMIT "+limit1+","+limit2
		con.execute(sel)
		fetch=con.fetchall()
	connection.commit()
    finally:
    	connection.close()      
    return jsonify(fetch)


@app.route("/select_from_community_2",methods=['GET','POST'])
def select_from_community_2():
    limit1=request.args['id']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
	    sel="SELECT * FROM comunity WHERE id="+str(limit1)+""
	    con.execute(sel)
	    fetch=con.fetchall()
	connection.commit()
    finally:
    	connection.close()     
    
    ##print(fetch)
    return jsonify(fetch)

@app.route("/show_comunity_article",methods=['POST','GET'])
def show_comunity_article():
    return render_template("community/show_comunity_article.html")


@app.route("/select_from_community__tutorials",methods=["POST","GET"])
def select_from_community__tutorials():
    id_send=request.args['id_send']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
    		sql="SELECT * FROM comunity_tutorial WHERE id_comunity_tutorial="+str(id_send)+""
	        con.execute(sql)
	        send_data=con.fetchall()
	connection.commit()
    finally:
    	connection.close()   

    return jsonify(send_data)



@app.route('/test',methods=["POST","GET"])
def test():
    test=request.args[id]
    session['id']=test
    return session['id']



@app.route('/select_from_tutorials',methods=['POST','GET'])
def select_from_tutorials():
    condidtion_mysql=request.args['condidtion_mysql']
    id1=request.args['id_page']
    id_articol=request.args['id_articol']
    ##print(condidtion_mysql)
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
    		sql="SELECT * FROM tutorials WHERE articol='"+str(id_articol)+"'"+condidtion_mysql
                con.execute(sql)
		tutorials=con.fetchall()
	connection.commit()
    finally:
    	connection.close()   
   
    
    return jsonify(tutorials)


@app.route('/select_programming_languages',methods=['POST','GET'])
def select_programming_languages():
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
    		sql="SELECT * FROM type_of_tutorials"
    		con.execute(sql)
		tut_progra=con.fetchall()
    	connection.commit()
    finally:
    	connection.close()      
    return jsonify(tut_progra);


@app.route('/select_user_data',methods=['POST','GET'])
def select_user_data():
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
    		sql="SELECT * FROM user_data WHERE id='"+str(session['id'])+"'"
    		con.execute(sql)
    		show=con.fetchall()
    	connection.commit()
    finally:
    	connection.close()   
    return jsonify(show)


@app.route('/requests_tab',methods=['POST','GET'])
def requests_tab():
	return render_template("popup/request_tab.html")


@app.route('/search_all',methods=['POST','GET'])
def search_for_all():
    find_out_data=request.args['search_parameter']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
    		sql="SELECT * FROM tutorials WHERE titlu LIKE '%"+find_out_data+"%' OR language LIKE '%"+find_out_data+"%'"   
		con.execute(sql)
		select=con.fetchall()
    	connection.commit()
    finally:
    	connection.close() 
    return jsonify(select)

@app.route('/select_data_post_tutorias',methods=['POST','GET'])
def select_data_post_tutorias():
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
    		sql="SELECT * FROM user_post_tutorials WHERE user_id='"+session['id']+"'"
	        con.execute(sql)
	        data=con.fetchall()
    	connection.commit()
    finally:
    	connection.close() 
    return jsonify(data)


@app.route('/games',methods=['POST','GET'])
def games():
    return render_template("/games/games.html")

@app.route('/game_play',methods=['POST','GET'])
def game_play():
    id_game=request.args['id_game']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
                sql="SELECT count(id) FROM problems"
                fetch = con.execute(sql)
		fetch = con.fetchall()
	connection.commit()
    finally:
        connection.close() 
    gen=0
    for i in fetch:
	gen=i
    print(gen[0])
    gen=randint(1, int(gen[0]))
    gen_a_game_id=randint(1, 12309)
    ##duel->1
    ##last_stand->2
    ##competitive->3
    ##contest->4
    now = datetime.datetime.now()
    print now.year, now.month, now.day, now.hour, now.minute, now.second
    time_start = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
    time_end = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+str(now.hour)+":"+str(now.minute+5)+":"+str(now.second)
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
                sql="INSERT INTO games_code_play VALUES('"+str(gen_a_game_id)+"','"+str(session['id'])+"','','','','','','"+str(id_game)+"','"+time_start+"','"+time_end+"','"+str(gen)+"','')"
                fetch = con.execute(sql)		
	connection.commit()
    finally:
        connection.close() 	

    return redirect(url_for("compile_python",default=0,id_problem=gen,game=id_game))



@app.route('/rooms_get',methods=['POST','GET'])
def rooms_get():
    id_game=request.args['id_game']
    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
    try:
	with connection.cursor() as con:
                sql="SELECT * FROM  games_code_play "
                fetch = con.execute(sql)
                fetch = con.fetchall()				
	connection.commit()
    finally:
        connection.close() 	
    return jsonify(fetch)

@app.route('/rooms',methods=['POST','GET'])
def rooms():
	game=request.args['id_game']
        connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
        try:
	   with connection.cursor() as con:
		        sql="DELETE  FROM  games_code_play WHERE time_end <= CURRENT_TIMESTAMP()"
		        con.execute(sql)
		       			
	   connection.commit()
        finally:
           connection.close() 	
	
	if int(game)==4:
	     return redirect(url_for("contest",id_game=game))
	else:	
	     return render_template("games/rooms.html")

@app.route('/room_add_player',methods=["POST","GET"])
def room_add_player():
	default=request.args['default']
	game=request.args['game']
	id_problem=request.args['id_problem']
	code_game=request.args['code_game']
        connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
        try:
	   with connection.cursor() as con:
		        sql="UPDATE games_code_play  SET id_user_2="+str(session['id'])+" WHERE id_game="+str(code_game)+" AND game_type_id="+str(game)
		        con.execute(sql)
		       			
	   connection.commit()
        finally:
           connection.close() 
	return redirect(url_for('compile_python',default=default,game=game,id_problem=id_problem))

@app.route('/contest',methods=['POST','GET'])
def contest():
	return render_template("games/contest.html")

@app.route('/back_upload2',methods=['POST','GET'])
def back_upload2():
     if request.method == 'POST':
        i=0
        f = request.files['file']
        file_path = os.path.join('static/stuff_to_update/user_image/', secure_filename(f.filename))
        file_path2 = os.path.join('static/stuff_to_update/user_image/', secure_filename(f.filename))
        exten=file_path[-3:]
        for i in ALLOWED_EXTENSIONS:
              if i==exten:
                f.save(file_path)
            ##    f.save(file_path)
                i=1
		connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
		try:
		     with connection.cursor() as con:
                	sql="UPDATE user_data SET img_pic='"+file_path2+"' WHERE id='"+str(session['id'])+"'"
                	con.execute(sql)
	 	     connection.commit()
		finally:
		     connection.close() 
        return redirect(url_for("profile2",id=session['id'],connect='connect'))


@app.route('/visualize_code',methods=['POST','GET'])
def visualize_code():
    take_page=request.args.get('id')
    if (take_page is not None) and (session['id'] is not None):
	connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
	try:
	    with connection.cursor() as con:
		sql="SELECT * FROM code_view WHERE id="+take_page     
		con.execute(sql)
		code_fet=con.fetchall()
	    connection.commit()
	finally:
            connection.close() 
    ##    import ast
    ##    for i in code_fet:
        ##    ast_object = ast.parse(i[1])
    ##    code = compile(ast_object, filename="", mode="exec")
    ##    Vars = {}
    ##    exec(code,globals(),Vars)
    ##    Result = Vars.get('Result')
    ##    print(Result)
        return render_template("codemirror/codemirror.html",code_fet=code_fet)
    else:
	connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
	try:
	    with connection.cursor() as con:
		sql="SELECT * FROM code_view "
		con.execute(sql)
		sql1=con.fetchall()
	    connection.commit()
	finally:
            connection.close() 
	connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
	try:
	    with connection.cursor() as con:
		sql2="SELECT * FROM user_data "	
		con.execute(sql2)
		sql2=con.fetchall()
	    connection.commit()
	finally:
            connection.close() 
        return render_template("not_working_page/not_working.html",sql1=sql1,sql2=sql2)


@app.route('/show_opinion',methods=['POST','GET'])
def show_opinion():
    return render_template("show_opinion.html")

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    sql="SELECT * FROM user_data "
    con=connection.cursor()
    con.execute(sql)
    con.close()
    sql=con.fetchall()
    return render_template("admin_folders/dashboard.html",sql=sql)

@app.route('/evaluate_word_send',methods=['POST','GET'])
def evaluate_word_send():
    word=request.args['word']
    cls_2=dictionary_word()
    result=cls_2.download_nltk_dictionary(word)
    ##sql="SELECT * FROM dictionary_programming_terms WHERE words LIKE '%"+str(word)+"%'"
##    con.execute(sql)
##    execute_sql=con.fetchall()
    return jsonify(result)

@app.route('/articles',methods=["POST","GET"])
def articles():
    sql="SELECT * FROM article_masterpiece_page "
    con=connection.cursor()
    con.execute(sql)
    con.close()
    sql=con.fetchall()
    return render_template("admin_folders/articles.html",sql=sql)


@app.route("/compile_python",methods=['POST','GET'])
def compile_python():
    if 'default' in request.args:
	default=request.args.get("default")
    else:
	default=1
    if 'game' in request.args:
    	game=request.args.get("game")	
    else:
	game=-1
    print(game)
    if 'id_problem' in request.args:
    	id_problem=request.args.get("id_problem")
    else:
	id_problem=-1
   
    if int(default) == 1 and int(id_problem)==-1:
	    code_id=request.args.get('code_id')
	    language=request.args.get('language')
	    if code_id!=None and language!=None:
		    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
		    try:
			with connection.cursor() as con:
		    	    sql="SELECT * FROM code_view WHERE id="+code_id+" AND language='"+language+"'"			    
			    con.execute(sql)
			    con.close()
			    fetch=con.fetchall()
			connection.commit()
		    finally:
			connection.close() 
	    return render_template("compile/python/compile.html",fetch=fetch,default=int(default),no_clock=True)

    if int(default)==0:
	if  int(id_problem)!=-1:
	    connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
	    try:
		with connection.cursor() as con:
			    sql="SELECT * FROM problems WHERE id='"+str(id_problem)+"'"
			    con.execute(sql)
			    fetc1=con.fetchall()
		connection.commit()
	    finally:
		connection.close() 
	    if int(game)!=-1:
	    	return render_template("compile/python/compile.html",default=int(default),id_problem=int(request.args["id_problem"]),fetc1=fetc1,game=int(game),no_clock=False)
	    elif int(game)==-1:
	    	return render_template("compile/python/compile.html",default=int(default),id_problem=int(request.args["id_problem"]),fetc1=fetc1,game=int(game),no_clock=False)		
	elif int(id_problem)==-1:
	    return render_template("compile/python/compile.html",default=int(default),id_problem=int(request.args["id_problem"]),no_clock=False)
    else:
	return "it was a parameter error"

    
	    
@app.route('/solve_problem',methods=['POST','GET'])
def solve_problem():
	id_problem=request.args['id_problem']
	return redirect(url_for('compile_python',id_problem=id_problem,default=0))

@app.route('/integration',methods=['POST','GET'])
def integration():
    sql="SELECT * FROM key_generated_for_api "
    con=connection.cursor()
    con.execute(sql)
    con.close()
    sql=con.fetchall()
    return render_template("admin_folders/integration_api.html",sql=sql)






@app.route('/code_analise',methods=['POST','GET'])
def code_analise():
    language=request.args['language']
    code_result=""
    if request.method=="POST":
	    code_to_put_file=request.get_json()
	    code_to_put_file=code_to_put_file['data']
	    
	    languages___=[
			["Python","/home/bogdan/Desktop/Code4YOU1-master/static/dockfile/python/",".py"],
			["Ruby","/home/bogdan/Desktop/Code4YOU1-master/static/dockfile/ruby/",".rb"],
			["Cpp","/home/bogdan/Desktop/Code4YOU1-master/static/dockfile/cpp/",".cpp"],
			["Bash","/home/bogdan/Desktop/Code4YOU1-master/static/dockfile/bash/",".sh"]
		      ]
	    
	    for i in languages___:
		if i[0]==language:
		    f = open(i[1]+"file"+i[2], "w")
		    f.write(code_to_put_file)
		    f.close()			
		    clf=print_code_results(i[1])
		    code_result=clf.show_result()[1]

    return code_result


@app.route('/index_compile',methods=['POST','GET'])
def index_compile():
	return render_template("compile/python/compile.html")

@app.route('/pdf_files',methods=['GET','POST'])
def pdf_files():
	id_article=request.args['id']
	show_=pdf_class(id_article)	
	return jsonify(show_.prelucrateData())


@app.route('/eval_problems',methods=['GET','POST'])
def eval_problems():
	id_article=request.args['id']
	if int(id_article)==1:
	    if request.method=="POST":
		    code_to_put_file=request.get_json()
		   ## code_to_put_file=code_to_put_file['data']
		    print(code_to_put_file)
	            connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
		    try:
		        with connection.cursor() as con:
				sql="INSERT INTO problems VALUES('','"+str(session['id'])+"','"+str(code_to_put_file['text_problem'])+"','"+str(code_to_put_file['problem_output'])+"','"+str(code_to_put_file['problem_code'])+"','"+str(code_to_put_file['problem_language'])+"','')"   
				con.execute(sql)				
			connection.commit()
		    finally:
		        connection.close() 
		
	return "Succes"


@app.route('/create_masterpiece',methods=['POST','GET'])
def create_masterpiece():
	masterpiece_name=request.args['masterpiece_name']
	connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
	try:
	   with connection.cursor() as con:
		sql="INSERT INTO verify_masterpiece VALUES('','"+str(session['id'])+"','"+str(masterpiece_name)+"')"   
		con.execute(sql)				
		connection.commit()

	finally:
          connection.close() 
	return "ok"	


@app.route('/show_data_problems',methods=['POST','GET'])
def show_data_problems():
	show=request.args['id']
	connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
	try:
	    with connection.cursor() as con:
			sql="SELECT * FROM problems,user_data WHERE language=(SELECT title FROM masterpiece WHERE id='"+str(show)+"') and user_id=user_data.id "  
			con.execute(sql)
			data=con.fetchall()				
	    connection.commit()
	finally:
		connection.close() 		
	return jsonify(data)

@app.route('/get_question',methods=['POST','GET'])
def get_question():
	article=request.args['article']
	masterpiece=request.args['masterpiece']
	print(masterpiece,article)
	connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
	try:
	    with connection.cursor() as con:
		sql="SELECT data FROM article_masterpiece_page WHERE menu_id='"+str(article)+"' AND id_masterpiece='"+str(masterpiece)+"'"
		con.execute(sql)
		data=con.fetchall()
	    connection.commit()
	finally:
		connection.close() 	
	
	for i in data:
	  ##  soup = BeautifulSoup(i,"html.parser")
          ##  store=soup.text
	   text1 = i[0]
	
	soup = BeautifulSoup(text1,"html.parser")
        store=soup.text
	result1= QandA()
	result = result1.ie_preprocess(store)
	return jsonify(result1.take_result_q_and_a(result))



if __name__=='__main__':
    socketio.run(app,debug=True)
