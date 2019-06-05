#!/usr/bin/env bash
RED='\033[1;31m'
ORANGE='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

assistant() {
    printf "Prepare ${ORANGE}Yowsapp Installer Assistant${NC}\n"
    printf "${NC}--------------------------\n"
    printf "${NC}Select the option that best suits your needs: \n"
    printf "${CYAN}1. ${NC}Install Yowsapp Framework: \n"
    printf "${CYAN}2. ${NC}Full Update Yowsapp Framework: \n"
    printf "${CYAN}3. ${NC}Register new Whatsapp Phone on Yowsapp Framework: \n"
    read -p "${CYAN}Insert your option: " installOption
    if [ $installOption == 1 ]
    then
        fullYowsappInstall
    fi
    if [ $installOption == 2 ]
    then
        updateYowsapp
    fi
    if [ $installOption == 3 ]
    then
        loginWhatsapp
    fi
    wait
}

prepare_enviroment() {
	printf "Prepare ${ORANGE}Linux Ubuntu Enviroment${NC}\n"
    printf "${NC}--------------------------\n"
	sudo apt update
	wait
	sudo apt install python -y && sudo apt install python-pip -y && sudo apt install python3 -y && sudo apt install python3-pip -y
	wait
	sudo apt-get install build-essential libssl-dev libffi-dev python-dev -y
	wait
	sudo pip install yowsup && sudo pip3 install yowsup && pip install pycrypto && pip install blinker && pip3 install pycrypto && pip3 install blinker && pip install cryptography==2.6.1 && pip3 install cryptography==2.6.1 && pip install flask && sudo pip3 install flask
	wait	
}

install_requirements() {
    module_requirements="$1"

    #printf "pip3 -qqq install -r $module_requirements"
    pip3 -qqq install -r $module_requirements

    return_code=$?
    if [ $return_code != 0 ]; then
        printf "${RED}Error:[%d]. Try running it with root privilages\n" $return_code
        exit $return_code
    fi
}

install_forked_yowsup() {
    printf "Installing ${ORANGE}yowsup libraries${NC}\n"
    printf "${NC}--------------------------\n"
	cd libs/
	sudo rm -R yowsup
	wait
	sudo rm -R yowsup.egg-info
	wait
	sudo rm -R build
	wait
	git clone https://github.com/tgalal/yowsup.git
	wait
	sudo python yowsup/setup.py install && sudo python3 yowsup/setup.py install
    cd python-axolotl
    python3 setup.py -qqq install
    wait
    printf "${NC}--------------------------\n"
    # Return to root
    cd ../../
}

whatsapp_login() {
    printf "Sign in on ${CYAN}WhatsApp${NC}\n"
    printf "${NC}Set your whatsapp information here. If the validation if success, yo receive a sms or call with WhatsApp code: \n"
    printf "${NC}--------------------------\n"
    read -p "Enter your country code: "  countryCode
    read -p "Enter your mobile number without country code and + and 00: "  mobileNumber
    read -p "Enter your MCC code <Lis of all MCC codes: https://www.mcc-mnc.com/>: " mccCode
    read -p "Enter your MNC code <Lis of all MCC codes: https://www.mcc-mnc.com/>: " mncCode
    read -p "Insert option number for code validation: 1. SMS - 2. VOICE: " validationOption
    if [ $validationOption == 1 ]
    then
        sudo yowsup-cli registration --requestcode sms --config-phone $countryCode$mobileNumber --config-cc $countryCode --config-mcc $mccCode --config-mnc $mncCode
    fi
    if [ $validationOption == 2 ]
    then
        sudo yowsup-cli registration --requestcode voice --config-phone $countryCode$mobileNumber --config-cc $countryCode --config-mcc $mccCode --config-mnc $mncCode
    fi
    wait
    printf "WhatsApp Code Validation\n"
    printf "${NC}Insert the code: \n"
    read -p "Enter a 6 numbers code: "  smsCode
    sudo yowsup-cli registration --register $smsCode --config-phone $countryCode$mobileNumber
    wait
}

install_modules() {
    printf "Configuring modules\n"
    printf "${NC}--------------------------\n"
    cd modules
    for D in *; do
        if [ -d "${D}" ] && [ "${D}" != "__pycache__" ]; then
            if [ -f ${D}/requirements.txt ]; then
                printf "[${CYAN}${D}${NC}] Installing dependencies...\n"
                module_requirements="${D}/requirements.txt"
                install_requirements "$module_requirements"
            else
                printf "[${CYAN}${D}${NC}] All good...\n"
            fi
        fi
    done
    wait

    printf "${NC}--------------------------\n"

    # Return to root
    cd ../
}

install_app_dependencies() {
    printf "Configuring framework\n"
    printf "${NC}--------------------------\n"
    printf "[${CYAN}mac${NC}] Installing dependencies...\n"

    app_requirements="app/requirements.txt"
    install_requirements "$app_requirements"
    wait
}

fullYowsappInstall () {
    prepare_enviroment

    install_forked_yowsup

    install_modules

    install_app_dependencies

    whatsapp_login
}

updateYowsapp () {
    install_forked_yowsup

    install_modules

    install_app_dependencies
}

loginWhatsapp () {
    whatsapp_login
}


assistant
