import os
import sys
import serverless_wsgi

# Add the project root to the Python path
# This allows Netlify's function (in netlify/functions/api.py) to find app.py in the root
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from app import app # Now it can find app.py

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
