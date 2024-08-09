import socket
import ipaddress
import os
import getopt
import sys

#定数 起動パラメータ
SERVER_IP = "192.1.2.207"
LISN_PORT_C = "2009"
LISN_PORT_H = "2010"
USER_NAME_C = "COOL"
USER_NAME_H = "HOT"

class Client:

    #CoolかHotか
    CH_COOL = 0
    CH_HOT = 1
    CoolHot = CH_COOL

    def ChkCoolHot(self,pGetEnemyFlag:bool) -> int:
        """
        @bool (bool): 敵側の種類を取得するかどうか
        """
        if self.port == "2009":
            self.CoolHot = self.CH_COOL
        else:
            self.CoolHot = self.CH_HOT
            
        result = self.CoolHot

        if pGetEnemyFlag == True:
            if self.CoolHot == self.CH_HOT:
                result = self.CH_COOL
            else:
                result = self.CH_HOT

        return result

    def __init__(self):
        if len(sys.argv) > 1:
            try:
                short_options = 'h:n:p:c:'
                long_options = ['host=', 'name=', 'port=', 'coolorhot=']                
                optlist, args = getopt.getopt(sys.argv[1:], short_options,long_options)
            except getopt.GetoptError as err:
                print(err)  # will print something like "option -a not recognized"
                sys.exit(2)
            for o, a in optlist:
                if o in ('-n','--name'):
                    self.name = a
                elif o in ('-p','--port'):
                    self.port = a
                elif o in ('-h','--host'):
                    self.host = a
                elif o in ('-c','--coolorhot'):
                    if a == 'c':
                        self.name = USER_NAME_C
                        self.port = LISN_PORT_C
                        self.host = SERVER_IP
                        break
                    elif a == 'h':
                        self.name = USER_NAME_H
                        self.port = LISN_PORT_H
                        self.host = SERVER_IP
                        break
                    else:
                        assert False, f"unhandled option: {a}"
                        break
                else:
                    assert False, f"unhandled option: {o}"
        else:
            self.port = input("ポート番号を入力してください → ")
            self.name = input("ユーザー名を入力してください → ")[:15]
            self.host = input("サーバーのIPアドレスを入力してください → ")

        if not self.port:
            self.port = 2009
        if not self.name:
            self.name = 'User1'
        if not self.host:
            self.host = '127.0.0.1'

        if not self.__ip_judge(self.host):
            os._exit(1)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, int(self.port)))

        print("port:", self.port)
        print("name:", self.name)
        print("host:", self.host)

        self.__str_send(self.name + "\r\n")

    def __ip_judge(self, host):
        try:
            ipaddress.ip_address(host)
        except Exception as e:
            print("IPアドレスの形式に誤りがあります : {0}".format(e))
            return False
        else:
            return True

    def __str_send(self, send_str):
        try:
            self.client.sendall(send_str.encode("utf-8"))
        except Exception:
            print("send error:{0}\0".format(send_str))

    def __order(self, order_str, gr_flag=False):
        """
        @order_str (strig): Command. must be 2 chars and upper case.
        @gr_flag (boolean): GetReady flag.
        """
        try:
            if gr_flag:
                responce = self.client.recv(4096)

                if(b'@' in responce):
                    pass  # Connection completed.
                else:
                    print("Connection failed. {0}".format(responce))

            self.__str_send(order_str + "\r\n")

            # response is 11 digits integer.
            responce = self.client.recv(4096)[0:11].decode("utf-8")

            if not gr_flag:
                self.__str_send("#\r\n")

            # if first digit is `0` game is over.
            if responce[0] == '1':
                return [int(x) for x in responce[1:10]]
            elif responce[0] == '0':
                raise OSError("Game Set!")
            else:
                msg = "responce[0] = {0} : Response error."
                print(msg.format(responce[0]))
                raise OSError("Responce Error")

        except OSError as e:
            print(e)
            self.client.close()
            os._exit(0)

    def get_ready(self):
        return self.__order("gr", True)

    def walk_right(self):
        return self.__order("wr")

    def walk_up(self):
        return self.__order("wu")

    def walk_left(self):
        return self.__order("wl")

    def walk_down(self):
        return self.__order("wd")

    def look_right(self):
        return self.__order("lr")

    def look_up(self):
        return self.__order("lu")

    def look_left(self):
        return self.__order("ll")

    def look_down(self):
        return self.__order("ld")

    def search_right(self):
        return self.__order("sr")

    def search_up(self):
        return self.__order("su")

    def search_left(self):
        return self.__order("sl")

    def search_down(self):
        return self.__order("sd")

    def put_right(self):
        return self.__order("pr")

    def put_up(self):
        return self.__order("pu")

    def put_left(self):
        return self.__order("pl")

    def put_down(self):
        return self.__order("pd")

    def serverStatusReport(self):
        return self.__str_send("ssr")
