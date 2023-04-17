#axp200075
#alan perez
#cs4395.001

import pickle
import json
import os
import csv
import random

import requests
import openai
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from textblob import TextBlob

# Fetching data from API to build the KB

API_KEY = ''
BASE_URL = ''


def generate_response(prompt):
    model_engine = 'text-davinci-002'
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text.strip()


def get_popular_movies(page=1):
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&page={page}"
    response = requests.get(url)
    popular_movies = response.json()
    return popular_movies['results']


# Fetch movie information by movie_id
def fetch_movie_info(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}?api_key={API_KEY}'
    response = requests.get(url)
    return response.json()


# Build the knowledge base
def build_knowledge_base(pages=1):
    knowledge_base = []
    for page in range(1, pages + 1):
        print("building knowledge base....")
        popular_movies = get_popular_movies(page)
        for movie_data in popular_movies:
            movie = fetch_movie_info(movie_data['id'])
            movie_entry = build_movie_entry(movie)
            knowledge_base.append(movie_entry)
    return knowledge_base


# Get the information you want to store in the knowledge base
def build_movie_entry(movie_data):
    movie_entry = {
        'id': movie_data['id'],
        'title': movie_data['title'],
        'release_date': movie_data['release_date'],
        'genres': [genre['name'] for genre in movie_data['genres']],
        'overview': movie_data['overview'],
        'vote_average': movie_data['vote_average']
    }
    # if 'credits' in movie_data and 'cast' in movie_data['credits']:
    #     movie_entry['actors'] = [cast['name'] for cast in movie_data['credits']['cast']]
    return movie_entry


# Build the knowledge base with 2 pages of popular movies (40 movies)
def save_knowledge_base(knowledge_base, file_path):
    # with open(file_path, 'wb') as f:
    #     pickle.dump(knowledge_base, f)
    with open(file_path, 'w') as f:
        json.dump(knowledge_base, f)


def load_knowledge_base(file_path):
    # with open(file_path, 'rb') as f:
    #     knowledge_base = pickle.load(f)
    with open(file_path, 'r') as f:
        knowledge_base = json.load(f)
    return knowledge_base


# Check if knowledge base file exists
knowledge_base_file = 'knowledge_base.txt'
if os.path.exists(knowledge_base_file):
    # Load knowledge base from file
    knowledge_base = load_knowledge_base(knowledge_base_file)
else:
    # Build the knowledge base and save to file
    knowledge_base = build_knowledge_base(pages=2)
    print("building...")
    save_knowledge_base(knowledge_base, knowledge_base_file)

# Test knowledge base
# print(knowledge_base)


# load the intents json
def load_intents(intent_json):
    with open('intents.json') as file:
        data = json.load(file)
    return data


GREETINGS = ['hello', 'hi', 'yo', 'hey', 'what up', 'sup', 'hola']
EXITING_STATEMENTS = ['bye', 'goodbye', 'adios', 'see ya', 'smell ya later', 'peace', "i'm outtie"]


