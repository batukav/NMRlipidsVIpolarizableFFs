
# coding: utf-8

# # Database test

# ## Simulation description file

# In[1]:
import sys
import importlib
import re
from random import randint

inp = sys.argv[1].split('.')[0]
print(inp)
inFile = importlib.import_module(inp, package=None)





# ## General Imports

# In[2]:


# Working with files and directories
import os

#For quering webs
import urllib.request
from urllib.error import URLError,HTTPError

# From time monitoring
from tqdm import tqdm

# Python program to find SHA256 hash string of a file
import hashlib

# For dealing with excel and cvs 
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

#To make real independent copies of lists
from copy import deepcopy


# ## Directories

# In[3]:


#dir_wrk = os.path.normpath(dir_wrk)
dir_wrk = inFile.dir_wrk
#mapping_dir =os.path.normpath(mapping_dir)
print(dir_wrk)
#print(mapping_dir)


# ## Check that the DOI link is valid

# In[4]:


DOI_url = 'https://doi.org/' + inFile.DOI
print(DOI_url)

try:
    response = urllib.request.urlopen(DOI_url)
    print("Status of the DOI link: {0}".format(response.msg))
except HTTPError as e:
    print(DOI_url)
    print('The server couldn\'t fulfill the request.')
    print('Error code: ', e.code)
    user_information = ""
    print('The code will not proceed, please fix DOI')
except URLError as e:
    print(DOI_url)
    print('We failed to reach a server.')
    print('Reason: ', e.reason)
    user_information = ""
    print('The code will not proceed, please fix DOI')
else:
    pass


# ## Read input description

# In[5]:


bNMRLIPIDS = False #Check if the link contains NMRLIPIDS metadata
nsims =0 # Counter number of simulations in a submission
sims = [] #Array with the dictionary containing the information of a simulation

for line in inFile.user_information.split("\n"):
    if line.strip() == "":
        continue
    if "#NMRLIPIDS BEGIN" in line:
        bNMRLIPIDS = True
        continue
    if "#NMRLIPIDS END" in line:
        bNMRLIPIDS = False
        continue
    if "@SIM" in line:
        #sims.append({"ID" : nsims, "STATUS" : 0})
        sims.append({"ID" : nsims})
        nsims += 1
        sims[-1]["DOI"] = inFile.DOI
        continue
    if not bNMRLIPIDS:
        continue
    if line.strip()[0] == "@":
        key, value = line.split("=")
        sims[-1][key.strip('@')] = value
print(nsims)
print(sims)      
        


# ### Dictionares

# In[6]:


#Molecules dictionary

lipids_dict = {
                'POPC' : {"REQUIRED": False,
                             "TYPE": "string",
                         },
                'POPG' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                'POPS' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                'POPE' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                'CHOL' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                }

molecules_dict = {
                
                'POT' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                'SOD' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                'CLA' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                'CAL' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                'SOL' : {"REQUIRED": False,
                            "TYPE" : "string",
                        },
                }


               
molecule_numbers_dict = {
                'NPOPC' : {"REQUIRED": False,
                              "TYPE": "array",
                          },
                'NPOPG' : {"REQUIRED": False,
                            "TYPE" : "array",
                         },
                'NPOPS' : {"REQUIRED": False,
                            "TYPE" : "array",
                        },
                'NPOPE' : {"REQUIRED": False,
                            "TYPE" : "array",
                        },
    
                'NCHOL' : {"REQUIRED": False,
                            "TYPE" : "array",
                        },
    
               'NPOT' : {"REQUIRED": False,
                            "TYPE" : "integer",
                        },
                'NSOD' : {"REQUIRED": False,
                            "TYPE" : "integer",
                        },
                'NCLA' : {"REQUIRED": False,
                            "TYPE" : "integer",
                        },
                'NCAL' : {"REQUIRED": False,
                             "TYPE" : "integer",
                         },
                'NSOL' : {"REQIRED": False,
                            "TYPE" : "integer",
                        },
    
                }
               
                
                

