import os
import sys
import time
import requests
import json
import nltk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tqdm import tqdm

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup


### setup

# start timer
T0 = time.time()
print(f"[Elapsed time: {time.time()-T0:.3f}s]")

# BART hyperparameters
SUMMARY_MODEL = 'sshleifer/distilbart-cnn-12-6'
MAX_TOKENS = 1024 # model dependent
BATCH_SIZE = 1 # hardware dependent
SUMMARY_MAX = 128 # use dependent
SUMMARY_MIN = 64 # use dependent

# ASIMILATE API
API_URL = 'https://zfgp45ih7i.execute-api.eu-west-1.amazonaws.com/sandbox/api/search'
with open('ASIMILATE.key', 'r') as f:
	API_KEY = f.readline().strip()


### functions

# type: (str) -> dict
def get_query(query, volume=1):
	request = requests.post(
		API_URL,
		headers={
			"Content-Type": "application/json",
			"x-api-key": API_KEY
		},
		data=json.dumps({
		  "query_text":query,
		  "result_size":volume,
		  "include_highlights":True,
		  "ai_answer":"basic"
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

# type: (str, str) -> str
def normalise_language(text, target='en'):
	try:
		return GoogleTranslator(source='auto', target=target).translate(text)
	except Exception as e:
		return f"[ERROR]: Translation failed"

# type: () ->
def url_2_txt(url):
	try:
		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		text = " ".join([p.get_text(strip=True) for p in soup.find_all('p')])
		return text
	except Exception as e:
		print(e)
		return f"[WARN]: Fetch failed"

# type: () ->
def load_pngs_to_numpy_list(directory):
    image_list = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith('.png'):
            img_path = os.path.join(directory, filename)
            image = Image.open(img_path).convert('RGB')  # or 'RGBA' if alpha channel is needed
            image_array = np.array(image)
            image_list[filename.replace('.png', '')] = image_array
    return image_list


### main

# define query
query = "Lasagna"#"Los Angeles Riots"

# fetch text and normalise language
query_results = get_query(query, volume=10)
query_urls = [x['url'] for x in query_results['results']]
query_text = list(map(url_2_txt, query_urls))
query_text_en = list(map(normalise_language, query_text))

# trace
for t in query_text_en:
	print(t)
	print("=============================")
print(f"[Elapsed time: {time.time()-T0:.3f}s]")

# perform analysis
summary_tokenizer = AutoTokenizer.from_pretrained(SUMMARY_MODEL)
summary_model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARY_MODEL).to('cuda' if torch.cuda.is_available() else 'cpu')
emotion_classifier = pipeline('text-classification', model='bhadresh-savani/bert-base-uncased-emotion')
#query_text_en_emotion = list(map(emotion_classifier, map(lambda t: summarize_txt(t, summary_tokenizer, summary_model), query_text_en)))
query_text_en_emotion = list(map(lambda t: emotion_classifier(t[:512]), query_text_en))
print(query_text_en_emotion)
print(f"[Elapsed time: {time.time()-T0:.3f}s]")

# plot analysis
fig, axis = plt.subplots(nrows=len(query_text_en_emotion)//5, ncols=5, figsize=(20, 20))
axis_flat = axis.ravel()
emotion_images = load_pngs_to_numpy_list('assets')
for ax, data, url in zip(axis_flat, query_text_en_emotion, query_urls):
	source = url.split('/')[2]
	emotion = data[0]['label']
	score = data[0]['score']
	ax.imshow(emotion_images[emotion], alpha=score)
	ax.text(10, 30, f"{source}\n\"{query}\" {emotion}: {score*100:.2f}%", c='r', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=1.5'))
	ax.set_xticks([],[])
	ax.set_yticks([],[])
print(f"[Elapsed time: {time.time()-T0:.3f}s]")
plt.tight_layout()
plt.show()
