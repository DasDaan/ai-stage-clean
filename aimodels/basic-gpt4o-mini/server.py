# websocket_server.py
import asyncio  # For asynchronous operations
import websockets  # For WebSocket server functionality
from model import call_openai, validate_api_key  # Import OpenAI functions

# Global event that triggers server shutdown
shutdown_event = asyncio.Event()

# Handles incoming messages from a connected WebSocket client
async def websocket_handler(websocket):
    try:
        async for message in websocket:
            # Check for different message types
            
            # Check for shutdown command
            if message == "__shutdown__":
                print("🔻 Shutdown command received. Stopping server...")
                await websocket.send("🛑 Server is shutting down.")
                # Trigger shutdown event
                shutdown_event.set()
                break
                
            # Handle STT start notification
            elif message == "__stt_start__":
                print("[STT] Speech recognition started")
                continue
                
            # Handle STT text result
            elif message.startswith("__stt_text__:"):
                text = message[12:]  # Remove the prefix
                print(f"[STT] Speech recognized: '{text}'")
                continue
                
            # Handle normal messages to send to OpenAI
            elif message.startswith("__message__:"):
                user_message = message[11:]  # Remove the prefix
                print(f"[Client] Message: '{user_message}'")
                
                # Process normal user message via OpenAI
                try:
                    response = await call_openai(user_message)
                    print(f"[OpenAI] Response: '{response[:60]}...'")
                    # Send AI response back to the client
                    await websocket.send(response)
                except Exception as openai_error:
                    print(f"[Error] Problem calling OpenAI: {openai_error}")
                    await websocket.send("Error calling OpenAI.")
            
            # Handle any other messages
            else:
                print(f"[Client] Received unrecognized message: '{message}'")
                await websocket.send("Message format not recognized")

    # Handle connection closed errors
    except websockets.exceptions.ConnectionClosed as cc:
        print(f"[Error] Connection closed: {cc}")
    # Catch any unexpected server-side errors
    except Exception as e:
        print(f"[Error] Unknown error in websocket handler: {e}")
        try:
            await websocket.send(f"Server error: {e}")
        except:
            pass

# Starts the WebSocket server and waits for a shutdown event
async def start_server():
    try:
        print("🔍 Validating OpenAI API key...")
        is_valid = await validate_api_key()
        if not is_valid:
            print("❌ Invalid OpenAI API key. Check your .env file.")
            return

        # Launch WebSocket server on localhost:8765
        server = await websockets.serve(
            websocket_handler,
            "localhost",
            8765,
            ping_interval=10,
            ping_timeout=600
        )
        print("✅ WebSocket server started at: ws://localhost:8765")

        # Wait until shutdown_event is triggered
        await shutdown_event.wait()
        print("🧹 Shutting down WebSocket server...")

        # Cleanly close the server and all client connections
        server.close()
        await server.wait_closed()
        print("✅ Server closed successfully.")

    # Handle fatal startup errors
    except Exception as e:
        print(f"[Fatal] Could not start server: {e}")

# Run server only if script is executed directly
if __name__ == "__main__":
    asyncio.run(start_server())