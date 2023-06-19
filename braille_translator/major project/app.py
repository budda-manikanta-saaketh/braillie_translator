import os
from flask import Flask, render_template, request
from gtts import gTTS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    braille_text = request.form['braille_text']

    # Convert Braille text to English text
    english_text = braille_to_english(braille_text)

    # Generate audio file
    audio_filename = generate_audio(english_text)

    return render_template('translation.html', english_text=english_text, audio_filename=audio_filename)

def braille_to_english(braille_text):
    braille_dict = {
        '⠀': ' ', '⠁': 'a', '⠃': 'b', '⠉': 'c', '⠙': 'd', '⠑': 'e', '⠋': 'f', '⠛': 'g', '⠓': 'h',
        '⠊': 'i', '⠚': 'j', '⠅': 'k', '⠇': 'l', '⠍': 'm', '⠝': 'n', '⠕': 'o', '⠏': 'p', '⠟': 'q',
        '⠗': 'r', '⠎': 's', '⠞': 't', '⠥': 'u', '⠧': 'v', '⠺': 'w', '⠭': 'x', '⠽': 'y', '⠵': 'z',
        '⠂':',','⠆':';','⠲':'.','⠶':'(','⠶':')','⠦':'?','⠖':'!','⠤':'-','⠒':':',
    }

    english_text = ''
    for braille_char in braille_text:
        if braille_char in braille_dict:
            english_text += braille_dict[braille_char]
        elif braille_char == '⠀':  # Check for Braille space character
            english_text += ' '

    return english_text


def generate_audio(text):
    # Create a gTTS object
    tts = gTTS(text)

    # Set the path for the audio file
    audio_path = os.path.join(app.root_path, 'static', 'audio', 'translation.mp3')

    # Save the audio file
    tts.save(audio_path)

    # Return the filename of the audio file
    return 'audio/translation.mp3'


if __name__ == '__main__':
    app.run()
