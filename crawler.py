# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:05:36 2019

@author: pathouli
"""

class crawler(object):

    def my_scraper(self, tmp_url_in): 
        from bs4 import BeautifulSoup
        import requests
        import re
        tmp_text = ''
        #for query in the_query >> put loop here
        try:
            content = requests.get(tmp_url_in)
            #get() - method to return the value of the specified key
            soup = BeautifulSoup(content.text, 'html.parser')
            #BeautifulSoup()  running document through BeautifulSoup() gives us a
            #BeautifulSoup object, which represents a nested data structure
            #.text() - returns the text content of the selected elements
    
            tmp_text = soup.findAll('p') 
            #soup.findAll('p') - finds all <p> tags
            tmp_text = [word.text for word in tmp_text]
            #returns all of the text in the paragraphs
            tmp_text = ' '.join(tmp_text)
            #join() - method to join elements together by something, here by space ' '
            
            tmp_text = re.sub('\W+', ' ', re.sub('xa0', ' ', tmp_text))
        except:
            pass
    
        return tmp_text
    
    def fetch_urls(self, query_tmp, cnt):
        #now lets use the following function that returns
        #URLs from an arbitrary regex crawl form google
    
        #pip install pyyaml ua-parser user-agents fake-useragent
        import requests
        from fake_useragent import UserAgent
        from bs4 import BeautifulSoup
        import re 
        ua = UserAgent()

        query = '+'.join(query_tmp.split())
        #format to put into the google search
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(cnt)
        # str(cnt) - puts the number of pages (cnt) as a string (str())for the website 
        #this str(cnt) was added to only show the cnt number of most relevant searches in the results
        #eg this is a valid google search:https://www.google.com/search?q=qmss+columbia&oq=qmss+columbia&num=50 
        print (google_url)
        response = requests.get(google_url, {"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, "html.parser")

        result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})
        
        links = []
        titles = []
        descriptions = []
        for r in result_div:
            # Checks if each element is present, else, raise exception
            try:
                link = r.find('a', href = True)
                title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
                description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
    
                # Check to make sure everything is present before appending
                if link != '' and title != '' and description != '': 
                    links.append(link['href'])
                    titles.append(title)
                    descriptions.append(description)
            # Next loop if one element is not present
            except:
                continue  
    
        to_remove = []
        clean_links = []
        for i, l in enumerate(links):
            clean = re.search('\/url\?q\=(.*)\&sa',l)
 #           The enumerate() function adds a counter as the key of the enumerate object
            # i is the interation, l is the actual link, since enumerate returns a key eg 1 and then a value with that key 
            #re.search - search to see if the string (l) contains any of the characters
            #\/url - starts with /url?q= then anything, then &sa (patters for links)
            # Anything that doesn't fit the above pattern will be removed
            if clean is None:
                to_remove.append(i)
                continue
            clean_links.append(clean.group(1))

        return clean_links
    
    #def clean_data(self, var):
   #     import re
   #     from nltk.corpus import stopwords
   #     stopwords = set(stopwords.words('english'))
  #      stopwords.add('e')
        
 #       tmp_read = re.sub('[^a-zA-Z]+',' ', var)
 #       tmp_read = [word.lower() for word in tmp_read.split() if word not in stopwords]
 #       #tmp_read = [my_stem.stem(word) for word in tmp_read] #stemming has to scan
 #       tmp_read = [my_stem.lemmatize(word) for word in tmp_read] #lemma-ing to reduce 
 #       tmp_read = ' '.join(tmp_read)
 #       return tmp_read
 
    def write_crawl_results(self, the_path, my_query, the_cnt_in):
        #let use fetch_urls to get URLs then pass to the my_scraper function 
        import pandas as pd
        #import re
        from nltk.stem import PorterStemmer
        from nltk.corpus import stopwords
        stopwords = set(stopwords.words('english'))
        stopwords.add('e')
        my_stem = PorterStemmer()
        # guess loop needs to be here
        query_df = pd.DataFrame()
        for q in my_query:
            the_urls_list = self.fetch_urls(q, the_cnt_in)
            #print(the_urls_list)
            for word in the_urls_list:
                tmp_txt = self.my_scraper(word)
                if len(tmp_txt) != 0:
                    try:
                        body_stem = [my_stem.stem(word) for word in tmp_txt]
                        query_df = query_df.append(
                                {'body basic': tmp_txt,
                                 'body stem': body_stem,
                                 'label': q}, ignore_index = True)
    
                        #query_df['body basic'] = query_df.append(tmp_txt, ignore_index = True)
                      #  query_df['body stem'] = query_df.append([my_stem.stem(word) for word in tmp_txt], ignore_index = True)
                       # query_df['label'] = query_df.append(q, ignore_index = True)
                        
                    #tmp_txt = [word.lower() for word in tmp_txt.split() if word not in stopwords]
                       # tmp_df = pd.DataFrame([tmp_txt], columns =['body basic'])
                        #tmp_df['stemmed text'] = self.clean_data(tmp_txt)
                       # tmp_df['body stem'] = [my_stem.stem(word) for word in tmp_txt] 
                       # tmp_df['label'] = my_query
                       # query_df = query_df.append(tmp_df, ignore_index=True)
                    except:
                        pass

        print(query_df)        
         