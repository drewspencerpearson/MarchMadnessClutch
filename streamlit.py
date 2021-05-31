import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from utils import *



#@st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data
teams = pd.read_csv('./teams_data.csv')


st.title('How Has Your University Done?')
st.markdown('This app will allow you to analyze various college basketball programs. First we will show you some visualizations\
    to help you get familiar with the data and look at some of the best teams in the last 15 years. \
    Then **You** can choose what programs you wish to examine and explore regarding the teams \
    performance in the NCAA college basketball tournament. The statistics are drawn from data from \
    the 2003 to the 2018 season. Enjoy!')

# ====================================================================================

st.header('Top Universities')
st.subheader('Who has made the most tournaments?')
plot_top20_tournament_appearances(teams)
st.pyplot()

# ===================================================================================
st.subheader('Who has the best average seed?')
plot_top20_average_seeds(teams)
st.pyplot()

# ===================================================================================


st.subheader('Who has the best average finish?')
st.markdown('TODO:::Geoff/Nick create a query and a graph to visualize the 15 programs or whatever who have \
    the best average finish')


st.header('Top Conferences')
st.subheader('TODO::::Kevin')

# =====================================================================================

st.header('Analyze Your Team')

st.subheader('Which team you would like to examine?')

# Get the users input for the team name. 
universities = st.text_input('Type in the name of the University. (Please capitalize)')

# If multiple, split it up by commas
team_names = universities.split(', ')
str_names = ", ".join(team_names)

# take a subset of our data based on the team(s) they entered
sub_teams = teams[teams['TeamName'].isin(team_names)]

# if they entered the name and we don't have it in our data, tell the user
if len(sub_teams) == 0 and len(universities)>0:
    st.markdown("We are sorry, we do not have that team name. Please try again")

    # Check to see if we have any teams similar to the input they gave, if so, display that
    possible_options = teams[teams['TeamName'].str.contains(team_names[0])]
    if len(possible_options) > 0:
        st.write("Perhaps you meant: {}".format(possible_options.TeamName.values))

# create our inital display table and display it
initial_display_df = sub_teams[['TeamName','number_of_tourneys', 'percent_of_tourneys_made','most_recent']]

if len(sub_teams)>0: # The user has put in an entry, and we found a team so we can show the table
    st.table(initial_display_df)

# ====================================================================================

# Plot performance compared to others

# The user has put in a team and we found a team, we can show the visual. 
if len(sub_teams)>0: 
    st.subheader('{} Tournament Appearances Versus Nations Average'.format(str_names))
    plot_tournament_appearances_compared_to_nation(teams, sub_teams, str_names, team_names)
    st.pyplot()

st.subheader('TODO::: Graph of their number of appearances compared to conference')

# ================================================================================================ #

# Seeding - Ask the user if they want to see info about seeding. If yes, display that info
st.subheader('Seeding')
show_seeding = st.text_input('Would you like to know how your team has been seeded in the tournaments? Yes or No')

if show_seeding =='Yes' or show_seeding == 'yes':
    seeding_display_df = sub_teams[['TeamName', 'number_of_tourneys','best_seed','worst_seed','average_seed']]
    st.table(seeding_display_df)


# ================================================================================================ #

# Performance - Ask the user if they want to see info about performance. If Yes, display that info
st.subheader('Performance')
show_performance = st.text_input('Would you like to know about their best and worst finishes? Yes or No')

if show_performance == 'Yes' or show_performance == 'yes':
    performance_display_df = sub_teams[['TeamName', 'number_of_tourneys', 'best_finish', 'best_season',\
     'worst_finish', 'worst_season', 'average_finish']]
    st.table(performance_display_df)



st.subheader('TODO::: Who did they lose to in their best finish?')


# ================================================================================================= #
# Cluth of their team

st.header('Is your team Clutch?')
st.markdown('We constantly hear, "my team always chokes" or "My team never performs up to expectations" \
    Well this section will analyze if your team typically over performs or underperforms in the \
    tournament based on their seeding')

# Read in the dataframe that has the teams performance with regards to expectations (seed)
expectations = pd.read_csv('./teams_data_expectations.csv')

# create a subset of the dataframe for the team of interest and pull out the info we will display
expectations_team = expectations[expectations['TeamName'].isin(team_names)]
expectations_display = expectations_team[['TeamName', 'Number of Tournaments', 'Number of Tournaments Overperform', \
'Number of Tournaments Underperform', 'Number of Tournaments Expected Performance']]

if len(sub_teams)>0:
    st.table(expectations_display)



# ========================================================================================================== #
### Plot the teams performance with regards to their seeding

#plt.xticks(wrap = True, fontsize = 8)
#plt.tight_layout()
if len(sub_teams)>0: # means the user entered a team and we found the right team, so we can display visuals
    st.subheader('Breakdown of {} the Perfomances in the Tournament'.format(str_names))
    plot_teams_performance_with_regards_to_seeding(str_names, expectations_team) 
    st.pyplot()


# ========================================================================================================== #
# Plot the expectation performance vs. other teams with same # of tournament appearances

st.subheader('{} performance in tournaments compared to others who have the same number \
    of Tournament Appearances'.format(str_names))


if len(sub_teams)>0:
    plot = plot_teams_performance_compared_to_others(expectations, team_names, expectations_team, str_names)
    if plot == True: # means the plot met the conditions
        st.pyplot()
    else:
        st.text('Sorry, there are no other teams with the same number of tournament appearances as {}'.format(str_names))
        


# ========================================================================================================== #
# Plot the expectation performance vs. other teams with similar seed

st.subheader('Breakdown of {} performance in tournaments compared to others who have a \
        similar average seed (within +-1 of average)'.format(str_names))

if len(sub_teams)>0:
    plot_seed_performance = plot_teams_performance_compared_to_otherssimilarseed(sub_teams, teams, expectations, team_names, str_names, expectations_team)
    if plot_seed_performance == True: # means the plot met the conditions
        
        st.pyplot()
    else:
        st.text('Sorry, there are no other teams with a similar average seeding as {}'.format(str_names))


