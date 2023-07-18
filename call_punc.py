
from transformers import GPT2LMHeadModel, GPT2Tokenizer

import torch

# Load the pre-trained tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Load the trained model
model = GPT2LMHeadModel.from_pretrained("trained_model/")  # Replace with the actual path

# Set the model to evaluation mode
model.eval()

# Example user input
user_input = "What is the cBioPortal for Cancer Genomics?"

# Tokenize the user input
input_ids = tokenizer.encode(user_input, return_tensors="pt")

# Generate model output
with torch.no_grad():
    outputs = model.generate(input_ids, max_length=100, num_return_sequences=1)

# Decode and print the generated response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("ChatGPT: ", response)


