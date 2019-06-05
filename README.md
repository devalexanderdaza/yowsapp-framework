# Yowsapp Framework 



###### [DONATE HERE](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=55HW9CL6HLWGS&source=url)

Yowsapp is a whatsapp bot/framework I made as a weekend project. The project itself has all you need to make your own custom bot easily.

Yowsapp has built-in human behavior so you only have to worry about the functions you make. Every module works completely separated from the core, this means that you can erease every module and mac will keep working

_**NOTE: I highly recommend making use of the library in a completely clean linux environment. My recommendation would be to use a Digital Ocean VPS here: https://m.do.co/c/ec1e4f467265 **_

_This needs **Python >= 2.7 and <=3.7**_

# Setup:
1. Clone this repository (with submodules since it uses tgalal's yowsup3 library)
```sh
> git clone https://github.com/devalexanderdaza/yowsapp-framework.git
```
2. Run yowsapp_installer.sh (Most likely on sudo since its going to install some libraries)
```sh
> sudo ./yowsapp_installer.sh

OR IF YOU ARE MAC USER
> sudo ./yowsapp_installer_osx.sh
```
3. Register your phone and get a password with like this:
`The process of registering the telephone line will be done within the execution of the file yowsapp_installer.sh`
4. Save the login JSON response, rename **config_example.py** to **config.py**
```sh
> mv config_example.py config.py
```
5. Open **config.py** and add set your credentials

6. Ready to go! (Now you can add your own whatsapp modules)
```sh
> ./start.sh
```

# Quickstart
Create your own module inside [`modules/`](https://github.com/danielcardeenas/whatsapp-framework/tree/master/modules) directory
```python
# modules/hi_module.py

from app.mac import mac, signals

@signals.message_received.connect
def handle(message):
    if message.text == "hi":
        mac.send_message("Hello", message.conversation)
        
        # Can also send media
        #mac.send_image("path/to/image.png", message.conversation)
        #mac.send_video("path/to/video.mp4", message.conversation)
```
Now you should only add it into [`modules/__init__.py`](https://github.com/danielcardeenas/whatsapp-framework/blob/master/modules/__init__.py) to enable the module
```python
# modules/__init__.py
...
from modules import hi_module
...
```
And that's it! You are ready to go.

###### If your module needs libraries from pip you should add them into a `requirements.txt` and run `sudo ./setup.sh` to download the dependencies

###### _You can take [`hihelp module`](https://github.com/danielcardeenas/whatsapp-framework/blob/master/modules/hihelp/hihelp.py) as an example._


# Updates
The project is not submoduling yowsup now due to a lot of the modifications made are focused for this project only and to make things simpler.
- [x] Notification on messages receipt (received and blue check marks)
- [x] Get contacts statuses
- [x] Get contacts profile picture (also from groups)
- [x] Set profile picture (also from groups)
- [x] Send videos (needs ffmpeg installed)
- [x] Add support for @tag messages
- [x] Add support for reply messages
- [x] Add support for receiving images
- [x] Add support for big receiving big files (downloading and decryption done in chunks)
- [x] Add support for sending images
- [ ] Add support for encrypting images in chunks (_TODO_)
- [ ] Add pickle support to remember the messages when mac its turned off(_TODO_)

# Example screenshots:
![](https://i.imgur.com/ZRlk5Uj.png)
![](https://i.imgur.com/JmPbPXB.png)
![](https://i.imgur.com/L4ebZql.png)
<img src="https://i.imgur.com/pLiwAm5.png" width="253px" height="450px">
<img src="https://i.imgur.com/poLpmAR.png" width="253px" height="450px">
<img src="https://i.imgur.com/CRNKfHj.png" width="253px" height="450px">
