import os,sys,re
fenics_dir = '/home/dokken/dev/dolfin-simon/'
demos='demo/documented'

# Copies all python demos from given fenics directory to current directory
os.system( 'find ' + fenics_dir + demos +' -iname \'*.py.rst\' -exec cp \'{}\' `pwd`  \';\'')
# Copies all meshes for demos
os.system( 'find ' + fenics_dir + demos +' -iname \'*.xml.gz\' -exec cp \'{}\' `pwd`  \';\'')

# Add some magic to make matplotlib backendparameter
oldfiles = []
newfiles = []
for fil in os.listdir("."):
    if fil.endswith(".rst"):
        oldfiles.append(fil)
        f=open(fil, "r")
        contents=f.readlines()
        print "Parsing through %s for changing to notebook format" %fil
        i=0
        while i < len(contents):
            if "from dolfin import *" in contents[i]:
                whitespaces=re.split(r'(\s+)', contents[i])
                contents.insert(i+1,
                                 "\nSpecifying matplotlib as backend::\n\n")
                contents.insert(i+2, whitespaces[1] + "%matplotlib inline\n")
                contents.insert(i+3, whitespaces[1] +
                                "import matplotlib.pyplot as plt\n")
                contents.insert(i+4, whitespaces[1] +
                                "parameters[\"plotting_backend\"]=\"matplotlib\"")
                i+=3
            
            elif ("Mesh(\".." or "Mesh(\'..") in contents[i]:
                contents[i]=''.join(contents[i].split('../'))

            elif ("plot(" in contents[i]):
                whitespaces=re.split(r'(\s+)', contents[i])
                contents.insert(i, whitespaces[1]+"plt.figure()\n")
                i+=1
            i+=1
        f.close()
        f = open(fil, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()


        
# Creating .ipynb filenames and converting from rst-files to ipynb
for i in range(len(oldfiles)):
    tmp = oldfiles[i]
    newfiles.append(tmp[:-7]+'.ipynb')
for i in range(len(oldfiles)):
    os.system('python convert.py %s %s' %(oldfiles[i],newfiles[i]))

# Post-processing ipynb files for functions
# for fil in newfiles:
#     if not fil=='demo_maxwell-eigenvalues.ipynb':
#         continue
#     ipynb = open(fil,'r')
#     contents=ipynb.readlines()

#     # Counter running through file
#     i=0
#     # Boolean for start of definition
#     cell_def=False
#     end_def = 0
#     # Dictionary for what should be added
#     subblock = {}
    
#     print fil
#     while (i<len(contents)):
#         if "\"cell_type\": \"code\"" in contents[i]:
#             j=i
#             while "\"source\": [" not in contents[j]: j+=1
#             start=j
#             while contents[j].split()[0]!="]": j+=1
#             end=j
#             # Check if this is start of definition
#             if any(["def" in s for s in contents[start:end]]):
#                 cell_def=True
#                 end_def=j-1
#             if "#\\n" in contents[start+1]:
#                 subblock[end_def]=[start+2,end]
#                 end_def=end_def+end-start-2

#         i+=1

#     print subblock
#     for key in sorted(subblock.keys()):
#         print key
#         j=0
#         tmp=contents[subblock[key][0]:subblock[key][1]+1]
#         del contents[subblock[key][0]:subblock[key][1]+1]
#         for i in range(len(tmp)):
#             place = int(key)+j+1
#             if len(tmp[i])==5:
#                 contents.insert(place, "")
#             else:
#                 contents.insert(place, tmp[i])
#             j+=1

#     ipynb.close()
    # ipynb = open(fil, "w")
    # contents = "".join(contents)
    # ipynb.write(contents)
    # ipynb.close()

# Converting all py.rst-files to ipynb-files
# os.system('find . -iname \'*.py.rst\' -exec python convert.py \'{}\' \'{}\'.ipynb \';\'')
