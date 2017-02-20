# -*- coding: utf-8 -*-
import urllib2

def getPubIPAddr():
    try:
        url = urllib2.urlopen("http://members.3322.org/dyndns/getip")
        return url.read().strip('\n')
    except HTTPError as e:
        print "Pub Ip : ", e
        return None

if __name__ == '__main__':
    print getPubIPAddr()