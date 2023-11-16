import socketio
import asyncio

# Socket client made for testing purpose

sio_client = socketio.AsyncClient()
# Should always fetch a valid token using /token endpoint in swagger ui for testing purpose
accessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiX2ZlbmdAdWNzYi5lZHUiLCJleHAiOjE3MDAxMDc3NTN9.gagdmzQ5tDaJvfqxldtmz10cf4tUrMRwLdiHscbkYKw'

@sio_client.event
async def connect():
    print("CLIENT: I'm connected.")


@sio_client.event
def connect_error(data):
    print("CLIENT: The connection failed!")


@sio_client.event
async def disconnect():
    print("CLIENT: I'm disconnected.")


@sio_client.on('server_login_confirm')
async def client_receive_server_login_confirm(data):
    print(f"CLIENT: Login confirmation from the server: {data}")


@sio_client.event
async def private_dm(message):
    print(f"CLIENT: Received message from the server: {message}")


async def main():
    print("CLIENT: Initiating socket connection to server...")
    await sio_client.connect(url='http://localhost:8000', socketio_path='/ws/sockets.io', auth={'Authorization': accessToken})
    await sio_client.sleep(1) # Wait for server response on client connection request
    await sio_client.call("private_dm", {
        "content": "How are you doing Kirill?",
        "auth_token": accessToken,
        "receiver_id": 3
    })
    await sio_client.disconnect()


asyncio.run(main())
