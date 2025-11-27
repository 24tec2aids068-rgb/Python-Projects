from gtts import gTTS
from playsound import playsound

text = input("Enter text to convert to speech: ")

# Convert text → speech
speech = gTTS(text=text, lang='en')

# Save audio file
file = "output.mp3"
speech.save(file)
print("Audio saved as output.mp3")

# Play the audio
playsound(file)
