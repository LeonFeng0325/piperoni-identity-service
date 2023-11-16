import socketio
import asyncio

# Socket client made for testing purpose

sio_client = socketio.AsyncClient()
# Should always fetch a valid token using /token endpoint in swagger ui for testing purpose
accessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiX2ZlbmdAdWNzYi5lZHUiLCJleHAiOjE3MDAxNjgzMDB9.kxVJGHg9jxvaPVn6aXBoi_A4fJHYDHuSZCKFmYB4Qcg'

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
    try:
        print("CLIENT: Initiating socket connection to server...")
        await sio_client.connect(url='http://localhost:80', socketio_path='/ws/sockets.io', auth={'Authorization': accessToken})
        await sio_client.sleep(1)  # Wait for server response on client connection request
        await sio_client.call("private_dm", {
            "content": "How are you doing Kirill?",
            "auth_token": accessToken,
            "receiver_id": 3
        })
    except Exception as e:
        print(f"CLIENT: Connection failed with error: {e}")
    finally:
        # Ensure that the client session is properly closed
        await sio_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