# Gromacs
gromacs_dict = {
               'INI' : {"REQUIRED": False,
                        "TYPE" : "files",
                        "EXTENSION" : ("gro", "pdb",),
                       }, # Could be not needed in the future (tpr)
               'MDP' : {"REQUIRED": False,
                        "TYPE" : "file",
                        "EXTENSION" : ("mdp",),
                       }, # Could be not needed in the future (tpr)
               'TRJ' : {"REQUIRED": True,
                        "TYPE" : "files",
                        "EXTENSION" : ("xtc","trr",),
                       },
               'TPR' : {"REQUIRED": True,
                        "TYPE" : "file",
                        "EXTENSION" : ("tpr",),
                       },
               'CPT' : {"REQUIRED": False,
                        "TYPE" : "file",
                        "EXTENSION" : ("cpt",),
                       },
               'TOP' : {"REQUIRED": False,
                        "TYPE" : "file",
                        "EXTENSION" : ("top",),
                       },
               'ITP' : {"REQUIRED": False,
                        "TYPE" : "files",
                        "EXTENSION" : ("itp",),
                       },
               'FF'  : {"REQUIRED": False,
                        "TYPE" : "string",
                       },
               'FF_SOURCE' : {"REQUIRED": False,
                              "TYPE" : "string",
                              },
               'FF_DATE' : {"REQUIRED": False,
                            "TYPE" : "date",
                           },
               'DOI' : {"REQUIRED": True,
                            "TYPE" : "string",
                           },
    
               'SYSTEM' : {"REQUIRED": True,
                            "TYPE" : "string",
                           },
            'TEMPERATURE' : {"REQUIRED": False,
                            "TYPE" : "integer",
                            },
             'TRJLENGTH' : {"REQUIRED": False,
                           "TYPE" : "integer",
                           },
            'PREEQTIME' : {"REQUIRED": True,
                          "TYPE" : "integer",
                          },
          'TIMELEFTOUT' : {"REQUIRED":True,
                          "TYPE" : "integer",
                          },
            'MAPPING' : {"REQUIRED": True,
                             "TYPE" : "string",
 #                        "EXTENSION": ("txt"),
                             },
              
               }

# Amber
amber_dict = {}

# NAMD
namd_dict = {   
            'TRJ' : { "REQUIRED": True,
                      "TYPE": "files",
                      "EXTENSION": ("dcd"),
                    },
            'INP' : { "REQUIRED": False,
                      "TYPE": "file",
                      "EXTENSION": (".inp"),
                    },
            'LOG' : { "REQUIRED": False,
                      "TYPE": "files",
                      "EXTENSION": ("log"),
                      # can be parsed to get software version etc.
                    },
            'PSF' : { "REQUIRED": False,
                      "TYPE": "file",
                      "EXTENSION": ("psf"),
                    },
            'FF'  :  { "REQUIRED": False,
                      "TYPE" : "string",
                    },
            'FF_SOURCE' : {"REQUIRED": False,
                           "TYPE" : "string",
                              },
            'FF_DATE' : {"REQUIRED": False,
                         "TYPE" : "date",
                        },
            'PDB'  : { "REQUIRED": True,
                    "TYPE": "file",
                    "EXTENSION": "pdb",}
               }
          
# CHARMM
charmm_dict = {}

