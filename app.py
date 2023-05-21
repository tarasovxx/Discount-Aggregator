from flask import Flask, render_template
import json

app = Flask(__name__)

with open('my_dict.json', encoding='utf-8') as file:
    data = json.load(file)

promotions = list(data)
# # Пример списка акций
# promotions = [
#     {'store': 'Магазин 1', 'title': 'Скидка 10%', 'description': 'Только сегодня'},
#     {'store': 'Магазин 2', 'title': 'Акция "Купи два, получи скидку"', 'description': 'До конца месяца'},
#     {'store': 'Магазин 3', 'title': 'Бесплатная доставка', 'description': 'При заказе от 1000 рублей'},
# ]


@app.route('/')
def index():
    return render_template('index.html', promotions=promotions)


if __name__ == '__main__':
    app.run()
