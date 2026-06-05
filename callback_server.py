from flask import Flask, request

app = Flask(__name__)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    print("\n==============================")
    print("🎉 NHẬN ĐƯỢC CODE TỪ TIKTOK")
    print("==============================")
    print("code =", code)
    print("==============================\n")
    return "Received! You can close this tab."

app.run(port=8000)
