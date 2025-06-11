from transformers import pipeline
from bertopic import BERTopic

# example prompt
prompt = "Tensions rise in the South China Sea as the United States moves to target commercial transports in contested border region"

# emotion classifier
emotion_classifier = pipeline('text-classification', model='bhadresh-savani/bert-base-uncased-emotion')
emotion_prediction = emotion_classifier(prompt)
print(prediction)

# politics classifier ###! (no class labels)
politic_classifier = pipeline('text-classification', model='harshal-11/Bert-political-classification')
politic_prediction = politic_classifier(prompt)
print(prediction)

# BERT Topic classifier
topic_classifier = BERTopic.load("MaartenGr/BERTopic_Wikipedia")
topic, prob = topic_model.transform(prompt)
print(topic_model.topic_labels_[topic])
