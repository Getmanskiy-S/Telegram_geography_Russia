import os
from main import main
import resource
from flask import Flask

memory_limit = 500 * 1024 * 1024  # 500 МБ
resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

app = Flask(__name__)


@app.route("/")
def index():
    return "Привет от приложения Flask"


if __name__ == '__main__':
    main()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
