#
# Based on https://github.com/haexhub/huaweiBootloaderHack
# Based on https://gist.github.com/alex-spataru/b187bdc3d987a0fcb1cae4e9b17c0e9e
#
# Usage:
#     python android-bootloader-unlock.py <YOUR_IMEI_CODE>
#
# Please enable USB debugging on your phone before using this
# tool, hope it helps you :)
#

import sys
import json
import math
import subprocess
import os
import configparser
config = configparser.ConfigParser()
config.read('config.cfg')
times_before_restart_str = config['main']['times_before_restart']
times_before_restart = int(times_before_restart_str)

def get_imei_from_file_or_user(filename='imei_list.json'):
    """
    Attempts to read a list of IMEI numbers from a JSON file.
    If the file doesn't exist, it asks the user to enter and save one.
    Returns the selected IMEI number as an integer.
    """
    imei_list = None
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            
            if isinstance(data, list):
                imei_list = [int(imei) for imei in data]
            else:
                print(f"The content of '{filename}' is not a list. Will ask for user input.")
        except (json.JSONDecodeError, ValueError):
            print(f"Could not read valid JSON from '{filename}'")

    if not imei_list:
        print(f"File '{filename}' not found or is invalid")
        
        while True:
            try:
                user_imei_str = input("Please input your IMEI code: ")
                user_imei = int(user_imei_str)
                break
            except ValueError:
                print(f"'{user_imei_str}' is invalid, please enter a valid number.")
        
        save_choice = input("Do you want to save your IMEI to a file? [Yes or No] ")
        if save_choice.lower() in ["y", "yes"]:
            try:
                with open(filename, 'w') as file:
                    json.dump([str(user_imei)], file, indent=4)
                print(f"IMEI = '{user_imei}' saved to '{filename}'.")
            except IOError:
                print(f"Could not save '{user_imei}' to '{filename}'.")
        
        return user_imei
    
    else:
        print("Found IMEI numbers in the file:")
        for i, imei_num in enumerate(imei_list):
            print(f"[{i}] {imei_num}")
        
        while True:
            try:
                choice_str = input("Please enter the number corresponding to the IMEI you want to select: ")
                choice = int(choice_str)
                if 0 <= choice < len(imei_list):
                    return imei_list[choice]
                else:
                    print(f"Please enter a number from the list [0-{len(imei_list)-1}].")
            except ValueError:
                print(f"'{choice_str}' is not a number. Please enter a number.")
                
def get_attempts():
    '''
    Reads the list of failed passwords and returns them as a set.
    In case the attempts.json file does not exist (or is invalid),
    this function will return an empty set.
    '''
    try:
        with open('attempts.json', 'r') as file:
            attempts = json.load(file)
            if type(attempts) == list:
                return set(attempts)
            else:
                return set([])
    except:
        return set([])

def save_attempts(attempts = []):
    '''
    Writes the current failed password attempts to an external file,
    which is later used to continue trying even more passwords...
    '''
    with open('attempts.json', 'w') as file:
        json.dump(attempts, file)

def string_to_int_array(n):
    '''
    Converts an array of characters to an array of integers
    '''
    return [int(d) for d in str(n)]

def luhn_checksum(imei):
    '''
    Obtains the checksum of the IMEI string using Luhn's algorithm
    '''
    digits = string_to_int_array(imei)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for digit in even_digits:
        checksum += sum(string_to_int_array(digit * 2))
    return checksum % 10

def unlock_bootloader(imei, checksum, failed_attempts = set([])):
    '''
    Generates new OEM codes/passwords and tries running "fastboot oem unlock"
    until it succeeds. 

    @note The function automatically reboots the Android device every 4
          failed attempts in order to avoid a lock-up.
    '''

    
    unlocked = False
    attempt_count = 0
    oem_code = 1000000000000000
    while not unlocked:
        attempt_count += 1
        while oem_code in failed_attempts:
            oem_code += int(checksum + math.sqrt(imei) * 1024)
        print(f'Shot {len(failed_attempts) + 1} with OEM code/password {oem_code}...')
        answer = subprocess.run(
            ['fastboot', 'oem', 'unlock', str(oem_code)],
            stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL
        )
        if answer.returncode == 0:
            unlocked = True
            return oem_code
        else:
            failed_attempts.add(oem_code)
        if attempt_count >={times_before_restart} :
            attempt_count = 0
            save_attempts(list(failed_attempts))
            print('Restarting device...\n')
            subprocess.run(
                ['fastboot', 'reboot', 'bootloader'],
                stdout = subprocess.DEVNULL,
                stderr = subprocess.DEVNULL
            )
        oem_code += int(checksum + math.sqrt(imei) * 1024)

if __name__ == '__main__':
    imei = get_imei_from_file_or_user()
    checksum = luhn_checksum(imei)
    print(f'Using IMEI: {imei}')
    print(f'IMEI checksum (Luhn): {checksum}')
    print('Rebooting device...')
    subprocess.run(
        ['adb', 'reboot', 'bootloader'],
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL
    )
    input('Press any key when your device is in fastboot mode...\n')
    failed_attempts = get_attempts()
    oem_code = unlock_bootloader(imei, checksum, failed_attempts)
    subprocess.run(['fastboot', 'getvar', 'unlocked'])
    subprocess.run(['fastboot', 'reboot'])
    print('\n\n')
    print(f'Device unlocked! OEM code/password: {oem_code}')
    sys.exit()