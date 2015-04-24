#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flickrapi
import webbrowser

from local_settings import API_KEY, API_SECRET, USER_ID


def auth():
    print "authenticate"
    flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')
    flickr.authenticate_via_browser(perms='write')
    return flickr


def get_album(flickr, name):
    print "get album"
    sets = flickr.photosets.getList(user_id=USER_ID)
    amelie = [s for s in sets['photosets']['photoset'] if
        s['title']['_content'] == name][0]
    photos = flickr.photosets.getPhotos(photoset_id=amelie['id'])


def update_metas(flickr, photo_id):
    infos = flickr.photos.getInfo(photo_id=photo_id)
    if infos['photo']['dates']['takenunknown'] == '1':
        import ipdb; ipdb.set_trace()
    else:
        print infos['photo']['dates']['taken']


def main():
    flickr = auth()
    amelie = get_album(flickr, u'Sakura Amélie')
    print "update photos metas"
    for photo in reversed(photos['photoset']['photo']):
        update_metas(flickr, photo['id'])


if __name__ == '__main__':
    main()