# OPENMM
openmm_dict = {
               'INI' : {"REQUIRED": False,
                        "TYPE" : "files",
                        "EXTENSION" : ("gro", "pdb",),
                       }, # Could be not needed in the future (tpr)
               'MDP' : {"REQUIRED": False,
                        "TYPE" : "file",
                        "EXTENSION" : ("mdp",),
                       }, # Could be not needed in the future (tpr)
               'TRJ' : {"REQUIRED": True,
                        "TYPE" : "files",
                        "EXTENSION" : ("xtc","trr",),
                       },
               'PDB' : {"REQUIRED": True,
                        "TYPE" : "file",
                        "EXTENSION" : ("pdb",),
                       },
               'TPR' : {"REQUIRED": False,
                        "TYPE" : "file",
                        "EXTENSION" : ("tpr",),
                       },
               'CPT' : {"REQUIRED": False,
                        "TYPE" : "file",
                        "EXTENSION" : ("cpt",),
                       },
               'TOP' : {"REQUIRED": False,
                        "TYPE" : "file",
                        "EXTENSION" : ("top",),
                       },
               'ITP' : {"REQUIRED": False,
                        "TYPE" : "files",
                        "EXTENSION" : ("itp",),
                       },
               'FF'  : {"REQUIRED": False,
                        "TYPE" : "string",
                       },
               'FF_SOURCE' : {"REQUIRED": False,
                              "TYPE" : "string",
                              },
               'FF_DATE' : {"REQUIRED": False,
                            "TYPE" : "date",
                           },
               'DOI' : {"REQUIRED": True,
                            "TYPE" : "string",
                           },
    
               'SYSTEM' : {"REQUIRED": True,
                            "TYPE" : "string",
                           },
            'TEMPERATURE' : {"REQUIRED": False,
                            "TYPE" : "integer",
                            },
             'TRJLENGTH' : {"REQUIRED": False,
                           "TYPE" : "integer",
                           },
            'PREEQTIME' : {"REQUIRED": True,
                          "TYPE" : "integer",
                          },
          'TIMELEFTOUT' : {"REQUIRED":False,
                          "TYPE" : "integer",
                          },
            'MAPPING' : {"REQUIRED": False,
                             "TYPE" : "string",
 #                        "EXTENSION": ("txt"),
                             },
              
               }

# SOFTWARE
software_dict = {
                "GROMACS" : gromacs_dict, 
                "AMBER"   : amber_dict,
                "NAMD"    : namd_dict,
                "CHARMM"  : charmm_dict,
                "OPENMM"  : openmm_dict,
                }

print(software_dict.keys())


# ### Check software used by the simulation

# In[7]:


sims_valid_software = []
for sim in sims:
    if sim['SOFTWARE'].upper() in software_dict.keys():
        msg_info = "Simulation {0} uses supported software {1} and will be further processed"
        print (msg_info.format(sim['ID'], sim['SOFTWARE'].upper()))
        sims_valid_software.append(sim.copy())
    else:
        msg_err="Simulation {0} performed in an UNSUPPORTED software {1} and will NOT be further processed"
        print(msg_err.format(sim["ID"], sim["SOFTWARE"].upper()))
print(sims_valid_software) 


# ### Check that all entry keys provided for each simulation are valid:

# In[8]:


sims_valid_entries = []
for sim in sims_valid_software:
    #print("ID {0}".format(sim["ID"]))
    wrong_key_entries = 0
    software_dict_name = "{0}_dict".format(sim['SOFTWARE'].lower())
    print(sim.items())
    for key_sim, value_sim in sim.items():
        #print(key_sim, value_sim)
        #print(key_sim.upper())
        if key_sim.upper() in ("ID", "SOFTWARE"):
            #print("NOT REQUIRED")
            continue
    #Anne: check if key is in molecules_dict or molecule_numbers_dict too
        if key_sim.upper() not in software_dict[sim['SOFTWARE'].upper()].keys() and key_sim.upper() not in molecules_dict.keys() and key_sim.upper() not in lipids_dict.keys() and key_sim.upper() not in molecule_numbers_dict:
            print ("{0} NOT in {1}".format(key_sim, software_dict_name))
            wrong_key_entries += 1
    if wrong_key_entries:
        print("Simulation {0} has {1} unknown entry/ies and won't be longer considered, please correct.\n".format(sim['ID'],wrong_key_entries))
    else:
        msg_info = "All entries in simulation {0} are understood and will be further processed\n"
        print (msg_info.format(sim['ID']))
        sims_valid_entries.append(sim.copy())
