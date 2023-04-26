This chatbot retrieves information regards movies and provides recommondations to the user. I used TMDB API to generate my knowledge base by saving the top 40 popular movies. The goal was to have a dynamic conversation regarding movies it fetches, but I ran into some issues so I hard coded responses and included some rule based intents for the bot to follow. 

In order to run is by using PyCharm you must have the chatbot.py, knowledge_base.txt, user pickle, and the intents in the same directory and manually run the program. Once ran it should automatically generate the Knowledge_Base
but it's probably best just to use the knowledge_base.txt since you would need to have your own API KEY from TMDB and users_models.p. 

An issue you might run into is when it prompts for the name it might not accept it the first time. Theres some issues extracting particular names, but if you input "My name is" it should be able to extract your name. When an existing user is loaded it displays their likes and dislikes and in order for a genre to get added to their likes/dislikes the user must input something similar to " I really love horror movies" and based off the inputs sentiment score it would be added to the users likes. 

When you first run it, prompts user, if new user it creates it inside the txt file/pickle file. It asks for genre of movie(drama, horror thriller, action, fantasy, science fiction) or you can simply type the name of the movie and it should give back a list or the movie details.

Here's some sample dialog

Hi, I'm MovieBot, I love to talk about movies! What is your name?
You: Alan
Welcome back, Alan! Here are your favorite genres: action, adventure, horror, drama and the ones you dislike: horror
You: I like horror movies
sentiment score  0.0
I recommend you to watch the following Horror movies:
- The Pope's Exorcist
- Winnie the Pooh: Blood and Honey
- The Park
- The Mummy Resurrection

You: Can you give more info about Evil Dead
sentiment score  -1.2
Here's more information about evil dead rise:
Release Date: 2023-04-12
Genres: Horror, Thriller, Fantasy
Overview: Two sisters find an ancient book that gives birth to bloodthirsty demons that run amok in a Los Angeles apartment building and thrusts them into a primal battle for survival as they face the most nightmarish version of family imaginable.
Vote Average: 7.6
Any other genres(action, thriller, horror, comedy,drama, family, fantasy, Science Fiction, adventure)  you'd be interested in?

You: top rated
sentiment score  0.5
The highest rated movie is Puss in Boots: The Last Wish with a rating of 8.307.
