import os,sys,re
fenics_dir = '/home/dokken/dev/dolfin-simon/'
demos='demo/documented'

def insert_runcell(contents,old_end):
    leading_spaces = (len(contents[old_end+1])
                      - len(contents[old_end+1].lstrip()))
    contents.insert(old_end+1,  " "*leading_spaces+"{\n")
    contents.insert(old_end+2,  " "*(leading_spaces+1)+\
                    "\"cell_type\": \"code\",\n")
    contents.insert(old_end+3,  " "*(leading_spaces+1)+\
                    "\"execution_count\": null,\n")
    contents.insert(old_end+4,  " "*(leading_spaces+1)+\
                    "\"metadata\": {\n")
    contents.insert(old_end+5,  " "*(leading_spaces+2)+\
                    "\"collapsed\": true\n")
    contents.insert(old_end+6,  " "*(leading_spaces+1)+\
                    "},\n")
    contents.insert(old_end+7,  " "*(leading_spaces+1)+\
                    "\"outputs\": [],\n")
    contents.insert(old_end+8,  " "*(leading_spaces+1)+\
                    "\"source\": [\n")
    contents.insert(old_end+9,  " "*(leading_spaces+2)+\
                    "\"%run_split_cell\"\n")
    contents.insert(old_end+10,  " "*(leading_spaces+1)+\
                    "]\n")
    contents.insert(old_end+11,  " "*(leading_spaces)+\
                    "},\n")
    return contents

# Copies all python demos from given fenics directory to current directory
os.system( 'find ' + fenics_dir + demos +' -iname \'*.py.rst\' -exec cp \'{}\' `pwd`  \';\'')
# Copies all meshes for demos
os.system( 'find ' + fenics_dir + demos +' -iname \'*.xml.gz\' -exec cp \'{}\' `pwd`  \';\'')

# Add some magic to make matplotlib backendparameter
oldfiles = []
newfiles = []
files = []
for fil in os.listdir("."):
    if fil.endswith(".rst"):
        oldfiles.append(fil)

for fil in oldfiles:
    # Open current file and read content
    f=open(fil, "r")
    contents=f.readlines()
    f.close()

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
                            "parameters[\"plotting_backend\"]=\"matplotlib\"\n")
            i+=3

        elif ("Mesh(\".." or "Mesh(\'..") in contents[i]:
            contents[i]=''.join(contents[i].split('../'))

        elif ("plot(" in contents[i]):
            whitespaces=re.split(r'(\s+)', contents[i])
            contents.insert(i, whitespaces[1]+"plt.figure()\n")
            i+=1
        i+=1

    # Replace information if file
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

#Post-processing ipynb files for functions
for fil in newfiles:

    ipynb = open(fil,'r')
    contents=ipynb.readlines()
    ipynb.close()
    print fil
    old_start = 0 # Start of last code-cell,at "source:"
    old_end = 0 # End of last code-cell, at ]
    first = 0 # Start of first code-cell, at "source:"
    first_time=True
    first_header=True
    start_func = 0 # First cell with function, at "source:"
    cell=False # True: Last cell has def, False: Last cell is not dep
    i = 0
    while i<len(contents):
        # Find first dolfin code cell
        if ("\"cell_type\": \"code\"" in contents[i] and first==0):
            while "from dolfin import *" not in contents[i]: i+=1
            first =i-1
        elif ("\"cell_type\": \"code\"" in contents[i]):
            while ("source" not in contents[i] and
                   "#\\n" not in contents[i+1]): i+=1
            # Check if this cell depends on last cell
            if "source" in contents[i] and "#\\n" in contents[i+1]:
                old_start=i
                cell = True
            # Check if this cell contains definition
            elif "source" in contents[i]:
                while i<len(contents) and "def " not in contents[i]: i+=1
                # If reached end of file
                if i == len(contents):
                    if not first_header:
                        contents = insert_runcell(contents, old_end+1)
                    break
                start_func = i-1
                first_time=True
            # Finding end of last cell
            while (len(contents[i].strip())!=1 and
                   ("]" not in contents[i].strip()[0])): i+=1
            # Found cell which dependencies to older cell
            if cell and old_start!=0:
                if first_time and not first_header:
                    contents = insert_runcell(contents,old_end+1)
                    old_start+=11
                    start_func+=10
                    i+=10
                if first_header:
                    leading_spaces = (len(contents[first+1])
                                      - len(contents[first+1].lstrip()))
                    contents.insert(first+1, " "*leading_spaces + \
                                    "\"%load_ext splitcell\\n\",\n")
                    if first+1<old_start: old_start+=1
                    first_header = False
                # Entering splitcell at top of function
                if first_time:
                    contents.insert(start_func+2, "\"%%split_cell\\n\",\n")
                    if start_func+2<old_start: old_start+=1
                    first_time = False

                old_end = i
                contents[old_start+1] = "\"%%split_cell\\n\",\n"

            old_start = 0

        i+=1

    # Use another way of doing this, see what min has pushed
    table=False
    for i in range(len(contents)):
        if "attributes" in contents[i]:
            contents[i-3]="\"cell_type\": \"markdown\",\n"
            # table=True
        # elif table and "\"source\": [" in contents[i]:
        #     leading_spaces = (len(contents[first+2])
        #                       - len(contents[first+2].lstrip()))
        #     contents.insert(i+1," "*leading_spaces+"\"\"\"\n")
        # elif (table and len(contents[i].strip())==1 and
        #       "]" in contents[i].strip()[0]):
        #     contents.insert(i, " "*leading_spaces+"\"\"\"\n")
        #     table=False

    ipynb = open(fil, "w")
    contents = "".join(contents)
    ipynb.write(contents)
    ipynb.close()
