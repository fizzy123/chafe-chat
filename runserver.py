import time, sys, os, urllib, uuid, re, random
import redis
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app, async_mode='threading')
r_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route("/", methods=['GET'])
def index():
    keys = r_client.keys()
    topics = []
    for key in keys:
        topic = {
            'id': key,
            'topic': r_client.get(key)
        }
        topics.append(topic)
    print(topics)
    return render_template('index.html', topics=topics)

@app.route("/topic/<topic_id>", methods=['GET'])
def chat(topic_id):
    topic = r_client.get(topic_id)
    if not request.args.get('created'):
        r_client.delete(topic_id)
    return render_template('chat.html', topic=topic, topic_id=topic_id)

@app.route("/", methods=['POST'])
def topic_post():
    topic = request.form['topic']
    key = str(uuid.uuid4())
    r_client.set(key, topic)
    return redirect('/topic/' + key + "?created=true")

@socketio.on('message')
@app.route("/message", methods=['POST'])
def handle_message():
    data = dict(request.form)
    data['message'] = re.sub(r"(almost|nearly|I think that|probably|usually|mostly)", "", data['message'], flags=re.I)
    if random.random() < 0.05:
        choices = ["Wrong.", "False.", "Nope.", "How do you not know"]
        data['message'] = random.choice(choices) + " " + ['data.mesasge']

    if random.random() < 0.5:
        words = ["stupid", "ridiculous", "idiotic", "crazy"]
        data['message'] = re.sub(r"argument", random.choice(words) + " argument", data['message'], flags=re.I)

    if random.random() < 0.1:
        responses = ["Wow", "Seriously?", "Hahahahahahahahaha", "holy shit"]
        socketio.emit('message', {"topic": data['topic'],
                                  "client_id": data['client_id'],
                                  "message": random.choice(responses)
                                 }
                    )

    if random.random() < 0.1:
        data['message'] = re.sub(r"you", "people like you", data['message'], flags=re.I)

    if random.random() < 0.1:
        words = data['message'].split()
        index = random.choice(range(0, len(words)))
        words[index] = words[index].upper()
        data['message'] = " ".join(words)
    socketio.emit('message', data)
    return jsonify({"success": True})

socketio.run(app, port=3000, debug=True, host='0.0.0.0')
