'''Machine enrichment API: lists various enrichment services.
Current available enrichments:

 - NERD (for further details see http://nerd.eurecom.fr)

Usage:
  app.py  [-p PORT]

  -p port          Port in which the server runs. [default: 8081]
'''
from docopt import docopt

import connexion
from flask_cors import CORS

# Add relative path to keep downloaded package separate from the rest
import sys
sys.path.append('./nerd/')

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml', arguments={
    'title':
    'Labs enrichment API: lists (and is a proxy for) '
    'various enrichment services\n'})

if __name__ == '__main__':
    arguments = docopt(__doc__)
    CORS(app.app)
    port = int(arguments['-p'])
    app.run(port=port, debug=True)
