from flask import Flask, redirect, url_for, render_template, request
import pika
import uuid
app = Flask(__name__)

# Home
@app.route('/')
def first():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def home():

    data = request.form['data']

    output = int(sentiment_model_rpc.call(data))
    
    return render_template('home.html', prediction_text=output)


class SentimentModelRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, msg):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(msg))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


sentiment_model_rpc = SentimentModelRpcClient()



if __name__ == "__main__":
    app.run(debug=True)