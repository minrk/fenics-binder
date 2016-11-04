"""splitcell extension

Record partial cells and execute them later.

Allows interleaving markdown cells in class and function declarations.
"""

_recorded_cells = []
def record_split_cell(line, cell):
    """Record the current cell as part of a split cell
    
    so you can have markdown cells in the middle of a code block
    """
    _recorded_cells.append(cell)

def run_split_cell(line):
    """Evaluate the split cell recorded with %split_cell
    
    Add -v to echo the code to be executed.
    """
    cell = '\n'.join(_recorded_cells)
    # reset record
    _recorded_cells[:] = []
    if '-v' in line:
        print(cell)
    get_ipython().run_cell(cell)

def load_ipython_extension(ip):
    ip = get_ipython()
    ip.register_magic_function(record_split_cell, 'cell', magic_name='split_cell')
    ip.register_magic_function(run_split_cell)
