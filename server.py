from flask import Flask, jsonify, request
import json, time, os

app = Flask(__name__)

# كلمة سر API (يجب تغييرها)
SECRET = os.environ.get("LICENSE_SECRET", "MY_SECRET_12345")

def load_db():
    with open("db.json", "r") as f:
        return json.load(f)

@app.get("/check/<key>")
def check(key):

        # يجب إرسال auth=MY_SECRET_12345
        if request.args.get("auth") != SECRET:
            return jsonify({"valid": False, "message": "Unauthorized"})

        data = load_db()

        if key not in data:
            return jsonify({"valid": False, "message": "Invalid key"})

        info = data[key]

        if not info["active"]:
            return jsonify({"valid": False, "message": "Key disabled"})

        now = int(time.time())
        if now > info["expires"]:
            return jsonify({"valid": False, "message": "Expired"})

        return jsonify({
            "valid": True,
            "user": info["user"],
            "expires": info["expires"]
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
