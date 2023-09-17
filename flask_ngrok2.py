# @title Modified functions from the `flask-ngrok` package which doesn't work with the latest version of `ngrok`
import time
import json
import atexit
import requests
import subprocess
from threading import Timer


def _run_ngrok(port):
  ngrok = subprocess.Popen(["ngrok", 'http', str(port)])
  atexit.register(ngrok.terminate)
  localhost_url = "http://localhost:4040/api/tunnels"  # Url with tunnel details
  time.sleep(1)
  tunnel_url = requests.get(localhost_url).text  # Get the tunnel information
  j = json.loads(tunnel_url)

  tunnel_url = j['tunnels'][0]['public_url']  # Do the parsing of the get
  return tunnel_url


def start_ngrok(port):
  ngrok_address = _run_ngrok(port)
  print(f" * Running on {ngrok_address}")
  print(f" * Traffic stats available on http://127.0.0.1:4040")

def run_with_ngrok(app):
  """
  The provided Flask app will be securely exposed to the public internet
  via ngrok when run, and the its ngrok address will be printed to stdout
  :param app: a Flask application object
  :return: None
  """
  old_run = app.run

  def new_run(*args, **kwargs):
    port = kwargs.get('port', 5000)
    thread = Timer(1, start_ngrok, args=(port,))
    thread.setDaemon(True)
    thread.start()
    old_run(*args, **kwargs)
  app.run = new_run