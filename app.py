import random
import gradio as gr
import speech_recognition as sr
from piper.voice import PiperVoice
import numpy as np
import sounddevice as sd


print(sd.query_devices())
print(sd.default.device)

# Charger le modèle Piper
# model_path = "./voices/en_US-lessac-medium.onnx"
# model_path = "./voices/en_GB-alan-medium.onnx"
model_path = "./voices/en_US-joe-medium.onnx"
voice = PiperVoice.load(model_path)

# Variables globales pour stocker le dernier audio
last_audio_data = None
last_sample_rate = None

def play_tts_simple(text):
    """Version simplifiée utilisant directement les données audio"""
    global last_audio_data, last_sample_rate
    
    try:
        print(f"Synthèse simple de: '{text}'")
        
        audio_stream = voice.synthesize(text)
        
        # Prendre le premier chunk pour les métadonnées
        first_chunk = next(audio_stream)
        sample_rate = first_chunk.sample_rate
        
        # Collecter toutes les données audio
        all_audio_bytes = first_chunk.audio_int16_bytes
        
        for audio_chunk in audio_stream:
            all_audio_bytes += audio_chunk.audio_int16_bytes
        
        # Stocker pour la répétition
        last_audio_data = all_audio_bytes
        last_sample_rate = sample_rate
        
        # Convertir en numpy array et jouer directement
        audio_array = np.frombuffer(all_audio_bytes, dtype=np.int16)
        sd.play(audio_array, sample_rate)
        sd.wait()
        
        print("Audio joué avec la méthode simple")
        
    except Exception as e:
        print(f"Erreur dans play_tts_simple: {e}")

def repeat_last_audio():
    """Répète le dernier audio généré"""
    global last_audio_data, last_sample_rate
    
    if last_audio_data is not None and last_sample_rate is not None:
        try:
            print("Répétition de l'audio...")
            audio_array = np.frombuffer(last_audio_data, dtype=np.int16)
            sd.play(audio_array, last_sample_rate)
            sd.wait()
            return "🔊 Audio répété !"
        except Exception as e:
            print(f"Erreur lors de la répétition: {e}")
            return "❌ Erreur lors de la répétition"
    else:
        return "❌ Aucun audio à répéter - générez d'abord un audio"

# Initialiser la reconnaissance vocale
recognizer = sr.Recognizer()

# Liste de phrases aléatoires
phrases = [
    # Salutations et politesse
    "Good morning! How are you?",
    "Good afternoon!",
    "Good evening!",
    "Nice to meet you.",
    "How are you doing?",
    "Have a great day!",
    "See you later!",
    "Take care!",
    "Thank you very much.",
    "You're welcome.",
    "Excuse me.",
    "I'm sorry.",
    "No problem.",
    "My pleasure.",
    
    # Présentations
    "My name is...",
    "I'm from France.",
    "Nice to meet you too.",
    "What's your name?",
    "Where are you from?",
    
    # Communication de base
    "Can you repeat that, please?",
    "I don't understand.",
    "Could you speak more slowly?",
    "What does that mean?",
    "How do you say that in English?",
    "Can you help me?",
    "I'm sorry, I don't speak English very well.",
    "Do you speak French?",
    
    # Questions essentielles
    "Where is the bathroom?",
    "How much does it cost?",
    "What time is it?",
    "Where is...?",
    "Can I have...?",
    "Do you have...?",
    "Is there a... nearby?",
    
    # Restaurant et nourriture
    "I'm hungry.",
    "I'm thirsty.",
    "Can I see the menu, please?",
    "I'd like to order.",
    "The check, please.",
    "Can I have some water?",
    "This looks delicious!",
    "I'm allergic to...",
    "Do you have vegetarian options?",
    
    # Shopping
    "How much is this?",
    "Can I try this on?",
    "Do you have this in a different size?",
    "I'm just looking, thanks.",
    "I'll take it.",
    "Can I pay by card?",
    "Do you accept credit cards?",
    
    # Directions
    "I'm lost.",
    "Can you show me on the map?",
    "How do I get to...?",
    "Is it far from here?",
    "Turn left.",
    "Turn right.",
    "Go straight ahead.",
    "It's on the right.",
    "It's on the left.",
    
    # Urgences
    "Help!",
    "Call the police!",
    "I need a doctor.",
    "It's an emergency.",
    "Where is the hospital?",
    "I need help.",
    
    # Transports
    "Where is the train station?",
    "What time does the bus leave?",
    "A ticket to..., please.",
    "Which platform?",
    "Is this seat taken?",
    "Excuse me, this is my seat.",
    
    # Hôtel
    "I have a reservation.",
    "Can I check in?",
    "What time is checkout?",
    "Can I have the wifi password?",
    "Is breakfast included?",
    "Can you call a taxi for me?",
    
    # Conversation courante
    "That makes sense.",
    "I see what you mean.",
    "Let me think about it.",
    "If I understand correctly...",
    "That's a good point.",
    "I agree.",
    "I disagree.",
    "What do you think?",
    "In my opinion...",
    "It's up to you.",
    "I'm not sure.",
    "Maybe.",
    "Definitely.",
    "Probably.",
    "I'll be right back.",
    "Just a moment, please.",
    "Sounds good!",
    "No worries.",
    "That's okay.",
    "Don't worry about it."
]

