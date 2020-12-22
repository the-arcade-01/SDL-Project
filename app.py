import pickle
import pandas,requests
from flask import Flask, request, render_template, jsonify
import gzip

app = Flask(__name__)


with open("mov2.pkl", "rb") as f2:
    mv_tags_list = pickle.load(f2)

with gzip.open("svd.pkl", "rb") as f:
    p = pickle.Unpickler(f)
    algo = p.load()


# links = pandas.read_csv(
#     "ml-latest/links.csv"
# )  # contains imdb, tmbd links for respective movies


def hybrid(userId, title):

    taglist = mv_tags_list[mv_tags_list.title.str.contains(title, case=False)]
    if not taglist.shape[0]:
        return " empty "
    else:
        target_tag_list = taglist.tag_list.values[0]
        # mv_tags_list_sim is anew table prepared from mv_tags_list with given column names
        mv_tags_list_sim = mv_tags_list[
            ["movieId", "title", "genres", "tag_list", "wr"]
        ]

        # mv_tags_list_sim['jaccard_sim'] will hold the jaccard similarity of any 2 values
        mv_tags_list_sim["jaccard_sim"] = mv_tags_list_sim.tag_list.map(
            lambda x: len(set(x).intersection(set(target_tag_list)))
            / len(set(x).union(set(target_tag_list)))
        )

        sim_scores = mv_tags_list_sim.sort_values(
            by="jaccard_sim", ascending=False
        ).head(10)

        movie_indices = [i for i in sim_scores["movieId"]]

        rec_mov = mv_tags_list_sim.loc[mv_tags_list_sim["movieId"].isin(movie_indices)]
        rec_mov = rec_mov.merge(links, on="movieId")

        rec_mov["est"] = [algo.predict_pair(userId, x) for x in movie_indices]

        # Sorting mv_tags_list_sim by jaccard similarity
        rec_mov = rec_mov.sort_values("est", ascending=False)

        return rec_mov.head(10)

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
    print(result)
    return result

def predict(name):
    prediction = hybrid(165, name)
    result = []
    data_range = 6
    if len(prediction) < 6:
        data_range = len(prediction)

    for i in range(data_range):
        namelist = prediction.loc[i,"title"].split(' ')[:-1]
        name = ''

        for j in range(len(namelist)):
            if j == len(namelist)-1:
                name += namelist[j]
            else:
                name += namelist[j]+" "

        row ={
            "name":name
        }
        result.append(row)
    print(result)
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


@app.route("/api/<name>", methods=["POST","GET"])
def api(name):
    """
    For rendering results on HTML GUI
    """
    prediction = hybrid(165, name)
    result = []
    for i in range(10):
        row = {
            "movie_id": int(prediction.loc[i, "movieId"]),
            "title": prediction.loc[i, "title"],
            "genres": prediction.loc[i, "genres"],
            "tag_list": prediction.loc[i, "tag_list"],
            "rating": float(prediction.loc[i, "wr"]),
            "jaccard_sim": float(prediction.loc[i, "jaccard_sim"]),
            "imdbId": str(prediction.loc[i, "imdbId"]),
            "tmdbId": str(prediction.loc[i, "tmdbId"]),
        }
        result.append(row)
    return jsonify(result)


# prediction_text= prediction.to_json(double_precision=2)
# return prediction_text

if __name__ == "__main__":
    app.run(port=5000, debug=True)

