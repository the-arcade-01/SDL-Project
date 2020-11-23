import pandas as pd
from funk_svd import SVD
import gzip, pickle, pickletools

df = pd.read_csv("output.csv", header=0)
df.rename(columns={"userId": "u_id", "movieId" : "i_id"}, inplace=True)

train = df.sample(frac=0.8, random_state=7)
val = df.drop(train.index.tolist()).sample(frac=0.5, random_state=8)

svd = SVD(learning_rate=0.001, regularization=0.005, min_rating=0, max_rating=5)

filepath = "svd.pkl"

with gzip.open(filepath, "wb") as f:
    pickled = pickle.dumps(svd)
    optimized_pickle = pickletools.optimize(pickled)
    f.write(optimized_pickle)
