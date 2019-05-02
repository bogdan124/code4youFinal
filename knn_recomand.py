from sklearn.neighbors import NearestNeighbors
from recomandation_engine import recomandation_engine
import math
import pymysql

connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)
con=connection.cursor()
alingment=[["left",1],["center",2],["right",3]]
text_font=[["helvetica",1],["inherit",0]]
##color in decimal and convert them after
##alingmennt:1-left,2-center,3-right
##helvetica-1

cls__2=recomandation_engine()
cls__2= cls__2.get_users_preferences()
x=cls__2
con.close()
class classifier():
    def class_KNN(self,predict_data):
            nbrs = NearestNeighbors(n_neighbors=2, algorithm='auto').fit(x)
            distances,indices = nbrs.kneighbors()
            self.user_predict=[x[indices[0][0]]]
            return [x[indices[0][0]]]
