"""
>>----------------------------> <---------------------------<<
IMPLEMENTASI PROTOKOL TCP DAN WEBSERVICE PADA LAMPU LALU LINTAS
>>----------------------------> <---------------------------<<

@Friday, 13 May 2016
@TODO:  Line 148 TypeError: list indices must be integers, not str.

@Saturday, 14 May 2016
@TODO: Hard-code for WebService with Flask

@Wednesday, 18 May 2016
@TODO: User Interface

Pemrograman Jaringan
FAKULTAS ILMU KOMPUTER
UNIVERSITAS BRAWIJAYA

@ Dosen Pengampu
    Mahendra Data

@ Mahasiswa
    Muhammad Sholeh
    Hasbi Razzak
    Muharrom Abdillah
    Rizky Julianto
"""
import socket, json, time, thread
import urllib
from datetime import datetime

class Client(object):
    def __init__(self, id_client):
        self.id = id_client
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, address, port):
        is_connect = False
        try:
            self.clientsock.connect((address, port))
            is_connect = True
        except socket.error:
            print "LOG: Gagal terhubung ke server."
            is_connect = False
        while is_connect:
            try:
                print "LOG: Mengirim id ke server."
                self.clientsock.send(json.dumps({'id': self.id}))
                data = json.loads(self.clientsock.recv(1024))
                print "LOG: Menerima data dari server."
                if data['response'] == 'success':
                    print "MERAH:   ", data['merah']
                    print "HIJAU:   ", data['hijau']
                    print "KUNING:  ", data['kuning']
                    print ">>------>"
                else:
                    print "LOG: ID Client tidak terdaftar."
                time.sleep(2)
            except socket.error, KeyboardInterrupt:
                print "LOG: Server offline."
                self.clientsock.close()
                break

class Server(object):
    def __init__(self, id_server):
        """ Inisialisasi object server dengan identitas ID """
        self.id_server = id_server
        #self.ipserverutama, self.portserverutama = ('127.0.0.1', 6000)
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.database = {
            'date-modified': str(datetime.now()),
            'data': [
                {'response': 'success', 'id_client': 1, 'merah': 0, 'hijau': 0, 'kuning': 0},
                {'response': 'success', 'id_client': 2, 'merah': 0, 'hijau': 0, 'kuning': 0},
                {'response': 'success', 'id_client': 3, 'merah': 0, 'hijau': 0, 'kuning': 0},
                {'response': 'success', 'id_client': 4, 'merah': 0, 'hijau': 0, 'kuning': 0}
            ]
        }
    def connect(self, server_address, server_port):
        """ Melakukan koneksi ke server utama """
        self.server_address = server_address
        self.server_port = server_port

    def start(self, address, port):
        """ Menjalankan server pada address dan port yang ditentukan """
        self.serversock.bind((address, port))
        self.serversock.listen(4)
        print "Server Running on %s:%s" % (address, port)
        print "Membuat thread baru untuk menghandle request ke server utama."
        try:
            thread.start_new_thread(self.handleserver, (self.server_address, self.server_port))
            while True:
                    clientsock, address = self.serversock.accept()
                    print "Membuat thread baru untuk menghandle client."
                    thread.start_new_thread(self.handleclient, (clientsock, address))
        except KeyboardInterrupt:
            self.serversock.close()

    def handleclient(self, clientsock, address):
        """ Mengatur proses penerimaan dan pengiriman data ke client """
        print "Koneksi dari ", address
        while True:
                try:
                    print "LOG: Menerima request dari client."
                    data_from_client = json.loads(clientsock.recv(1024))
                    data_in_db = self.database['data']
                    is_exist = False
                    for i in range(len(data_in_db)):
                        if data_from_client['id'] == data_in_db[i]['id_client']:
                            is_exist = True
                            data = json.dumps(data_in_db[i])
                            print "LOG: Mengirim data ke client."
                            clientsock.send(data)
                            break
                    if is_exist == False:
                        print "LOG: Id client %s tidak terdaftar." % (address)
                        clientsock.send(json.dumps({'response': 'error'}))
                except (KeyboardInterrupt, KeyError, ValueError, socket.error):
                    clientsock.close()
                    print "%s:%s disconnect." % (address[0], address[1])
                    break

    def handleserver(self, address, port):
        """ Mengatur proses request dan memperbarui data dengan server utama """
        while True:
            try:
                url = "http://%s:%s/data/%s" % (address, port, self.id_server)
                response = urllib.urlopen(url)
                data = json.loads(response.read())
                print "LOG: Request data ke server utama."
                if data['response'] == 'success':
                    print "LOG: Response success"
                    date_serverutama = datetime.strptime(
                        data['date-modified'], "%Y-%m-%d %H:%M:%S.%f"
                    )
                    date_server = datetime.strptime(
                        self.database['date-modified'], "%Y-%m-%d %H:%M:%S.%f"
                    )
                    if date_serverutama > date_server:
                        print "LOG: Mengupdate data terbaru"
                        self.database['date-modified'] = data['date-modified']
                        clients = self.database['data']
                        clients_serverutama = data['clients']
                        for i in range(len(clients_serverutama)):
                            if clients[i]['id_client'] == clients_serverutama[i]['id_client']:
                                print "LOG: Mengupdate data client."
                                clients[i]['merah'] = clients_serverutama[i]['merah']
                                clients[i]['hijau'] = clients_serverutama[i]['hijau']
                                clients[i]['kuning'] = clients_serverutama[i]['kuning']
                            else:
                                print "LOG: Menambah data client"
                                clients.append(clients_serverutama[i])
                        print "LOG: Selesai Mengupdate data."
                    else:
                        print 'LOG: Tidak terdapat data terbaru.'
                        del data
                else:
                    print "LOG: Tidak mendapat response dari server."
                    del data
                time.sleep(1)
            except (IOError, ValueError):
                print 'Gagal terhubung ke server utama.'
            #except ValueError:
            #    print 'Gagal menerima data dari server.'
