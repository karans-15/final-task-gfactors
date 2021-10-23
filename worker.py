#!/usr/bin/env python
import pika

# All required imports for prediction
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle

# Data processing parameters and hyper-parameters
vocab_size = 40000
embedding_dim = 16
max_length = 120
trunc_type = 'post'
oov_tok = '<oov>'
padding_type = 'post'

# Loading Model
model = load_model('SentimentModel')

# Loading Tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Defining prediction function
def predict_sentiment(predict_msg):
    new_seq = tokenizer.texts_to_sequences(predict_msg)
    padded = pad_sequences(new_seq, maxlen =max_length,
                      padding = padding_type,
                      truncating=trunc_type)

    # New
    prediction = np.array(model.predict(padded))[0][0]
    if prediction>0.5:
        return 1    
    else:
        return 0

# Establish Connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare Queue
channel.queue_declare(queue='rpc_queue')

# Callback function
def on_request(ch, method, props, body):
    user_input = body

    print(" [.] predict(%s)" % user_input)
    response = predict_sentiment([str(user_input)])
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()