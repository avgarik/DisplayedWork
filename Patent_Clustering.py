#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 
import re
from sklearn.feature_extraction.text import CountVectorizer


# In[2]:

#Remove punctuation and make lowercase
def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r"[^a-zA-Z0-9\s\.,;:()-]", "", text)
        text = re.sub(r"[\.]", "", text)
        text = text.lower()

    return text


# In[3]:

#Remove common patent words (equivalent of patent stopwords)
def clean_patent(text):
    if isinstance(text,str):
        text = re.sub(r"preparation", "", text)
        text = re.sub(r"invention", "", text)
        text = re.sub(r"application", "", text)
        text = re.sub(r"method", "", text)
        text = re.sub(r"claim*", "", text)
        text = re.sub(r"following", "", text)
        text = re.sub(r"comprising", "", text)
        text = re.sub(r"thereof new", "", text)
        text = re.sub(r"comprises steps", "", text)
        text = re.sub(r"present relates", "", text)
        text = re.sub(r"utility model", "", text)
    return text


# In[4]:

#Run KMeans clustering and return distortion
def ag_kmeans(n_clusters, data):
    kmeans = KMeans(n_clusters = n_clusters, init = "random")
    kmeans.fit(data)
    inertia = kmeans.inertia_
    distortion = inertia/n_clusters
    return(distortion)


# In[5]:


df = pd.read_excel("mycelium_patents.xlsx")


# In[6]:

#Only using two title columns and abstract column
df = df[["Title (English)", "Title - DWPI", "Abstract (English)"]]
df = df.rename(columns={"Title (English)":"Title", "Title - DWPI":"Title_DWPI", "Abstract (English)":"Abstract"})


# In[7]:

#Remove NAs
df["Title"] = df["Title"].fillna("")
df["Title_DWPI"] = df["Title_DWPI"].fillna("")
df["Abstract"] = df["Abstract"].fillna("")

#Clean text
df["Title"] = df["Title"].apply(clean_text)
df["Title_DWPI"] = df["Title_DWPI"].apply(clean_text)
df["Abstract"] = df["Abstract"].apply(clean_text)

#Remove patent stopwords
df["Title"] = df["Title"].apply(clean_patent)
df["Title_DWPI"] = df["Title_DWPI"].apply(clean_patent)
df["Abstract"] = df["Abstract"].apply(clean_patent)

#Add spaces at the end of text in first two columns
df["Title"] = df["Title"] + " "
df["Title_DWPI"] = df["Title_DWPI"] + " "

#Concatenate into one text block
df["Text"] = df["Title"] + df["Title_DWPI"] + df["Abstract"]


# In[8]:

#Ensure no NAs, duplicates, and transform to list
df_text = df.copy()
df_text = df_text[["Text"]]
df_text = df_text.dropna()
df_text = df.Text.unique()
text = list(df_text)


# In[9]:

#Vectorize using TF-IDF, remove stopwords, tokenize into bigrams, remove any words that appear in over 60% of documents, return a maximum of 1,000 features
vectorizer = TfidfVectorizer(lowercase = True, stop_words="english", max_df = 0.6, ngram_range = (2,2), max_features = 1000) 
vectorized_text = vectorizer.fit_transform(text)
#Extract feature names (top 1,000 words according to TF-IDF after above cleaning)
words = vectorizer.get_feature_names_out()


# In[10]:

#Run KMeans for cluster sizes 1-10 and compute distortion
distortions = []
n_clusters = [*range(1, 9, 1)]

for i in range(0, len(n_clusters)):
    distortions.append(ag_kmeans(n_clusters[i], vectorized_text))


# In[11]:

#Plot elbow plot
plt.plot(n_clusters, distortions)
plt.show()


# In[12]:

#Disregarded elbow plot, decided best differentiation between clusters at number of clusters = 8
n_clusters = 8

kmeans = KMeans(n_clusters = n_clusters, init = "random")
kmeans.fit(vectorized_text)

#Find top 10 most important words in each cluster
cluster_centers = kmeans.cluster_centers_

#Sort arrays in order of words most used
descending_indices = (-cluster_centers).argsort()

print(words[descending_indices[0][0:10]])
print(words[descending_indices[1][0:10]])
print(words[descending_indices[2][0:10]])
print(words[descending_indices[3][0:10]])
print(words[descending_indices[4][0:10]])
print(words[descending_indices[5][0:10]])
print(words[descending_indices[6][0:10]])
print(words[descending_indices[7][0:10]])

