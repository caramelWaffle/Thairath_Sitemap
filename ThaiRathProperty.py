import pythainlp
import pandas as pd
import os

path = "/Users/macintoshhd/Thairath_Crawler/test_10.csv"
thairath_df = pd.read_csv(path, encoding='utf-8')


def get_abstractedness_score(article_set, summary_set):
    ab_score = 0
    for summary in summary_set:
        if summary not in article_set:
            ab_score = ab_score + 1
    return (ab_score * 100) / len(summary_set)


def generate_ngrams(tokens, n):
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return ["".join(ngram) for ngram in ngrams]


for index, row in thairath_df.iterrows():
    article_token = pythainlp.word_tokenize(row['body'], engine='newmm', keep_whitespace=False)
    summary_token = pythainlp.word_tokenize(row['summary'], engine='newmm', keep_whitespace=False)

    thairath_df.loc[index, 'article_length'] = len(article_token)
    thairath_df.loc[index, 'summary_length'] = len(summary_token)

    thairath_df.loc[index, 'abstractedness_n1'] = get_abstractedness_score(set(article_token), set(summary_token))
    thairath_df.loc[index, 'abstractedness_n2'] = get_abstractedness_score(set(generate_ngrams(article_token, 2)),
                                                                           set(generate_ngrams(summary_token, 2)))
    thairath_df.loc[index, 'abstractedness_n3'] = get_abstractedness_score(set(generate_ngrams(article_token, 3)),
                                                                           set(generate_ngrams(summary_token, 3)))
    thairath_df.loc[index, 'abstractedness_n4'] = get_abstractedness_score(set(generate_ngrams(article_token, 4)),
                                                                           set(generate_ngrams(summary_token, 4)))
    thairath_df.loc[index, 'abstractedness_n5'] = get_abstractedness_score(set(generate_ngrams(article_token, 5)),
                                                                           set(generate_ngrams(summary_token, 5)))
    percent = (index * 100) / len(thairath_df)
    print(index+1, " of ", len(thairath_df), " || ", percent, "%")

article_avg_size = thairath_df['article_length'].mean()
summary_avg_size = thairath_df['summary_length'].mean()

abstract_avg_size = thairath_df['abstractedness'].mean()
abstract_avg_size_2 = thairath_df['abstractedness_n2'].mean()
abstract_avg_size_3 = thairath_df['abstractedness_n3'].mean()
abstract_avg_size_4 = thairath_df['abstractedness_n4'].mean()
abstract_avg_size_5 = thairath_df['abstractedness_n5'].mean()

print("\nDataset size : ", len(thairath_df))
print("Article_avg_size : ", article_avg_size)
print("Summary_avg_size : ", summary_avg_size)

print("Abstract_avg_size : ", abstract_avg_size)
print("Abstract_2_avg_size : ", abstract_avg_size_2)
print("Abstract_3_avg_size : ", abstract_avg_size_3)
print("Abstract_4_avg_size : ", abstract_avg_size_4)
print("Abstract_5_avg_size : ", abstract_avg_size_5)


subdirectory = "detail"
file_name_ = "test_10-statistic"

try:
    os.mkdir(subdirectory)
except FileExistsError:
    pass
thairath_df.to_csv(os.path.join(subdirectory, "cleaned_" + file_name_ + ".csv"), index=False, encoding='utf-8-sig',
                   columns=["body", "summary", "article_length", "summary_length", "abstractedness_n1",
                            "abstractedness_n2", "abstractedness_n3", "abstractedness_n4", "abstractedness_n5"])