print(sims_valid_entries)


# ### Process entries with files information to contain file names in arrays

# In[9]:


sims_files_to_array = deepcopy(sims_valid_entries)

for sim in sims_files_to_array:
    print("ID {0}".format(sim["ID"]), flush=True)
    software_sim = software_dict[sim['SOFTWARE'].upper()]
    for key_sim, value_sim in sim.items():
        try:
            entry_type = software_sim[key_sim]['TYPE']
            if "file" in entry_type:
                if isinstance(value_sim, list): continue  
                files_list = []
                print("{0} added to list".format(value_sim))
                # Place filenames into arrays
                for file_provided in value_sim.split(";"):
                    files_list.append([file_provided.strip()])
                sim[key_sim] = files_list
        except: #It is notmal that fails for "ID" and "SOFTWARE"
            continue
print(sims_files_to_array)
print(sims_valid_entries)


# ### Check for multiple files in entries that can only contain one

# In[10]:


sims_valid_file_entries = []
for sim in sims_files_to_array:
    print("ID {0}".format(sim["ID"]), flush=True)
    files_issues = 0
    software_sim = software_dict[sim['SOFTWARE'].upper()]
    for key_sim, value_sim in sim.items():
        try:
            entry_type = software_sim[key_sim]['TYPE']
            if entry_type == "file"  and len(value_sim) > 1:
                print("Multiple values found in {0} and only one allowed (Please correct):\n {1}".format(key_sim,value_sim))
                files_issues += 1
        except: #It is notmal that fails for "ID" and "SOFTWARE"
            continue
    if files_issues:
        print("Sim {0} will be no longer processed".format(sim["ID"]))
    else:
        sims_valid_file_entries.append(sim.copy())
#print(sims_valid_file_entries)


# ### Check if the submitted simulation has rssion has all required files and information

# In[11]:


sims_required_entries = []
for sim in sims_valid_file_entries:
    print("ID {0}".format(sim["ID"]))
    missing_required_keys = 0
    for key, value in software_dict[sim['SOFTWARE'].upper()].items():
        if value["REQUIRED"]:
            try:
                sim[key]
            except:
                print("Entry not found: {0} {1}".format(key, value))
                missing_required_keys += 1
    if missing_required_keys:
        print("{0} missing required entry/ies, please correct.".format(missing_required_keys))
        print("Entry with ID={0} will not be further processed.\n".format(sim["ID"]))
    else:
        print("All required entries present.\n")
        sims_required_entries.append(sim.copy())


# ### Check status links

# In[12]:


# Download link
def download_link(doi, file):
    if "zenodo" in doi.lower():
        zenodo_entry_number = doi.split(".")[2]
        return 'https://zenodo.org/record/' + zenodo_entry_number + '/files/' + file
    else:
        print ("DOI provided: {0}".format(doi))
        print ("Repository not validated. Please upload the data for example to zenodo.org")
        return ""


# In[13]:


#print(sims_required_entries)
sims_working_links = []         
for sim in sims_required_entries:
    print("ID {0}".format(sim["ID"]))
    wrong_links = 0
    software_sim = software_dict[sim['SOFTWARE'].upper()]
    for key_sim, value_sim in sim.items():
        #print("key_sim = {0} => value_sim = {1}".format(key_sim, value_sim))
        try:
            entry_type = software_sim[key_sim]['TYPE']
            extension_type = software_sim[key_sim]['EXTENSION']
            #print("entry_type = {0}".format(entry_type))
            if "file" in entry_type and "txt" not in extension_type:
                for file_provided in value_sim:
                    #print("File={0}".format(file_provided[0]))
                    file_url = download_link(DOI, file_provided[0])
                    if file_url == "":
                        
                        wrong_links += 1
                        continue
                    try:
                        if key_sim == 'INI':
                            continue
                        response = urllib.request.urlopen(file_url)
                        #print("Status of the DOI link: {0}".format(response.msg))
                    except HTTPError as e:
                        print("\nkey={0} => file={1}".format(key_sim, file_provided[0]))
                        print(file_url)
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                        wrong_links += 1
                    except URLError as e:
                        print(key_sim, file_provided[0])
                        print(file_url)
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                        wrong_links += 1
                    else:
                        pass
        except: #It is notmal that fails for "ID" and "SOFTWARE"
            continue
    if wrong_links:
        print("{0} link/s failed, please correct.".format(wrong_links))
        print("Sim={0} will not be further processed.\n".format(sim["ID"]))
    else:
        print("All links work.\n")
        sims_working_links.append(sim.copy())
