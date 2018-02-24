
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re


def is_good_response(resp):
    """
    Ensures that the response is a html.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and 
            content_type is not None 
            and content_type.find('html') > -1)

def get_html_content(url):
    """
    Retrieve the contents of the url.
    """
    # Get the html from the url
    try:
        with closing(get(url, stream=True)) as resp:
            content_type = resp.headers['Content-Type'].lower()
            if is_good_response(resp):
                return resp.content
            else:
                # Unable to get the url responce
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))


if __name__ == '__main__':
    '''
    Extraxt data for each ski resort and sort into relevant features.
    '''
    # loop through each page
    # http://www.skiresort.info/ski-resorts/page/<index>/
    # need to think about how to cycle through each page while getting the urls for each resort on each page.


    
    # Sk resort website url
    url = 'http://www.skiresort.info/ski-resorts/'
    content = get_html_content(url)

    # Get a list of all ski resorts (go through each page)
    # <div id="resortList">
    html = BeautifulSoup(content, 'html.parser')
    
    pageLinks = html.find("ul", {"id": "pagebrowser1"})
    # Extract the total number of pages
    lastpage = int(re.findall('[0-9][0-9]' ,pageLinks.contents[-2].find('a')['href'])[0])
    
    # Cycle through each resort
    for resort in resorts:
        if resort != ' ':
            # Get the URL for each resort
            resortUrl = resort.find("a", {"class": "pull-right btn btn-default btn-sm"})['href']
            print ("Resort: ",resortUrl)
            
            # Extract the HTML
            resortHtml = BeautifulSoup(resortContent, 'html.parser')

            # Get altitude info
            altitudeDescipriton = resortHtml.find("div", {"id": "selAlti"}).contents
            print("Altitude: "+altitudeDescipriton[0])

            # Get Slope statistics
            slopeTable = resortHtml.find("table", {"class": "run-table"})
            slopeSatistics={}
            print("Slope Statistics:")
            for row in slopeTable.findAll("tr"):
                key = row.contents[1].contents[1]
                value = float(row.contents[3].contents[0].split("km")[0])
                
                slopeSatistics[key] = value
                print (key,": ",value)
            
            # Extract the Lift details.
            liftStatistics = {}
            print("Lift numbers:")
            for lift in resortHtml.findAll("div", {"class": "lift-count"}): #lifts:
                key = lift['title']
                value = int(lift.get_text())
                liftStatistics[key] = value

                print (key,": ",value)
                
            # Extract the ticket prices
            adultPrices = resortHtml.findAll("td", {"id": "selTicketA"})[0].contents[0]
            youthPrices = resortHtml.findAll("td", {"id": "selTicketY"})[0].contents[0]
            childPrices = resortHtml.findAll("td", {"id": "selTicketC"})[0].contents[0]

            # go to resort report to get ratings <stars>
            # <resortURL>/test-report/





