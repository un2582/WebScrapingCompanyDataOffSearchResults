# WebScrapingCompanyDataOffSearchResults
I saw a request on upwork to grab company data off a website which displays all the lumber based companies off of a search result
Thought it would be a fun personal project so I went ahead and scraped it (Note: I did not make a proposal for the job, simply doing this as a project). I created a script to crawl through all the pages of the search results and grab the company data. Note that after the first page, there's a lot of None values for certain attributes. This is because the first page has a lot of company website url and emails posted on them, but from pages 2 and on, most of them do not seem to list this. I saved the data frame into a csv file named output.csv
