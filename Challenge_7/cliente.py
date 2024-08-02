import socket
import threading

username = input("Ingresar username: ")

host = '127.0.0.1'
port = 55555

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

def recibir_mensaje():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje == "username":
                cliente.send(username.encode('utf-8'))
            else:
                print(mensaje)
        except:
            print("Ha ocurrido un error")
            cliente.close()
            break

def escribir_mensaje():
    while True:
        mensaje = f"{username}: {input('')}"
        cliente.send(mensaje.encode('utf-8'))

recibir_thread = threading.Thread(target=recibir_mensaje)
recibir_thread.start()

escribir_thread = threading.Thread(target=escribir_mensaje)
escribir_thread.start()
