# Sentiment Model

## What this webpage does:
This app is a simple sentiment analyzer created with the help of tensorflow. It takes in user input and then predicts if the sentiment is positive or negative.

## Major Elements of this repo:
- The `requirements.txt` are the basic python libraries required to use the project.
- The `app.py` is a Flask Webpage. This takes care of getting the data from the form and working as a RabbitMQ Producer.
- The `templates` folder holdes the `home.html` webpage that has the form and displays the result.
- The `worker.py` is a RabbitMQ worker that recieves the message from the Producer, makes a prediction and sends a reply back to the Producer.

## How it works:
