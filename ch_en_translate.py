from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en")

ch_text = "随着美国采取行动打击有争议边境地区的商业运输，南海紧张局势加剧"


# tokenize input
inputs = tokenizer([ch_text], return_tensors='pt', padding=True, truncation=True)
input_ids = inputs['input_ids'].to('cpu')
attention_mask = inputs['attention_mask'].to('cpu')
en_text = tokenizer.batch_decode(model.generate(input_ids, attention_mask=attention_mask), return_tensors='pt', padding=True, truncation=True, skip_special_tokens=True)[0]

print(ch_text)
print(en_text)