#print(sims_working_links)


# ## Download files from links

# In[14]:



# Create temporary directory where to download files and analyze them
dir_tmp = os.path.join(dir_wrk, "tmp_6-" + str(randint(100000, 999999)))
if (not os.path.isdir(dir_tmp)): os.mkdir(dir_tmp)

for sim in sims_working_links:
    print("ID {0}".format(sim["ID"]), flush=True)
    software_sim = software_dict[sim['SOFTWARE'].upper()]
    dir_sim = os.path.join(dir_tmp, str(sim["ID"]))
    DOI = sim['DOI']
    if (not os.path.isdir(dir_sim)): os.mkdir(dir_sim)
    for key_sim, value_sim in sim.items():
        print("key_sim = {0} => value_sim = {1}".format(key_sim, value_sim))
        try:
            entry_type = software_sim[key_sim]['TYPE']
            extension_type = software_sim[key_sim]['EXTENSION']
            print("entry_type = {0}".format(entry_type))
            if "file" in entry_type and "txt" not in extension_type:
                for file_provided in tqdm(value_sim, desc = key_sim):
                    file_url = download_link(DOI, file_provided[0])
                    file_name = os.path.join(dir_sim, file_provided[0])
                    if (not os.path.isfile(file_name)):
                        response = urllib.request.urlretrieve(file_url, file_name)
        except: #It is normal that fails for "ID" and "SOFTWARE"
            continue
            


# ## Calculate hash downloaded files

# In[15]:


#dir_tmp = os.path.join(dir_wrk, "tmp/")
sims_hashes = deepcopy(sims_working_links)

for sim in sims_hashes:
    print("ID {0}".format(sim["ID"]), flush=True)
    software_sim = software_dict[sim['SOFTWARE'].upper()]
    dir_sim = os.path.join(dir_tmp, str(sim["ID"]))
    
    #list_containing the sha1 sums for all required files
    sha1_list_requied = []
    
    # Make empty dataframe with the desired columns
    df_files = pd.DataFrame(columns=['NAME','TYPE','REQUIRED','HASH'])
    
    for key_sim, value_sim in sim.items():
        #print("key_sim = {0} => value_sim = {1}".format(key_sim, value_sim))
        try:
            entry_type = software_sim[key_sim]['TYPE']
            #print("entry_type = {0}".format(entry_type))
            if "file" in entry_type:
                files_list = []
                for file_provided in value_sim:
                    file_name = os.path.join(dir_sim, file_provided[0])
                    sha1_hash = hashlib.sha1()
                    with open(file_name,"rb") as f:
                        # Read and update hash string value in blocks of 4K
                        for byte_block in iter(lambda: f.read(4096),b""):
                            sha1_hash.update(byte_block)
                        #print(file_provided, sha256_hash.hexdigest())
                        df_files = df_files.append({
                            "NAME":file_provided[0],
                            "TYPE":key_sim,
                            "REQUIRED": software_dict[sim['SOFTWARE'].upper()][key_sim]['REQUIRED'],
                            "HASH":sha1_hash.hexdigest(),
                        }, ignore_index=True)
                    files_list.append([file_provided[0], sha1_hash.hexdigest()])
                #Find the keys of the required files to calculate the master_hash 
                if software_dict[sim['SOFTWARE'].upper()][key_sim]['REQUIRED'] == True:
                    sha1_list_requied.append(sha1_hash.hexdigest())
                sim[key_sim] = files_list #Problematic
        except: #It is notmal that fails for "ID" and "SOFTWARE"
            continue
    print(df_files)
    print("\n{0}\n".format(sha1_list_requied))      
    # Calculate the hash of a file contaning the hashes of each of the required files
    # This should be always invariant as it will be used unique identifier for a simualtion
    # Note order the hashes of the required files before calculating the hash (That means that the required files cannot change)
