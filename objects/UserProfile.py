from Utilities import Utilities
import urllib2
import json
import requests
from flask import redirect

util = Utilities()
mongoDB = util.mongoDBConnect()


class UserProfile:
    def __init__(self):
        pass

    def buildUserProfileFromFB(self, token):
        userProfileResponse = urllib2.urlopen(
            "https://graph.facebook.com/me?access_token=" + token).read()
        user = json.loads(userProfileResponse)

        userPictureResponse = requests.get(
            'https://graph.facebook.com/' + str(user['id']) + '/picture?type=normal')

        preparedLinkUsername = ''.join(e for e in user['name'] if e.isalnum())

        profile = {
            "username": user['id'],
            # "usernameurl": preparedLinkUsername.lower(),
            "facebookid": "",
            "name": user['name'],
            "picture": str(userPictureResponse.url)
        }

        mongoDB.profiles.insert_one(profile)

        return profile

    def getUserProfile(self, item):

        if item.isdigit():
            # item is a facebook id
            credential = mongoDB.profiles.find_one(item)
            return credential

        elif len(item) > 100:
            # item is a facebook access token
            try:
                userProfileResponse = urllib2.urlopen(
                    "https://graph.facebook.com/me?access_token=" + item).read()
                user = json.loads(userProfileResponse)
                credential = mongoDB.profiles.find_one(
                    {'username': user['id']})
                return credential
            except:
                return 'error'

        # elif len(item) < 100:
        #     # item is a username
        #     credential = mongoDB.profiles.find_one({'username': item})
        #     return credential

        else:
            # item failure
            return 'error'

    def getUserProfileFromDB(self, username):
        profile = mongoDB.profiles.find_one({'username': username})
        return profile
