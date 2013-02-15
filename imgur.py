#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import os, sys
import json

LIST = []
ERROR = []

def color(text, color=None, on_color=None, attrs=None):
    HIGHLIGHTS = dict(list(zip(['on_grey','on_red','on_green','on_yellow','on_blue','on_magenta','on_cyan','on_white'],list(range(40, 48)))))
    COLORS = dict(list(zip(['grey','red','green','yellow','blue','magenta','cyan','white',],list(range(30, 38)))))
    ATTRIBUTES = dict(list(zip(['bold','dark','','underline','blink','','reverse','concealed'],list(range(1, 9)))))
    del ATTRIBUTES['']
    RESET = '\033[0m'
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)
        text += RESET
    return text


def info(text): return color(text,'magenta')
def error(text): return color(text,'red')
def critic(text): return color(text,'blue','on_red',attrs=['bold'])
def warning(text): return color(text,'yellow')

def norm(b):
    #b = str(b)
    while b.find('\n') != -1 :b = b.replace('\n','')
    while b.find('\r') != -1 :b = b.replace('\r','')
    while b.find('  ') != -1 :b = b.replace('  ',' ')
    while b.find('&lt;') != -1 :b = b.replace('&lt;','<')
    while b.find('&gt;') != -1 :b = b.replace('&gt;','>')
    while b.find('&lte;') != -1 :b = b.replace('&lte;','<=')
    while b.find('&gte;') != -1 :b = b.replace('&gte;','>=')
    while b.find('/r/') != -1 :b = b.replace('/r/','R-')
    while b.find('/') != -1 :b = b.replace('/','')
    while b[0] == ' ' :b = b[1:]
    while b[-1] == ' ' :b = b[0:len(b)-1]
    return b

def makeSaveDir(save_dir):
    """Creates direectory. Returns a valid directory name."""
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
            LIST.append(line[:-1])
        f.close()
    except:
        ERROR.append([subreddit,'List file not found','file .list.txt does not exists!'])
        print critic('List not found') + ' , creating new one!'
        #exit()
        return

def downloadPostsFrom(subreddit,mode='new',start=0,end=0):
    global LIST
    #baseUrl = 'imgur.com'
    baseUrl = 'filmot.org'
    if mode == 'new':
        makeSaveDir(subreddit)
    else:
        makeSaveDir(subreddit+'/'+mode.replace('/','-'))
    loadList(subreddit)
    lst = open('.list.txt','a+')
    print 'Download images from page ',start,' to ',end,' of ',mode,' images of www.'+baseUrl+'/r/'+subreddit+' into '+subreddit+' folder'
    i = end
    while i >= 0:
        url = "http://www."+baseUrl+"/r/"+subreddit+"/"+mode+"/page/"+str(i)+".json"
        i -= 1
        print 'Geting Page : '+info(url)
        try:
            rl = urllib2.Request(url)
            f = urllib2.urlopen(rl)
        except urllib2.HTTPError, e:
            print subreddit+' >>  '+critic(' Error ')+error(': Cannot download image list, Error '+str(e.code))
            continue
        respone = json.loads(f.read().decode("utf-8"))
        if respone['success']:
            images = respone['data']
        else:
            continue
        for img in reversed(images):
            uri = 'http://i.'+baseUrl+'/'+img['hash']+img['ext']
            if img['hash'] in LIST:
                #print 'Duplicate :',img['hash']
                continue
            file_name = norm(img['hash'] + ' - ' + img['title'])
            maxFileName = 255 - len(img['ext'])
            if len(file_name.encode('utf-8')) > maxFileName:
                i = maxFileName
                while len(file_name[0:i].encode('utf-8')) > maxFileName: i -= 1
                file_name = file_name[0:i]

            file_name = file_name + img['ext']
            try:
                with open(file_name) as f: f.close()
                ERROR.append([subreddit,'Image already exists','file '+f+' already exists!'])
                print ERROR[-1][0] + ' >>  ' + ERROR[-1][1]
                continue
            except:
                JustForErrors = 0
            LIST.append(img['hash'])
            try:
                rl = urllib2.Request(uri)
                f = urllib2.urlopen(rl)
            except urllib2.HTTPError, e:
                print subreddit+' >>  '+critic(' Error ')+error(': Cannot Download File, Error '+str(e.code))
                continue
            print subreddit+' >>   '+'Save to '+info(file_name)
            with open(file_name, "wb") as image_file:
                respone = f.read()
                image_file.write(respone)
                image_file.close()

            lst.write(img['hash']+'\n')
            lst.close()
            lst = open('.list.txt','a+')
    lst.close()

def main():
    """Use app as console program."""
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
