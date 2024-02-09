import streamlit as st
import time
import speech_recognition as sr
import pyttsx3
import pygame

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def countdown_timer(hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds

    while total_seconds:
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        st.write(f"Time Remaining: {timeformat}")

        time.sleep(1)
        total_seconds -= 1

    st.success("Time's up!")
    play_beep_sound()

def play_beep_sound():
    # Initialize pygame mixer
    pygame.mixer.init()

    # Loading sound file
    filename = "mixkit-censorship-beep-1082.wav"
    pygame.mixer.music.load(filename)

    # Play the beep sound
    pygame.mixer.music.play()

if __name__ == "__main__":
    st.title("Speech-Activated Countdown Timer ")

    with st.sidebar:
        st.write("### Voice Activation")
        activate_countdown = st.checkbox("Activate Countdown on 'Start'")

    # Input for hours, minutes, and seconds
    countdown_hours = st.number_input("Enter Countdown Hours:", min_value=0, value=0)
    countdown_minutes = st.number_input("Enter Countdown Minutes:", min_value=0, max_value=59, value=0)
    countdown_seconds = st.number_input("Enter Countdown Seconds:", min_value=0, max_value=59, value=0)

    # Added a start button
    manual_start = st.button("Start Countdown Manually")

    if activate_countdown or manual_start:
        if activate_countdown:
            st.write("Say 'start' to start the countdown!")

        # Initializing speech recognition 
        recognizer = sr.Recognizer()

        try:
            if not manual_start:
                with sr.Microphone() as source:
                    audio_data = recognizer.listen(source, timeout=10)

                spoken_text = recognizer.recognize_google(audio_data).lower()

                if "start" in spoken_text:
                    st.success("Voice detected! Starting Countdown...")
                    countdown_timer(countdown_hours, countdown_minutes, countdown_seconds)
                else:
                    st.error("Did not recognize voice. Try again!")
                    
            else:
                st.success("Manual countdown starting...")
                countdown_timer(countdown_hours, countdown_minutes, countdown_seconds)

        except sr.UnknownValueError:
            st.warning("Speech recognition could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
