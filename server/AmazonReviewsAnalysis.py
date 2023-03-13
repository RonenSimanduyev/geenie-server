
# import pandas as pd
# import numpy as np
# import nltk #classification for semantic reasoning, text processing libraries
# from nltk.sentiment.vader import SentimentIntensityAnalyzer #collection of lexical elements classified as positive or negative
# import re 
# import numpy as np
# from sklearn.cluster import AffinityPropagation
# import distance
# from textblob import TextBlob #process textual data
# from sklearn.feature_extraction.text import TfidfVectorizer
# from wordcloud import WordCloud #analyse phrases based on frequency & importance
# from nltk.corpus import stopwords #remove stopwords for tf-idf
# from nltk.corpus import wordnet
# from nltk.stem import WordNetLemmatizer #lemmatizer to normalize words to their simple forms
# import seaborn as sns
# import matplotlib.pyplot as plt
# import cufflinks as cf
# # get_ipython().run_line_magic('matplotlib', 'inline')
# from plotly.offline import init_notebook_mode, iplot
# init_notebook_mode(connected = True)
# cf.go_offline();
# import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# from time import time
# import warnings
# warnings.filterwarnings("ignore")
# warnings.warn("this will not show")
# t=time()

# def reviewAnalysis(fileName):
    
#     df = pd.read_csv(fileName)

#     def missing_values_analysis(df):
#         na_columns = [col for col in df.columns if df[col].isnull().sum() > 0]
#         n_miss = df[na_columns].isnull().sum().sort_values(ascending=True)
#         ratio = (df[na_columns].isnull().sum() / df.shape[0]*100).sort_values(ascending=True)
#         missing_df = pd.concat([n_miss,np.round(ratio,2)],axis=1,keys=["missing values","ratio"])
#         missing_df = pd.DataFrame(missing_df)
#         return missing_df


#     #unique values analysis
#     def check_class(df):
#         unique_df = pd.DataFrame({"Variable": df.columns,
#                                 "Classes": [df[i].nunique() \
#                                             for i in df.columns]})
#         unique_df = unique_df.sort_values("Classes",ascending = False)
#         unique_df = unique_df.reset_index(drop = True)
#         return unique_df

#     check_class(df)


#     df = df.dropna(subset=["Body"])
#     df = df.drop_duplicates(subset=["Body"])

#     #converting to correct types
#     df["Body"] = df["Body"].astype(str)

#     #using regex to clean data of commas and numbers and convert all data to lowercase & to normal form of the word, & remove stopwords

#     rt = lambda x: re.sub("[^a-zA-Z]"," ",str(x))
#     df["Body"] = df["Body"].map(rt)
#     df["Body"] = df["Body"].str.lower()
#     df.head(5)

#     #removing stopwords
#     import nltk
#     nltk.download('stopwords')

#     stop_words = stopwords.words("english")
#     rt = lambda x: re.sub(r'\b({})\b\s+'.format('|'.join(stop_words)),"",str(x))
#     df["Body"] = df["Body"].map(rt)
#     rt = lambda x: re.sub("\s+"," ",str(x))
#     df["Body"] = df["Body"].map(rt)


#     nltk.download('wordnet')

#     nltk.download('punkt')

#     #lemmantizing words
#     import nltk
#     nltk.download('omw-1.4')

#     lemmatizer = WordNetLemmatizer()

#     def do_lemmantize(sentence):
#         word_list = nltk.word_tokenize(sentence)
#         result = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
#         return sentence
        
#     df["Body"] = df["Body"].apply(do_lemmantize)
#     df.head(5)


#     # step 1. extract topics and opinions

#     # detecting key phrases using tf-idf, 
#     # filtering on tf-idf score to remove less relevant topics,
#     # filtering similar topics,
#     # calculating # of appearances of topics in reviews,
#     # and finding opinions relevant to topics

#     #algorithm uses tf_idf to find what reviewers liked about the product and what reviewers disliked about it

