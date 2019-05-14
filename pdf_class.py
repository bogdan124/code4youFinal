import math
import pymysql

connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)


class pdf_class():
	def __init__(self,articol_id):
		self.articol_id=articol_id
	def getDateFromDB(self,articol_id):
		connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
		try:
		   with connection.cursor() as con: 
			sql="SELECT * FROM article_masterpiece_page WHERE id_masterpiece="+str(self.articol_id)+" ORDER BY menu_id ASC"
			con.execute(sql)
                	getDateFromDB__=con.fetchall()
		   connection.commit()
		finally:
		   connection.close()  
		##self.get_data = getDateFromDB__
		return getDateFromDB__
	def prelucrateData(self):
		l=""
		for i in self.getDateFromDB(self.articol_id):
			if i[3]!=0:
			   l=l+i[2]+"</br>"		
		return l


