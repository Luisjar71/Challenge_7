import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)  # Corrección aquí, escucha con un backlog de 5 conexiones
print(f"Server conectado en {host}:{port}")

clientes = []
usernames = []

def broadcast(mensaje, _cliente):
    for cliente in clientes:
        if cliente != _cliente:
            try:
                cliente.send(mensaje)
            except:
                cliente.close()
                remove_client(cliente)

def remove_client(cliente):
    if cliente in clientes:
        index = clientes.index(cliente)
        username = usernames[index]
        broadcast(f"ChatBot: {username} desconectado".encode('utf-8'), cliente)
        clientes.remove(cliente)
        usernames.remove(username)

def handle_message(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            broadcast(mensaje, cliente)
        except:
            remove_client(cliente)
            break

def recibir_conexion():
    while True:
        cliente, direccion = server.accept()

        cliente.send("username".encode('utf-8'))
        username = cliente.recv(1024).decode('utf-8')

        clientes.append(cliente)
        usernames.append(username)

        print(f"El {username} está conectado con la dirección {str(direccion)}")

        mensaje = f"ChatBot: {username} se ha unido al chat".encode('utf-8')
        broadcast(mensaje, cliente)
        cliente.send("Conectado al servidor".encode('utf-8'))

        thread = threading.Thread(target=handle_message, args=(cliente,))
        thread.start()

recibir_conexion()


