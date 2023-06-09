import openai
import pyttsx3
import speech_recognition as sr
import time

#Set your OpenAI API key
openai.api_key = ""

#Initializes the text to speech engine
engine = pyttsx3.init()

#Function to transform audio to text
def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unkown error")

#Obtains the response for GPT in text format
def generate_response(prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop = None,
        temperature = 0.5
    )
    return response["choices"][0]["text"]

#Converts the response into audio
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

#Main function
def main():
    while True:
        print("Say 'Hello' to start recording!")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hello":
                    #Record audio
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wave_data())
                    
                    #Transcribe audio to text
                    text = trascribe_audio_to_text(filename)
                    if text:
                        print("You said {text}")

                        #Generate response
                        response = generate_response(text)
                        print("GPT3 says {response}")

                        #Read the response
                        speak_text(response)
            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
