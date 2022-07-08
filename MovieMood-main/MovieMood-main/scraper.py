"""
this script designed to scrape off information from two major movie rating websites: IMDB and Rotten Tomatoes
twelve movie ratings are obtained from each source.
"""
from bs4 import BeautifulSoup as SOUP #web scraping library
import re #send and recieve http requests

import requests
from math import log 
import pandas as pd
import matplotlib.pyplot as plt

def locate_url(user_emotion):#in main defined by the inteface output

    file_path = "url/"
    emotions = ["Happy", "Sad", "Satisfying", "Angry",
                "Peaceful", "Fearful", "Excited", "Depressed",
                "Content", "Sorrowful"]

    url_lst = []
    with open(file_path + "IMDB.txt") as f1, open(file_path + "RT.txt") as f2:#crawler and scraper takes link form the txt file
        f1_lst = f1.read().splitlines()
        f2_lst = f2.read().splitlines()
        
        for i in range(len(emotions)):
            if emotions[i] in user_emotion:#if emotion input equal to  the one above
            
                IMDB = f1_lst[i]
                RT = f2_lst[i]
                url_lst.append(IMDB)
                
                url_lst.append(RT)##
                
    return url_lst

"""sort movies based on their rating, from high to low
   through this function, the recommender is able to select the movie with highest weighted rating
"""
def rank_movies(movie_dict):
    ranked_dict = {}
    rating = []
    for movie_info in movie_dict.values():
        if type(movie_info[-1]) == float:
            rating.append(movie_info[-1])
    rating = sorted(rating, reverse = True)
    for r in rating:
        for k in movie_dict.keys():
            if movie_dict[k][-1] == r:
                ranked_dict[k] = movie_dict[k]
               # print(ranked_dict[k])
    return ranked_dict 
    

# IMDB should be a single link
def scrape_IMDB(IMDB, num, folder_path = None): # taking out specific information from the link
    folder_path = "Documents\MovieMood-main\MovieMood-main\movie_summary" # you only need the folder_path when you need to store movie summary
    response = requests.get(IMDB) #get data of whole page
    
    data = SOUP(response.text, 'lxml') #
    #print(data)
    
    # we hope to have movie's name, grading, runtime, and rating
    IMDB_dict = {}
    title_lst = []
    num_reviews = []
    # genre_lst = []


    # IMDB lists top 50 from each genre
    #extracting...  
    for movie in data.findAll('div', class_= "lister-item-content"):#using the data stored by soap now extracting:
        
        
        # title
      
        title = movie.find("a", attrs = {"href" : re.compile(r'\/title\/tt+\d*\/')}) #regex used to collect only title form url using scraper soap
        #print(title)
        title = str(title).split('">')[1].split('</')[0]

        IMDB_dict[title] = []
        title_lst.append(title)
        
        
        # movie summary
        summary = movie.findAll('p', {'class':'text-muted'})
        if summary != None:
           # print(summary)
            summary = str(summary).split(', <p class="text-muted">')[1].replace("\n", "").replace("</p>]", "")  #clean the summary text
            #print(summary)
            IMDB_dict[title].append(summary)#identofy titles previously and match the summary
            #print(IMDB_dict[title].append(summary))
        
        
        # grading
        grading = movie.find('span', class_= "certificate")
        if grading != None:
            grading = str(grading).split('">')[1].split('</')[0]
        else:
            grading = "Not Found"
        IMDB_dict[title].append(grading)
       
        # runtime
        length = movie.find('span', class_ = "runtime")
        if length != None:
            length = str(length).split('">')[1].split('</')[0]
        else:
            length = "Not Found"
        IMDB_dict[title].append(length)

    # No. of reviewers
    for title, movie in zip(title_lst, data.findAll('p', class_ = "sort-num_votes-visible")):
        numRater = int(re.sub("[^0-9]", "",movie.text))
        num_reviews.append(numRater)
    
    

    
    # rating
    for review, title, movie in zip(num_reviews, title_lst, data.findAll('div', class_ = "ratings-bar")):
        rating = movie.find('div', class_ = "inline-block ratings-imdb-rating")
        try :
            rating = float(re.search(r'[\d]*[.][\d]+', str(rating).split(' ')[3]).group())# taking out only rating and not other elements
        except AttributeError:
            rating = float(re.search(r'\d+', str(rating).split(' ')[3]).group())

        # score adjustments based on number of reviewers through logistic regression 
        #LOGISTIC REGRESSION

        weightedRating = rating * log(log(review, 5), 10)# gives rating out of 10 
        #print(weightedRating)
        weightedRating = round(weightedRating, 1)
        
       # print(weightedRating)
        IMDB_dict[title].append(weightedRating)#match title with rating
        #print(IMDB_dict[title].append(weightedRating))
        
        
        # sklearn.linear_model.LogisticRegression

