from flask import Flask, request, jsonify, send_file
import subprocess
import os
import openai

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = "your-openai-api-key"

# Route to handle espeak TTS
@app.route("/espeak_tts", methods=["POST"])
def espeak_tts():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Use espeak to generate a TTS audio file
    output_file = "output.wav"
    command = f'espeak "{text}" --stdout > {output_file}'
    subprocess.call(command, shell=True)

    return send_file(output_file, mimetype="audio/wav")

# Route to handle OpenAI TTS (using hypothetical TTS support)
@app.route("/openai_tts", methods=["POST"])
def openai_tts():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # OpenAI's TTS (assuming such a model exists; modify per API docs)
        response = openai.Audio.create(model="tts-advanced", text=text)
        audio_data = response["audio"]

        output_file = "openai_tts_output.wav"
        with open(output_file, "wb") as f:
            f.write(audio_data)

        return send_file(output_file, mimetype="audio/wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
