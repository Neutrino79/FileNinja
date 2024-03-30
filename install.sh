#!/bin/bash

# install swig
echo "[+] Installing swing...\n\n"
sleep 2
sudo apt install -y swig

if [[ $? -eq 0 ]];
then
	sleep 1
	echo "\n\n[+] Swig installed successfully...\n"
	sleep 1 && clear
else
	echo "\n\n[!] Error in instaling swig! Please retry!"
	exit 1
fi


# install dependacies
printf "[+] Installing dependacies...\n\n"
sleep 2
pip3 install -r requirements.txt

if [[$? == 0]];
then
	sleep 1
	clear
	printf "\n\n[✓] Installed sucessfully!"
else
	printf "\n\n[!] Something went wrong!"
	printf "\n[!] Please try again!"
fi