# def deviance(X, y, model):
    # return 2*metrics.log_loss(y, model.predict_proba(X), normalize=False)
        

     

    ranked_dict = rank_movies(IMDB_dict)#returns
    ranked_dict = dict(list(ranked_dict.items())[0: num])
    print(ranked_dict)
    ##Run when analysing#
    pd.json_normalize(ranked_dict)
    print (pd.json_normalize(ranked_dict))
   
  
    return ranked_dict

# RT should be a single link
def scrape_rt(RT, num):
    response = requests.get(RT)
    data = SOUP(response.text, 'lxml')
    RT_dict = {}
    title_lst = []
    rel_lst = []
    reviews_lst = []

    # Rotten Tomatoes lists top 100 from each genre

    # as above, we hope to obtain name, grading, runtime, and rating
    for movie in data.findAll('tr'):
        # title
        title = movie.find("a", class_ = "unstyled articleLink")
        if title != None:
            cleanTitle = str(title).split('">')[1].split(" (")[0].strip('\n').strip()
            RT_dict[cleanTitle] = []
            title_lst.append(cleanTitle) #100

            # link to movie profile
            rel_link = str(title).split('href="')[1].split('">\n')[0]
            link = "https://www.rottentomatoes.com/" + rel_link
            RT_dict[cleanTitle].append(link)
            
        # numbers of reviews:
        num_reviews = movie.find('td', class_ = "right hidden-xs")
        if num_reviews != None:
            num_reviews = int(str(num_reviews).split('">')[1].split('</')[0]) #100

            # collect number of reviewers for later movie score adjustments
            reviews_lst.append(num_reviews)

    # rating
    for review, title, movie in zip(reviews_lst, title_lst, data.findAll('span', class_ = 'tMeterIcon tiny')):
        rating = movie.find('span', class_ = "tMeterScore")
        rating = str(rating).split('">\xa0')[1].split('%</')[0]
        # transform RT rating into the same scale as IMDB rating (out of 10)
        weightedRating = int(rating)/10

        # score adjustments
        weightedRating = weightedRating * log(log(review, 4),5)
        weightedRating = round(weightedRating, 1)
        RT_dict[title].append(weightedRating)

    # to increase the efficiency of the script,
    # we are going to rank movies based on rating
    # and only look up movie profiles of top-ranked movies

    

    ranked_dict = rank_movies(RT_dict)
    ranked_dict = dict(list(ranked_dict.items())[0: num])
    for value in ranked_dict.values():
        rel_lst.append(value[0])
        value.pop(0)


    new_title_lst = list(ranked_dict.keys())

    # # grading and runtime information are inside movie profile links

    for title, link in zip(new_title_lst, rel_lst): 
        response = requests.get(link)
        data_1 = SOUP(response.text, 'lxml')

        #movie summary
        for div_tag in data_1.findAll('div', {'class':'movie_synopsis clamp clamp-6 js-clamp'}):
            summary = str(div_tag.text).replace("\n","")
            ranked_dict[title].insert(0, summary)

        for div_tag in data_1.findAll('li', {'class':'meta-row clearfix'}):
            movie_label= div_tag.find('div', {'class': 'meta-label subtle'}).text
            if movie_label == "Rating:":
                rating_info = div_tag.find('div', {'class': 'meta-value'}).text
                rating_info = rating_info.replace("\n","").replace(" ", "")
                ranked_dict[title].insert(1, rating_info)
            elif movie_label == "Runtime:":
                runtime_info = div_tag.find('div', {'class': 'meta-value'}).text
                runtime_info = runtime_info.replace("\n","").replace(" ", "")

                ranked_dict[title].insert(2, runtime_info)

    return ranked_dict

##  For Testing Purpose:
user_emotion = 'Happy'
RT_url = locate_url(user_emotion)[1]
IMDB_url = locate_url(user_emotion)[0]
#print(scrape_IMDB(IMDB_url, 12))
#print(scrape_rt(RT_url, 12))


movie_dict = {}
movie_dict.update(scrape_rt(RT_url, 12))
movie_dict.update(scrape_IMDB(IMDB_url, 12))
movie_dict = rank_movies(movie_dict)
