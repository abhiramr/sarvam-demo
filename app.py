import json
import time
import streamlit as st
import requests




def main():
    translate_api_url = "https://api.sarvam.ai/translate"
    speech_api_url = "https://api.sarvam.ai/text-to-speech"
    st.title("Sarvam Translate and Speak App")
    pick_a_language = ["hi-IN", "bn-IN", "kn-IN", "ml-IN", "mr-IN", "od-IN", "pa-IN", "ta-IN", "te-IN", "en-IN", "gu-IN"]  
    st.markdown("""---""")
    st.markdown("This app uses Sarvam's translation and text-to-speech APIs to translate and speak English text in different languages.")
    st.markdown("References:")
    st.markdown("_1. [Sarvam API Documentation](https://docs.sarvam.ai/api-reference-docs/introduction)_")
    st.markdown("_2. [Endpoints](https://docs.sarvam.ai/api-reference-docs/endpoints)_")
    st.markdown("_3. [Speech-To-Text](https://www.sarvam.ai/apis/speech-to-text)_")
    st.markdown("""---""")

    sarvam_key = st.text_input("Enter your Sarvam key. This is encrypted and will not be logged", type="password")
    headers = {
        'API-Subscription-Key': sarvam_key, "Content-Type": "application/json"
    }
    user_input = st.text_input("Enter some text in English:", "Sample text")
    pick_a_language = st.selectbox("Pick a language to translate to -", pick_a_language)

    if st.button("Translate and Speak"):
        payload_translate = {
        "input": f"{user_input}",
        "source_language_code": "en-IN",
        "target_language_code": pick_a_language,
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": True
    }

    
        response = requests.request("POST", translate_api_url, json=payload_translate, headers=headers)
        print(f"Translated = {response.json()}")

        if response.status_code == 200:
            translated = response.json()["translated_text"]
            payload_speech = {
                "inputs": [translated],
                "target_language_code": pick_a_language,
                "speaker": "meera",
                "pitch": 0.5,
                "pace": 1,
                "loudness": 1.0,
                "speech_sample_rate": 8000,
                "enable_preprocessing": True,
                "model": "bulbul:v1"
            }
            response = requests.request("POST", speech_api_url, json=payload_speech, headers=headers)

            import base64
            wav_file = open("temp.wav", "wb")
            txt = response.json()["audios"][0]
            decode_string = base64.b64decode(txt)
            wav_file.write(decode_string)
            time_now = time.strftime("%Y%m%d-%H%M%S")
            
            with open(f"working_{time_now}.json", "w", encoding='utf8') as wav_file_json:
                data_ = {
                    "text": user_input,
                    "translated": translated,
                    "language": pick_a_language,
                    "audio": response.json()
                }
                json.dump(data_, wav_file_json)
            st.audio("temp.wav", format="audio/wav", loop=False, autoplay=False)

if __name__ == "__main__":
    main()