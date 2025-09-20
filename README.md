# Brootforcer is a tool that unlocks the bootloader on android and mainly on Huawei and Honor devices
> This is my first Github repository.

## Dependencies
<ins>It works on devices up to EMUI 11.</ins>\
• Python 3.13 and later\
• Latest Android Debug Bridge(adb)\
• FFMPEG installation at: C:\FFMPEG
[Downloads](#dependencies-downloads)

## Instructions
1. Clone this repository with this command 
```
git clone https://github.com/Anastasis1175/Brootforcer.git
cd Brootforcer
cd app
python3 brootforcer.py
```
2. If it is your first time opening it you will need to input your IMEI. Your screen should look like this image: ![Screenshot of Brootforcer.py opening for the first time.](https://i.postimg.cc/j26Cjyw0/image.png)
3. Find your IMEI by going in your device's calling app and typing this code `*#06#`. Then write one of the IMEI code your device has, into the program
  - Answer if you want your IMEI to be saved in a file for future uses. Like shown in the image below. 
  - ![IMEI Save state](https://i.postimg.cc/y8ccZ3Md/image.png)
  - <ins>DO NOT PRESS ENTER</ins>
4. Plug in your device
5. Enable USB Debugging on your Android device:
  - Go into Setting
  - Go to the about or about phone tab
  - Click on the build number 7 times
  - Then go to the developer settings
  - Enable USB Debugging and OEM Unlocking or OEM Unlock Mode
  - Open your terminal and write adb devices
  - A small menu will popup on your device like this one below
  - ![Adb popup android](https://i.postimg.cc/qqrDndRh/image.png)
  - Click `Allow always from this computer` and press OK
6. Open your terminal and write adb devices. If there is at least 1 device in the list then you are good.![adb devices example output](https://i.postimg.cc/Fs3c8JT4/image.png)
7. Go ahead and close your terminal and go back to the brootforcer app.
8. Now you may press enter. Your device shoud reboot into Fastboot & Rescue mode or Fastboot if your device isn't a honor or a huawei.
![Fasboot example](https://i.postimg.cc/4dRnz8TH/i4b7ipst5cd61.webp)
9. When your device finally gets to fastboot mode you have to press enter.\
![Fasboot enter](https://i.postimg.cc/s2rvW6zQ/image.png)
10. You have to leave your device with your computer until it finds the oem code. Eventually it will restart after a certain amount of tries. This is configurable see [Config File](#config-file).![Attempts](https://i.postimg.cc/pVf5B5k5/image.png)
11. When it finds the oem code it will stop and ask you if you want to save it to a file.Example of how the program ends![OEM_FINAL](https://i.postimg.cc/SQf7xvBP/image.png)

## Config File
This program also comes with a config file called `config.cfg`.\
In this file you can change how many tries the program attempts before it restarts the android device the deafult value is 100.

## Dependencies Downloads
[Latest Python Version](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe)
[ADB for Windows](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)
[ADB for Macos](https://dl.google.com/android/repository/platform-tools-latest-darwin.zip)
[ADB for Linux](https://dl.google.com/android/repository/platform-tools-latest-linux.zip)
# Disclaimer
I am not the owner of the software above and I don't claim that I'm related to the software that I have in the [Dependencies Downloads](#dependencies-downloads).