class User:
    def __init__(self, name):
        self.name = name
        self.search_history = []
        self.likes = []
        self.dislikes = []

    def save_pickle(self):
        user_models = {}

        if os.path.exists('user_models.p'):
            with open('user_models.p', 'rb') as f:
                user_models = pickle.load(f)

        user_models[self.name] = self

        with open('user_models.p', 'wb') as f:
            pickle.dump(user_models, f)

    def save_csv(self):
        if not os.path.exists('user_models.csv'):
            with open('user_models.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["name", "search_history", "likes", "dislikes"])

        with open('user_models.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            rows = [row for row in reader]

        with open('user_models.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            found = False
            for row in rows:
                if row and row[0] == self.name:
                    writer.writerow([self.name, self.search_history, self.likes, self.dislikes])
                    found = True
                else:
                    writer.writerow(row)

            if not found:
                writer.writerow([self.name, self.search_history, self.likes, self.dislikes])

    @classmethod
    def load_pickle(cls, name):
        try:
            with open('user_models.p', 'rb') as f:
                user_models = pickle.load(f)
            return user_models.get(name)
        except FileNotFoundError:
            return None

    @classmethod
    def load_csv(cls, name):
        if not os.path.exists('user_models.csv'):
            return None

        with open('user_models.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == name:
                    search_history = eval(row[1])
                    likes = eval(row[2])
                    dislikes = eval(row[3])
                    return cls(name, search_history, likes, dislikes)

        return None


def extract_name(user_input):
    # tokenize input

    tokens = word_tokenize(user_input)

    # pos tagging
    tags = pos_tag(tokens)

    # Look for name
    for name, tag in tags:
        if tag == 'NNP':
            return name
    # return none if no jname
    return None


positive_words = ['like', 'love', 'enjoy', 'adore', 'great', 'good']
negative_words = ['dislike', 'hate', 'loathe', 'terrible', 'awful', 'bad']


def preprocess_user_input(user_response, user_object, intents_data, knowledge_base):
    # Tokenize user input
    tokens = word_tokenize(user_response.lower())
    tokenized = [w for w in tokens if w.isalpha() and w not in stopwords.words('english')]

    # Tag the parts of speech in the user's response
    user_response_postag = pos_tag(tokens)

    # Identify any positive or negative words in the response
    response_label = None
    for word, pos in user_response_postag:
        if pos.startswith('JJ'):
            if word in positive_words:
                response_label = 'like'
            elif word in negative_words:
                response_label = 'dislike'

    # Label the response as a question and add it to the user's search history
    question_label = False
    if '?' in user_response:
        question_label = True
    user_object.search_history.append({'question': question_label, 'response': user_response})

    sentiment_scores = []
    for token in tokenized:
        sentiment_scores.append(TextBlob(token).sentiment.polarity)

    overall_sentiment_score = sum(sentiment_scores)

    # Create sets for genres, movie titles, and actor names
    genres = set()
    movie_titles = set()
    ratings = set()

    for movie in knowledge_base:
        movie_titles.add(movie['title'].lower())
        for genre in movie['genres']:
            genres.add(genre.lower())
        ratings.add(str(movie['vote_average']))

    # Add the labeled response to the user's likes or dislikes list
    if response_label == 'like':
        genre = next((token for token in tokenized if token in genres), None)
        if genre and genre not in user_object.likes:
            user_object.likes.append(genre)
            print(f"Added {genre} to likes")
    elif response_label == 'dislike':
        genre = next((token for token in tokenized if token in genres), None)
        if genre and genre not in user_object.dislikes:
            user_object.dislikes.append(genre)
            print(f"Added {genre} to dislikes")

    # Identify the intent using the intents_data
    lemmatizer = WordNetLemmatizer()
    tokenized_lemmatized = [lemmatizer.lemmatize(w) for w in tokenized]
    intent_scores = {intent["tag"]: 0 for intent in intents_data["intents"]}


    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = word_tokenize(pattern.lower())
            pattern_tokens_lemmatized = [lemmatizer.lemmatize(w) for w in pattern_tokens]
            common_tokens = set(tokenized_lemmatized).intersection(pattern_tokens_lemmatized)
            intent_scores[intent["tag"]] += len(common_tokens)

    identified_intent = max(intent_scores, key=intent_scores.get)

    # Check if any of the preprocessed tokens match any of the items in the sets
    mentioned_genre = None
    mentioned_movie_title = None
    mentioned_rating = None

    for token in tokenized:
        if token in genres:
            mentioned_genre = token
        if any(token in movie_title.lower() for movie_title in movie_titles):
            mentioned_movie_title = next(movie_title for movie_title in movie_titles if token in movie_title.lower())
        if token in ratings:
            mentioned_rating = token

    if overall_sentiment_score > 0:
        if mentioned_genre and mentioned_genre not in user_object.likes:
            user_object.likes.append(mentioned_genre)
            print(f"Added {mentioned_genre} to likes")
    elif overall_sentiment_score < 0:
        if mentioned_genre and mentioned_genre not in user_object.dislikes:
            user_object.dislikes.append(mentioned_genre)
            print(f"Added {mentioned_genre} to dislikes")
    print('sentiment score ', overall_sentiment_score)
    return tokenized, identified_intent, mentioned_genre, mentioned_movie_title,mentioned_rating, overall_sentiment_score

def get_sentiment(overview):
    analysis = TextBlob(overview)
    return analysis.sentiment.polarity


def add_sentiment_analysis(knowledge_base):
    for movie_id, movie_data in knowledge_base.items():
        movie_data['overview_sentiment'] = get_sentiment(movie_data['overview'])


def recommend_movie_by_genre(genre, knowledge_base):
    recommended_movies = []
    for movie in knowledge_base:
        if genre.lower() in [g.lower() for g in movie['genres']]:
            recommended_movies.append(movie['title'])
    return recommended_movies


def recommend_movie_by_sentiment(sentiment, knowledge_base):
    recommended_movies = []
    for movie in knowledge_base:
        if movie['overview_sentiment'] >= float(sentiment):
            recommended_movies.append(movie['title'])
    return recommended_movies


def recommend_movie_by_rating(rating, knowledge_base):
    recommended_movies = []
    for movie in knowledge_base:
        if movie['vote_average'] >= float(rating):
            recommended_movies.append(movie['title'])
    return recommended_movies


def find_movie_info(title, knowledge_base):
    for movie in knowledge_base:
        if title.lower() == movie['title'].lower():
            return movie
    return None


def get_recommendations(user, knowledge_base, num_recommendations=5):
    recommended_movies = []

    for movie in knowledge_base:
        # Check if the movie matches the user's preferences
        if movie['title'] not in user.likes and movie['title'] not in user.dislikes:
            movie_genres = set(movie['genres'])
            liked= set(genre.lower() for genre in user.likes)
            disliked = set(genre.lower() for genre in user.dislikes)

            if movie_genres.intersection(liked) and not movie_genres.intersection(disliked):
                recommended_movies.append(movie)

    # Sort the movies by rating and return the top num_recommendations movies
    recommended_movies.sort(key=lambda x: x['vote_average'], reverse=True)
    return recommended_movies[:num_recommendations]
def moviebot():
    intents_data = load_intents('intents.json')
    print("Hi, I'm MovieBot, I love to talk about movies! What is your name?")
    user_input = input("You: ")
    name = extract_name(user_input)

    while not name:
        print("Sorry, I didn't catch your name. Can you please tell me your name again?")
        user_input = input("You: ")
        name = extract_name(user_input)

        # Check if the user already exists
    user = User.load_pickle(name)
    if not user:
        print(f"Hello, {name}. What genre of movies do you enjoy?")
        user = User(name)
        user.save_pickle()
    else:
        print(f"Welcome back, {name}. What other genre of movies do you enjoy?")

    while True:
        user_input = input("You: ")

        # Exit the conversation if the user input is an exit statement
        if user_input.lower() in EXITING_STATEMENTS:
            break

        preprocessed_input, identified_intent, mentioned_genre, mentioned_movie_title, mentioned_rating, overall_sentiment_score = preprocess_user_input(
            user_input, user, intents_data, knowledge_base)

        user.save_pickle()
        if identified_intent == 'genres':
            if mentioned_genre:
                recommended_movies = recommend_movie_by_genre(mentioned_genre, knowledge_base)
                if recommended_movies:
                    print(f"I recommend you to watch the following {mentioned_genre.capitalize()} movies:")
                    for movie_title in recommended_movies:
                        print(f"- {movie_title}")
                else:
                    print(f"Sorry, I couldn't find any movies in the {mentioned_genre} genre.")
            else:
                print(f"Please mention a genre, so I can recommend a movie.")
        elif mentioned_movie_title:
            movie_info = find_movie_info(mentioned_movie_title, knowledge_base)
            if movie_info:
                print(f"Here's more information about {mentioned_movie_title}:")
                print(f"Release Date: {movie_info['release_date']}")
                print(f"Genres: {', '.join(movie_info['genres'])}")
                print(f"Overview: {movie_info['overview']}")
                print(f"Vote Average: {movie_info['vote_average']}")
            else:
                print(f"Sorry, I couldn't find any information about {mentioned_movie_title}.")
            print(
                "Any other genres(action, thriller, horror, comedy,drama, family, fantasy, Science Fiction, adventure)  you'd be interested in?")
        elif identified_intent == 'genre':
            if mentioned_genre:
                recommended_movies = recommend_movie_by_genre(mentioned_genre, knowledge_base)
                if recommended_movies:
                    print(f"I recommend you to watch the following {mentioned_genre.capitalize()} movies:")
                    for movie_title in recommended_movies:
                        print(f"- {movie_title}")
                else:
                    print(f"Sorry, I couldn't find any movies in the {mentioned_genre} genre.")
            else:
                print(f"Please mention a genre, so I can recommend a movie.")
        elif identified_intent == 'genre_info':
            if mentioned_genre:
                recommended_movies = recommend_movie_by_genre(mentioned_genre, knowledge_base)
                if recommended_movies:
                    print(f"Some popular [genre] movies are [movies]. You might enjoy watching [movie1], [movie2], or [movie3].")
                    for movie_title in recommended_movies:
                        print(f"- {movie_title}")
                else:
                    print(f"Sorry, I couldn't find any movies in the {mentioned_genre} genre.")
            else:
                print(f"Please mention a genre, so I can recommend a movie.")
        elif identified_intent == 'rating':
            if mentioned_rating:
                recommended_movies = recommend_movie_by_rating(mentioned_rating, knowledge_base)
                if recommended_movies:
                    print(
                        f"I recommend you to watch the following movies with a rating of {mentioned_rating} or higher:")
                    print("Any other genres(action, thriller, horror, comedy,drama, family, fantasy, Science Fiction, adventure), title, or rating  you'd be interested in?")
                    for movie_title in recommended_movies:
                        print(f"- {movie_title}")
                else:
                    print(f"Sorry, I couldn't find any movies with a rating of {mentioned_rating} or higher.")
            else:
                print(f"Please mention a rating, so I can recommend a movie.")
        elif identified_intent == 'title':
            if mentioned_movie_title:
                movie_info = find_movie_info(mentioned_movie_title, knowledge_base)
                if movie_info:
                    print(f"Here's more information about {mentioned_movie_title}:")
                    print(f"Release Date: {movie_info['release_date']}")
                    print(f"Genres: {', '.join(movie_info['genres'])}")
                    print(f"Overview: {movie_info['overview']}")
                    print(f"Vote Average: {movie_info['vote_average']}")
                else:
                    print(f"Sorry, I couldn't find any information about {mentioned_movie_title}.")
            else:
                print(f"Please mention a movie title, so I can provide more information.")
        elif identified_intent == 'highest_rated':
            highest_rated_movie = max(knowledge_base, key=lambda x: x['vote_average'])
            print(
                f"The highest rated movie is {highest_rated_movie['title']} with a rating of {highest_rated_movie['vote_average']}.")
        elif identified_intent == 'thanks':
            print(random.choice((intents_data['intents'][2])['responses']))
            print("Any other genres you'd be interested in?")
        elif identified_intent == 'recommend_movie':
            recommended_movies = get_recommendations(user, knowledge_base)
            if recommended_movies:
                print("Here are some movies I recommend based on your preferences:")
                for movie in recommended_movies:
                    print(f"- {movie['title']}")
            else:
                print("Sorry, I couldn't find any movies to recommend based on your preferences.")
        elif identified_intent == 'fallback':
            prompt = f"User asked: {user_input}. Please provide a relevant response."
            generated_response = generate_response(prompt)
            print(generated_response)

    print("Goodbye!")


if __name__ == "__main__":
    # load the knowledge base
    kb = load_knowledge_base('knowledge_base.txt')


    # uncomment this out if you want to see the contents inside user
    # def print_pickle_contents():
    #     if not os.path.exists('user_models.p'):
    #         print("Pickle file not found.")
    #         return
    #
    #     with open('user_models.p', 'rb') as f:
    #         user_models = pickle.load(f)
    #
    #     for name, user in user_models.items():
    #         print(f"User: {name}")
    #         print(f"Search history: {user.search_history}")
    #         print(f"Likes: {user.likes}")
    #         print(f"Dislikes: {user.dislikes}")
    #         print()
    #
    #
    # print_pickle_contents()
    moviebot()
