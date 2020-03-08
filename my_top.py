# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 07:35:36 2019

@author: pathouli
"""

from crawler import crawler


my_path = '/Users/kimevarista/Desktop/'
the_query = ['paris','london','toronto','miami']

num_docs = 50

my_func = crawler()

test = my_func.write_crawl_results(my_path, the_query, num_docs)

print(test)

#1.	Observations – Google vs crawler text files 
#Comparing the text files output and the links returned from the crawler 
#to a manual Google search, the links were a close match in terms of which 
#sites were returned and in which order. The first page matched exactly, 
#and comparing the webpage link through Google and the first text file, 
#the text file scraped is the <p> html tags from the QMSS main webpage, 
#as per the line of code in the crawler tmp_text = soup.findAll('p'). 
#After taking a closer look at the script code, it appears that the reason 
#why the manual Google search results did not perfectly align with the urls 
#returned is because of specifying an exact number of results in our query 
#using the num_docs variable. This parameter will limit the number of 
#search results, and when doing so manually in a Google search the urls 
#returned will be the top num_docs amount, based on what the Google algorithm 
#deems are the top relative results. 
