FROM andrewosh/binder-base

USER root
RUN apt-get -y update && apt-get -y install rubygems
RUN apt-get -y install gfortran libglu-dev pandoc
# symlink seems to be needed for weird dolfin issue
RUN ln -s /usr/lib/x86_64-linux-gnu /usr/lib64
USER main

RUN conda create -y -n fenics -c minrk python=2.7 anaconda fenics
# RUN conda install -y jupyter
# install ipykernel as second stage, since dependency resolution is wrong if it's all in one command
RUN conda install -y -n fenics ipykernel

# make fenics kernel for env
RUN gem install -V --user a2km
RUN bash -c "source activate fenics && $(ruby -rubygems -e 'puts Gem.user_dir')/bin/a2km env-kernel fenics --user"
# symlink for IPython 3
RUN ln -s /home/main/.local/jupyter/kernels/fenics /home/main/.ipython/kernels/fenics

# sanity check dolfin with test.py
ADD test.py /home/main/test.py
RUN bash -c "source activate fenics && python test.py"

