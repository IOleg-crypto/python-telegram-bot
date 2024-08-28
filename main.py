from library import *
from spotifysearch.client import Client

# Bot token and Spotify credentials
bot = telebot.TeleBot("6895824327:AAEyCfrTRh-7wGuIjrAVSe9y2gXxx1Vpunk")
SPOTIFY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"
user_credentials = {}
messages_to_clear = {}


# Function to get Spotify client credentials
def get_spotify_client(chat_id):
    if (
            chat_id in user_credentials
            and "client_id" in user_credentials[chat_id]
            and "client_secret" in user_credentials[chat_id]
    ):
        client_id = user_credentials[chat_id]["client_id"]
        client_secret = user_credentials[chat_id]["client_secret"]
        return spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )
    else:
        return None


# Function to log messages for future clearing
def log_message(message):
    chat_id = message.chat.id
    if chat_id not in messages_to_clear:
        messages_to_clear[chat_id] = []
    messages_to_clear[chat_id].append(message.message_id)


# Start command handler
@bot.message_handler(commands=["start"])
def start(message):
    
    local_name = f"Hello, <b>{message.from_user.first_name + ' ' + message.from_user.last_name}</b>"
    bot.send_message(message.chat.id, local_name, parse_mode="html")

    # Create reply keyboard
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton("Find music in Spotify")
    itembtn2 = types.KeyboardButton("Find music in Google")
    itembtn3 = types.KeyboardButton("Find music in iTunes")
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(
        message.chat.id,
        "Please choose one of the following options:",
        reply_markup=markup,
    )
# get song name and artist
@bot.message_handler(commands=["findgoogle"])
def get_song_google(message):
    try:
        # Ask the user for the song name
        msg = bot.reply_to(message, "Please enter the song name you want to search for on Google.")
        bot.register_next_step_handler(msg, find_song_google)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")
@bot.message_handler(commands=["finditunes"])
def get_song_itunes(message):
    try:
        # Ask the user for the song name
        msg = bot.reply_to(message, "Please enter the song name you want to search for on ITunes.")
        bot.register_next_step_handler(msg, find_song_itunes)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")



# Handlers for button presses
@bot.message_handler(func=lambda message: message.text == "Find music in Spotify")
def handle_spotify_button(message):
    find_song_spotify(message)


@bot.message_handler(func=lambda message: message.text == "Find music in Google")
def handle_google_button(message):
    get_song_google(message)


@bot.message_handler(func=lambda message: message.text == "Find music in iTunes")
def handle_itunes_button(message):
    get_song_itunes(message)


def function(message):
    return message.text == "Clear" or message.text == "clear"


@bot.message_handler(func=function)
def handle_clear_signal(message):
    clear_chat(message)


# Function to find songs on Google

def find_song_google(message):
    try:
        query = message.text + " song"
        results = search(query, num_results=30)
        if results:
            response = "Top search results:\n" + "\n".join(results)
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "No results found.")
    except IndexError:
        bot.reply_to(message, "Please provide a song name.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred while searching: {str(e)}")



# Function to clear chat messages
@bot.message_handler(commands=["clear"])
def clear_chat(message):
    chat_id = message.chat.id

    try:
        # Delete the last 100 messages or until an error occurs
        for message_id in range(message.message_id, message.message_id - 100, -1):
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Could not delete message {message_id}: {e}")
                break  # Break the loop if we can't delete a message
    except Exception as e:
        bot.reply_to(message, f"Error while deleting messages: {e}")

    bot.reply_to(message, "Chat cleared.")


# Function to set Spotify Client ID
def process_id_step(message):
    chat_id = message.chat.id
    client_id = message.text

    if chat_id not in user_credentials:
        user_credentials[chat_id] = {}

    user_credentials[chat_id]["client_id"] = client_id
    bot.reply_to(message, "Spotify Client ID set successfully!")


@bot.message_handler(commands=["set_id"])
def set_id(message):
    msg = bot.reply_to(message, "Please send your Spotify Client ID")
    bot.register_next_step_handler(msg, process_id_step)


# Function to set Spotify Client Secret
def process_secret_step(message):
    chat_id = message.chat.id
    client_secret = message.text

    if chat_id not in user_credentials:
        user_credentials[chat_id] = {}

    user_credentials[chat_id]["client_secret"] = client_secret
    bot.reply_to(message, "Spotify Client Secret set successfully!")


@bot.message_handler(commands=["set_secret"])
def set_secret(message):
    msg = bot.reply_to(message, "Please send your Spotify Client Secret")
    bot.register_next_step_handler(msg, process_secret_step)


# Function to handle /website command
@bot.message_handler(commands=["website"])
def site(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Go to website", url="https://github.com/IOleg-crypto/")
    markup.add(button)

    bot.send_message(
        message.chat.id,
        "That author's repository: https://github.com/IOleg-crypto/",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "Go to website")
def go_to_website(message):
    bot.send_message(
        message.chat.id,
        "Opening the website: https://github.com/IOleg-crypto/",
    )


# Function to search iTunes for a song
def find_song_itunes(message):
    try:
        query = message.text.split(" ", 1)[1]
        results = search_itunes(query)
        if results:
            response = "\n".join(
                [
                    f"{song['trackName']} by {song['artistName']}\n{song['trackViewUrl']}"
                    for song in results[:5]
                ]
            )
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "No results found.")
    except IndexError:
        bot.reply_to(message, "Please provide a song name. For example: /finditunes Imagine")


def search_itunes(query):
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []


# Function to search Spotify for a song
@bot.message_handler(commands=["findspotify"])
def find_song_spotify(message):
    try:
        query = message.text.split(" ", 1)[1]
        client = Client(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
        search_results = client.search(query)

        if search_results and search_results.get_tracks():
            track = search_results.get_tracks()[0]
            track_info = f"{track.name} by {track.artist.name}\n{track.url}"
            bot.reply_to(message, track_info)
        else:
            bot.reply_to(message, "No results found on Spotify.")
    except IndexError:
        bot.reply_to(message, "Please provide a song name. For example: /findspotify Imagine")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


# Generic message handler
@bot.message_handler(func=lambda message: True)
def info(message):
    if message.text.lower() in ["hello", "hi"]:
        bot.reply_to(message, "Hello, how are you?")
    else:
        bot.reply_to(message, "I don't understand. Use command menu")


# Start polling
bot.infinity_polling()
