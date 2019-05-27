# Billboard to Spotify
This project was created to be used with a mobile application in conjunction with Spotify.

## Steps to Use:
1. Install dependencies
2. Run the Flask Server
3. Interface with the server with the client application or web browser.

## Note for PyInstaller
There is an issue with PyInstaller and dateparser (specifically _strptime)  
Even when using a hook or hidden import with PyInstaller, it doesn't seem to work properly.  
So in the dataparser/utils/strptime.py file, I changed the following lines:  

From:
```
__strptime = patch_strptime()
```
  
To:
```
import _strptime
__strptime = _strptime._strptime_time
```
