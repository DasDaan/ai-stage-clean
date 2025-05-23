# start.py
import asyncio  # For asynchronous operations
import websockets # For WebSocket client communication
import stt  # Connecting with the stt

# Main function that connects to the WebSocket server and handles user input
async def main():
    uri = "ws://localhost:8765"  # Address of the WebSocket server
    print("\nWelcome at AI Stage\n")
    print("Type something to chat with the AI")
    print("Type 'speak' or 's' to speak instead of typing")
    print("Type 'stop' to quit.\n")

    try:
        # Connect to the WebSocket server
        async with websockets.connect(uri) as websocket:
            while True:
                # Get user input from terminal
                user_input = input("🟢 You: ")

                # If user types 'stop', send shutdown signal and exit loop
                if user_input.lower() == "stop":
                    print("📴 Stopping server...")
                    # Special shutdown command
                    await websocket.send("__shutdown__")
                    print("👋 Until next time!")
                    break

                # If user wants to speak instead of type
                if user_input.lower() in ["speak", "s"]:
                    # Tell the server we're starting speech recognition
                    await websocket.send("__stt_start__")
                    
                    # Display info for the user
                    print("⏱️ You have 5 seconds to speak")
                    print("🎙️ Recording started...")
                    
                    # Get speech input
                    user_input = stt.get_speech_input()
                    
                    # Tell the server we got the transcript
                    await websocket.send(f"__stt_text__:{user_input}")
                    
                    print(f"📝 Text: {user_input}")

                # Send message to the server for AI processing
                print("📤 Sending message to the AI...")
                await websocket.send(f"__message__:{user_input}")

                # Wait for AI response
                print("⏳ Waiting for a response...")
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30)
                    print(f"🤖 AI: {response}\n")
                except asyncio.TimeoutError:
                    print("❌ Timeout while waiting for response from server.")
                except Exception as e:
                    print(f"❌ Error while receiving response: {e}")

    # Handle connection errors (e.g., server not running)
    except Exception as e:
        print(f"❌ Could not connect to server: {e}")

# Start the script
if __name__ == "__main__":
    asyncio.run(main())