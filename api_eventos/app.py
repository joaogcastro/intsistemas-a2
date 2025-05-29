from flask import Flask, request, jsonify
import redis
import json
import threading
import pika
import time

app = Flask(__name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

events = []
EVENT_CACHE_KEY = 'events'

def load_events_from_cache():
    cached = redis_client.get(EVENT_CACHE_KEY)
    if cached:
        global events
        events.extend(json.loads(cached))

def cache_events():
    redis_client.setex(EVENT_CACHE_KEY, 300, json.dumps(events))  # 5 minutes cache

@app.route('/event', methods=['POST'])
def receive_event():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    event = {
        'id': len(events) + 1,
        'data': data,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    events.append(event)
    cache_events()

    return jsonify({'status': 'Event received', 'event': event}), 201

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(events)

def consume_from_rabbitmq():
    def callback(ch, method, properties, body):
        try:
            msg = json.loads(body.decode())
            event = {
                'id': len(events) + 1,
                'data': msg,
                'source': 'PHP',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            events.append(event)
            cache_events()
            print(f"[RabbitMQ] Received message: {msg}")
        except Exception as e:
            print(f"[RabbitMQ] Error handling message: {e}")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='php_events')
        channel.basic_consume(queue='php_events', on_message_callback=callback, auto_ack=True)

        print('[RabbitMQ] Waiting for messages from PHP...')
        channel.start_consuming()
    except Exception as e:
        print(f"[RabbitMQ] Connection failed: {e}")

def start_rabbitmq_thread():
    thread = threading.Thread(target=consume_from_rabbitmq, daemon=True)
    thread.start()

if __name__ == '__main__':
    load_events_from_cache()
    start_rabbitmq_thread()
    app.run(host='0.0.0.0', port=5000)
