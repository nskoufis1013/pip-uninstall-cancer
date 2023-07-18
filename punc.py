from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
import os

# Load the pre-trained tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Define the path to the directory containing your text files
data_dir = "training_data/"

# Get a list of all text files in the directory
file_list = [os.path.join(data_dir, filename) for filename in os.listdir(data_dir) if filename.endswith(".txt")]

# Create an empty list to store the examples
examples = []

# Process each file in the directory
for file_path in file_list:
    # Read the content of the file
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Tokenize the text and convert it to input examples
    tokenized_text = tokenizer.encode(text)
    examples.extend(tokenized_text)

# Create a TextDataset from the combined examples
dataset = TextDataset(examples, tokenizer)

# Initialize the pre-trained model
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Create a data collator for language modeling
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Define the training arguments
training_args = TrainingArguments(
    output_dir="trained_model/",  # Replace with the path to save the trained model
    overwrite_output_dir=True,
    num_train_epochs=3,  # Adjust the number of training epochs according to your needs
    per_device_train_batch_size=1,  # Adjust the batch size according to your computational resources
    save_steps=1000,
    save_total_limit=2,
)

# Create a Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

# Start the training
trainer.train()

# Save the trained model
trainer.save_model("trained_model/")  # Replace with the desired save path