print(sims_hashes)


# In[16]:


str(sims_working_links)


# ## Make a dictionary of mapping files and save it in the simulation dictionary

# In[20]:

for sim in sims_working_links :

    mapping = sim['MAPPING'].split(',')
    mapping_dict = {}

    for i in range(0, int(len(mapping)/2)):
        lipid = mapping[2*i]
        print(i)
        print(lipid)
        path = mapping[2*i+1]
        mapping_dict[lipid]=path

    #print(mapping_dict)

    sim['MAPPING_DICT'] = mapping_dict

    print(sim['MAPPING_DICT'])
    print(sim)


# ## Read molecule numbers into dictionary

# In[21]:

for sim in sims_working_links :
    print(sim['MAPPING_DICT'])
    mapping_filesTST = []
    for value in sim['MAPPING_DICT'].values():
        mapping_filesTST.append(value)
    print(mapping_filesTST)

# In[22]:




# In[23]:




# # Save to databank

# In[24]:


#import json
import yaml
os.system("mkdir ../../Data")
os.system("mkdir ../../Data/Simulations")
data_directory = {}
for sim in sims_working_links:
    ID=sim.get('ID')
    # Batuhan: Creating a nested directory structure as discussed on the Issue here https://github.com/NMRLipids/NMRlipidsVIpolarizableFFs/issues/3
    
    head_dir = sims_hashes[ID].get('TPR')[0][1][0:3]
    sub_dir1 = sims_hashes[ID].get('TPR')[0][1][3:6]
    sub_dir2 = sims_hashes[ID].get('TPR')[0][1]
    sub_dir3 = sims_hashes[ID].get('TRJ')[0][1]
    
   # !mkdir {'../TABLEIII/'}
   # !mkdir {'../Data/Simulations'}
   # !mkdir {'../Data/Simulations/TABLEIII'}
    
    os.system("mkdir " +  '../../Data/Simulations/' + str(head_dir))
    os.system("mkdir " + '../../Data/Simulations/' + str(head_dir) + '/' + str(sub_dir1))
    os.system("mkdir " +  '../../Data/Simulations/' + str(head_dir) + '/' + str(sub_dir1) + '/' + str(sub_dir2))
    os.system("mkdir " + '../../Data/Simulations/' + str(head_dir) + '/' + str(sub_dir1) + '/' + str(sub_dir2) + '/' + str(sub_dir3))
    
    DATAdir = '../../Data/Simulations/' + str(head_dir) + '/' + str(sub_dir1) + '/' + str(sub_dir2) + '/' + str(sub_dir3)
    data_directory[str(ID)] = DATAdir
    
    # SAMULI: I am writin now in txt, but using json might be better in the future
   # outfileDICT=open(str(DATAdir)+'/README.md','w')
   # outfileDICT=str(dir_wrk)+'/tmp/'+str(ID)+'/'+ 'README.json'
    
   # with open(outfileDICT, 'w') as f:
   #     json.dump(sim, f)
   

    #!cp {str(dir_wrk)}'/tmp/'{str(ID)}'/README.json' {data_directory.get(str(ID))}  
# dictionary saved in yaml format
    outfileDICT=str(dir_tmp)+ '/' + str(ID)+'/'+ 'README.yaml'
    
    with open(outfileDICT, 'w') as f:
        yaml.dump(sim,f, sort_keys=False)
        
    os.system("cp " +  str(dir_tmp) + '/' + str(ID) + '/README.yaml' + " " + data_directory.get(str(ID)))
    #outfileDICT.write(str(sim))
    #outfileDICT.close()
   


