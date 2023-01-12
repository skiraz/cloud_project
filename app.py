from app import predict
import streamlit as st                                                                                                              app.py

st.set_page_config(page_title="URL Phishing Detection", layout="wide")


st.title("URL Phishing Detection")
st.write("What is URL Phishing Detection?")
st.write(
    """
URL phishing detection is a process or a system that is designed to identify and prevent phishing attacks that use fake or malicious URLs. Phishing attacks are a common form of cybercrime that involves tricking people into visiting fake websites that are designed to ste$"""
)

st.write(
    """
The main advantage of using a URL phishing detection system is that it can help to protect people from falling victim to phishing attacks. By identifying and blocking fake or malicious URLs, these systems can help to prevent people from visiting fake websites and inadve$"""
)

st.write(
    """
One of the main disadvantages of URL phishing detection systems is that they can be difficult to configure and maintain. These systems often rely on complex algorithms and machine learning models to identify and block fake or malicious URLs, and they may require frequen$"""
)

Url = st.text_input("Enter Url:")

if st.button("Submit"):
    result = predict(Url)
    if result:
        st.error('this url is infected')
    else:
        st.success('this url is safe')
