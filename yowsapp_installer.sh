#!/usr/bin/env bash
RED='\033[1;31m'
ORANGE='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

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
    cd libs/python-axolotl
    python3 setup.py -qqq install
    wait
    cd ../yowsup
    python3 setup.py install
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

# Steep 1
install_forked_yowsup

# Steep 2
install_modules

# Steep 3
install_app_dependencies

# Steep 4
whatsapp_login