# # Analysis starts here
# 

# In[ ]:


from OrderParameter import *
import warnings
#from corrtimes import *
import subprocess
import mdtraj
import json
#!cp corr_ftios_ind.sh {dir_wrk}
for sim in sims_working_links:
    trj=sim.get('TRJ')
    tpr=sim.get('TPR')
    ID=sim.get('ID')
    software=sim.get('SOFTWARE')
    
    ext=trj[0][0][-3:] # getting the trajectory extension
    
    # BATUHAN: Adding a few lines to convert the trajectory into .xtc using MDTRAJ
    #          We will need users to install MDTRAJ in their system so that we can convert other trajectories into xtc

    if ext != "xtc":
        
        print("converting the trajectory into xtc")
        
        pdb = sim.get('PDB')
        output_traj = str(dir_tmp) + '/' + str(ID) + '/' + 'tmp_converted.xtc'
        input_traj = str(dir_tmp) + '/' + str(ID) + '/' + trj[0][0]
        input_pdb = str(dir_tmp) + '/' + str(ID) + '/' + pdb[0][0]
      
        if os.path.isfile(output_traj): # when we're done with the converted trajectory we can simply remove it
            os.system('rm {output_traj}')
        
        os.system('echo System | mdconvert {input_traj} -o {output_traj} -t {input_pdb} --force # force overwrite')
        
        # SAMULI: this xtcwhole does not necessarily have molecules as whole. Only if {input_traj} has.
        xtcwhole = str(dir_tmp) + '/' + str(ID) + '/' + 'tmp_converted.xtc'
        tpr=input_pdb
        
        print("trajectory conversion is completed")
        
#    else:
#    
#        xtc = str(dir_tmp) + '/' + str(ID) + '/' + str(trj[0][0])  
#        tpr = str(dir_tmp) + '/' + str(ID) + '/' + str(tpr[0][0])
#        xtcwhole=str(dir_tmp) + '/' + str(ID) + '/whole.xtc'
#        os.system('echo System | gmx trjconv -f {xtc} -s {tpr} -o {xtcwhole} -pbc mol ')
   

    
    print("Calculating order parameters")
    

    for key in sim['MAPPING_DICT']:    
        mapping_file = sim['MAPPING_DICT'][key]
        OrdParam=find_OP('../mapping_files/'+mapping_file,str(dir_tmp) + '/' + str(ID) + '/' + str(tpr[0][0]),str(dir_tmp) + '/' + str(ID) + '/' + str(trj[0][0]))

        outfile=open(str(dir_tmp) + '/' + str(ID)+'/' + key + 'OrderParameters.dat','w')
        line1="Atom     Average OP     OP stem"+'\n'
        outfile.write(line1)
    
        data = {}
        outfile2=str(dir_tmp) + '/' + str(ID)+'/' + key + 'OrderParameters.json' 
        
        for i,op in enumerate(OrdParam):
            resops =op.get_op_res
            (op.avg, op.std, op.stem) =op.get_avg_std_stem_OP
            line2=str(op.name)+" "+str(op.avg)+" "+str(op.stem)+'\n'
            outfile.write(line2)
    
            data[str(op.name)]=[]
            data[str(op.name)].append(op.get_avg_std_stem_OP)
        
        with open(outfile2, 'w') as f:
            json.dump(data,f)

        outfile.close()

        os.system("cp " + str(dir_tmp) + '/' + str(ID) +'/'+str(key)+'OrderParameters.dat ' + data_directory.get(str(ID))   )
        os.system("cp " + str(dir_tmp) + '/' + str(ID) +'/'+str(key)+'OrderParameters.json '+ data_directory.get(str(ID))  )
    
    print("Done calculating order parameters.")
