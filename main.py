# Import the required modules
import speech_recognition as sr
import os
import sys
import time
from pathlib import Path
from openai import OpenAI
from googleapiclient.discovery import build

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")#  Openai API Key: https://platform.openai.com/api-keys
GOOGLE_CSE_API_KEY = os.environ.get("GOOGLE_CSE_API_KEY") # Custom Seacrch Engine API Key: https://developers.google.com/custom-search/v1/introduction
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")# Custom Search Engine ID: https://programmablesearchengine.google.com/controlpanel/all

# Initialize the speech recognizer and the OpenAI client
recognizer = sr.Recognizer()
client = OpenAI(api_key=OPENAI_API_KEY)

wake_word = "hello"

speech_file_path = Path(__file__).parent / "speech.mp3"

class GoogleAPI():
    def __init__(self):
        # Initialize Google Custom Search Engine
        self.service = build(
            "customsearch", "v1", developerKey=GOOGLE_CSE_API_KEY
        )
        
    def google_search(self, query):
        # Call Google Search API and retrieve search results
        response = (
            self.service.cse()
            .list(
                q=query,
                cx=GOOGLE_CSE_ID,
            )
            .execute()
        )
        return response['items']

class OpenaiAPI():
    
    def get_search_query(self, history, query):
        # Prepare user messages for generating a search query using OpenAI Chat API
        messages = [{"role": "system",
                     "content": "You are an assistant that helps convert text into a web search engine query, knowing that the default location is Nottingham in the UK. You output only 1 query for the latest message and nothing else."}]

        for message in history:
            messages.append({"role": "user", "content": message[0]})

        messages.append({"role": "user", "content": "Based on my previous messages, what is the most relevant web search query for the text below?\n\n"
                                                    "Text: " + query +
                                                    "\n\nQuery:"})

        # Generate search query using OpenAI Chat API
        search_query = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        ).choices[0].message.content

        return search_query.strip("\"")

    def get_chatgpt_response(self, history, query):
        
        play_mp3_file("wait.mp3")
        
        ga = GoogleAPI()
        
        # Get the search query
        search_query = self.get_search_query(history, query)

        #print("Search query: ", search_query)
        

        # Add a system message to the front
        messages = [{"role": "system",
                     "content": "You are a search assistant that answers questions based on search results. You do not include links in your response and keep the response concise."}]

        # Unpack history into messages
        for message in history:
            messages.append({"role": "user", "content": message[0]})
            if message[1]:
                messages.append({"role": "assistant", "content": message[1]})

        # Construct prompt from search results
        prompt = "Answer query using the information from the search results below: \n\n"
        results = ga.google_search(search_query)
        for result in results:
            prompt += "Link: " + result['link'] + "\n"
            prompt += "Title: " + result['title'] + "\n"
            prompt += "Content: " + result['snippet'] + "\n\n"
        prompt += "Query: " + query
        messages.append({"role": "user", "content": prompt})

        # Generate response using OpenAI Chat API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        ).choices[0].message.content

        # Only add query and response to history
        # The context is not needed
        history.append((query, response))

        return history
    
    def text_to_speech(self,history):
        client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=history[-1][1]
            ).stream_to_file(speech_file_path)
    
class SpeechRecognitonAPI():
    def listen(self,timeout=0):
        with sr.Microphone() as source:
            print("Listening")

            try:
                # Adjust microphone sensitivity and energy threshold
                recognizer.adjust_for_ambient_noise(source)
                #recognizer.energy_threshold = 4000 this is for more precise control setup and test on rpi

                # Set a timeout for listening
                audio = recognizer.listen(source,timeout)

                if audio:
                    print("Recognizing")
                    text = recognizer.recognize_google(audio)  # Convert speech to text
                    return text

                print("Timeout: Nothing was heard.")
                return None
            except sr.UnknownValueError:
                print("Unknown Value: Nothing was heard.")
                return None
            except sr.RequestError as e:
                print(f"Request Error: {e}")
                return None

    # Define a function that checks if the text contains the wake word
    def check_for_wakeword(self, text):
        if text is not None and wake_word in text.lower():
            return True
        else:
            return False     

def play_mp3_file(mp3_file_location):
    if sys.platform == 'darwin':
        os.system("afplay "+mp3_file_location)
    else:
        os.system("mpg123 "+mp3_file_location)
    
if __name__ == '__main__':
    sra = SpeechRecognitonAPI()
    oa = OpenaiAPI()
    history = []
    start_time = time.time()

    while True:
        try:
            if sra.check_for_wakeword(sra.listen()):
                print("Wake Word Detected")
                play_mp3_file("listening.mp3")
                user_input = sra.listen(timeout=5)
                
                history.append((user_input, None))

                history = oa.get_chatgpt_response(history, user_input)

                oa.text_to_speech(history)

                play_mp3_file("speech.mp3")
                    
                #reseting timer
                start_time = time.time()
            
            if time.time() - start_time > 60:
                print("No input for 60 seconds. Clearing history.")
                history = []
        except KeyboardInterrupt:
            exit()
        except:
            play_mp3_file("restarting.mp3")