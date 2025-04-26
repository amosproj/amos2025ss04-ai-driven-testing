# Generate model with correct promt and input-file
import ollama

from specifications import model_name, code_path

# Initialize the Ollama client
client = ollama.Client()

# Read the content of the file
with open(code_path, 'r') as file:
    file_content = file.read()

# Create a prompt that describes what you want the model to do with the file content
prompt = f"""{file_content}"""

# Send the query to the model
response = client.generate(model=model_name, prompt=prompt)

# Print the response into a file
with open("response.txt", "w") as file:
    file.write(response.response)

print("done")