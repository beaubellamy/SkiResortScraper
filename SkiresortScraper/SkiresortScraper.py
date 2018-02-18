
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def get_html_content(url):
    """
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
    Main program
    '''

    url = 'http://www.skiresort.info/ski-resorts/'
    content = None
        
    # Get the html from the url
    #try:
    #    with closing(get(url, stream=True)) as resp:
    #        content_type = resp.headers['Content-Type'].lower()
    #        if is_good_response(resp):
    #            content = resp.content
    #        #else:
    #            # Unable to get the url responce
    
    #except RequestException as e:
    #    log_error('Error during requests to {0} : {1}'.format(url, str(e)))

    content = get_html_content(url)

    # Get a list of all ski resorts (go through each page)
    # <div id="resortList">
    html = BeautifulSoup(content, 'html.parser')
    resorts = html.find("div", {"id": "resortList"})

    pageLinks = html.find("ul", {"id": "pagebrowser1"})
    # Extract the total number of pages
    lastpage = int(re.findall('[0-9][0-9]' ,pageLinks.contents[-2].find('a')['href'])[0])



    # loop through each page
    for resort in resorts:
        if resort != ' ':
            # <a class="pull-right btn btn-default btn-sm" href="http...">Details</a>
            resortUrl = resort.find("a", {"class": "pull-right btn btn-default btn-sm"})['href']
            print ("Resort: ",resortUrl)
            
            resortContent = get_html_content(resortUrl)
            #try:
            #    with closing(get(resorturl, stream=true)) as resp:
            #        content_type = resp.headers['content-type'].lower()
            #        if is_good_response(resp):
            #            resortContent = resp.content

            
            resortHtml = BeautifulSoup(resortContent, 'html.parser')
            # Get altitude info
            altitudeDescipriton = resortHtml.find("div", {"id": "selAlti"}).contents
            # Get Slope statistics
            slopeTable = resortHtml.find("table", {"class": "run-table"})
            slopeSatistics={}
            print("Slope Statistics:")
            for row in slopeTable.findAll("tr"):
                key = row.contents[1].contents[1]
                value = re.findall('[0-9][0-9].[0-9] km',row.contents[3].contents[0])
                if not value:
                    # Value is less than 10.0
                    value = re.findall('[0-9].[0-9] km',row.contents[3].contents[0])

                slopeSatistics[key] = value
                print (key,": ",value)
            


            lifts = resortHtml.find("div", {"class": "lift-count"})
            # not quite right.
            liftStatistics = {}
            print("Lift numbers:")
            for lift in lifts:
                key = lifts['title']
                value = int(lifts.get_text())
                liftStatistics[key] = value

                print (key,": ",value)
                

        # Extract Elevation, 
        # Slopes: Easy, Intermediate, difficult, additional
        # Lifts: type: number
        # Pass prices: (get the currency as well)
        # Operating times






