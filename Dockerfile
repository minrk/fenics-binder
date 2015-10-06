FROM andrewosh/binder-base

ENV DEBIAN_FRONTEND noninteractive
USER root
RUN apt-get -y -qq update && apt-get -y -qq install rubygems gfortran libglu-dev pandoc > /dev/null
# symlink seems to be needed for weird dolfin issue
RUN ln -s /usr/lib/x86_64-linux-gnu /usr/lib64
USER main

RUN conda create -y -q -n fenics -c minrk python=2.7 anaconda fenics > /dev/null
# RUN conda install -y jupyter
# install ipykernel as second stage, since dependency resolution is wrong if it's all in one command
RUN conda install -y -q -n fenics ipykernel > /dev/null

# make fenics kernel for env
RUN gem install --user a2km
RUN bash -c "source activate fenics && $(ruby -rubygems -e 'puts Gem.user_dir')/bin/a2km env-kernel fenics --user"
# symlink for IPython 3
RUN ln -s /home/main/.local/share/jupyter/kernels/fenics /home/main/.ipython/kernels/fenics

# sanity check dolfin with test.py
ADD test.py /home/main/test.py
RUN bash -c "source activate fenics && python test.py"
