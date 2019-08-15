import requests
import pandas
from bs4 import BeautifulSoup
#This is for the first page of the search results
r = requests.get("http://bls.mind-over-data.com/index.cfm/external/SearchResults/Handbook/1/%20/speciesRegionCompanyType/-1/7")
c = r.content
soup = BeautifulSoup(c,"html.parser")
all = soup.find_all("div",{"class","form-actions well"})
l= []
for item in all:
    d = {}
    try:
        d["Company Name"] = (item.find("h2",{"class","gray company-name"}).text)
    except:
        d["Company Name"] = None

    try:
        d["Company Category"] = item.find("address").text.replace("\r","").replace("\t","").replace(u'\xa0', u' ').splitlines()[2].strip()
    except:
        d["Company Category"] = None

    try:
        d["Company Address"] = item.find("address").text.replace("\r","").replace("\t","").replace(u'\xa0', u' ').splitlines()[5].strip()
    except:
        d["Company Address"] = None

    try:
        d["Company Locality"] = item.find("address").text.replace("\r","").replace("\t","").replace(u'\xa0', u' ').splitlines()[8].strip()
    except:
        d["Company Locality"] = None

    d["Company Phone Number"] = None
    d["Company Fax Number"] = None
    d["Company Website"] = None
    d["Company Email"] = None

    #iterate through address to pull the text we want out
    for content in item.find_all("address"):
            phone_number = ""
            fax_number = ""
            website = ""
            email = ""

            #iterate through the multiple phone numbers and pull each one out, same with fax
            for numbers in content.find_all("div"):#.text.replace(" ","").replace("\n","").replace("\r","").replace("\t",""))
                if "Phone: " in numbers.text:
                    phone_number += numbers.text.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace("Phone:","").replace(u'\xa0', u' ') + " "
                    d["Company Phone Number"] = phone_number

                if "Fax: " in numbers.text:
                    fax_number += numbers.text.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace("Fax:","").replace(u'\xa0', u' ') + " "
                    d["Company Fax Number"] = fax_number

            for urls in content.find_all("a"):
                if "www" in urls.text:
                    website += urls.text.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace(u'\xa0', u' ') + " "
                    d["Company Website"] = website

                if "@" in urls.text:
                    email += urls.text.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace(u'\xa0', u' ') + " "
                    d["Company Email"] = email






    l.append(d)

#The following is for pages 2 until the last one
baseurl_1 = "http://bls.mind-over-data.com/index.cfm/external/SearchResults/Handbook/"
baseurl_2 = "/%20/speciesRegionCompanyType/-1/7"
#the following lines of code gets page numbers and then iterates through all pages of the search result
page_list = soup.find_all("div", {"class":"pagination"})[0]
page_number = page_list.find_all("li")[-2].text.replace("\n","")
page_number
for page in range(1, int(page_number)):
    url = (baseurl_1 + str(page + 1) + baseurl_2)
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    all = soup.find_all("div",{"class","form-actions well nonAdResult"})
    for item in all:
        d = {}
        try:
            d["Company Name"] = (item.find("h3",{"class","gray company-name"}).text)
        except:
            d["Company Name"] = None

        try:
            d["Company Category"] = item.find("address").text.replace("\r","").replace("\t","").replace(u'\xa0', u' ').splitlines()[2].strip()
        except:
            d["Company Category"] = None

        try:
            #if the Address tag contains just a bunch of empty white space, give None value to address
            if item.find("address").text.replace("\r","").replace("\t","").replace(u'\xa0', u' ').splitlines()[5].isspace() == True:
                d["Company Address"]= None
            else:
                d["Company Address"] = None#item.find("address").text.replace("\r","").replace("\t","").replace(u'\xa0', u' ').splitlines()[5].strip()
        except:
            d["Company Address"] = None

        try:
            d["Company Locality"] = item.find("address").text.replace("\r","").replace("\t","").replace(u'\xa0', u' ').splitlines()[7].strip()
        except:
            d["Company Locality"] = None

        d["Company Phone Number"] = None
        d["Company Fax Number"] = None
        d["Company Website"] = None
        d["Company Email"] = None

        #iterate through address to pull the text we want out
        for content in item.find_all("address"):
                phone_number = ""
                fax_number = ""
                website = ""
                email = ""

                #iterate through the multiple phone numbers and pull each one out, same with fax
                for numbers in content.find_all("div"):#.text.replace(" ","").replace("\n","").replace("\r","").replace("\t",""))
                    if "Phone: " in numbers.text:
                        phone_number += numbers.text.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace("Phone:","").replace(u'\xa0', u' ') + " "
                        d["Company Phone Number"] = phone_number

                    if "Fax: " in numbers.text:
                        fax_number += numbers.text.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace("Fax:","").replace(u'\xa0', u' ') + " "
                        d["Company Fax Number"] = fax_number

                for urls in content.find_all("a"):
                    if "www" in urls.text:
                        website += urls.text.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace(u'\xa0', u' ') + " "
                        d["Company Website"] = website

                    if "@" in urls.text:
                        email += urls.text.replace(" ","").replace("\n","").replace("\r","").replace("\t","").replace(u'\xa0', u' ') + " "
                        d["Company Email"] = email






        l.append(d)
l
df = pandas.DataFrame(l)
df
