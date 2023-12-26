from flask import Flask, render_template, request, jsonify
import random, json, os

app = Flask(__name__)

def find_words(json_file_path, num_words=1, num_letters=None): # Find words with the given criteria !.
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return json.dumps([{"word": "Error: File not found", "definitions": [], "synonyms": []}], indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return json.dumps([{"word": "Error: Invalid JSON format", "definitions": [], "synonyms": []}], indent=2, ensure_ascii=False)

    if num_words > len(data):
        num_words = len(data)
        
    selected_words = set()
     
    attempts = 0
    max_attempts = num_words * 2

    while len(selected_words) < num_words and attempts < max_attempts:
        entry = random.choice(data)
        word = entry.get('word', '')
        if (num_letters is None or len(word) == num_letters) and word not in selected_words:
            selected_words.add(word)
            #print("Adding word", word)
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

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/random')
def about():
    length = None
    count = 1
    
    if request.args.get('length'):
        length = request.args.get('length')
        
    if request.args.get('count'):
        length = request.args.get('count')
        
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "data.json")
    res = find_words(file_path, count, length)
    
    return jsonify(res)
