from transformers import pipeline

prompt = "Tensions rise in the South China Sea as the United States moves to target commercial transports in contested border region"

classifier = pipeline('text-classification', model='bhadresh-savani/bert-base-uncased-emotion', return_all_scores=True)
prediction = classifier(prompt)
print(prediction)

classifier = pipeline('text-classification', model='harshal-11/Bert-political-classification', return_all_scores=True)
prediction = classifier(prompt)
print(prediction)
