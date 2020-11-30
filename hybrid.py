import pickle
import pandas
from flask import Flask, request, render_template, jsonify
import gzip

with open("mov1.pkl", "rb") as f1:
    movies = pickle.load(f1)

with open("mov2.pkl", "rb") as f2:
    mv_tags_list = pickle.load(f2)

with gzip.open("svd.pkl", "rb") as f:
    p = pickle.Unpickler(f)
    algo = p.load()


links = pandas.read_csv(
    "ml-latest/links.csv"
)  # contains imdb, tmbd links for respective movies


def hybrid(userId, title):

    target_tag_list = mv_tags_list[
        mv_tags_list.title.str.contains(title)
    ].tag_list.values[0]
    # mv_tags_list_sim is anew table prepared from mv_tags_list with given column names
    mv_tags_list_sim = mv_tags_list[["movieId", "title", "genres", "tag_list", "wr"]]

    # mv_tags_list_sim['jaccard_sim'] will hold the jaccard similarity of any 2 values
    mv_tags_list_sim["jaccard_sim"] = mv_tags_list_sim.tag_list.map(
        lambda x: len(set(x).intersection(set(target_tag_list)))
        / len(set(x).union(set(target_tag_list)))
    )

    sim_scores = mv_tags_list_sim.sort_values(by="jaccard_sim", ascending=False).head(
        10
    )

    movie_indices = [i for i in sim_scores["movieId"]]

    rec_mov = mv_tags_list_sim.loc[mv_tags_list_sim["movieId"].isin(movie_indices)]
    rec_mov = rec_mov.merge(links, on="movieId")

    rec_mov["est"] = [algo.predict_pair(userId, x) for x in movie_indices]

    # Sorting mv_tags_list_sim by jaccard similarity
    rec_mov = rec_mov.sort_values("est", ascending=False)

    return rec_mov.head(10)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict(name):
    """
    For rendering results on HTML GUI
    """
    m_name = request.form["m_name"]
    prediction = hybrid(165, m_name)
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

