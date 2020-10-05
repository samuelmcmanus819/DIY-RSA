import socket
import MyIO
import Encryption

Host = '127.0.0.1'
Port = 12345
e = 79
d = 1019
n = 3337


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as S:
    S.bind((Host, Port))
    S.listen()
    Conn, Addr = S.accept()
    with Conn:
        #Accepts a file name from the client and makes them repeat it if they entered
        #an incorrect filename
        while True:
            Filename = Conn.recv(4096)
            Filename = MyIO.TrimSocket(Filename)
            FileText = MyIO.ReadFile(Filename)
            if(FileText == ""):
                Conn.sendall(bytes("bad", "utf-8"))
            else:
                Conn.sendall(bytes("good", "utf-8"))
                break
        
        #Sets the private key of the server
        MyPrivKey = Encryption.PrivateKey(d, n)
        #Sends the public key
        Conn.send(bytes(str(e) + " " + str(n), "utf-8"))
        #Sets the client's public key
        publickey = MyIO.TrimSocket(Conn.recv(4096))
        ce = int(publickey.split()[0])
        cn = int(publickey.split()[1])
        MyPubKey = Encryption.PublicKey(ce, cn)
        #Signs the message being sent to the client
        SignedMessage = MyPrivKey.DigitallySign(FileText)
        #Encrypts the message with the client's public key
        EncryptedMessage = MyPubKey.Encrypt(SignedMessage)
        #Sends the signed message to the client
        Conn.sendall(bytes(EncryptedMessage, "utf-8"))
