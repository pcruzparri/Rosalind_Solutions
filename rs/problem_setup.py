from os import mkdir, listdir
import nbformat as nbf
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from shutil import rmtree

"""
Sets up a folder and a jupyter notebook for a Rosalind problem.
Usage: python problem_setup.py PROBLEM_ID INPUT_PARSE_MODE
PROBLEM_ID: str, the Rosalind problem ID, e.g. "revc"
INPUT_PARSE_MODE: int, 1 for single row input, 0 for multirow input
"""
parser = ArgumentParser(prog='problem_setup', 
                        formatter_class=RawDescriptionHelpFormatter,
                        description="""
Sets up a folder and a jupyter notebook for working on a Rosalind problem.

The folder will be named after the problem ID, and will contain a notebook with cells for reading data and writing the solution.
The folder will be named PROBLEM_ID.
The notebook will be named PROBLEM_ID.ipynb.
The data file will be read from rosalind_PROBLEM_ID.txt. (This is the default name for doenloaded Rosalind data files.)
The solution will be written to rosalind_PROBLEM_ID_solution.txt.
                        """,
                        epilog="Example usage: python problem_setup.py revc 1 OR python problem_setup.py revc",
                        usage="python %(prog)s.py PROBLEM_ID INPUT_PARSE_MODE[optional]")
parser.add_argument("PROBLEM_ID", type=str, help="The Rosalind problem ID, e.g. 'revc'. Must be lowercase for proper file naming.")
parser.add_argument("INPUT_PARSE_MODE", type=int, nargs='?', choices=[0,1], default=0, help="1 for single row input, 0 for multirow input. Default is 0.")
#parser.add_argument("ROW_READ_HANDLER")
args = parser.parse_args()

probID = args.PROBLEM_ID
input_parse_mode =  args.INPUT_PARSE_MODE# 1 for single row input, 0 for multirow input.

cont_options = {'y':True, 'n':False}
cont = True
if probID in listdir():
    cont = cont_options[input("Are you sure? This will remake folder files and the current ones will be lost.[y/n]").lower()]

if cont:
    if probID not in listdir():
        mkdir(probID)
    notebook = nbf.v4.new_notebook()
    data_cell_code = f"""# Read Data
                    data_path = 'rosalind_{probID}.txt'
                    
                    with open('rosalind_{probID}.txt') as f:
                        \tdata = [i.strip() for i in f.readlines()]{'[0]' if input_parse_mode else ''}
                    data"""
    solution_cell_code = f"""# Solution
                             solution_path = 'rosalind_{probID}_solution.txt'
                             solution = []
                             
                             ################################################
                             ############## SOLUTION GOES HERE ##############
                             ################################################
                             
                             with open(solution_path, 'w') as f:
                             \tf.writelines(solution)"""
    
    data_cell_code = '\n'.join([i.lstrip(' ') for i in data_cell_code.splitlines()])
    solution_cell_code = '\n'.join([i.lstrip(' ') for i in solution_cell_code.splitlines()])
    
    notebook.cells = [nbf.v4.new_code_cell(data_cell_code),
                      nbf.v4.new_code_cell(solution_cell_code)]
    
    with open(f'{probID}/{probID}.ipynb', 'w') as f:
        nbf.write(notebook, f)
else:
    print('Aborted.')