echo 'setting up directories'
mkdir ~/apps

echo 'installing essentials'
sudo apt install -y terminator
sudo apt install -y vim
sudo apt-get install usbutils



echo 'installing mobfs'
cd ~/apps
git clone --depth 10 https://github.com/MobSF/Mobile-Security-Framework-MobSF.git
mv Mobile-Security-Framework-MobSF/ mobsf
cd mobsf/
./setup.sh

echo 'installing libimobiledevice'
sudo apt-get install usbmuxd libimobiledevice6 libimobiledevice-utils


echo 'installing frida-tools'
pip install frida-tools


