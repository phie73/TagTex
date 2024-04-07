import argparse
import requests
import numpy as np
import pandas as pd
import json
import re 
import unicodedata
import pycountry

# configuration
parser = argparse.ArgumentParser(description="Main script")
parser.add_argument('-c',"--comp_id",
                    help="competition id")
parser.add_argument('-o',"--order_by",
                    help="Order of nametags for printing, options: id, name, default: id",
                    default='id')
parser.add_argument('-od', "--print_orga_delegate",
                    help="print orga and delegate role on nametag, options y, n, default: n",
                    default='n')
#parser.add_argument('-l',"--layout",
#                    help="Number of nametags to place on a page,\
#                    given by rows x columns x (h/p)\
#                    where h is for horizontal, p for portrait mode", default="5 x 2 x p")
# currently, layout is just handled in preamble of the document itself, independent of content
args = parser.parse_args()

# read in user args
comp_id = args.comp_id
order_by = args.order_by
print_orga_delegate = args.print_orga_delegate

# get competitor information for specific competition
res = requests.get("https://worldcubeassociation.org/api/v0/competitions/" + comp_id + "/wcif/public")

# todo some checks for 200 and resonable answer
res_json = res.json()
activities = res_json['schedule']['venues'][0]['rooms'][0]['activities']
mAAp = dict()
for activity in activities:
    mAAp[activity['id']] = activity['activityCode']
    for child in activity['childActivities']:
        mAAp[child['id']] = child['activityCode']
persons = res_json['persons']

if order_by == 'name':
    persons = sorted(persons, key=lambda persons: persons['name'])

# event order
EVENTORDER = ['333', '222', '444', '555', '666', '777', '333bf', '333fm', '333oh', 'clock', 'minx', 'pyram', 'skewb', 'sq1', '444bf', '555bf', '333mbf']

