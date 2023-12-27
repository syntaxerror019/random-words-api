# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#         # This is not the file you are looking for! #         #
#                                                               #
#       This is not the API, code. Its the redirect code        #
#       to the repl.it website. The real API code can be        #
#       found in the API_CODE folder on the GitHub Repo         #
#                       Sorry to disappoint.                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



from flask import Flask, render_template, request, jsonify, g
import random, json, os, time

app = Flask(__name__)

request_data = {}

# Maximum allowed requests per minute
MAX_REQUESTS_PER_MINUTE = 30
RATE_LIMIT_PERIOD = 60  # 60 seconds for a minute

@app.before_request
def rate_limit():
    # Get the IP address of the requester
    ip_address = request.remote_addr

    # Check if the IP address is in the request_data dictionary
    if ip_address in request_data:
        # Check if the time since the last request is within the rate limit period
        elapsed_time = time.time() - request_data[ip_address]["timestamp"]

        if elapsed_time < RATE_LIMIT_PERIOD:
            # Increment the request count for the IP address
            request_data[ip_address]["count"] += 1

            # Check if the request count exceeds the limit
            if request_data[ip_address]["count"] > MAX_REQUESTS_PER_MINUTE:
                # Rate limit exceeded, return a 429 Too Many Requests response
                return jsonify([{"word": "Too many requests.", "definitions": "You are limited to 30 calls per minute in order to save resources on this serverless API, and let others enjoy low-latency. If you need a higher quota, reach out to me for your specific need, or deploy this API locally.", "synonyms": ["too fast","slow down"]}]), 429
        else:
            # Reset the request count if the time period has passed
            request_data[ip_address]["count"] = 1
            request_data[ip_address]["timestamp"] = time.time()
    else:
        # If the IP is not present, initialize the count and timestamp
        request_data[ip_address] = {"count": 1, "timestamp": time.time()}

@app.route('/')
def home(): 
    return render_template("index.html")

@app.route('/random')
def random():
    return jsonify([{"word": "This API has moved!", "definitions": "random-word-api is no longer hosted on vercel. Either go to the main page of this vercel to get redirected to the new repl.it site, or use the following link in your project: https://random-word-api.sky-wired.repl.co/", "synonyms": ["404", "We Moved", "Get outa here!"]}])
