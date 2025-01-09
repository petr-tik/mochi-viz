import logging
from unittest import registerResult
from cluster import make_links

from flask import Flask, request
import requests

from opentelemetry import metrics

# Acquire a meter.
meter = metrics.get_meter("diceroller.meter")

# Now create a counter instrument to make measurements with
roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by roll value",
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mochi')

app = Flask(__name__)


def get_card_page(api_key, bookmark=None):
    return requests.get("https://app.mochi.cards/api/cards", params={"bookmark":bookmark}, auth=(api_key, None)).json()


@app.route("/api/cards", methods=['POST'])
def get_cards():
    try:
        cards = []
        api_key = request.form.get('api_key')  
        response = get_card_page(api_key=api_key)
        cards += response['docs']
        while len(response['docs']) > 0 and len(cards) < 500:
            response = get_card_page(api_key, response['bookmark'])
            cards += response['docs']
        links = make_links(cards)
        result = {'error': False, 'cards': cards, 'links': links}
    except KeyError:
        result = {'error': True, 'cards': [], 'links': []}
    return result


if __name__ == "__main__":
    roll_counter.add(1, {"roll.value": "3"})
    app.run(host='0.0.0.0', port=5000, debug=True)
