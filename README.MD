YouTube search results downloader
=================================

#### Install ####
`git clone https://github.com/codebyzen/YoutubeSearchResultsDownloader.git`

Install tampermonkey for chrome or firefox

Add new UserScript [a relative link](userscript.js)

Install youtube-dl `sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o ./bin/youtube-dl`

Install Aria2 `sudo apt-get install aria2`

Copy `aria2c` to `./bin` Example: `cp /usr/local/aria2/bin/aria2c ./bin`


#### Usage #####
Goto youtube.com, search something, scroll down to view all results

Click to tampermonkey icon on top

Click Run This Now

Download list.txt to this directory

Run `./dl.py -f list.txt`

#### Info ####
Video will be downloaded to folders by years.

Example `My first homevideo!!!` uploaded to YouTube in 2017. It will be downloaded to `./2019/my-first-homevideo.mp4`