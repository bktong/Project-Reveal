This is a Python repository for my FlatIron Data Science Capstone project on the 2020 Presidential Election.  

# Project Goal:
The goal of my project is to explore just how small of a subsection of voters is needed to win the Presidency.  It in itself is a very loaded question but in the age of extreme political polarization I felt we could explore the parameters of this through the various techniques learned throughout this course.  

As with all things we needed to understand the baseline rules of the presidential election process.

# Project Isssues:

Data Collection is ... inconsistent (to put it lightly):

Election data and its ancillary data sources is extremely fragmented as elections are run and organized individually by state and somehow cobbled together nationally.  Although the end vote is all that matters, other data is pretty much the Wild, wild west.  As such formats, naming conventions, etc can be all over the place.   

Once you try to dig deeper, state-level data is often also not collected in a systematic manner that makes aggregation easy.  (I think this is by design).  Often-times when collecting specific data in Florida, I had to visit each county individually and then write some helper functions to clean up and mismatched, misnamed data.  One county ("Gulf") in Florida actually attempted to install malware onto my computer and I got in touch with their IT group to inform them of their unwanted issue.  Extrapolate this by the 3141 counties in the US, and I can see why election night is a nightmare.   Perhaps there's a project available on Election Logistics Reform.


# Background Facts:
1. The Electoral College casts ballots for who wins the presidency.  Not the voters directly.  
2. There are a total of 538 Electoral Votes to be won (50 states + DC), so the real race is to 270.
3. Each state gets a designated number of electoral votes accounting for their share of the population.  
4. The Electoral voters in each state cast all their votes for the popular vote winner of that state.   It is winner take all, meaning if Trump wins a popular vote in Florida by 5 total votes, Trump would get all 29 of the electoral votes from Florida.  
5. This project will not worry about a situation where the candidates tie at 269 votes each, but contingency procedures are in place as established by the 12th Amendment.

Given the Background, the project scope followed both a top down and bottoms up approach to reach the targeted demographic.

Top Down:   
National Polling -> State Polling -> Electoral College -> Swing States -> States Needed for 270 -> Undecided Voters

Bottoms Up:
Key States -> Voter Demographics -> Voter Priorities -> Simulations on Undecided Voter Population

Data Sources:
anywhere and everywhere

TV ads all politicians
https://www.democracyinaction.us/2020/ads/ads.html

Federal Election Commission
https://www.fec.gov/data/

Polls - Real Clear Politics
https://www.realclearpolitics.com/epolls/latest_polls/state_president/

Pollster ranking
https://github.com/fivethirtyeight/data/blob/master/pollster-ratings/pollster-ratings.csv
https://github.com/fivethirtyeight/data/blob/master/pollster-ratings/pollster-stats-full.xlsx
https://projects.fivethirtyeight.com/pollster-ratings/

538 aggregate polls
https://projects.fivethirtyeight.com/polls-page/president_polls.csv

Gallup Polls (
https://news.gallup.com/poll/276932/several-issues-tie-important-2020-election.aspx

Voter Turnout Numbers
http://www.electproject.org/home/voter-turnout/voter-turnout-data

Registered Voters by State
https://worldpopulationreview.com/states/number-of-registered-voters-by-state/

County level returns for Presidential Elections (2000-2016)
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ


Pull requests are welcome. Suggestions and comments on anything from the programming to the modeling are also welcome.

The third-party packages used are

- Pandas
- Numpy
- matplotlib
- scikit-learn
- scipy
- statsmodels
