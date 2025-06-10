from transformers import BertTokenizer

# Load the WordPiece tokenizer from BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Tokenize a text
text = "These models are usually initialized with Gaussian random values."
tokens = tokenizer.encode(text)
print(f"Token IDs: {tokens}")
print(f"Tokens: {tokenizer.convert_ids_to_tokens(tokens)}")
print(f"Decoded: {tokenizer.decode(tokens)}")