FROM andrewosh/binder-base

USER root
RUN apt-get -y update && apt-get -y install rubygems libopenblas-base ptscotch
USER main

RUN conda create -y -n fenics -c olitheolix python=2.7 anaconda fenics
# RUN conda install -y jupyter
# install ipykernel as second stage, since dependency resolution is wrong if it's all in one command
RUN conda install -y -n fenics ipykernel

RUN gem install -V --user a2km
RUN bash -c "source activate fenics && $(ruby -rubygems -e 'puts Gem.user_dir')/bin/a2km env-kernel fenics --user"
