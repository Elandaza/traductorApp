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
        # Prepare the translation request
        headers = {
            'Ocp-Apim-Subscription-Key': cog_key,
            'Ocp-Apim-Subscription-Region': cog_region,
            'Content-Type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': text
        }]

        params = {
            'api-version': '3.0',
            'to': target_language
        }

        # Send the translation request
        response = requests.post(
            f"{translator_endpoint}/translate",
            headers=headers,
            params=params,
            json=body
        )

        if response.status_code == 200:
            translated_text = response.json()[0]['translations'][0]['text']
        else:
            translated_text = 'Translation failed'
        source_language = ''
        
        return render_template('home.html', translated_text=translated_text,lang_detected=source_language)
    
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
