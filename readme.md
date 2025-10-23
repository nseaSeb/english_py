# 🎧 Voice & TTS Practice App

Application interactive pour pratiquer l'anglais avec reconnaissance vocale et synthèse vocale (Text-to-Speech).
<img width="1242" height="568" alt="image" src="https://github.com/user-attachments/assets/36aea02e-f036-48f6-9efd-36d9a672dafd" />

## 📋 Fonctionnalités

-   **🎙️ Reconnaissance vocale** : Parlez dans le microphone et l'application reconnaîtra ce que vous avez dit
-   **🎲 Phrases aléatoires** : Écoutez des phrases anglaises choisies aléatoirement
-   **✍️ Texte personnalisé** : Saisissez votre propre texte et écoutez-le prononcé
-   **🔁 Répétition** : Répétez le dernier audio généré dans chaque onglet

## 🛠️ Prérequis

-   Python 3.8 ou supérieur
-   Un microphone (pour la reconnaissance vocale)
-   Des haut-parleurs ou un casque

### Prérequis système (Linux/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

### Prérequis système (macOS)

```bash
brew install portaudio
```

### Prérequis système (Windows)

PyAudio devrait s'installer automatiquement avec pip. Si vous rencontrez des problèmes, téléchargez le fichier wheel approprié depuis
[ici](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

## 📦 Installation

### 1. Cloner ou télécharger le projet

```bash
git clone https://github.com/nseaSeb/english_py.git
cd voice-tts-app
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/macOS :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Télécharger les modèles de voix Piper

Créez un dossier `voices` et téléchargez les modèles ONNX depuis le [dépôt Piper](https://github.com/rhasspy/piper/releases).

```bash
mkdir voices
cd voices
```

Téléchargez au moins un de ces modèles :

-   `en_US-joe-medium.onnx` (voix masculine américaine - utilisée par défaut)
-   `en_US-lessac-medium.onnx` (voix féminine américaine)
-   `en_GB-alan-medium.onnx` (voix masculine britannique)

**Important** : Téléchargez aussi les fichiers `.json` correspondants (même nom que le fichier .onnx).

Exemple de téléchargement :

**Avec wget (Linux) :**

```bash
# Télécharger la voix (remplacez l'URL par la version actuelle)
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-joe-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-joe-medium.onnx.json
```

**Avec curl (macOS) :**

```bash
# Télécharger la voix (remplacez l'URL par la version actuelle)
curl -L -O https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-joe-medium.onnx
curl -L -O https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-joe-medium.onnx.json
```

### 5. Structure des fichiers

Votre projet devrait ressembler à ceci :

```
voice-tts-app/
├── voice_app_updated.py
├── requirements.txt
├── README.md
└── voices/
    ├── en_US-joe-medium.onnx
    ├── en_US-joe-medium.onnx.json
    └── (autres modèles optionnels)
```

## 🚀 Exécution

### Lancer l'application

```bash
python app.py
```

Selon votre installation ce peut être aussi

```bash
python3 app.py
```

L'application ouvrira automatiquement une interface web dans votre navigateur par défaut (généralement à l'adresse `http://127.0.0.1:7860`).

### Changer de voix

Ouvrez le fichier `voice_app_updated.py` et modifiez la ligne :

```python
model_path = "./voices/en_US-joe-medium.onnx"
```

Remplacez par le chemin vers un autre modèle de voix.

## 📖 Utilisation

### Onglet "Speech Recognition"

1. Cliquez sur le bouton du microphone
2. Parlez en anglais
3. Cliquez sur "Transcribe & Speak Back"
4. L'application affichera ce qu'elle a compris et le répètera à voix haute

### Onglet "Random Sentences"

1. Cliquez sur "🎲 Choose & Speak a Sentence"
2. Une phrase aléatoire sera choisie et prononcée
3. La phrase apparaît dans le champ texte

### Onglet "Custom Text"

1. Tapez votre texte dans le champ
2. Cliquez sur "🔊 Speak This Text"
3. Le texte sera prononcé à voix haute

### Bouton de répétition

Chaque onglet dispose d'un bouton "🔁 Répéter" pour rejouer le dernier audio généré.

## 🔧 Dépannage

### Erreur de microphone

-   Vérifiez que votre microphone est correctement connecté
-   Autorisez l'accès au microphone dans votre navigateur
-   Vérifiez les permissions du système

### Erreur audio

-   Vérifiez que vos haut-parleurs/casque fonctionnent
-   Le script affiche les périphériques audio disponibles au démarrage

### PyAudio ne s'installe pas

-   Sur Linux : `sudo apt-get install portaudio19-dev python3-pyaudio`
-   Sur macOS : `brew install portaudio`
-   Sur Windows : Utilisez un fichier wheel pré-compilé

### Problème de connexion (Speech Recognition)

La reconnaissance vocale utilise l'API Google et nécessite une connexion Internet.

## 📝 Personnalisation

### Ajouter des phrases aléatoires

Modifiez la liste `phrases` dans le fichier Python :

```python
phrases = [
    "Good morning! How are you today?",
    "Votre nouvelle phrase ici",
    # ...
]
```

### Changer la langue de reconnaissance

Modifiez le paramètre `language` dans la fonction `recognize_and_reply` :

```python
text = recognizer.recognize_google(audio_data, language="en-US")
```

Langues disponibles : `en-US`, `en-GB`, `fr-FR`, etc.

## 📄 Licence

Ce projet utilise :

-   Gradio (Apache 2.0)
-   Piper TTS (MIT)
-   SpeechRecognition (BSD)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📧 Support

Pour toute question ou problème, ouvrez une issue sur le dépôt GitHub.

---

**Bon apprentissage de l'anglais ! 🎓🇬🇧🇺🇸**