tex_builder = ''
for person in persons:
    # structure {Name}{WCAID}{country}{reg id}{assignments[event & comp & scr & judge & run\\]}
    tmpName = person["name"].replace('ä', '\\"{a}').replace('ó', "\\'{o}").replace('ü', '\\"{u}').replace('ö', '\\"{o}').replace("é", "\\'{e}").replace("É", "\\'{E}").replace("á", "\\'{a}") #latex is stupid no support for this kind of characters in commands and it is way easier to do something like this in python than in latex
    tex_builder += '\card' + '{' + (tmpName, '\\begin{CJK*}{UTF8}{gbsn}' + tmpName + '\\end{CJK*}')[bool((re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')).search(person["name"])) != False] + '}'
    tex_builder += '{' + (person["wcaId"], '\\textcolor{ForestGreen}{Newcomer}')[person["wcaId"] == None] + '}'# either wcaId or 'Newcommer'
    tex_builder += '{' + pycountry.countries.get(alpha_2=person["countryIso2"]).name + '}'
    tex_builder += '{' + str(person["registrantId"]) 
    tex_builder += ('' , ('', (' \\textcolor{Red}{' + " ".join(str(x) for x in person["roles"]) + '}'))[person["roles"] != []])[print_orga_delegate == 'y'] + '}'

    assignments = dict()
    for a in person['assignments']:
        a['activityId'] = mAAp[a['activityId']]
        
        if (a['activityId'].startswith("333fm")):
            pass
        else:
            # acitvityId is build like event-round-group
            # build dict (or whatever it is python there are no datatypes) 'event' : '[comp,scr,judge,run]'
            tmpHelp = a['activityId'].split('-') # alles was ich im studium gelehrnt habe. irgendeine variable/function oder irgendwas muss immer hilfe heißen. Wenn es hilfe schon gibt, alternative dann HILFE, mehrHilfe, maximalHilfe usw.
            if not(tmpHelp[0] in assignments):
                assignments[tmpHelp[0]] = [' ',' ',' ',' ']
            if a['assignmentCode'] == 'competitor':
                assignments[tmpHelp[0]][0] += ((tmpHelp[2])[1:], (',' + (tmpHelp[2])[1:]))[assignments[tmpHelp[0]][0] != ' '] 
            elif a['assignmentCode'] == 'staff-scrambler':
                assignments[tmpHelp[0]][1] += ((tmpHelp[2])[1:], (',' + (tmpHelp[2])[1:]))[assignments[tmpHelp[0]][1] != ' ']
            elif a['assignmentCode'] == 'staff-judge':
                assignments[tmpHelp[0]][2] += ((tmpHelp[2])[1:], (',' + (tmpHelp[2])[1:]))[assignments[tmpHelp[0]][2] != ' ']   
            elif a['assignmentCode'] == 'staff-run':
                assignments[tmpHelp[0]][3] += ((tmpHelp[2])[1:], (',' + (tmpHelp[2])[1:]))[assignments[tmpHelp[0]][3] != ' ']
    # todo do optional sorting
    assignments = {key: i for i, key in enumerate(EVENTORDER)}
    print(assignments)
    tex_builder += '{'
    for k in assignments:
        tex_builder += k + '&' + assignments[k][0] + '&' + assignments[k][1] + '&' + assignments[k][2] + '&' + assignments[k][3] + '\\\\'
    tex_builder += '}'

# writing to tex/content.tex
# overwriting everything, makes no sense if there is already something in
f = open("tex/content.tex", "w")
f.write(tex_builder)
f.close()

#writing comp name
f = open("tex/name.tex", 'w')
f.write(res_json['name'])
f.close()





# names = competitors['Name']
# countries = competitors['Country']
# # replace NaN Ids with Str 'Newcomer' for proper printout
# competitors['WCA ID'].replace(np.nan, 'Newcomer', inplace=True) # for all views of the column
# wca_ids = competitors['WCA ID']
# # get competition information (associated staff like organizers and delegates)
# competitions = pd.read_csv(f'{WCA_database_path}WCA_export_Competitions.tsv',sep='\t')
# this_comp = competitions[competitions['id'] == comp_id]

# delegates = this_comp['wcaDelegate']
# orga = this_comp['organiser']
# comp_name = this_comp['name'].values[0]

# # go from a series (pandas) to a list, then split until only names remain
# delegates_ = [d for d in delegates]
# delegates_ = delegates_[0].split('] [')
# delegates_ = [d.split('}{')[0].split('{')[1] for d in delegates_]
# orga_ = [o for o in orga]
# orga_ = orga_[0].split('] [')
# orga_ = [o.split('}{')[0].split('{')[1] for o in orga_]
                          
# # write LaTeX snippet that can be used for labels
# for i in range(len(competitor_ids)):
#     tex_builder = '\\addresslabel{\centering{\selectlanguage{english} ' + comp_name + '\\vspace{1.1em} \Huge \\\\ '
    
#     name_string = f'{names[i]}'
#     multi_row_name = False
#     if '(' in name_string and ')' in name_string:
#         multi_row_name = True
#         # this is a name with additional local string with other characters
#         # would require a linebreak most likely, so the string is split into two
#         # and later the second part is written with a smaller fontsize
#         name_string_a, name_string_b = name_string.split('(')
#         name_string_a = name_string_a[:-1]
#         name_string_b = name_string_b[:-1]
#         tex_builder += '\\textbf{\\centering \\begin{minipage}{82mm}\\centering '+ name_string_a + '\\end{minipage}\\vspace{1.5mm}}'
#         tex_builder += '}'
#         tex_builder += '\\\\'
#         if countries[i] == 'Russia' or countries[i] == 'Ukraine':
#             tex_builder += ' \\selectlanguage{russian} '
#         if countries[i] == 'China':
#             tex_builder += ' \\begin{CJK*}{UTF8}{gbsn} '
#             tex_builder += '(' + name_string_b + ')'
#             tex_builder += ' \\end{CJK*}'
#         else:
#             tex_builder += '(' + name_string_b + ')'
#     else:
#         tex_builder += '\\textbf{\\centering \\begin{minipage}{82mm}\\centering '+ name_string + '\\end{minipage}}}'
#     tex_builder += '\\\\ '
    
    
#     country_string = f'{countries[i]}'
#     wca_id_string = f'{wca_ids[i]}'
#     if wca_id_string == 'Newcomer':
#         wca_id_string = '\\textcolor{ForestGreen}{' + wca_id_string + '}'
#     competitor_id_string = competitors['competitor_ids'][i]
    
#     is_del = True if names[i] in delegates_ else False
#     is_orga = True if names[i] in orga_ else False
#     optional_role_string = ''
#     if is_del and is_orga:
#         optional_role_string = 'Delegate, Organizer'
#     else:
#         if is_del:
#             optional_role_string = 'Delegate'
#         elif is_orga:
#             optional_role_string = 'Organizer'
    

#     if optional_role_string != '':
#         tex_builder += '\\selectlanguage{english} \\ \\\\ ' + '\\textcolor{Red}{' + optional_role_string + '} \\\\ '
    
#     tex_builder += '\\selectlanguage{english} \\begin{tabular}{lcr}	\\qquad &  \\qquad & \\qquad  \\\\' + wca_id_string + '&' + country_string + '& ID: ' + f'{competitor_id_string}' + '\\\\ \\end{tabular}'
    
#     tex_builder += '}'
    
#     print(tex_builder)