#     # tf–idf is a numerical statistic that is intended to reflect how important a word is to a document in a corpus. 
#     #tf score = number of times term appears in document / number of terms in document
#     #idf score = number of documents / number of documents containing the term
#     #tf-idf = tf score * idf score (a bigger score is a term that appears a lot in its document and little in all documents)
#     def tf_idf(corpus, min_word_num, max_word_num):
#         cv = TfidfVectorizer(ngram_range=(min_word_num,max_word_num))
#         corpus = cv.fit_transform(corpus)
#         avg = corpus.mean(axis=0)
#         avg = pd.DataFrame(avg, columns=cv.get_feature_names_out())
#         avg=avg.T
#         avg=avg.rename(columns={0:"score"})
#         avg["word"]=avg.index
#         avg=avg.sort_values("score",ascending=False)
#         return avg


#     tf_idf_res = tf_idf(df['Body'],2,3)


#     tf_idf_res.sort_values(by=["score"],ascending=False)
#     tf_idf_res = tf_idf_res.reset_index()
#     tf_idf_res = tf_idf_res.drop(["index"],axis=1)



#     tf_idf_res = tf_idf_res[tf_idf_res.score > 0.0009]

#     tf_idf_res = tf_idf_res.reset_index()
#     tf_idf_res = tf_idf_res.drop(["index"],axis=1)
    
#     # filter similar topics

#     #similar uses sequence matcher to find how similar strings are to each other
#     #then if they are similar, filters
#     from difflib import SequenceMatcher

#     def similar(a, b):
#         return SequenceMatcher(None, a, b).ratio()

#     topics_list = list(tf_idf_res.word)


#     for i in range(0, len(tf_idf_res)):
#         try:
#             curr_phrase = tf_idf_res.loc[i].word
#             for topic in topics_list:
#                 if curr_phrase != topic and similar(curr_phrase,topic) > 0.6:
#                     tf_idf_res = tf_idf_res[tf_idf_res.word != topic]
#         except:
#             continue

#     tf_idf_res = tf_idf_res.reset_index()
#     tf_idf_res = tf_idf_res.drop(["index"],axis=1)


#     reviews = list(df.Body)

#     tf_idf_res['appearances']=0

#     for i in range(0, len(tf_idf_res)):
#         try:
#             curr_phrase = tf_idf_res.loc[i].word
#             count_a = 0
#             for review in reviews:
#                 if curr_phrase in review:
#                     count_a += 1
#             tf_idf_res.at[i,'appearances'] =count_a
#         except:
#             continue

#     tf_idf_res = tf_idf_res.sort_values(by=["appearances"],ascending=False)


#     # using opinion corpus, goes through topics and relevant reviews to them, and finds if opinion about topic exists in review,
#     # if it does, adds it to review column

#     nltk.download('opinion_lexicon')

#     from nltk.corpus import opinion_lexicon


#     cons_words = opinion_lexicon.negative()

#     pros_words = opinion_lexicon.positive()

#     opinions_dict = {word:1 for word in cons_words + pros_words} 


#     tf_idf_res['opinion']=""

#     for i in range(0, len(tf_idf_res)):
#         try:
#             curr_phrase = tf_idf_res.loc[i].word
#             opinion = ""
#             for review in reviews:
#                 if curr_phrase in review and len(review.split(" ")) < 15:
#                     review_words = review.split(" ")
#                     for word in review_words:
#                         if word in opinions_dict:
#                             opinion = opinion + word +" "
#             tf_idf_res.at[i,'opinion'] =opinion
#         except:
#             continue


#     len(tf_idf_res[tf_idf_res.opinion == ""])


#     tf_idf_res = tf_idf_res[tf_idf_res.opinion != ""]

#     # step 2. sentiment analysis
#     # using sentiment analysis on opinion column to classify if the opinion of the reviewers on the topic was positive, negative or neutral



#     from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#     # Function uses TextBlob to determine review's polarity, subjectivity, and overall sentiment score(Neg/Neu/Pos)

#     # TextBlob's sentiment property returns a namedtuple of the form Sentiment(polarity, subjectivity). 
#     # The polarity score is a float within the range [-1.0, 1.0]. 
#     # The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

#     # SentimentIntensityAnalyzer maps lexical features to emotion intensities known as sentiment scores. 
#     # The sentiment score of a text can be obtained by summing up the intensity of each word in the text.

#     # Finally, the function uses sentiment scores to classify review as overall positive, negative, or neutral

