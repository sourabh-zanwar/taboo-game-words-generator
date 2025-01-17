from flask import Flask, render_template_string, session
import random
import json

i = 0


def draw_word(keys):
    global i
    curr_word = keys[i]
    i += 1
    return curr_word, keys


def game_play(curr_word, action, completed_words):
    past_words = completed_words[action]
    past_words.append(curr_word)
    completed_words[action] = list(set(past_words))
    return completed_words


def complete_round(remaining_keys, completed_words):
    keys = remaining_keys + completed_words["skip"]
    keys = list(set(keys))
    # Reset the completed_words dictionary
    completed_words["skip"] = []
    completed_words["correct"] = []
    completed_words["incorrect"] = []
    return keys, completed_words


with open("./data/words_list.json", "r") as f:
    data = json.load(f)

keys = list(data.keys())
random.shuffle(keys)

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management


def update_keys(keys):
    curr_word, keys = draw_word(keys)
    return curr_word


# Function to get a random dictionary element
def get_item():
    curr_word = update_keys(keys)
    return curr_word, data[curr_word]


completed_words = {"skip": [], "correct": [], "incorrect": []}


def update_word_list_0(completed_words, curr_word, action):
    completed_words = game_play(curr_word, action, completed_words)


def update_word_list(curr_word, action):
    update_word_list_0(completed_words, curr_word, action)


@app.route("/")
def home():
    # Retrieve the action stored in the session (if any)
    action = session.get("action", "None")
    score = {
        "correct": len(completed_words["correct"]),
        "incorrect": len(completed_words["incorrect"]),
        "skip": len(completed_words["skip"]),
    }
    key, values = get_item()

    return render_template_string(
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Word List</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
                flex-direction: column;  /* Ensures elements stack vertically */
            }
            .key {
                background-color: #BE3144; /* Dark purple */
                color: white;
                font-weight: 900;
                padding: 20px;
                margin-bottom: 20px;
                font-size: xx-large;
                min-width: 250px
            }
            .value {
                background-color: #E17564; /* Light purple */
                color: black;
                padding: 10px;
                font-weight: 700;
                margin-bottom: 5px;
                font-size: x-large;
                min-width: 270px
            }
            .key, .value {
                width: 80%; /* You can adjust this as per your requirement */
                margin: 10px auto;
                border-radius: 5px;
                display: block; /* Ensures each element takes its own line */
            }
            .boxx {
                background-color: #09122C;
                padding: 10px;
                border-radius: 10px;
                min-width: 300px
            }
            .button-container {
                margin-top: 20px;
            }
            button {
                font-size: 16px;
                padding: 12px;
                margin: 3px;
                cursor: pointer;
                background-color: #BE3144;  /* Dark purple to match the theme */
                color: white;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #9e2542;  /* Slightly lighter purple on hover */
            }
            .button-container {
                margin-top: 10px;  /* To move it below the other buttons */
            }
            .correct {
                background-color: #387478;
                font-weight: 600;
                font-size: x-large;
            }
            .incorrect {
                background-color: #A04747;
                font-weight: 600;
                font-size: x-large;
            }
            .skip {
                background-color: #3C3D37;
                font-weight: 600;
                font-size: x-large;
            }
            .complete-round {
                background-color: #03346E;
                font-weight: 600;
                font-size: x-large;
                margin-top: 10px;
            }
            .score {
                margin-bottom: 20px;
                font-size: x-large;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="score">
            &#9989; {{ score['correct'] }} | &#10060; {{ score['incorrect'] }} | &#9193; {{ score['skip'] }}
        </div>
        <div class="boxx">
        <div class="key">{{ key }}</div>
        {% for value in values %}
            <div class="value">{{ value }}</div>
        {% endfor %}
        </div>
        <div class="button-container">
            <button class="skip" onclick="location.href='/action/skip'">Skip</button>
            <button class="correct" onclick="location.href='/action/correct'">Correct</button>
            <button class="incorrect" onclick="location.href='/action/incorrect'">Incorrect</button>
        </div>
        <div class="button-container">
            <button class="complete-round" onclick="location.href='/action/complete_round'">Complete Round</button>
        </div>
    </body>
    </html>
    """,
        score=score,
        key=key,
        values=values,
        action=action,
    )


@app.route("/action/<action>")
def action(action):
    # Store the action clicked in the session
    session["action"] = action
    global keys, completed_words

    if action == "complete_round":
        remaining_keys = keys[i:]  # The remaining keys after the current index
        keys, completed_words = complete_round(remaining_keys, completed_words)
        print("Round completed, updated keys:", keys)
    else:
        update_word_list(keys[i - 1], action)

    score = {
        "correct": len(completed_words["correct"]),
        "incorrect": len(completed_words["incorrect"]),
        "skip": len(completed_words["skip"]),
    }

    # Get a new random dictionary item after the button click
    key, values = get_item()
    print(f"Action: {action} - Showing: {key} with {values}")

    return render_template_string(
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Word List</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
                flex-direction: column;  /* Ensures elements stack vertically */
            }
            .key {
                background-color: #BE3144; /* Dark purple */
                color: white;
                font-weight: 900;
                padding: 20px;
                margin-bottom: 20px;
                font-size: xx-large;
                min-width: 250px
            }
            .value {
                background-color: #E17564; /* Light purple */
                color: black;
                padding: 10px;
                font-weight: 700;
                margin-bottom: 5px;
                font-size: x-large;
                min-width: 270px
            }
            .key, .value {
                width: 80%; /* You can adjust this as per your requirement */
                margin: 10px auto;
                border-radius: 5px;
                display: block; /* Ensures each element takes its own line */
            }
            .boxx {
                background-color: #09122C;
                padding: 10px;
                border-radius: 10px;
                min-width: 300px
            }
            .button-container {
                margin-top: 20px;
            }
            button {
                font-size: 16px;
                padding: 12px;
                margin: 5px;
                cursor: pointer;
                background-color: #BE3144;  /* Dark purple to match the theme */
                color: white;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #9e2542;  /* Slightly lighter purple on hover */
            }
            .button-container .complete-round {
                margin-top: 10px;  /* To move it below the other buttons */
            }
            .correct {
                background-color: #387478;
                font-weight: 600;
                font-size: x-large;
            }
            .incorrect {
                background-color: #A04747;
                font-weight: 600;
                font-size: x-large;
            }
            .skip {
                background-color: #3C3D37;
                font-weight: 600;
                font-size: x-large;
            }
            .complete-round {
                background-color: #03346E;
                font-weight: 600;
                font-size: x-large;
                margin-top: 10px;
            }
            .score {
                margin-bottom: 20px;
                font-size: x-large;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="score">
            &#9989; {{ score['correct'] }} | &#10060; {{ score['incorrect'] }} | &#9193; {{ score['skip'] }}
        </div>
        <div class="boxx">
        <div class="key">{{ key }}</div>
        {% for value in values %}
            <div class="value">{{ value }}</div>
        {% endfor %}
        </div>
        <div class="button-container">
            <button class="skip" onclick="location.href='/action/skip'">Skip</button>
            <button class="correct" onclick="location.href='/action/correct'">Correct</button>
            <button class="incorrect" onclick="location.href='/action/incorrect'">Incorrect</button>
        </div>
        <div class="button-container">
            <button class="complete-round" onclick="location.href='/action/complete_round'">Complete Round</button>
        </div>
    </body>
    </html>
    """,
        score=score,
        key=key,
        values=values,
        action=action,
    )


if __name__ == "__main__":
    app.run(debug=True)
