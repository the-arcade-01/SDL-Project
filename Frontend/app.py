from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

def predict(name):
    data = [{'name':'Batman'},{'name':'Kimi no na wa'},{'name':'UP'},{'name':'Avengers'},{'name':'Spiderman'},{'name':'Married Life'}]
    return data

def moviesData(name):
    base_url = f'https://api.themoviedb.org/3/search/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb&query={name}'
    response = requests.get(base_url)
    data = response.json()
    results = data['results'][0]
    path = results['poster_path']
    if path:
        new_path = "http://image.tmdb.org/t/p/w500"+path
        results['poster_path'] = new_path

    result = {'title':results['title'],'poster_path':results['poster_path'],'vote_average':results['vote_average'],'overview':results['overview']}

    return result

@app.route('/',methods = ['POST','GET'])
def index():
    if request.method == "POST":
        name = request.form['name']

        data = predict(name)

        results = []

        for item in data:
            results.append(moviesData(item['name']))

        return render_template('index.html',results = results)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
