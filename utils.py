from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


# This file is a bunch of helper files that are used in streamlit.py 

def get_top20(teams, category, ascend):
	"""This function gets the top 20 teams in a given category then returns the dataframe
	of those top twenty teams in either ascending or descending order based on the ascend parameter"""
	teams_sorted = teams.sort_values(by = [category], ascending = ascend)
	top20 = pd.DataFrame(teams_sorted.head(20), columns = ['TeamName', category])
	return top20


def plot_top20_tournament_appearances(teams):
	"""This function plots the 20 teams that have the most tournament appearances"""

	# get the teams that are in the top 20 in tournament appearances
	top20appearances = get_top20(teams, 'number_of_tourneys', False)
	top20appearances.plot.bar(x='TeamName', y='number_of_tourneys')
	plt.tight_layout()
	plt.show()

def plot_top20_average_seeds(teams):
	"""This function plots the 20 teams with the best average seed"""

	top20averageseeds = get_top20(teams, 'average_seed', True)
	top20averageseeds.plot.bar(x="TeamName", y="average_seed")
	plt.tight_layout()

def get_other_teams_tournament_appearances(teams, team_names):
	"""This function gets the rest of nations average and median number of tournament appearances"""
	rest_of_nation = teams[~(teams['TeamName'].isin(team_names))]
	average_tournaments = np.mean(rest_of_nation.number_of_tourneys.values)
	median_tournaments  = np.median(rest_of_nation.number_of_tourneys.values)
	return average_tournaments, median_tournaments

def plot_tournament_appearances_compared_to_nation(teams, sub_teams, str_names, team_names):
	"""This function plots the tournament appearance for the team of interest in sub_teams
	compared to the rest of the nation"""
	# Get the rest_of_nations information for mean and median tournament appearances
	
	# get the teams average number of appearances and the rest of nations
	teams_average = np.mean(sub_teams.number_of_tourneys.values)
	average_other, median_other = get_other_teams_tournament_appearances(teams, team_names)

	# Graph the selected teams number of appearances vs. that nations average
	
	plt.bar(x = [str_names, 'Other teams Average', 'Other teams median'], \
		    height = [teams_average, average_other, median_other])
	plt.tight_layout()



def plot_teams_performance_with_regards_to_seeding(str_names, expectations_team):
	"""This function plots the teams performance with regards to their seeding"""
	plt.bar(x = ['% of Tournaments {} \n exceeded expectations'.format(str_names), \
            '% of Tournaments {} \n met expectations'.format(str_names), \
            '% of Tournaments {} \n under expectations'.format(str_names)], \
    		height = [expectations_team['Percent of Tournaments exceeded expectations'].values[0], \
              expectations_team['Percent of Tournaments met expectations'].values[0], \
              expectations_team['Percent of Tournaments under expectations'].values[0]])

	plt.ylabel('Percent of Tournaments \n {} appeared in'.format(str_names))


	plt.xticks(wrap = True, fontsize = 8)
	plt.tight_layout()

def get_others_with_equal_tournament_appearances(expectations, team_names, expectations_team):
	"""This function finds all the other teams in the nation that have been in the same number
	of tournaments as the team of interest and returns the data frame"""

	teams_tournaments = expectations_team['Number of Tournaments'].values[0]
	others = expectations[expectations['Number of Tournaments']==teams_tournaments]
	# make sure the team of interest is not in the others df
	others = others[~(others['TeamName'].isin(team_names))]
	return others

def plot_teams_performance_compared_to_others(expectations, team_names, expectations_team, str_names):
	"""This function will plot the percent of tournaments the team of interest exceeded expections
	versus the average percent of tournaments other teams exceeded expectations who have been in 
	the same number of tournaments"""
	
	others = get_others_with_equal_tournament_appearances(expectations, team_names, expectations_team)

	if len(others) >0: # means there is at least 1 other team we can compare too
		# plot the times team of interest exceeds expectations verses the average of the other teams
	    plt.bar(x = ['% of tournaments {} \n exceeded expectations'.format(str_names),\
	                '% of tournaments {} other teams \nexceeded expectations'.format(len(others))], \
	            height = [expectations_team['Percent of Tournaments exceeded expectations'].values[0],\
	                    np.mean(others['Percent of Tournaments exceeded expectations'].values)],
	            ) #color = [(.31, .31, .44)]

	    plt.ylabel('Percent of Tournaments')
	    plt.xticks(wrap = True)
	    plt.tight_layout()
	    return True
	else: 
		# This case is when the user found a team, but there are no other teams that have the same
	    # number of tournaments, so we had nothing to compare the team of interest to
		return False


def get_others_with_similar_average_seed(sub_teams, teams, expectations, team_names):
	"""This function finds all other teams in the nation that have an average seed +-1 
	of the team of interest. return the dataframe of all the other teams expectations performance"""

	# get the team of interests average seed and then all other teams that are +-1
	average_seed = sub_teams.average_seed.values[0]
	others = teams[(teams['average_seed']<average_seed+1)&(teams['average_seed']>average_seed-1)]

	# Get the team names and then get their expectation data. 

	other_names = others.TeamName.values
	others_expecations = expectations[expectations['TeamName'].isin(other_names)]

	#Ensure that the team of interest is not included
	others_expecations = others_expecations[~(others_expecations['TeamName'].isin(team_names))]
	return others_expecations



def plot_teams_performance_compared_to_otherssimilarseed(sub_teams, teams, expectations, team_names, str_names, expectations_team):
	"""his function will plot the percent of tournaments the team of interest exceeded expections
	versus the average percent of tournaments other teams exceeded expectations who have a similar
	average seeding"""
	others_expecations = get_others_with_similar_average_seed(sub_teams, teams, expectations, team_names)

	if len(others_expecations) > 0:
		plt.bar(x = ['% of tournaments {} \n exceeded expectations'.format(str_names), \
			'% of tournaments {} other teams \n exceeded expectations'.format(len(others_expecations))], \
			height = [expectations_team['Percent of Tournaments exceeded expectations'].values[0], \
			np.mean(others_expecations['Percent of Tournaments exceeded expectations'].values)])
		plt.ylabel('Percent of Tournaments')
		plt.xticks(wrap = True)
		plt.tight_layout()
		return True
	else:
		# This case is when the user found a team, but there are no other teams that have the same
		# number of tournaments, so we had nothing to compare the team of interest to
		return False