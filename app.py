from flask import Flask, render_template
import json

app = Flask(__name__)

with open('my_dict.json', encoding='utf-8') as file:
    data = json.load(file)

promotions = list(data)

@app.route('/')
def index():
    return render_template('index.html', promotions=promotions)


if __name__ == '__main__':
    app.run(debug=True)
