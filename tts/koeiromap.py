import os, sys
import requests
import base64
from ast import literal_eval
import pyaudio, wave, soundfile

class TTS():
    def __init__(self) -> None:
        self.speaker_x = 2.67
        self.speaker_y = 1.88

    def _get_audio(self, message, style):
        if os.path.exists("temp.wav"):
            os.remove("temp.wav")
        # POSTメソッドのみ対応 curl --location 'https://api.rinna.co.jp/models/cttse/koeiro' --header 'Content-Type: application/json' --data '{"text": "こんにちは",  "speaker_x": 0.0,  "speaker_y": 0.0,  "style": "talk"}'
        # use requests
        url = 'https://api.rinna.co.jp/models/cttse/koeiro'
        headers = {'Content-Type': 'application/json'}
        data = {
            'text': message,
            'speaker_x': self.speaker_x,
            'speaker_y': self.speaker_y,
            'style': style
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # save as temp.wav
            encoded_audio = literal_eval(response.content.decode('utf-8'))["audio"].split(",")[1] # base 64 encoded
            wav_file = open("temp.wav", "wb")
            decode_audio = base64.b64decode(encoded_audio)
            wav_file.write(decode_audio)
            wav_file.close()

            # change temp.wave to 16-bit wav file
            with open('temp.wav', 'rb') as f:
                data, samplerate = soundfile.read(f)
                soundfile.write('temp.wav', data, samplerate, subtype='PCM_16')
            return
        else:
            print('Error: ', response.status_code)
            return

    def say(self, message, style):
        # style: 
        #   talk: 通常の話し声
        #   happy: 嬉しい
        #   sad: 悲しい
        #   angry: 怒った
        #   fear: 恐怖
        #   surprise: 驚いた
        self._get_audio(message, style)
        self.play()

    def play(self):
        # play temp.wav
        CHUNK = 1024
        wf = wave.open("temp.wav", 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
        data = wf.readframes(CHUNK)
        while data != b'':
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
        # os.remove("temp.wav")

if __name__ == '__main__':
    tts = TTS()
    tts.say('こんにちは', style='happy')
        