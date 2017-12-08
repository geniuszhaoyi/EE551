# coding: utf-8

DEFINES_ONLY = True

from bs4 import BeautifulSoup
import time
import requests

def reviews(url,type,name):
    count=0;
    restname=[]
    fw=open(name,'w') # output file
    for p in range(1,80):
        pageLink=url+'/search?find_loc=Los+Angeles,+CA&start='+str(p*10)+'&cflt=' +type# make the page url
        for i in range(5): # try 5 times
                    try:
                        #use the browser to access the url
                        response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                        html=response.content # get the html
                        break # we got the file, break the loops
                    except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                        print ('failed attempt',i)
                        time.sleep(2) # wait 2 secs
        				
        		
        if not html:continue # couldnt get the page, ignore
                
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
        divget=soup.findAll('div',{'class':'media-story'})
        
        for div in divget:
            #print(review)
            #print(div)
            try:
                restaurant=div.find('a', {'class':'biz-name js-analytics-click'}) # get all the review divs
                kind=div.find('span',{'class':'category-str-list'})
                #print(restaurant)
               
                if restaurant:
                    if 'ad_business_id' not in restaurant['href']:
                        kind_s=kind.findAll('a')
                        if len(kind_s)==1:
                            
                            reviewnum=div.find('span',{'class':'review-count rating-qualifier'})
                            
                            reviewnum=reviewnum.text.replace('reviews','')
                            reviewnum=reviewnum.replace(' ','')
                           
                            if float(reviewnum)>200 and count<=50:
                                #print(kind)
                                print(reviewnum)
                                nextse=restaurant['href']
                                print(nextse)
                                sp=restaurant.find('span')
                                print(sp.text)
                                if sp.text not in restname:
                                    fw.write(str(count)+'\t'+reviewnum+'\t'+nextse+'\t'+sp.text+'\n')
                                    restname.append(sp.text)
                                    count+=1
                                print('\n')
                                    
                            elif count>50 :
                                fw.close()
                                return
            except Exception as e:
                continue

if DEFINES_ONLY == False:
    reviews('https://www.yelp.com', 'chinese', 'chinese.txt')

import time
import requests
import os, shutil

def getReviews(urlBase, url, filepath, maxReviews = 300):
    for p in range(0, int(maxReviews / 20)):
        pageLink=urlBase + url + '?start=' + str(p * 20) + '&sort_by=date_desc'# make the page url
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loops
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs


        if not html:
            raise Exception()
            continue # couldnt get the page, ignore
        else:
            with open(filepath + '/' + str(p) + '.html', 'w') as f:
                f.write(html.decode('ascii', 'ignore'))


#reviews('https://www.yelp.com', '/biz/lao-sze-chuan-glendale-5')

def getGene(name, maxReviews = 300):
    with open(name + '.txt', 'r') as f:
        ls = f.readlines()
        print(int(len(ls) / 3))
        for i in range(0, len(ls), 3):
            id = ls[i].strip()
            path = ls[i + 2].strip().split('\t')[0]
            print(id + " " + ls[i + 2].strip().split('\t')[1])
            if os.path.exists(os.path.join(os.getcwd(), name + "_" + id)) == False:
                try:
                    os.mkdir(os.path.join(os.getcwd(), 'temp'))
                except FileExistsError as e:
                    shutil.rmtree(os.path.join(os.getcwd(), 'temp/'))
                    os.mkdir(os.path.join(os.getcwd(), 'temp'))
                try:
                    getReviews('https://www.yelp.com', path, os.path.join(os.getcwd(), 'temp'), maxReviews = 300)
                    with open(os.path.join(os.getcwd(), 'temp') + '/metadata', 'w') as f:
                        f.write(ls[i] + ls[i + 1] + ls[i + 2] + str(int(maxReviews / 20)) + '\n')
                    os.rename(os.path.join(os.getcwd(), 'temp'), os.path.join(os.getcwd(), name + "_" + id))
                except Exception as e:
                    print ('failed attempt', name + "_" + id)
                    continue
            
if DEFINES_ONLY == False:
    getGene('chinese')

from bs4 import BeautifulSoup
import re
import time
import requests
import pandas as pd
import os

def get1(div_review, classdesc):
    try:
        li_friends = div_review.findAll('li', {'class': classdesc})
        li_friends_b = li_friends[0].findAll('b')
        friends = li_friends_b[0].contents[0]
        return friends
    except:
        return 0


