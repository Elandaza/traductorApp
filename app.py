from flask import Flask, request, render_template
import os
import requests, json

global translator_endpoint    
global cog_key    
global cog_region

try:
    cog_key = os.environ.get("COG_SERVICE_KEY")
    cog_region = os.environ.get("COG_SERVICE_REGION")      
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'   
except Exception as ex:        
    print(ex)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        # Aquí es donde procesarías el texto. Por ahora, solo devolvemos el mismo texto.
        source_language = ''
        translated_text = text
        
        # inicio de coidgo deteccion de lenguaje
        params = {
            'api-version': '3.0'
        }

        headers = {
            'Ocp-Apim-Subscription-Key': cog_key,
            'Ocp-Apim-Subscription-Region': cog_region,
            'Content-type': 'application/json'
        }

        body = [{
            'text': text
        }]

        # Send the request and get response
        request = requests.post(url, params=params, headers=headers, json=body)
        response = request.json()

        # Parse JSON array and get language
        source_language = response[0]["language"]
        #language = response[0]["language"]
        
        #Fin codigo deteccion de lenguaje

        #inicio codigo traduccion
        # Build the request
        params = {
            'api-version': '3.0',
            'from': source_language,
            'to': ['en']
        }

        headers = {
            'Ocp-Apim-Subscription-Key': cog_key,
            'Ocp-Apim-Subscription-Region': cog_region,
            'Content-type': 'application/json'
        }

        body = [{
            'text': text
        }]

        # Send the request and get response
        request = requests.post(url, params=params, headers=headers, json=body)
        response = request.json()

        # Parse JSON array and get translation
        translation = response[0]["translations"][0]["text"]
        #Fin codigo de traducción


        return render_template('home.html', translated_text=translated_text,lang_detected=source_language)
    
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)