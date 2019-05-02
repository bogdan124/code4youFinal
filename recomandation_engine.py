import math
import pymysql
from sklearn.neighbors import NearestNeighbors

connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='code4you',autocommit=True)





matrix_user_and_preferences=[]
matrix_user_and_preferences_2=[]
matrix_user_and_preferences_3=[]


class recomandation_engine():
    def __init__(self):
        matrix_user_and_preferences_2=[]
        matrix_user_and_preferences_3=[]
        matrix_user_and_preferences=[]

    def get_data_mysql(self):
	con=connection.cursor()
        sql="SELECT * FROM user_data "
        con.execute(sql)
	con.close()
        asd=con.fetchall()
	con=connection.cursor()
        sql2="SELECT * FROM recomand_engine_text_masterpiece"
        con.execute(sql2)
	con.close()
        take_preferences=con.fetchall()

        for i in asd:##users
            matrix_user_and_preferences.append([i[0],i[1]])

        for i in take_preferences:##preferences
            matrix_user_and_preferences_3.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15]])


        for i in matrix_user_and_preferences_3:
            for l in matrix_user_and_preferences:
                if i[1]==l[0]:
                    matrix_user_and_preferences_2.append([l[1],i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[9],i[10],i[11],i[12],i[14],i[15]])
        return matrix_user_and_preferences_2

    def get_users_preferences(self):
        sql2="SELECT * FROM recomand_engine_text_masterpiece"
	con=connection.cursor()
        con.execute(sql2)
	con.close()
        take_preferences=con.fetchall()
        for i in take_preferences:##preferences
            matrix_user_and_preferences_3.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[9],i[10],i[11],i[12],i[14],i[15]])
        return matrix_user_and_preferences_3









#
