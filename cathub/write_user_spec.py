import json
from sys import argv
import os 

try:  #sherlock 1 or 2
    sherlock = os.environ['SHERLOCK']
    if sherlock == '1':
        catbase = '/home/winther/data_catapp/'
    elif sherlock == '2':
        catbase = '/home/users/winther/data_catapp/'
except:  # SUNCAT
    catbase = '/nfs/slac/g/suncatfs/data_catapp/'

print(catbase)

user, pub, DFT, XC, reaction, metal, facet, site, final = argv[1:10]

if site != 'None':
    site = int(site)
else:
    site = None
user_dict = {'user': user,
             'pub_level': int(pub),
             'DFT_level': int(DFT),
             'XC_level': int(XC),
             'reaction_level': int(reaction),
             'metal_level': int(metal),
             'facet_level':int(facet),
             'site_level': site,
             'final_level': int(final)
             }
    
user_file = '{}winther/user_specific/{}.txt'.format(catbase, user) 
json.dump(user_dict, open(user_file, 'w'))



