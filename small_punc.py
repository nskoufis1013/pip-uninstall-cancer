from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Load the pre-trained tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Load your text data and create a dataset
dataset = TextDataset(
    tokenizer=tokenizer,
    file_path="FAQ.txt",  # Replace with the path to your text database
    block_size=128,  # Adjust the block size according to your needs
)

# Initialize the pre-trained model
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Create a data collator for language modeling
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Define the training arguments
training_args = TrainingArguments(
    output_dir="small_model/",  # Replace with the path to save the trained model
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
trainer.save_model("small_model/")  # Replace with the desired save path
