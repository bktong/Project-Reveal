import pandas as pd
import requests
import math
from datetime import datetime


# Update the Pres Poll with latest file

def update_Polls():

    '''
    # note we initially downloaded the file from 538, but they closed this off as a point of usage.  
    url = 'https://projects.fivethirtyeight.com/polls-page/president_polls.csv'
    r = requests.get(url, allow_redirects=True)
    open('data/Polling/president_polls.csv', 'wb').write(r.content)
    '''
    
    # download current data set as a df directly.  Save df locally
    url = 'https://projects.fivethirtyeight.com/polls-page/president_polls.csv'
    df = pd.read_csv(url)
    df.to_csv('data/Polling/president_polls.csv', index=True)
    
    pass

def get_Poll(pollID, df):
    
    # pass in pollID
    # determine state or general level ("state")
    # grab candidate name ("candidate_name"), polling percentage("pct")
    
    # retrieve both rows for each polling number
    trump = df[((df["poll_id"]==pollID) & (df["candidate_name"]=="Donald Trump"))]
    biden = df[((df["poll_id"]==pollID) & (df["candidate_name"]=="Joseph R. Biden Jr."))]
    
    # calculating Margin of Error
    # we want 95% confidence, so z score = 1.96
    z = 1.96
    ss = trump.sample_size.values[0]
    poll_max = max([biden.pct.values[0], trump.pct.values[0]]) / 100
    x = ( poll_max*(1-poll_max) / ss )
    
    # multiply by 100 so we get the % confidence.
    MoE = round(1.96 * math.sqrt( x ), 4 )*100
    
    # Standard deviation. -  Calculating it, we know we use 95% confidence to calculate MoE above.
    # that is roughly 2 standard deviations, so one standard deviation is roughly half our MoE.
    
    # return a list of values.   
    # {pollid, state, , sample size, date, biden %, trump %, MoE}  
    return ([pollID, biden.state.values[0], biden.sample_size.values[0], biden.start_date.values[0], 
             biden.pct.values[0], trump.pct.values[0], abs(biden.pct.values[0] - trump.pct.values[0]), MoE, MoE/2])


def sanitize_Polls():
    # When we call sanitize_Polls, we go and update our current file of president polls (from 538) and we
    # aggregate only the data we care about.  Polling data between trump/biden when the race became officially 
    # the two of them.   
    
    # we return the resultant dataframe with the following fields
    # ['poll_id', 'state', 'date', 'biden_pct', 'trump_pct']
    
    data = pd.read_csv("data/Polling/president_polls.csv")
    
    # if state is left blank, it is a general election poll
    data["state"] = data.state.fillna("General")
    
    # Nebraska and Maine are weird, so we need to do some converting for sanity sake (right now)
    data.state.replace('Nebraska CD-2', 'Nebraska')
    
    #convert string date to datetime
    data["start_date"] = pd.to_datetime(data['start_date'])
    
    #filtering for only state-based polls.
    states = data[data["state"] != "General"].copy()
    
    #bernie dropped out 4/8 so throw out all polls prior.
    bernie = datetime.strptime("4/8/20", "%m/%d/%y")
    states = states[states.start_date > bernie]
    
    # the raw data we get is really ugly and we have to recreate our own df that we pass back.
    #get all unique pollIDs so we can down filter the ugliness of single row per candidate.
    
    pollID_values = states.poll_id.unique()
    
    # creating our sanitized df
    column_names = ['poll_id', 'state', 'sample_size', 'date', 'biden_pct', 'trump_pct', 'poll_diff', 'conf', 'stdev']
    df = pd.DataFrame(columns = column_names)
    
    # fill out the df with the polls we actually care about.
    for i in pollID_values:
        row_values = get_Poll(i, states)
        x = dict ((val, row_values[idx]) for idx, val in enumerate(column_names))
        df = df.append(x, ignore_index=True)
    
    # we need this step to line up the Nebraska Vote.   If Nebraska turned out to be a swing state
    # we would need to seperate out the different electoral votes individually here, but 
    # it isn't worth it as this time.
    
    df = df.replace(to_replace = 'Nebraska CD-2', value = 'Nebraska')
    return df


def build_state_level_Poll (df):
    
    # pass in the "sanitized df"
    # returns states df with columns ['state', 'biden_avg', 'trump_avg', 'voting_pop', 'percent_reg']
    
    registered_voters = pd.read_csv("data/USA/registered_voters_by_state.csv")
    
    polled_states = df['state'].unique()
    column_names = ['state', 'biden_avg', 'trump_avg', 'voting_pop', 'percent_reg']
    states = pd.DataFrame(columns = column_names)

    for s in polled_states:
        temp_state = df[(df["state"]==s)]
        reg_voters = registered_voters[registered_voters['State'] == s]
        
        # this can change to last 3 / 5 values or something else as we get more specific / trends.
        state_values = [s, round(temp_state.biden_pct.mean(), 3),
                        round(temp_state.trump_pct.mean(), 3), 
                        reg_voters.totalRegistered.values[0], 
                        reg_voters.registeredPerc.values[0] 
                       ]
        x = dict ((val, state_values[idx]) for idx, val in enumerate(column_names))
        states = states.append(x, ignore_index=True)

    states['eligible_pop'] = states['voting_pop']/states['percent_reg']
    return (states)