def analyseHtml(html, rId):
    results = []
    print(rId)

    soup = BeautifulSoup(html,'lxml') # parse the html 
    reviews=soup.findAll('div',{'class':'review review--with-sidebar'})
    
    for div_review in reviews:
        result = {'restaurantId': rId}
        
        review_id = div_review['data-review-id']
        result['review_id'] = review_id

        try:
            a_username = div_review.findAll('a', {'class': 'user-display-name js-analytics-click'})
            username = a_username[0].contents[0]
            result['username'] = username
        except IndexError:
            result['username'] = ''
        
        num_friends = get1(div_review, 'friend-count responsive-small-display-inline-block')
        result['num_friends'] = num_friends
        num_reviews = get1(div_review, 'review-count responsive-small-display-inline-block')
        result['num_reviews'] = num_reviews
        num_photos = get1(div_review, 'photo-count responsive-small-display-inline-block')
        result['num_photos'] = num_photos
        
        try:
            review_text = div_review.findAll('p', {'lang': 'en'})[0].contents[0]
            result['review_text'] = review_text
        except IndexError:
            result['review_text'] = ''
        
        rating_qualifier = div_review.findAll('span', {'class': 'rating-qualifier'})[0].contents[0]
        result['date'] = rating_qualifier.strip()
        
        elite = len(div_review.findAll('a', {'href': '/elite'}))
        result['elite'] = elite
        
        try:
            a_useful = div_review.findAll('class', {'ybtn ybtn--small useful js-analytics-click'})[0]
            span_useful = a_useful.findAll('span', {'class': 'count'})[0]
            useful = span_useful.contents[0]
            result['useful'] = useful
        except IndexError:
            result['useful'] = 0
        
        rating = div_review.findAll('div', {'class': 'rating-large'})[0]['title']
        result['rating'] = rating.split()[0]
    
        results.append(result)
        
    return results

def analyseDir(path, rId):
    csvfilepath = os.path.join(path, 'data.csv')
    if os.path.isfile(csvfilepath) == True:
        return pd.read_csv(csvfilepath)
    else:
        res = []
        tempfilepath = 'temp.csv'
        f = open(os.path.join(path, 'metadata'))
        pages = int(f.readlines()[3])
        for page in range(pages):
            res += analyseHtml(open(os.path.join(path, str(page) + '.html')).read(), rId)
        df2 = pd.DataFrame(res)
        df2.to_csv(tempfilepath)
        os.rename(tempfilepath, csvfilepath)
        return df2

def analyseGene(name, max_id, path='/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/'):
    dfs = []
    for id in range(max_id + 1):
        df = analyseDir(path + name + '_' + str(id), name + '_' + str(id))
        dfs.append(df)
    return pd.concat(dfs)

def main(name, max_id, path):
    df2 = analyseGene(name, max_id, path=path)
    df2.to_csv(name + '.csv')
    return df2

if DEFINES_ONLY == False:
    main('chinese', 50, '/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/')

import pandas as pd
import re
import operator
from nltk.corpus import stopwords

import nltk
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize
from nltk import load

from textblob import TextBlob

def getFreq(inputcsv, outputcsv):
    csv_path = inputcsv
    data = pd.read_csv(csv_path)

    wordcount = {}
    stop_words =  set(stopwords.words('english'))
    costumer_stop_words = ['chinese', 'italian', 'mexican', 'good', 'great', 'food', 'place', 'los', 'angeles', 'hoboken']
    for word in costumer_stop_words: stop_words.add(word)
    costumer_not_stop_words = []
    for word in costumer_not_stop_words: stop_words.discard(word)
    file_stop_words = [word.strip().lower() for word in open('stopwords.txt').readlines()]
    for word in file_stop_words: stop_words.add(word)

    #make a new tagger
    _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
    tagger = load(_POS_TAGGER)


    jsons = []

    review_number = 0
    for index, row in data.iterrows():
        try:
            review = row['review_text']
            restaurantId = row['restaurantId']

            blob = TextBlob(review)
            blob.noun_phrases

            for i in range(len(blob.sentences)):
                sentence = blob.sentences[i]

                terms = nltk.word_tokenize(sentence.raw.lower())
                tagged_terms=tagger.tag(terms)

                for tg in ngrams(tagged_terms,2):
                    if tg[0][1].startswith('NN') and tg[1][1].startswith('NN') and tg[0][0] not in stop_words and tg[1][0] not in stop_words:
                        key = tg[0][0] + " " + tg[1][0]
                        json = {
                            "restaurantId": restaurantId,
                            "review_id": index,
                            "sentence_id": i,
                            "sentence": sentence.raw,
                            "phrase": key
                        }
                        jsons.append(json)

        except TypeError:
            print("TypeError");
        finally:
            if review_number%20 == 0:
                print(review_number)
            review_number += 1

    df = pd.DataFrame(jsons)
    df.to_csv('test.csv')
    print(df)
    
if DEFINES_ONLY == False:
    getFreq('chinese.csv', 'test.csv')

import pandas as pd
import json

