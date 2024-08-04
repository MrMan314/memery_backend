from flask import Flask, request, send_file
from base64 import b64encode
from io import BytesIO
import replicate
import urllib.request

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def hello():
	input = {
		"prompt": "a meme about " + request.args.get("prompt") + " with comprehensible english text",
		"output_quality": 100,
		"disable_safety_checker": True
	}

	output = replicate.run(
		"black-forest-labs/flux-schnell",
		input=input
	)
	contents = urllib.request.urlopen(output).read()
	return send_file(BytesIO(contents), mimetype="image/webp", download_name="generated.webp")
