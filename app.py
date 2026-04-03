import os
import base64
import json
import anthropic
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (your game HTML)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "Trash Recognition API is running!"})

@app.route("/recognize", methods=["POST"])
def recognize():
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "Missing 'image' field (base64 string)"}), 400

        b64 = data["image"]
        mime = data.get("mime_type", "image/jpeg")

        # Validate base64
        try:
            base64.b64decode(b64)
        except Exception:
            return jsonify({"error": "Invalid base64 image data"}), 400

        # Call Claude Vision API
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime,
                                "data": b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Is there trash or garbage in this image? "
                                "Reply with JSON only, no markdown formatting:\n"
                                '{"is_trash": true, "trash_type": "垃圾類型（繁體中文）", '
                                '"eco_tip": "一句環保知識（繁體中文）", "confidence": "high/medium/low"}\n'
                                'or {"is_trash": false, "trash_type": "", "eco_tip": "", "confidence": "high"}'
                            ),
                        },
                    ],
                }
            ],
        )

        text = message.content[0].text.strip()

        # Parse JSON from response
        try:
            # Strip markdown code blocks if any
            clean = text.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean)
        except json.JSONDecodeError:
            # Fallback: extract JSON object from text
            import re
            match = re.search(r"\{.*?\}", text, re.DOTALL)
            if match:
                result = json.loads(match.group())
            else:
                result = {
                    "is_trash": True,
                    "trash_type": "垃圾",
                    "eco_tip": "請做好垃圾分類，保護環境！",
                    "confidence": "low",
                }

        return jsonify(result)

    except anthropic.APIError as e:
        return jsonify({"error": f"Claude API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
