from transformers import T5Tokenizer
import os
# set your HF_TOKEN !!!
os.environ["HF_TOKEN"] = "hf_XXX"

# Load the T5 tokenizer (which uses SentencePiece+Unigram)
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Tokenize a text
text = "SentencePiece is a subword tokenizer used in models such as XLNet and T5."
tokens = tokenizer.encode(text)
print(f"Token IDs: {tokens}")
print(f"Tokens: {tokenizer.convert_ids_to_tokens(tokens)}")
print(f"Decoded: {tokenizer.decode(tokens)}")


## Training a SentencePiece tokenizer 训练

# from datasets import load_dataset
# from tokenizers import SentencePieceUnigramTokenizer
#
# ds = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1")
# tokenizer = SentencePieceUnigramTokenizer()
#
# tokenizer.train_from_iterator(ds["train"]["text"])
# tokenizer.save("my-tokenizer.json")