def toJson(inputcsv, outputjson, restaurantDictName):
    csv_path = inputcsv
    data = pd.read_csv(csv_path)

    reduce1 = {}
    print('reducing 1')

    for index, row in data.iterrows():
        key = str(row['restaurantId']) + "|" + row['phrase'] + "|" + str(row['review_id']) 
        if key not in reduce1:
            reduce1[key] = []
        reduce1[key].append(row['sentence'])

    reduce2 = {}
    print('reducing 2')

    for k, v in reduce1.items():
        parts = k.split("|")
        key = parts[0] + "|" + parts[1] # restaurantId | phrase
        if key not in reduce2:
            reduce2[key] = []
        reduce2[key].append({'review_id': parts[2], 'sentences': v})

    reduce3 = {}
    print('reducing 3')

    for k, v in reduce2.items():
        parts = k.split("|")
        key = parts[0] # restaurantId
        if key not in reduce3:
            reduce3[key] = []
        reduce3[key].append({'phrase': parts[1], 'reviews': v})

    def sort_top_100(arr):
        return sorted(arr, key = lambda k: len(k['reviews']), reverse=True)[:100]

    print('finally')

    dictIdName = {}
    i = 0
    for l in open(restaurantDictName + '.txt').readlines():
        parts = l.split('\t')
        print(l, parts)
        if(len(parts) == 3):
            dictIdName[restaurantDictName + '_' + str(i)] = parts[2]
            i += 1
    
    res = []
    for k, v in reduce3.items():
        res.append({'restaurantId': k, 'restaurantName': dictIdName[k], 'top-none-phrases': sort_top_100(v)})

    with open(outputjson, 'w') as f:
        json.dump(res, f, indent=4, sort_keys=True)

    return res

# DEFINES_ONLY = False
DEFINES_ONLY = True
if DEFINES_ONLY == False:
    toJson('test.csv', 'json.json', 'customer')

from textblob import TextBlob
import json

def getresult(inputjson, outputfile, dictname):
    d = {}
    with open(inputjson) as json_data:
        d=json.load(json_data)

    dictIdName = {}
    i = 0
    for l in open(dictname + '.txt').readlines():
        parts = l.split('\t')
        print(l, parts)
        if(len(parts) == 3):
            dictIdName[dictname + '_' + str(i)] = parts[2]
            i += 1

    for restaurant in d: #[0:5]:
        outputfile.write('\n')
#         outputfile.write(dictIdName[restaurant['restaurantId']])
        outputfile.write(restaurant['restaurantName'] + '\n')
        likes=[]
        dislikes=[]
        for topword in restaurant['top-none-phrases'][0:10]:

            scoreword=0
    #        print(topword['phrase'])
            for reviews in topword['reviews']:
                countse=0
                scorese=0;
                for sentence in reviews['sentences']:
                    sentence=sentence.replace('chicken','beef')
                    blob = TextBlob(sentence)
                    blob.tags
                    blob.noun_phrases
                    ns=blob.sentences[0].sentiment.polarity
                    scorese+=ns
    #                print(sentence)
    #                print(ns)
                    countse+=1;
                scoreword+=scorese/countse
            result_word_score_avg=scoreword/len(topword['reviews'])
            if result_word_score_avg>0:
                likes.append(topword['phrase'])
            else:
                dislikes.append(topword['phrase'])
    #        print(result_word_score_avg)
        outputfile.write('What the Guests loved Most: ' + '\n')
        for like in likes:
            outputfile.write(like + '\n')
        outputfile.write('\n')
        outputfile.write('What nedd to be improved: ' + '\n')
        for dislike in dislikes:
            outputfile.write(dislike + '\n')
        outputfile.write('\n')
        outputfile.write('\n')
    
if DEFINES_ONLY == False:
    getresult('json.json', sys.stdout)

import sys, os
import shutil

def customerRestaurant(url, name, outputfile, clean=True):
    if clean:
        try:
            os.remove('customer.txt')
            shutil.rmtree('customer_0')
        except FileNotFoundError:
            pass
    open('customer.txt', 'w').write('0\n300\n\t' + url + '\t' + name + '\n')
    getGene('customer')
    main('customer', 0, '/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/')
    getFreq('customer.csv', 'test.csv')
    toJson('test.csv', 'json.json', 'customer')
    getresult('json.json', outputfile, 'customer')

def runGene(geneName):
    if os.path.exists(geneName + '.txt') == False:
        reviews('https://www.yelp.com', geneName, geneName + '.txt')
    getGene(geneName)
    main(geneName, 50, '/Users/enyaning/Desktop/BIA660/BIA660_TEAM_2/')
    getFreq(geneName + '.csv', 'test.csv')
    toJson('test.csv', 'json.json', geneName)
    getresult('json.json', open(geneName + '_result.txt', 'w'), 'customer')
    
if DEFINES_ONLY == False:
    runGene('chinese')
    customerRestaurant('/biz/king-szechuan-palace-jersey-city', 'King Szechuan Palace', sys.stdout)

os.environ['PATH'] += ":/Users/enyaning/Desktop/BIA660/week10/"
if __name__ == '__main__':
    url = '/biz/la-isla-restaurant-uptown-hoboken'
    if(len(sys.argv) >= 2):
        url = sys.argv[1]
    else:
        url = input("What is the url of the restaurant? ")
    name = 'Ulivo'
    if(len(sys.argv) >= 3):
        name = sys.argv[2]
    else:
        name = input("What is the url of the restaurant? ")
    # customerRestaurant(url, name, fifo)
    with open('fifo', 'w') as fifo:
        customerRestaurant(url, name, fifo)
