from flask import Flask, request, abort
import requests
import json
import redis
import threading

from prototype.app.thing.model.thing import Thing


app = Flask(__name__)

thing = Thing()

destination_url="http://localhost:5000"
headers = {'Content-Type': 'application/json'}

@app.route('/ping')
def ping():
    return "pong"


@app.route('/health')
def health():
    try:
        storage_health = thing.get_storage().connection.ping()
    except redis.exceptions.ConnectionError:
        storage_health = False

    health = {
        "db": storage_health,
        "service": True
    }

    return str(health)

@app.route('/task', methods=['GET'])
def get_number_of_tasks():
    return str(thing.get_source_stream().qsize())


@app.route('/task', methods=['POST'])
def new_task():
    params = request.get_json()

    if ("inputs" not in params) or ("neuron_id" not in params):
        abort(500)
    else:
        thing.assign_new_task(params["neuron_id"], params["inputs"])
        process_thread = threading.Thread(target=process())
        process_thread.start()
        return "Current number of tasks: " + str(thing.get_source_stream().qsize())


def process():
    result = thing.compute_next_task()
    if result:
        requests.post(destination_url, json.dumps(thing.get_destination_stream().get()), headers)

@app.route('/result', methods=['GET'])
def get_result():
    return str(thing.get_destination_stream().get())