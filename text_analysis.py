from transformers import pipeline
classifier = pipeline('text-classification', model='bhadresh-savani/bert-base-uncased-emotion', return_all_scores=True)
prediction = classifier("I love using transformers. The best part is wide range of support and its easy to use", )
print(prediction)

classifier = pipeline('text-classification', model='harshal-11/Bert-political-classification', return_all_scores=True)
prediction = classifier("I love using transformers. The best part is wide range of support and its easy to use", )
print(prediction)