# Reconnaissance vocale + réponse audio
def recognize_and_reply(audio):
    if audio is None:
        return "No sound detected."
    
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="en-US")
        except sr.UnknownValueError:
            text = "I didn't understand."
        except sr.RequestError:
            text = "Connection error."
    
    reply = f"Did you say {text}?"
    play_tts_simple(reply)
    return reply

# Lecture d'une phrase aléatoire
def say_random_sentence():
    sentence = random.choice(phrases)
    play_tts_simple(sentence)
    return f"🎲 {sentence}"

# Lecture d'une phrase personnalisée
def say_custom_text(text):
    if not text or text.strip() == "":
        return "❌ Veuillez saisir un texte"
    
    play_tts_simple(text)
    return f"🔊 {text}"

# Interface Gradio avec trois onglets
with gr.Blocks() as demo:
    gr.Markdown("# 🎧 Voice & TTS Practice App")
    

    with gr.Tab("🎙️ Speech Recognition"):
        gr.Markdown("Speak into the microphone. The app will recognize what you said and reply aloud.")
        mic_input = gr.Audio(sources=["microphone"], type="filepath", label="Speak here")
        stt_output = gr.Textbox(label="Recognized text")
        mic_button = gr.Button("Transcribe & Speak Back")
        mic_button.click(fn=recognize_and_reply, inputs=mic_input, outputs=stt_output)
        
        # Bouton de répétition dans l'onglet
        with gr.Row():
            tab_repeat_button = gr.Button("🔁 Répéter la réponse", variant="secondary")
            tab_repeat_output = gr.Textbox(label="Status", interactive=False)

    with gr.Tab("🎲 Random Sentences"):
        gr.Markdown("Click below to hear a random English sentence.")
        random_output = gr.Textbox(label="Sentence played", interactive=False)
        random_button = gr.Button("🎲 Choose & Speak a Sentence")
        random_button.click(fn=say_random_sentence, outputs=random_output)
        
        # Bouton de répétition dans l'onglet
        with gr.Row():
            random_repeat_button = gr.Button("🔁 Répéter la phrase", variant="secondary")
            random_repeat_output = gr.Textbox(label="Status", interactive=False)

    with gr.Tab("✍️ Custom Text"):
        gr.Markdown("Type any text below and click the button to hear it spoken aloud.")
        custom_input = gr.Textbox(
            label="Your text",
            placeholder="Type your sentence here...",
            lines=3
        )
        custom_output = gr.Textbox(label="Text played", interactive=False)
        custom_button = gr.Button("🔊 Speak This Text")
        custom_button.click(fn=say_custom_text, inputs=custom_input, outputs=custom_output)
        
        # Bouton de répétition dans l'onglet
        with gr.Row():
            custom_repeat_button = gr.Button("🔁 Répéter le texte", variant="secondary")
            custom_repeat_output = gr.Textbox(label="Status", interactive=False)

    gr.Markdown("App powered by Python, PiperTTS and Gradio.")
    
    # Connexions des boutons de répétition
    tab_repeat_button.click(fn=repeat_last_audio, outputs=tab_repeat_output)
    random_repeat_button.click(fn=repeat_last_audio, outputs=random_repeat_output)
    custom_repeat_button.click(fn=repeat_last_audio, outputs=custom_repeat_output)

demo.launch()