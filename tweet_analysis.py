import cv2
import pytesseract
from pytrends.request import TrendReq
import pandas as pd
from operator import itemgetter
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from PIL import Image

def tweet_text(image_path):

    img = cv2.imread(image_path)

    try:
        
        string = pytesseract.image_to_string(img)

    except TypeError:

        return 'imgur format'
    
    stop_words = set(stopwords.words('english')) 

    print(string)

    word_tokens = word_tokenize(string) 

    filtered_sentence = [] 

    for w in word_tokens: 
	    if w not in stop_words: 
		    filtered_sentence.append(w) 

    filtered_sentence = filtered_sentence[3:]
    print(filtered_sentence)

    with open('1-1000.txt','r') as fin:
        lines = fin.readlines()

    common = []

    for line in lines:
        common.append(line.rstrip('\n'))

    
    filtered_sentence = [s for s in filtered_sentence if not s.lower() in common]     

    
    filtered_sentence = [x for x in filtered_sentence if len(x) > 2 and '\n' not in x and 
                '.' not in x and ',' not in x and 'Retweets' not in x and 
                'Likes' not in x and 'iPhone' not in x and 'Twitter' not in x and 
                '/' not in x and 'Retweeted' not in x and '|' not in x and
                '©' not in x and '>' not in x and 'Comments' not in x and
                ':' not in x and '-' not in x and 'ing' not in x]
    
    
    filtered_sentence = list(dict.fromkeys(filtered_sentence))
    print(filtered_sentence)
    

    trends_values_ca = []
    trends_values_ny = []

    for items in filtered_sentence:

        temp = []
        temp.append(items)

        if len(items) > 0:

            pytrend_ca = TrendReq(hl='en-US', tz=360)
            pytrend_ny = TrendReq(hl='en-US', tz=360)

            pytrend_ca.build_payload(kw_list=list(temp), timeframe='now 1-d', geo='US-CA')
            pytrend_ny.build_payload(kw_list=list(temp), timeframe='now 1-d', geo='US-NY') 

            df_ca = pytrend_ca.interest_over_time()
            df_ny = pytrend_ny.interest_over_time()


            try:

                trends_values_ca.append(sum(list(df_ca[items])[-20:])/(len(df_ca.index)-20))

            except KeyError:

                trends_values_ca.append(0)

            try:

                trends_values_ny.append(sum(list(df_ny[items])[-20:])/(len(df_ca.index)-20))

            except KeyError:

                trends_values_ny.append(0)

    filtered_sentence = sorted((list(zip(filtered_sentence, 
                                list(map(lambda x, y: (x*0.82+y*0.18)/2, trends_values_ca, trends_values_ny))))),
                                key=itemgetter(1), reverse=True)

    print(filtered_sentence)


    if len(filtered_sentence) > 3:
        print("#" + filtered_sentence[0][0] + " #" + filtered_sentence[1][0] + " #" + filtered_sentence[2][0] + " #" + filtered_sentence[3][0])
        return "#" + filtered_sentence[0][0] + " #" + filtered_sentence[1][0] + " #" + filtered_sentence[2][0] + " #" + filtered_sentence[3][0]

    elif len(filtered_sentence) == 3:
        print("#" + filtered_sentence[0][0] + " #" + filtered_sentence[1][0] + " #" + filtered_sentence[2][0])
        return "#" + filtered_sentence[0][0] + " #" + filtered_sentence[1][0] + " #" + filtered_sentence[2][0]

    elif len(filtered_sentence) == 2:
        print("#" + filtered_sentence[0][0] + " #" + filtered_sentence[1][0])
        return "#" + filtered_sentence[0][0] + " #" + filtered_sentence[1][0]

    elif len(filtered_sentence) == 1:
        print("#" + filtered_sentence[0][0])
        return "#" + filtered_sentence[0][0]

    else:
        return ""

#tweet_text("test.jpg")
