#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# TIPS

## Delete pics
> photos = flickr.photosets.getPhotos(photoset_id=album_id, user_id=USER_ID,
    extras='date_taken,tags')['photoset']['photo'] 
> pics = [p for p in photos if p['datetaken'].startswith('2015-04-27') and
    p['tags'] == 'line']
> flickr.photosets.removePhotos(photoset_id=album_id,photo_ids=','.join([p['id']
    for p in today_pics]))
"""

import collections
import flickrapi
import webbrowser
import sys

from local_settings import API_KEY, API_SECRET, USER_ID, ALBUM_NAME
from utils import find_date_taken



IMAGE_CACHE = []
with open('./images_done.txt', 'r') as f:
    IMAGE_CACHE = f.read().split('\n')


def auth():
    print("authenticate")
    flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')
    flickr.authenticate_via_browser(perms='write')
    return flickr


def get_album(flickr, name):
    print("get album")
    sets = flickr.photosets.getList(user_id=USER_ID)
    album = [s for s in sets['photosets']['photoset'] if
        s['title']['_content'] == name][0]
    return album['id'], flickr.photosets.getPhotos(photoset_id=album['id'])


def update_metas(flickr, photo_id):
    infos = flickr.photos.getInfo(photo_id=photo_id)
    title = infos['photo']['title']['_content']
    date_taken = infos['photo']['dates']['taken']

    # Check date taken
    if infos['photo']['dates']['takenunknown'] == '1':
        date_taken = find_date_taken(title)
        if date_taken:
            result = flickr.photos.setDates(photo_id=photo_id, date_taken=date_taken)
        else:
            import ipdb; ipdb.set_trace()

    # Check visibility
    if not infos['photo']['visibility']['isfamily']:
        flickr.photos.setPerms(photo_id=photo_id, is_public=0, is_friend=0,
                is_family=1, perm_comment=1, perm_addmeta=1)
        sys.stdout.write("@"),
        sys.stdout.flush()


    if not infos['photo']['id'] in IMAGE_CACHE:
        print(date_taken)
        with open('./images_done.txt', 'a') as f:
            f.write('{}\n'.format(infos['photo']['id']))
        


def main():
    flickr = auth()
    album_id, photos = get_album(flickr, ALBUM_NAME)
    print("update photos metas")
    for photo in photos['photoset']['photo']:
        if not photo['id'] in IMAGE_CACHE:
            update_metas(flickr, photo['id'])
        else:
            sys.stdout.write("."),
            sys.stdout.flush()

    print("\nReorder album")
    photos = flickr.photosets.getPhotos(photoset_id=album_id, user_id=USER_ID,
        extras='date_taken')['photoset']['photo']
    photos = sorted(photos, key=lambda p: p['datetaken'], reverse=True)
    flickr.photosets.reorderPhotos(
        photoset_id=album_id,
        photo_ids=','.join([p['id'] for p in photos]),
    )

    duplicates = [x for x, y in collections.Counter([p['title'] for p in
        photos]).items() if y > 1]
    if duplicates:
        print("\nRemoving duplicates")
        to_remove = []
        for p in photos:
            if p['title'] in duplicates:
                to_remove.append(p['id'])
                duplicates.pop(duplicates.index(p['title']))
        flickr.photosets.removePhotos(
            photoset_id=album_id,
            photo_ids=','.join(to_remove),
        )
        print("Removed {} duplicates".format(len(to_remove)))


if __name__ == '__main__':
    main()
