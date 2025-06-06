import os
from main import main
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Привет от приложения Flask"


if __name__ == '__main__':
    main()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
