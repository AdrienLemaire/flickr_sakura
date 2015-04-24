#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flickrapi
import webbrowser
import sys

from local_settings import API_KEY, API_SECRET, USER_ID, ALBUM_NAME
from utils import find_date_taken


def auth():
    print "authenticate"
    flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')
    flickr.authenticate_via_browser(perms='write')
    return flickr


def get_album(flickr, name):
    print "get album"
    sets = flickr.photosets.getList(user_id=USER_ID)
    album = [s for s in sets['photosets']['photoset'] if
        s['title']['_content'] == name][0]
    return flickr.photosets.getPhotos(photoset_id=album['id'])


def update_metas(flickr, photo_id):
    infos = flickr.photos.getInfo(photo_id=photo_id)
    if infos['photo']['dates']['takenunknown'] == '1':
        title = infos['photo']['title']['_content']
        date_taken = find_date_taken(title)
        if date_taken:
            result = flickr.photos.setDates(photo_id=photo_id, date_taken=date_taken)
        else:
            import ipdb; ipdb.set_trace()
    else:
        date_taken = infos['photo']['dates']['taken']
        if date_taken.endswith('00:00:00'):
            import ipdb; ipdb.set_trace()
        else:
            print date_taken
            with open('./images_done.txt', 'a') as f:
                f.write('{}\n'.format(infos['photo']['id']))
        

def get_list_images_done():
    with open('./images_done.txt', 'r') as f:
        return f.read().split('\n')


def main():
    flickr = auth()
    photos = get_album(flickr, ALBUM_NAME)
    print "update photos metas"
    done = get_list_images_done()
    for photo in photos['photoset']['photo']:
        if not photo['id'] in done:
            update_metas(flickr, photo['id'])
        else:
            sys.stdout.write("."),
            sys.stdout.flush()
            


if __name__ == '__main__':
    main()
