import tweepy
import sys
import time
import os
import json
import csv
import traceback
import keys

USER_DIR = os.path.abspath('uiuc_members')
JSON_DIR = os.path.abspath('uiuc_json')

MAX_FRIENDS = 250
MAX_FRIENDS_OF_FRIENDS = 250

if not os.path.exists(USER_DIR):
	os.makedirs(USER_DIR)

if not os.path.exists(JSON_DIR):
	os.makedirs(JSON_DIR)

CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET

appauth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
#oauth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
#oauth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
api = tweepy.API(appauth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
# api = tweepy.API(oauth)

# Encode string into ascii
enc = lambda x: x.encode('ascii', errors='ignore')

#Looking at followers of UIUC connected twitter accounts
target_accounts = ('Illinois_Alma','EngineeringAtIL','IEEE_UIUC','eceILLINOIS','IllinoisCS','acmuiuc','BeckmanInst','acmreflections','HackIllinois','illini_drumline','BlackSheep_UIUC','UIResearchPark')

def get_friend_ids(centre, max_depth=1, current_depth=0, taboo_list=set()):
 
    # print 'current depth: %d, max depth: %d' % (current_depth, max_depth)
    # print 'taboo list: ', ','.join([ str(i) for i in taboo_list ])

    if current_depth == max_depth:
        print 'out of depth'
        return taboo_list
 
    if centre in taboo_list:
        # we've been here before
        print 'Already been here.'
        return taboo_list
    else:
        taboo_list.add(centre)
 
    :
        userfname = os.path.join(JSON_DIR, str(centre) + '.json')
        fname = os.path.join(USER_DIR, str(centre) + '.csv')
        if not os.path.exists(userfname):
            print 'Retrieving user details for twitter id %s' % str(centre)
            while True:
                try:
                    user = api.get_user(centre)
 
                    d = {'name': user.name,
                         'screen_name': user.screen_name,
                         'id': user.id,
                         'friends_count': user.friends_count,
                         'followers_count': user.followers_count,
                         'statuses_count' : user.statuses_count}
 
                    with open(userfname, 'w') as outf:
                        outf.write(json.dumps(d, indent=1))

                    user = d
                    break
                except tweepy.TweepError, error:
                    print type(error)
 
                    if str(error) == 'Not authorized.':
                        print 'Can''t access user data - not authorized.'
                        return taboo_list
 
                    if str(error) == 'User has been suspended.':
                        print 'User suspended.'
                        return taboo_list
 
                    errorObj = error[0][0]
 
                    print errorObj
 
                    # if errorObj['message'] == 'Rate limit exceeded':
                    #     print 'Rate limited. Sleeping for 15 minutes.'
                    #     time.sleep(15 * 60 + 15)
                    #     continue
 
                    return taboo_list
        else:
            user = json.loads(file(userfname).read())
 
        screen_name = enc(user['screen_name'])
        fname = os.path.join(USER_DIR, screen_name + '.csv')
        friendids = []
 
        # only retrieve friends of TED... screen names
        if not os.path.exists(fname):
            print 'No cached data for screen name "%s"' % screen_name
            with open(fname, 'w') as outf:
                params = (enc(user['name']), screen_name)
                print 'Retrieving followers for user "%s" (%s)' % params
                writer = csv.writer(outf,dialect='excel')
                
                # page over friends
                if current_depth == 0:
                	c = tweepy.Cursor(api.followers, id=user['id']).items()
                else:
                	c = tweepy.Cursor(api.friends, id=user['id']).items()
                
                friends_count = 0

                while True:
                    try:
                        follower = c.next()
                        friendids.append(follower.id)
                        params = (follower.id, enc(follower.screen_name), enc(follower.name))
                        writer.writerow(params)
                        friends_count += 1
                        if current_depth !=0 and friends_count >= MAX_FRIENDS:
                            print "Reached max no. of friends for '%s'." % follower.screen_name
                            break
                    except tweepy.TweepError,error:
                  			if str(error) == 'Not authorized.':
												print 'Can''t access user data - not authorized.'
												return taboo_list

                    except StopIteration:
                        break
                
        else:
            with open(fname, 'r') as outf:
                reader = csv.reader(outf,dialect='excel')
                friendids = [row[0] for row in reader]
 
        print 'Found %d followers for %s' % (len(friendids), screen_name)

        # get friends of friends
        cd = current_depth
        if cd+1 < max_depth:
            for fid in friendids[:MAX_FRIENDS_OF_FRIENDS]:
                taboo_list = get_friend_ids(fid, max_depth=max_depth,
                    current_depth=cd+1, taboo_list=taboo_list)

        if cd+1 < max_depth and len(friendids) > MAX_FRIENDS_OF_FRIENDS:
            print 'Not all friends retrieved for %s.' % screen_name
 
    except Exception, error:
        print 'Error retrieving friends for user id: ', centre
        print str(error)
        traceback.print_exc()

        if os.path.exists(fname):
             os.remove(fname)
             print 'Removed file "%s".' % fname
 
        sys.exit(1)
 
    return taboo_list

acm_account = target_accounts[5]
print "Processing followers of " + acm_account

matches = api.lookup_users(screen_names=[acm_account])
depth = 2
if len(matches) == 1:
    get_friend_ids(matches[0].id,max_depth=depth)
else:
    print 'Sorry, could not find twitter user with screen name: %s' % acm_account

