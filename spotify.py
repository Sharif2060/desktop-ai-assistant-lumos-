import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import speech_recognition as sr

# Set your Spotify credentials (Replace with your Spotify API credentials)
CLIENT_ID = "your_spotify_client_id"
CLIENT_SECRET = "your_spotify_client_secret"

# Spotify authentication (No need for Premium features, only public data access)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

# Function to get user's voice command for music
def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a song to play...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            return None

# Function to search and open song in Spotify Web Player
def open_song_in_spotify(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_url = track['external_urls']['spotify']
        print(f"Opening: {track['name']} by {track['artists'][0]['name']}")
        webbrowser.open(track_url)
    else:
        print(f"Sorry, I couldn't find the song: {song_name}")

# Main function to listen to the command and open the requested song
def main():
    song_name = get_voice_command()
    if song_name:
        open_song_in_spotify(song_name)

if __name__ == "__main__":
    main()
