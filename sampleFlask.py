from flask import Flask, request 

app = Flask(__name__)

@app.route("/")
def index():
  return "<h2> saad <h2>"


if __name__ == "__main__":
  app.run()
