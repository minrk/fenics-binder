# fenics-binder
This repository consists of software which is used to make FEniCS demos written as notebooks available for direct use.
For information about [Binder](http://mybinder.org/).

## For developers
If you want to use your own FEniCS version to create .ipynb files from the FEniCS demos, replace content of the string 
`fenics_dir` with the path to your FEniCS installation in `rst-to-ipynb-demos.py`
##List of demos
- ** demo_auto-adaptive-poisson **: Working
- ** demo_hyperelasticity **: Plotting of displacement not supported in matplotlib
- ** demo_biharmonic **: Working
- ** demo_maxwell-eigenvalues **: Functions in multiple cells not supported
- ** demo_built-in-meshes **: Working
- ** demo_nonlinear-poisson **: Working
- ** demo_cahn-hilliard **: Working
- ** demo_poisson **: Working
- ** demo_eigenvalue **: Missing PETSC and probably SLEPC
- ** demo_singular-poisson-rst **: Missing PETSC

##Problems/FIXME
- Functions in different cells should be possible/FIXME: Use splitcell
- Math-env using & must be align