import interface
import json
from scraper import locate_url, rank_movies, scrape_IMDB, scrape_rt
from sklearn.model_selection import train_test_split
import movie_page
from movie_summary import get_movie_summary
from similarity_analyzer import find3MostSim
import summary_page

from tkinter import *

if __name__ == "__main__":

    # call interface.py

    window = Tk()
    interface = interface.interface(window)
    window.mainloop()
    user_inputs = [] # obtain user selections
    for i in interface.result:
        user_inputs.append(interface.emotions[i])

    # apply self-built crawler

    user_emotion = user_inputs
    url_lst = locate_url(user_emotion)
    
    movie_dict = {}

    for url in url_lst:#3 options
        if "www.imdb.com" in url:
            if len(user_emotion) == 1:
                movie_dict.update(scrape_IMDB(url, 12))#amount of results 
            elif len(user_emotion) == 2:
                movie_dict.update(scrape_IMDB(url, 6))
                
            elif len(user_emotion) == 3:
                movie_dict.update(scrape_IMDB(url, 4))
        elif "www.rottentomatoes.com" in url:
            if len(user_emotion) == 1:
                movie_dict.update(scrape_rt(url, 12))
            elif len(user_emotion) == 2:
                movie_dict.update(scrape_rt(url, 6))
            elif len(user_emotion) == 3:
                movie_dict.update(scrape_rt(url, 4))
    movie_dict = rank_movies(movie_dict)
    #print(movie_dict)
    # outfile = open('movie_dict.txt','a')
    # outfile.write(str(movie_dict) + '\n')
    # outfile.close()
    # #print(user_emotion)
    # file = open('mood.txt','a')
    # file.write(str(user_emotion) + '\n')
    # file.close()
    
    # filename= 'Book-4.csv'
    # infile = open(filename, 'r')
    # data = infile.read()
    # print(data)
    # infile.close()
    
   
    # filename= 'Book.csv'
    # infile = open(filename, 'r')
    # data1 = infile.read()
    # print(data1)
    # infile.close()
  
  
  
   
    # X_train, X_test, y_train, y_test = train_test_split(data,data1,test_size=0.2)
    # w = len(X_train)
    # from sklearn.linear_model import LinearRegression
    # clf= LinearRegression()
    # clf.fit(X_train,y_train)
    # clf.predict(X_test)
    # pp = clf.score(X_test,y_test)
    # print(pp)
    
    
    
    
    
    # load movie page
    root = Tk()
    movie_page = movie_page.movie_page(root, movie_dict)
    root.mainloop()
    
    # Cosine-Similarity analysis
    userClicked = movie_page.selected_movie
    userClicked = list(set(userClicked))
    movieName = userClicked[0]
    
    summary_list = get_movie_summary(movie_dict, movieName)#logistic regression and cosine is proceeded
    
    
    
    targetIndex = find3MostSim(movie_dict, summary_list)#continued cosine
    #print(targetIndex)
    
   # print(targetIndex)
    targetMovies = []
    targetMovieSummary = []
    mainSummary = summary_list[1]
    #print(mainSummary)
    for i in targetIndex:
        summary = summary_list[0][i]
        targetMovieSummary.append(summary)
        for key, value in movie_dict.items():
            if summary == value[0]:
                targetMovies.append(key)
                


    # load tkinter based on users' selection
    SP = Tk()
    Summary_Page = summary_page.Summary_Page(SP, targetMovies, targetMovieSummary, mainSummary)
    
    SP.mainloop()











