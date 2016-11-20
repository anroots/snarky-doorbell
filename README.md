sudo apt-get install python-dev libboost-python-dev python-pip
sudo pip install pi_switch


./bootstrap.sh --with-libraries=python --with-python=python3.2
sudo ./b2 install