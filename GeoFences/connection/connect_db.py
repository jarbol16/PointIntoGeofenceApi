import mysql.connector
from mysql.connector import errorcode
import time
from . import server as s
class Connect_DB:
    conn = None
    config = []

    def open_conn(self,Host,User,Pwd,Database,Port):
        self.config = [Host,User,Pwd,Database,Port]
        try:
            _cn = mysql.connector.connect(user=User, password=Pwd, host=Host, database=Database, port=Port, use_pure=False,autocommit=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
        self.conn = _cn
        return _cn

    # Function to Get DB Info
    def query_get(self,Query,_cn):
        status = _cn.is_connected()
        qryOut = _cn.cursor()
        qryOut.execute(Query)
        row = qryOut.fetchall()
        qryOut.close()
        return row




    #RETORNA LA CONSULTA COMO UN DICCIONARIO
    def query_get_keys(self,Query,_cn):
        status = _cn.is_connected()
        qryOut=_cn.cursor(dictionary=True)
        qryOut.execute(Query)
        row = qryOut.fetchall()
        qryOut.close()
        return row

    # Function to execute queries 
    def query_exec(self,Query,_cn):
        qryOut=_cn.cursor()
        res = qryOut.execute(Query)
        _cn.commit()
        return res

    def query_exec_update(self,Query,_cn):
        qryOut=_cn.cursor()
        qryOut.execute(Query)
        _cn.commit()
        res = qryOut.rowcount
        return res

    # Function to execute queries de insercion
    #RETORNA EL ID NUEVO GENERADO
    def query_insert(self,Query,_cn,param=None):
        qryOut=_cn.cursor()
        if param is not None:
            qryOut.execute(Query,param)
        else:
            qryOut.execute(Query)
        _cn.commit()
        id = qryOut.lastrowid
        return id

    def ArrQryExec(self,ArrQuery,_cn):
        qryOut=_cn.cursor()
        for Qry in ArrQuery:
            qryOut.execute(Qry)
            _cn.commit()

    # Function to close DB Conn
    def close_conn(self,_cn):
        print("SE cierra la conexion")
        _cn.close()
