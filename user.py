FACEBOOK_APP_ID = "189677034479391"
FACEBOOK_APP_SECRET = "d49ebeca41d4f0c4790e74c1c5ea263a"

import os
import facebook
import logging


from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

class User(db.Model):
    id = db.StringProperty(required=True) #facebook user-id
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True) #fb OAUTH access token
    phone_number = db.StringProperty()
 

class BaseHandler(webapp.RequestHandler):
    
    @property
    def current_user(self):
        """Returns the logged in Facebook user, or None if unconnected."""
        if not hasattr(self, "_current_user"):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
                # Store a local instance of the user data so we don't need
                # a round-trip to Facebook on every request
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    logging.debug("fbuser "+profile["name"])
                    user = User(key_name=str(profile["id"]),
                                id=str(profile["id"]),
                                name=profile["name"],
                                profile_url=profile["link"],
                                access_token=cookie["access_token"])
                    user.put()
                elif user.access_token != cookie["access_token"]:
                     user.access_token = cookie["access_token"]
                     user.put()
                self._current_user = user
        return self._current_user
        
    
        
class HomeHandler(BaseHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), "login.html")
        args = dict(current_user=self.current_user, facebook_app_id=FACEBOOK_APP_ID)
        self.response.out.write(template.render(path, args))
   
  




application = webapp.WSGIApplication([('/users', HomeHandler)])

def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()                    
                    
                    
                    