This is a simple console application written in python to download images from imgur.com image hosting site

Code download iamges to subfolder with name of sort mode ( if sort mode is new use no subdirectory ) in channel folder from run directory.
Save list of downloaded images to .list.txt.
Save files with this format for name : "(ending hash code)  -  (image title)"

Run arguments :
python imgur.py channel [sort=new] [startPage=0 endPage=0]

channel is subreddit section of imgur ( like this eyes make imgur.com/r/eyes )
sort is sort mode of that pages ( new , top/all , top/month , top/week , top/day )
startPage and endPage is starting and ending page of imgur channel

Code is using imgur RestFull Api.

This code is depends of python 2.7 ( work with 2.6 )
