import flickrapi
import webbrowser

from local_settings import API_KEY, API_SECRET, USER_ID


def main():
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    flickr.authenticate_via_browser(perms='write')
    sets = flickr.photosets.getList(user_id=USER_ID)
    amelie = [s for s in sets['photosets']['photoset'] if
        s['title']['_content'] == u'Sakura Amélie'][0]
    photos = flickr.photosets.getPhotos(photoset_id=amelie['id'])


if __name__ == '__main__':
    main()
