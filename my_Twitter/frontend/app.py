import streamlit as st
import requests

st.title("Tweet Classification with Logistic Regression and CNN")

input_text = st.text_area("Enter tweet(s) to classify (one per line):")

if st.button("Classify"):
    if input_text:
        texts = input_text.split('\n')
        if len(texts) == 1:
            response = requests.post("http://127.0.0.1:8000/predict", json={"text": texts[0]})
            result = response.json()
            st.write(f"Text: {texts[0]}")
            st.write(f"Logistic Regression Prediction: {result['prediction']}, Probability: {result['logreg_prob']}")
            st.write(f"CNN Prediction: {result['cnn_pred']}, Probability: {result['cnn_prob']}")
        else:
            response = requests.post("http://127.0.0.1:8000/predict", json={"texts": texts})
            results = response.json()['predictions']
            for text, result in zip(texts, results):
                st.write(f"Text: {text}")
                st.write(f"Logistic Regression Prediction: {result['prediction']}, Probability: {result['logreg_prob']}")
                st.write(f"CNN Prediction: {result['cnn_pred']}, Probability: {result['cnn_prob']}")
