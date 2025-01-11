import logging
from unittest import registerResult
from cluster import make_links

from flask import Flask, request
import requests

from opentelemetry import trace
from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource(attributes={
    SERVICE_NAME: "MOCHI_POWERED_BY_LLMs"
})

zipkin_exporter = ZipkinExporter(endpoint="http://zipkin:9411/api/v2/spans")


provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(zipkin_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("TRACER_TEST")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mochi')

app = Flask(__name__)


def get_card_page(api_key, bookmark=None):
    return requests.get("https://app.mochi.cards/api/cards", params={"bookmark":bookmark}, auth=(api_key, None)).json()


def get_all_cards(api_key):
    cards = []
    with tracer.start_as_current_span("card_getter") as getter_span:
        response = get_card_page(api_key=api_key)
        # TODO publish a span for how long it took to retrieve cards
        cards += response['docs']
        while len(response['docs']) > 0 and len(cards) < 500:
            response = get_card_page(api_key, response['bookmark'])
            cards += response['docs']
        getter_span.set_attribute("cards_retrieved", len(cards))
    return cards


@app.route("/api/cards", methods=['POST'])
def get_cards():
    try:
        api_key = request.form.get('api_key')
        cards = get_all_cards(api_key)

        # TODO publish a span for how long it took to make all the links
        links = make_links(cards)
        result = {'error': False, 'cards': cards, 'links': links}
    except KeyError:
        result = {'error': True, 'cards': [], 'links': []}
    return result


if __name__ == "__main__":
    with tracer.start_as_current_span("service_start") as parent:
        parent.set_attribute("LOOK_AT_ME", 696969)
        parent.add_event("Starting the server")
    app.run(host='0.0.0.0', port=5000, debug=True)
