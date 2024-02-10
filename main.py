import time
import sys
from Spam import Spam

message_cache = {
    "messages": [
         {
            "message_id": 27634872634,
            "message": "Some message",
            "timestamp": time.time()
        },
        {
            "message_id": 27634872635,
            "message": "Another message",
            "timestamp": time.time()  
        },
    ]
}

spam = Spam(message_cache)

while True:
    message = input("Type your message here: ")
    
    if message.lower() == "exit":
        break
    
    timestamp = time.time()
    message_id = len(message_cache["messages"]) + 1  # Generate unique message ID
    new_message = {
        "message_id": message_id,
        "message": message,
        "timestamp": timestamp
    }
    message_cache["messages"].append(new_message)
    print("Message added to cache.")
    
    analyze = spam.analyze()
    print(analyze)
    sys.stdout.flush()

print("Final message cache:")
print(message_cache)