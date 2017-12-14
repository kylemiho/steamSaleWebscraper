import urllib
import urllib.request
from bs4 import BeautifulSoup

#open url and return the parsed data using Beautiful Soup
def openURL(url):
    page = urllib.request.urlopen(url)
    parsedHTML = BeautifulSoup(page,"html.parser")
    return parsedHTML

#write text to file, while encoding it to utf8
def writeToFile(text,filename):
    file = open(filename+'.txt','wb')
    file.write(text.encode('utf8'))
    file.close()

#check if a string is a valid int, used for findMaxPages
def isValidInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

#finds max number of steamSpecialPages
def findMaxPages(soup):
    #base case 0 maxPages
    maxPages = 0
    for i in soup.findAll('div',{'class':'search_pagination_right'}):
        for k in i.findAll('a'):
            if (isValidInt(k.text)):
                if (int(k.text) > maxPages):
                    maxPages = int(k.text)
    return maxPages

#open steam special page 1 url
#TODO: run forloop opening urls, except with specials=_ replaced with valid page number
#

textParsed = ""

#get first page with parsed html and run it into function to find max pages to parse through
firstParsed = openURL("http://store.steampowered.com/search/?sort_by=Reviews_DESC&specials=1")
maxPages = findMaxPages(firstParsed)

#go through each webpage, and parse them
for page in range(1,maxPages+1):

    #open and parse url
    urlToOpen = "http://store.steampowered.com/search/?sort_by=Reviews_DESC&specials=1&page="+str(page)
    print("Opening URL: " + urlToOpen)
    steamParsed = openURL(urlToOpen)

    #organize game info
    for i in steamParsed.findAll('div',{'class':'responsive_search_name_combined'}):

        ###########
        #find title
        title = i.find('span',{'class':'title'}).text
        ###########

        ###########
        #find %discount
        discount = ""
        discountDiv = i.find('div',{'class':'col search_discount responsive_secondrow'}).find('span')

        #if found, set discount to string value, else put Not on Sale
        if discountDiv is not None:
            discount = discountDiv.text
        else:
            discount = "NOT_ON_SALE"
        ############

        ############
        #find Ratings
        rating = ""
        ratingDiv = i.find('div',{'class':'col search_reviewscore responsive_secondrow'}).find('span')

        #if found, get rating info, else put no Ratings
        if ratingDiv is not None:
            rating = str(ratingDiv)
        else:
            rating = "NO_RATINGS"

        ############

        #formatting
        textParsed = textParsed + 'Name: ' + title + '\n' + 'Discount: ' + discount + '\n' + 'Rating: ' + rating + '\n-------------------\n'

#write to file
print("Writing to file...")
writeToFile(textParsed,'steamData001')
print("Done.")