import sys
import mysql.connector
from mysql.connector import errorcode
from enum import Enum

class Error(Enum):
    DB_CONNECTION_ERROR = 1,
    ERROR_CODE = 2


def get_geofences(server):
    try:
        send = False
        db = server.get_conn()
        query = "select a.G_name as `name` ,ASTEXT(a.geometry) as `geometry` "
        query += "from a_geofences_r2 a limit 1000"
        cursor = db.query_get_keys(query, db.conn)
        response = {'geofences':[]}
        for res in cursor:
            print(res["geometry"])
            send = True
            response['geofences'].append(res)
        if send:
            db.close_conn(db.conn)
            return response
        else:
            return None
    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_CONNECTION_ERROR:
            return Error.DB_CONNECTION_ERROR
    except Exception as err:
        #print(err)
        return Error.ERROR_CODE