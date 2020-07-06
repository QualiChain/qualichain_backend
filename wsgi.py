import logging
import sys

from application.factory import create_app
from application.settings import API_PORT

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)
app = create_app()

if __name__ == '__main__':
    log.info("Starting Qualichain Mediator API service")
    app.run(host='0.0.0.0', port=API_PORT, debug=True)