#     tf_idf_res[["polarity","subjectivity"]] = tf_idf_res["opinion"].apply(lambda Text:pd.Series(TextBlob(Text).sentiment))


#     for index,row in tf_idf_res["opinion"].iteritems():
        
#         score = SentimentIntensityAnalyzer().polarity_scores(row)
        
#         neg = score["neg"]
#         neu = score["neu"]
#         pos = score["pos"]
        
#         if neg>pos:
#             tf_idf_res.loc[index,"sentiment"] = "Negative"
#         elif pos>neg:
#             tf_idf_res.loc[index,"sentiment"] = "Positive"
#         else:
#             tf_idf_res.loc[index,"sentiment"] = "Neutral"


#     tf_idf_res[tf_idf_res["sentiment"] == "Positive"].head(7)


#     tf_idf_res[tf_idf_res["sentiment"] == "Negative"].head(7)


#     neg_topics = tf_idf_res[tf_idf_res["sentiment"] == "Negative"][:50]
#     pos_topics = tf_idf_res[tf_idf_res["sentiment"] == "Positive"][:50]

#     neg_topics_str = list(neg_topics.word)


#     pos_topics_str = list(pos_topics.word)



#     def cluster_topics(words):
#         words = np.asarray(words) #So that indexing with a list will work
        
#         #Levenshtein distance is a string metric for measuring the difference between two sequences.
#         #applies to word set to see similarity between each sequence
#         lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words]).astype(float)

#         #affinity propagation (AP) is a clustering algorithm based on the concept of "message passing" between data points.
#         #takes as input measures of similarity between pairs of data points. 
#         #Real-valued messages are exchanged between data points until a high-quality set of exemplars and corresponding clusters gradually emerges.
#         #here uses lev similiarity between two sequences as similarity between pairs of data points to form exemplars as topics and relevant explanations as clusters
#         affprop = AffinityPropagation(affinity="precomputed", damping=0.5)
#         affprop.fit(lev_similarity)
        
#         res = {}
#         for cluster_id in np.unique(affprop.labels_):
#             exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
#             cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
#             cluster_str = ", ".join(cluster)
#             res[exemplar] = cluster_str
#             #print(" - *%s:* %s" % (exemplar, cluster_str))
            
#         return res



#     neg_clusters = cluster_topics(neg_topics_str)

#     pos_clusters = cluster_topics(pos_topics_str)


#     def get_precent_appearances(sentiment, clusters, topics_df):
#         res_df = pd.DataFrame(columns = ["topic","subtopics","precent_of_reviews"])
#         sum_topics = len(tf_idf_res[tf_idf_res["sentiment"] == sentiment])
#         for topics in clusters.items():
#             topics_str = topics[1]
#             count_a = 0
#             for topic in topics_str.split(', '):
#                 count_a += int(topics_df[topics_df.word == topic]["appearances"])
#             res_df = res_df.append({"topic": topics[0], "subtopics": topics[1], "precent_of_reviews": round(count_a * 100 / sum_topics)}, ignore_index = True)
#             #print(topics[0], round(count_a * 100 / sum_topics), "%")
#         return res_df.sort_values(by=["precent_of_reviews"],ascending=False)


#     pos_res = get_precent_appearances("Positive",pos_clusters,pos_topics)
#     pos_res

#     neg_res = get_precent_appearances("Negative",neg_clusters,neg_topics)
#     pos_list = [(topic,pos_res.loc[index].precent_of_reviews) for index,topic in enumerate(list(pos_res.topic)) ]
#     neg_list = [(topic,neg_res.loc[index].precent_of_reviews) for index,topic in enumerate(list(neg_res.topic)) ]
#     res =  pd.DataFrame(
#         {
#             "pos_count":len(tf_idf_res[tf_idf_res["sentiment"] == "Positive"]),
#             "neut_count":len(tf_idf_res[tf_idf_res["sentiment"] == "Neutral"]),
#             "neg_count":len(tf_idf_res[tf_idf_res["sentiment"] == "Negative"]),
#             "pos_topics":str(pos_list),
#             "neg_topics":str(neg_list)
#         }, index=[0])

#     analysis1= res.to_string(index=False)

#     print(time()-t)
#     return analysis1
