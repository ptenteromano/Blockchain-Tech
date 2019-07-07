# This file should do everything necessary to set up the app

# Change file permissions
chmod u+x ./install.sh
chmod u+x ./server.sh
chmod u+x ./App/Encryption/*

# Python Virtual environment
pip3 install virtualenv

if [ ! -d "venv" ]; then
  virtualenv -p python3 venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install the needed dependencies
pip3 install -r ./requirements.txt
