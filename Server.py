import socket
import threading
import random
import json






class Server():




    def __init__(self):

        self.host = "0.0.0.0"
        self.port = 7122
        self.server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_s.bind((self.host, self.port))



        # Make the feedy list and make one first-default feedy with dicionary and pull it in the list
        self.feedy_lists = []

        # Default Commentary 1
        self.Comment = ["Ja ich bin unter zugzwang aber ich finde es wird gehen"]
        self.default = {"Thema":"Feedy Bosse unter zugzwang!", "Feed":"Nach Tagen der Entwicklung sind die Feedy Bosse unter zugzwang,\n aber Sie geben nicht auf.", "Ort":"FeedyHomeCenter", "Kommentare":self.Comment, "Von":"Boss Watzke"}

        # Default Commentary 2
        self.Comment2 = ["Jetzt wird das Programm endlich was. Nicht mehr lange und es funktioniert"]
        self.default2 = {"Thema":"Feddy Boss komm in fahrt", "Feed":"Feedy Boss macht einen weiteren schritt in richtung Ziel", "Ort":"Hackerbase", "Kommentare":self.Comment2, "Von":"Caillou"}

        self.feedy_lists.append(self.default2)
        self.feedy_lists.append(self.default)






        # To now on which client the Feedy have to send, i make a list with all client's ip-adresses, when a client send data, he send stealth his ip adress NOT SAFE TO USE
        self.ip_list = []









    def listen(self):

        self.server_s.listen(100)
        print("Server listening...")

        while True:


            self.client, self.addr = self.server_s.accept()

            self.this_is = self.addr[0]

            print("Get connection from: " + self.this_is)

            threading.Thread(target=self.first_feedy, args=(self.client, self.addr)).start()











    def first_feedy(self, client_s, address):

        self.random_int = random.randrange(0, len(self.feedy_lists))

        self.data = self.feedy_lists[self.random_int]
        self.data = json.dumps(self.data).encode("utf-8")
        client_s.send(self.data)



        while True:


            self.data = client_s.recv(1024)



            if("Next" in str(self.data)):

                # Start "Next feed" thread, to give the users the new feeds
                self.next_feedy(client_s=client_s, addres=address)

            if("Load" in str(self.data)):

                # Start "get feedy" thread, to get new feed's from users and saved them to the dictionary
                self.get_feedy(client_s=client_s, addres=address)

            if("Com" in str(self.data)):


                while True:

                    self.commentary = ""
                    self.commentary = client_s.recv(1024).decode("utf-8")

                    self.feedy_lists[self.random_int]["Kommentare"].append(self.commentary)

                    break










    def next_feedy(self, client_s, addres):

        while True:

            self.random_int = random.randrange(0, len(self.feedy_lists))
            self.data_new_feedy = self.feedy_lists[self.random_int]


            self.data_new_feedy = json.dumps(self.data_new_feedy).encode("utf-8")
            client_s.send(self.data_new_feedy)





            break











    def get_feedy(self, client_s, addres):


        while True:

            self.temp_data = bytearray()
            self.data_get = client_s.recv(8192)
            self.temp_data = self.temp_data + self.data_get

            self.data_get_feedy = json.loads(self.temp_data.decode("utf-8"))

            self.Thema = ""
            self.Feed = ""
            self.Ort = ""
            self.Kommentare = ""
            self.Von = ""

            self.Thema = self.data_get_feedy["Thema"]
            self.Feed = self.data_get_feedy["Feed"]
            self.Ort = self.data_get_feedy["Ort"]
            self.Kommentare = self.data_get_feedy["Kommentare"]
            self.Von = self.data_get_feedy["Von"]






            self.default_user = {"Thema":self.Thema, "Feed":str(self.Feed), "Ort":self.Ort, "Kommentare":self.Kommentare, "Von":self.Von}
            self.feedy_lists.append(self.default_user)






            break







if(__name__ == "__main__"):

    server = Server()
    server.listen()






