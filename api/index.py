from flask import Flask, render_template, request, jsonify, g
import random, json, os, time

app = Flask(__name__)

# Dictionary to store request timestamps and counts for each IP address
request_data = {}

# Maximum allowed requests per minute
MAX_REQUESTS_PER_MINUTE = 30
RATE_LIMIT_PERIOD = 60  # 60 seconds for a minute



def find_words(json_file_path, num_words=1, num_letters=None): # Find words with the given criteria !.
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return {"word": "Error: Invalid JSON format", "definitions": [], "synonyms": []}

    if num_words > len(data):
        num_words = len(data)
        
    selected_words = set()
     
    attempts = 0
    
    max_attempts = num_words * 2
    if num_letters is not None:
        max_attempts *= 100

    while len(selected_words) < num_words and attempts < max_attempts:
        entry = random.choice(data)
        word = entry.get('word', '')
        if (num_letters is None or len(word) == num_letters) and word not in selected_words:
            selected_words.add(word)
        attempts += 1

    result = []

    

    if not selected_words:
        result.append({"word": "Error: No matching words found", "definitions": [], "synonyms": []})
    else:
        for word in selected_words:
            entry = next(entry for entry in data if entry.get('word') == word)
            word_info = {}
            word_info['word'] = entry.get('word', '')
            word_info['definitions'] = entry.get('definitions', [])
            word_info['synonyms'] = entry.get('synonyms', [])

            result.append(word_info)

    #return json.dumps(result, indent=2, ensure_ascii=False)
    return result

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
                return jsonify({"word": "Too many requests.", "definitions": "You are limited to 30 calls per minute in order to save resources on this serverless API, and let others enjoy low-latency. If you need a higher quota, reach out to me for your specific need, or deploy this API locally.", "synonyms": ["too fast","slow down"]}), 429
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
def about():
    length = None
    count = 1
    
    if request.args.get('length'):
        length = int(request.args.get('length'))
        
    if request.args.get('count'):
        count = int(request.args.get('count'))
    
    print("count", count, "     length", length)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "data.json")
    res = find_words(file_path, count, length)
    
    return jsonify(res)

