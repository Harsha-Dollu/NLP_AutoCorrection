# main_script.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import
from autocorrection import Autocorrection

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the Autocorrection model with a sample vocabulary file
checker = Autocorrection("words.txt")

# Route for autocorrect API
@app.route('/autocorrect', methods=['POST'])
def autocorrect():
    try:
        data = request.get_json()
        input_text = data.get('text', '').strip()

        if not input_text:
            return jsonify({"error": "Input text is required."}), 400

        # Split input into words and process each word
        words = input_text.split()
        corrected_words = []
        corrections = []

        for word in words:
            if not word.isalpha():  # Skip non-alphabetic words
                corrected_words.append(word)
                continue
                
            correction = checker.correct_spelling(word.lower())
            
            # If corrections are found, use the highest probability correction
            if correction and len(correction) > 0:
                best_correction = max(correction, key=lambda x: x[1])
                corrected_word = best_correction[0]
                corrected_words.append(corrected_word)
                corrections.append({
                    "original": word,
                    "corrected": corrected_word,
                    "probability": best_correction[1]
                })
            else:
                corrected_words.append(word)

        corrected_text = ' '.join(corrected_words)
        
        return jsonify({
            "corrected_text": corrected_text,
            "corrections": corrections
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Add logging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)