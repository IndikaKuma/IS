import logging

import connexion
from connexion.resolver import RestyResolver

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, specification_dir="openapi/")
app.add_api('placerecord-api.yaml',
            arguments={'title': 'Place Record API'})

app.run(host='0.0.0.0', port=5000, debug=True)
