#!/usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib3
import os, sys
from termcolor import colored as color

http = urllib3.PoolManager()
LIST = []
TITLE = []
ERROR = []

def info(text): return color(text,'magenta')
def error(text): return color(text,'red')
def critic(text): return color(text,'blue','on_red',attrs=['bold'])
def warning(text): return color(text,'yellow')

def norm(b):
  #b = str(b)
  while(b.find('\n') != -1):b = b.replace('\n','')
  while(b.find('\r') != -1):b = b.replace('\r','')
  while(b.find('  ') != -1):b = b.replace('  ',' ')
  while(b.find('&lt;') != -1):b = b.replace('&lt;','<')
  while(b.find('&gt;') != -1):b = b.replace('&gt;','>')
  while(b.find('&lte;') != -1):b = b.replace('&lte;','<=')
  while(b.find('&gte;') != -1):b = b.replace('&gte;','>=')
  while(b.find('/r/') != -1):b = b.replace('/r/','R-')
  while(b.find('/') != -1):b = b.replace('/','')
  while(b[0] == ' '):b = b[1:]
  while(b[-1] == ' '):b = b[0:len(b)-1]
  return b

def Ext(content_type):
    "Return extension for specified content type"
    return {
        'image/bmp':'bmp',
        'image/cis-cod':'cod',
        'image/gif':'gif',
        'image/ief':'ief',
        'image/jpeg':'jpg',
        'image/pipeg':'jfif',
        'image/png':'png',
        'image/svg+xml':'svg',
        'image/tiff':'tif',
        'image/x-cmu-raster':'ras',
        'image/x-cmx':'cmx',
        'image/x-icon':'ico',
        'image/x-portable-anymap':'pnm',
        'image/x-portable-bitmap':'pbm',
        'image/x-portable-graymap':'pgm',
        'image/x-portable-pixmap':'ppm',
        'image/x-rgb':'rgb',
        'image/x-xbitmap':'xbm',
        'image/x-xpixmap':'xpm',
        'image/x-xwindowdump':'xwd'
        }.get(content_type, 'jpg')

def makeSaveDir(save_dir):
    "Creates direectory. Returns a valid directory name."
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    os.chdir(save_dir)
    return ''

def loadList(subreddit):
    global LIST
    global TITLE
    global ERROR
    LIST , TITLE = [] , []
    try:
        f = open('.list.txt','r')
        for line in f:
            LIST.append(line.split(' ')[0])
            TITLE.append(line[len(LIST[-1])+5:])
        f.close()
    except:
        ERROR.append([subreddit,'List file not found','file .list.txt does not exists!'])
        print critic('List not found') + ' , creating new one!'
        #exit()
        return

def Exists(file_name):
    try:
        with open(file_name+'.jpg') as f: f.close()
        #print '> Dupplicate Found! '+file_name+'.jpg'
        return file_name+'.jpg'
    except:
        try:
            with open(file_name+'.png') as f: f.close()
            #print '> Dupplicate Found! '+file_name+'.png'
            return file_name+'.png'
        except:
            try:
                with open(file_name+'.gif') as f: f.close()
                #print '> Dupplicate Found! '+file_name+'.gif'
                return file_name+'.gif'
            except:
                return ''    

def download(uri,file_name,subreddit):
    global LIST
    global TITLE
    ret = (uri.split('/')[-1][:-4]+' --> '+file_name+'\n')
    file_name = uri.split('/')[-1][:-4] + ' - ' + file_name
    if len(file_name.encode('utf-8')) > 251:
        #ret += ' -- File name too long error happened! -- save to : '
        i = 251
        while len(file_name[0:i].encode('utf-8')) > 251: i -= 1
        file_name = file_name[0:i]
        #ret += file_name + '\n'
    f = Exists(file_name)
    if f != '':
        #print critic('Duplicate @'+uri.split('/')[-1][:-4])
        ERROR.append([subreddit,'Image already exists','file '+f+' already exists!'])
        return ret
    LIST.append(uri.split('/')[-1][:-4])
    TITLE.append(ret[10:])
    #print subreddit+' > Downloading '+info(uri)
    try:
        r = http.request('GET',uri)
    except:
        print subreddit+' >>  '+critic(' Error ')+error(': Cannot Download File')
        return
    file_name = file_name+'.'+Ext(r.headers['content-type'])
    print subreddit+' >>   '+'Save to '+info(file_name)
    if r.status == 200:
        with open(file_name, "wb") as image_file:
            image_file.write(r.data)
            image_file.close()
    return ret
    
def downloadPostsFrom(subreddit,mode='new',start=0,end=0):
    global LIST
    if mode == 'new':
        makeSaveDir(subreddit)
    else:
        makeSaveDir(subreddit+'/'+mode.replace('/','-'))
    loadList(subreddit)
    lst = open('.list.txt','a+')
    print 'Download images from page ',start,' to ',end,' of ',mode,' images of www.imgur.com/r/'+subreddit+' into '+subreddit+' folder'
    i = end
    while i >= 0:
        url = "http://www.imgur.com/r/"+subreddit+"/"+mode+"/page/"+str(i)+"?scrolled"
        print 'Geting Page : '+info(url)
        f = http.request('GET',url).data.decode("utf-8")
        soup = BeautifulSoup(f)
        images = soup.find('div',{'class':'posts'}).findAll('img')
        for img in reversed(images):
            uri = img['src'].replace('b.','.')
            if uri.split('/')[-1][:-4] in LIST:
                #print 'Duplicate :',uri.split('/')[-1][:-4]
                continue
            file_name = norm(img['title'][0:img['title'].find('<p>')])
            lst.write(download(uri,file_name,subreddit).encode('utf-8'))
            lst.close()
            lst = open('.list.txt','a+')
        i -= 1
    lst.close()

def main():
    "Use app as console program."
    if len(sys.argv) == 2:
        downloadPostsFrom(subreddit=sys.argv[1])
    elif len(sys.argv) == 3:
        downloadPostsFrom(subreddit=sys.argv[1],mode=sys.argv[2])
    elif len(sys.argv) == 4:
        downloadPostsFrom(subreddit=sys.argv[1],start=int(sys.argv[2]),end=int(sys.argv[3]))
    elif len(sys.argv) == 5:
        downloadPostsFrom(subreddit=sys.argv[1],mode=sys.argv[2],start=int(sys.argv[3]),end=int(sys.argv[4]))
    else:
        print "Pleas specify subreddit!"

if __name__ == '__main__':
    main()
