from sanic import Sanic

from config import parser
from route.meal import meal

if __name__ == "__main__":
    app = Sanic(__name__)

    app.add_route(meal, "/api/NUGU/meal", methods=["POST"])
    app.run(host=parser.get('DEFAULT', 'host'), port=parser.get('DEFAULT', 'port'), debug=parser.get('DEFAULT', 'debug'))