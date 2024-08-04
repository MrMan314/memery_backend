from flask import Flask, request, send_file
from base64 import b64encode
from io import BytesIO
import replicate
import urllib.request
from generate import generate
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def new():
	text = True if request.args.get("text") == "true" else False
	brainrot = True if request.args.get("brainrot") == "true" else False
	if request.args.get("prompt") == None:
		return "Bad request.", 400
	return send_file(BytesIO(generate(request.args.get("prompt"), text, brainrot)), mimetype="image/jpeg", download_name="generated.jpg")

@app.route("/old")
def old():
	if request.args.get("prompt") == None:
		return "Bad request.", 400
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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
