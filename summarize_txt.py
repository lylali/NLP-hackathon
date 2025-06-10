import sys
import time
import requests
import json
import nltk
import pandas as pd
from tqdm import tqdm

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


### setup

# start timer
T0 = time.time()
print(f"[Elapsed time: {time.time()-T0:.3f}s]")

# BART hyperparameters
MODEL = 'sshleifer/distilbart-cnn-12-6'
MAX_TOKENS = 1024 # model dependent
BATCH_SIZE = 1 # hardware dependent
SUMMARY_MAX = 32 # use dependent
SUMMARY_MIN = 8 # use dependent

# ASIMILATE API
API_URL = 'https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search'
API_KEY = sys.argv[1]


### functions

# type: (str) -> dict
def get_query(query):
	request = requests.post(
		API_URL,
		headers={
			"Content-Type": "application/json",
			"x-api-key": API_KEY
		},
		data=json.dumps({
		  "query_text": query,
		  "result_size": 1,
		  "include_highlights":True,
		  "ai_answer": "basic"
		})
	)
	return request.json()

# type: (str, AutoTokenizer, int) -> list[str]
def split_txt(text, tokenizer, max_tokens=MAX_TOKENS):
	
	# tokenize, slice by max_tokens, detokenize
	input_ids = tokenizer(text, return_tensors='pt', truncation=False)['input_ids'][0]
	text_chunks = [input_ids[i:i+max_tokens] for i in range(0, len(input_ids), max_tokens)]
	text_chunks = [tokenizer.decode(chunk_ids, skip_special_tokens=True) for chunk_ids in text_chunks]
	
	return text_chunks

# type: (list[str], AutoTokenizer, AutoModelForSeq2SeqLM, int) -> str
def summarize_txt_chunks(text_chunks, tokenizer, model, batch_size=BATCH_SIZE):
	
	# initialise
	summaries = []
	device = model.device
	
	# decode summaries
	for i in tqdm(range(0, len(text_chunks), batch_size)):
		
		# batch
		batch_chunks = text_chunks[i:i+batch_size]
		
		# tokenize input
		inputs = tokenizer(batch_chunks, return_tensors='pt', padding=True, truncation=True)
		input_ids = inputs['input_ids'].to(device)
		attention_mask = inputs['attention_mask'].to(device)
		
		# generate summary
		summary_ids = model.generate(
			input_ids,
			attention_mask=attention_mask,
			max_length=SUMMARY_MAX,
			min_length=SUMMARY_MIN,
			do_sample=False,
		)
		
		# detokenize output
		batch_summaries = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)
		summaries.extend(batch_summaries)
	
	# finalise summary
	summary = '\n'.join(summaries)
	
	return summary

# type: (str, AutoTokenizer, AutoModelForSeq2SeqLM) -> str
def summarize_txt(text, tokenizer, model):
	text_chunks = split_txt(text, tokenizer)
	summary = summarize_txt_chunks(text_chunks, tokenizer, model)
	return summary
