from ollama import chat
import TextSpllitor
message = [{"role": "user", "content": "Who is the principal of ILEAD Kolkata?"}]
# Run the Llama 3.1 8B model
response = chat(model="llama3.1", messages=message)

# Print the model's reply
print(response.message.content)
