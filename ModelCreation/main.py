# All required imports
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle

# # Data processing parameters and hyper-parameters
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
    return (model.predict(padded))


def main():
    print("Welcom to Sentiment Analysis")
    print("===================================================================")
    while(True):
        user_input = input("Input string: ")
        prediction = np.array(predict_sentiment([user_input]))[0][0]
        if prediction>=0.5:
            print("Positive Feedback!")
        else:
            print("Negative feedback!")


        user_input = input('Do you want another prediction? (y/[n])? ')
        if user_input != 'y':
            print("bye!")
            break

if __name__ == '__main__':
    main()



