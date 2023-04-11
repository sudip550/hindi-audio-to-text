import requests
import time

UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPTION_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

#write your api key in below line
api_key = "upload your api key here"
headers = {"authorization": api_key, "content-type": "application/json"}

def read_file(filename):
   with open(filename, 'rb') as _file:
       while True:
           data = _file.read(5242880)
           if not data:
               break
           yield data

#write your dataset path in below line
upload_response = requests.post(UPLOAD_ENDPOINT, headers=headers, data=read_file('give dataset path here'))
upload_response.json()

audio_url = upload_response.json()["upload_url"]
json = {'audio_url': audio_url,
        'language_code' : 'hi'}
transcript_response = requests.post(TRANSCRIPTION_ENDPOINT, json=json, headers=headers)
_id = transcript_response.json()["id"]

while True:
    polling_response = requests.get(TRANSCRIPTION_ENDPOINT + "/" + _id, headers=headers)

    if polling_response.json()['status'] == 'completed':
       with open(f'{_id}.txt', 'w') as f:
           f.write(polling_response.json()['text'])
       print('Transcript saved to', _id, '.txt')
       break
    elif polling_response.json()['status'] == 'error':
        raise Exception("Transcription failed. Make sure a valid API key has been used.")
    else:
       print("Transcription queued or processing ...")
    time.sleep(5)
