import pickle
import pandas
from flask import Flask, request, render_template
import gzip

with open('mov1.pkl', 'rb') as f1:
    movies = pickle.load(f1)

with open('mov2.pkl', 'rb') as f2:
    mv_tags_list = pickle.load(f2)

with gzip.open('svd.pkl', 'rb') as f:
    p = pickle.Unpickler(f)
    algo = p.load()


# links = pd.read_csv(
#     "ml-latest/links.csv"
# )  # contains imdb, tmbd links for respective movies


def hybrid(userId, title):

    target_tag_list = mv_tags_list[ mv_tags_list.title.str.contains(title)].tag_list.values[0]
    # mv_tags_list_sim is anew table prepared from mv_tags_list with given column names
    mv_tags_list_sim = mv_tags_list[["movieId", "title", "tag_list", "rating", "wr"]]

    # mv_tags_list_sim['jaccard_sim'] will hold the jaccard similarity of any 2 values
    mv_tags_list_sim["jaccard_sim"] = mv_tags_list_sim.tag_list.map(lambda x: len(set(x).intersection(set(target_tag_list)))/ len(set(x).union(set(target_tag_list))))

    sim_scores = mv_tags_list_sim.sort_values(by="jaccard_sim", ascending=False).head(10)

    movie_indices = [i for i in sim_scores["movieId"]]

    rec_mov = movies.loc[movies["movieId"].isin(movie_indices)]

    rec_mov["est"] = [algo.predict_pair(userId, x) for x in movie_indices]

    # Sorting mv_tags_list_sim by jaccard similarity
    rec_mov = rec_mov.sort_values("est", ascending=False)

    return rec_mov.head(10)

#print(hybrid(165,'Married Life'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    m_name =  request.get('m_name')
    print(m_name)
    prediction = hybrid(165, m_name)
    print(m_name)

    return render_template('index.html', prediction_text= prediction)

# @app.route('/predict_api',methods=['POST'])
# def predict_api():
#     '''
#     For direct API calls trought request
#     '''
#     data = request.get_json(force=True)
#     prediction = model.predict([np.array(list(data.values()))])

#     output = prediction[0]
#     return jsonify(output)

if __name__ == "__main__":
    app.run(port = 5000, debug=True)