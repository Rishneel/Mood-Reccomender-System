import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import svm, datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import seaborn as sns
from numpy import dot
from numpy.linalg import norm

stopwords = stopwords.words('english')
#############################################################################
def plot_heatmap(pathOut, fileName, data, title, precis=2, show=False):
    n = int(np.sqrt(len(data)))
    data = data.reshape(n, n)
    
    xy_labels = range(1, n+1)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    p = sns.heatmap(data=data, annot=True, fmt=f'.{precis}g', ax=ax,
                    cmap=cm.YlOrBr, xticklabels=xy_labels, yticklabels=xy_labels)

    ax.invert_yaxis()  # invert the axis if desired
    ax.set_title(f'{title}')
    fig.savefig(f'{pathOut}/{fileName}.pdf', format='pdf') 
    if (show == False ):
        plt.close(fig)        
    elif (show == True):        
        plt.show()
###############################################################
# Cleaning and preprocessing the summary 
def preprocess(text):
    # remove punctuation
    text = ''.join([w for w in text if w not in string.punctuation])
    # remove case
    text = text.lower()
    # remove stopwords
    text = ' '.join([w for w in text.split() if w not in stopwords])
    return text

# Find the movie similarly to the mood and genre program
def find3MostSim(movie_dict, summary_list):# main cosine similarity wth count vectoriser

    # stores each movie's summary
    summary = summary_list[0]
   # print(summary)
    # the last string in summary is our target for summary similarity analysis
    summary.append(summary_list[1])
    
    processed = list(map(preprocess, summary))
    #print(processed)
    # create matrix of unique words
    vectorizer = CountVectorizer().fit_transform(processed)
    vectors = vectorizer.toarray()
 
    # run cosine similarity analysis
    similarity = cosine_similarity(vectors)
    #print(similarity)
    # find the 3 most similar movies by their mood adn genre
    target = similarity[-1]
    #print(similarity)
    #res = {key: similarity[key] for key in similarity.keys() & {1, 1}}
    #print(res)
    split_rate = 0.5
    
    split_idx = int(len(similarity)*split_rate)
    
    train_r =  np.array(similarity)[:split_idx] 
 
    test_r =  np.array(similarity)[split_idx:] 
   
    train_c = train_r[:,10]
    test_c = test_r[:,10]
    
    a = train_c
    b = test_c
    
    cos_sim = (dot(a, b)/(norm(a)*norm(b))) * 100
    print(cos_sim)
    
  ###########################
    data = np.array([ 1, 0.078, 0.045, 0.1005, 0.04652, 0.5555, 0.072, 0.0465,  0.123])

    plot_heatmap('.', 'test', data, 'Heat Map', 4, True)
    
    ##################
    
    
    
    
    
    
    
    
    
    target[-1] = 0
    targetIndex = sorted(range(len(target)), key=lambda x: target[x])[-3:]
   # print(targetIndex)
    
    return targetIndex


