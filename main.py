import argparse
import numpy as np
import pandas as pd

# configuration
parser = argparse.ArgumentParser(description="Main script")
parser.add_argument('-c',"--competitors",
                    help="Path to competitors.csv (without file extension)")
parser.add_argument('-id',"--comp_id",
                    help="Short name of the competition by which one can access the website")
parser.add_argument('-l',"--layout",
                    help="Number of nametags to place on a page,\
                    given by rows x columns x (h/p)\
                    where h is for horizontal, p for portrait mode", default="5 x 2 x p")
args = parser.parse_args()

# read in user args
competitors_path = args.competitors
comp_id = args.comp_id
layout = args.layout

# hard-coded stuff
WCA_database_path = '../wca-competition-orga/WCA_export.tsv/'

# ToDo:
# - run validation before trying to read info à la `import validation from external; validation()`
#   - competitors.csv exists
#   - comp_id resolves to a real website
#   - layout makes sense and fits on a sheet

# get competitor information for specific competition
competitors = pd.read_csv(f'{competitors_path}.csv')
names = competitors['Name']
countries = competitors['Country']
# replace NaN Ids with Str 'Newcomer' for proper printout
competitors['WCA ID'].replace(np.nan, 'Newcomer', inplace=True) # for all views of the column
wca_ids = competitors['WCA ID']
# do not want zero-counting, we are humans and start with * 1 * :-)
competitor_ids = np.array(competitors.index + 1

# get competition information (associated staff like organizers and delegates)
competitions = pd.read_csv(f'{WCA_database_path}WCA_export_Competitions.tsv',sep='\t')
this_comp = competitions[competitions['id'] == comp_id]

delegates = this_comp['wcaDelegate']
orga = this_comp['organiser']

# go from a series (pandas) to a list, then split until only names remain
delegates_ = [d for d in delegates]
delegates_ = delegates_[0].split('] [')
delegates_ = [d.split('}{')[0].split('{')[1] for d in delegates_]
orga_ = [o for o in orga]
orga_ = orga_[0].split('] [')
orga_ = [o.split('}{')[0].split('{')[1] for o in orga_]
                          
# write LaTeX snippet that can be used for labels