from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    foods = [
        {"name": "한우", "type": "고기"},
        {"name": "아이스크림", "type": "디저트"},
        {"name": "음료수", "type": "디저트"}
    ]
    return render_template('index.html', foods=foods)

if __name__ == '__main__':
    app.run(debug=True)
