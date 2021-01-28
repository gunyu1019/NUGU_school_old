from sanic import Sanic

from config import parser
from log_config import LOGGING_CONFIG
from route.meal import meal
from route.timetable import timetable
from route.health import health

if __name__ == "__main__":
    app = Sanic(__name__, log_config=LOGGING_CONFIG)

    app.add_route(timetable, "/api/NUGU/timetable", methods=["POST"])
    app.add_route(meal, "/api/NUGU/meal", methods=["POST"])
    app.add_route(health, "/health", methods=["GET"])
    app.run(host=parser.get('DEFAULT', 'host'), port=parser.get('DEFAULT', 'port'), debug=parser.get('DEFAULT', 'debug'))