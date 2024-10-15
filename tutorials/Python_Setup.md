# Assuming python 2.

sudo apt install pip
sudo apt install virtualenv

sudo pip install pip -upgrade

cd ~/projects

virtualenv venv

# activate venv at startup by adding this to bashrc
# or just activate once for now
source ~/projects/venv/bin/activate


#### Get started with the packages we need
pip install ipython
pip install ipdb
pip install numpy
pip install matplotlib==1.5.3
## the latest (2.0) requires subprocess32 which has no wheel
## it needs to be compiled... so just use the older version
## using python3 would probably solve this issue

pip install opencv-python


### For running check_verts
pip install pypi
sudo apt install python-tk
