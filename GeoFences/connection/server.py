import base64
import sys
import time
# from Crypto.Cipher import AES
from .connect_db import Connect_DB
import core.log as log


class Server:
    conn = None
    __KEY = "hdsdgwsdg"

    def __init__(self, id, name, host, port, _user, _pass, last_id):
        self.id = id
        self.name = name
        self.host = host
        self.port = port
        self.user = _user
        # self.__pass = self.__set_pass(_pass)
        self._pass = _pass
        self.last_id = last_id

    def __set_pass(self, _pass):
        # _ = AES.new(self.__KEY,AES.MODE_ECB)
        self.__pass = _pass  # base64.b64encode(_.encrypt(_pass))

    def get_pass(self):
        # _ = AES.new(self.__KEY,AES.MODE_ECB)
        return self._pass  # _.decrypt(base64.b64decode(self._pass))

    def get_conn(self):
        try:
            status = self.conn.conn.is_connected()
        except Exception as err:
            status = False
        while not status:
            try:
                if self.conn is None:
                    self.conn = Connect_DB()
                    _ = self.conn.open_conn(self.host, self.user, self._pass, self.name, self.port)
                    if _ is not None:
                        log.log_info("Nueva Conexion")
                        log.log_info([self.host, self.user, self.name, self.port])
                    else:
                        self.conn = None
                    status = self.conn.conn.is_connected()
                else:
                    status = self.conn.conn.is_connected()
                    if not status:
                        self.conn.conn.close()
                        self.conn = None
                        log.log_error("Recuperando Connexion...")
            except Exception as err:
                self.conn = None
                log.log_error("Connectando ...")
                time.sleep(5)
        return self.conn