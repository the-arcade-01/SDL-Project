import pandas as pd
from data_clean_1 import movies

mv_tags = pd.read_csv(
    "ml-latest/genome-scores.csv"
)  # contains tag-relevance for any movie (movieId,tagId,relevance )

mv_tags_desc = pd.read_csv(
    "ml-latest/genome-tags.csv"
)  # contains tagId and its corresponding tag

# merging mv_tags with movies on column tagId
mv_tags_denorm = mv_tags.merge(mv_tags_desc, on="tagId")
mv_tags_denorm = mv_tags_denorm.merge(movies, on="movieId")

# for each movie, compute the relevance rank of tags
# so we can eventually rank order tags for each movie
mv_tags_denorm["relevance_rank"] = mv_tags_denorm.groupby("movieId")["relevance"].rank(
    method="first", ascending=False
)

mv_tags_denorm["relevance_rank"] = mv_tags_denorm["relevance_rank"].astype("int32")

mv_tags_list = (
    mv_tags_denorm[mv_tags_denorm.relevance_rank <= 100]
    .groupby(["movieId", "title", "genres", "wr"])["tag"]
    .apply(lambda x: " ,".join(x))
    .reset_index()
)

mv_tags_list["tag_list"] = mv_tags_list.tag.map(lambda x: x.split(","))
mv_tags_list.drop("tag", 1, inplace=True)

mv_tags_list.to_pickle("mov2.pkl")
