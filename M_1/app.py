from flask import Flask , render_template ,url_for , send_from_directory


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/resume')
def resume():
    return send_from_directory("static/Professional Resume")



if __name__ == '__main__':
    app.run(debug=True)