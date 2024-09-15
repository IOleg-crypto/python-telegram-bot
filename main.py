from library import *

# Your bot token (keep it safe)
bot = telebot.TeleBot("6895824327:AAEyCfrTRh-7wGuIjrAVSe9y2gXxx1Vpunk")

user_credentials = {}
messages_to_clear = {}

CLIENT_ID = "0476ac8beb094d76bb56edc85caed325"
CLIENT_SECRET = "dfc7084b525f47088abbd76007364efc"

spotify_auth = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=spotify_auth)


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


# Get song name and artist from Google
@bot.message_handler(commands=["findgoogle"])
def get_song_google(message):
    try:
        # Ask the user for the song name
        msg = bot.reply_to(message, "Please enter the song name you want to search for on Google.")
        bot.register_next_step_handler(msg, find_song_google)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


# Get song name and artist from iTunes
@bot.message_handler(commands=["finditunes"])
def get_song_itunes(message):
    try:
        # Ask the user for the song name
        msg = bot.reply_to(message, "Please enter the song name you want to search for on iTunes.")
        bot.register_next_step_handler(msg, find_song_itunes)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


# Function to search Spotify for a song (scraping method, for educational purposes)
def find_song_spotify(message):
    try:
        query = message.text
        results = sp.search(q=query, limit=10, type='track')

        if results and results['tracks']['items']:
            tracks = results['tracks']['items']
            response = "\n".join(
                [f"{track['name']} by {track['artists'][0]['name']}\n{track['external_urls']['spotify']}" for track in
                 tracks]
            )
            bot.reply_to(message, f"Top Spotify results:\n{response}")
        else:
            bot.reply_to(message, "No results found on Spotify.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


# Command to find song on Spotify
@bot.message_handler(commands=["findspotify"])
def command_find_song(message):
    # Strip command part and pass only the song query
    query = message.text.lstrip('/findspotify').strip()

    if query:
        # Set message.text to the extracted query for find_song_spotify to use
        message.text = query
        find_song_spotify(message)  # Call the function to process the query
    else:
        # If no query is provided, prompt the user to input one
        bot.reply_to(message, "Please provide a song name after the command.")


# Handlers for button presses
# Example handler to trigger Spotify search
@bot.message_handler(func=lambda message: message.text.startswith("Find music in Spotify"))
def handle_spotify_search(message):
    bot.reply_to(message, "Please enter the song name you want to search for on Spotify.")
    bot.register_next_step_handler(message, find_song_spotify)


# Handle Google search button press
@bot.message_handler(func=lambda message: message.text == "Find music in Google")
def handle_google_button(message):
    get_song_google(message)


# Handle iTunes search button press
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
        results = search(query, num_results=5)  # Limiting to 5 results
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

    bot.send_message(chat_id, "Chat cleared.")


# Function to handle /website command
@bot.message_handler(commands=["website"])
def site(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Go to website", url="https://github.com/IOleg-crypto/")
    markup.add(button)

    bot.send_message(
        message.chat.id,
        "Author's repository: https://github.com/IOleg-crypto/",
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
        query = message.text
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
        bot.reply_to(message, "Please provide a song name")


def search_itunes(query):
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []


# Generic message handler
@bot.message_handler(func=lambda message: True)
def info(message):
    if message.text.lower() in ["hello", "hi"]:
        bot.reply_to(message, "Hello, how are you?")
    else:
        bot.reply_to(message, "I don't understand. Use command menu")


# Start polling
bot.polling(none_stop=True)
