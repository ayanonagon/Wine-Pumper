from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import simplejson



class Wine(db.Model):
    name = db.StringProperty()
    year = db.IntegerProperty()
    rating = db.IntegerProperty()
    description = db.StringProperty()
    location = db.StringProperty()
    
class WineHandler(webapp.RequestHandler):
    
    def get(self):
        """wines = Wine.all()
        wine_list = []
        for wine in wines:
            w = {}
            w["name"] = wine.name
            w["year"] = wine.year
            w["rating"] = wine.rating
            w["description"] = wine.description
            w["location"] = wine.location
            wine_list.append(w)
        response_json = simplejson.dumps(wine_list)
        self.response.out.write(response_json)"""
        # Get as HTML
        wines = Wine.all()
        html_strings = []
        html_strings.append('''
        <!DOCTYPE html>
        <html lang="en">

        <head>
          <meta charset="utf-8" />

        	<!-- Set the viewport width to device width for mobile -->
        	<meta name="viewport" content="width=device-width" />

        	<title>Wine Pumper</title>

        	<!-- Included CSS Files -->
        	<link rel="stylesheet" href="/stylesheets/foundation.css">
        	<link rel="stylesheet" href="/stylesheets/app.css">
          <script src="/javascripts/app.js"></script>
        </head>

        <body>
            <div class="container">
              <div class="row">
                <div class="twelve columns">
                  <h2>Wine tastings</h2>
                  <h5>These are wines that <em>you</em> tasted!</h5>
                  <hr />
                </div>
              </div>
        ''')
        for wine in wines:
            name = wine.name
            year = wine.year
            rating = wine.rating
            description = wine.description
            location = wine.location
            html_strings.append("""
                <div class="row">
                      <div class="eight columns">
                        <div class="panel">
              	          <h5>%(name)s</h5>
              	          <p>Appelation: %(location)s</p>
              	          <p>Vintage: %(year)s</p>
              	          <p>Rating: %(rating)s</p>
              	          <p>Remarks: %(description)s</p>
                        </div>
                      </div>
                    </div>
            """ % {"name": name, "year": year, "location": location, "rating": rating, "description": description})
        html_strings.append("""
                </div>
            </body>
            </html>
        """)
        self.response.out.write(''.join(html_strings))
              
    def post(self):
        wine = Wine()
        wine.name = self.request.get("name")
        wine.year = int(self.request.get("year"))
        wine.rating = int(self.request.get("rating"))
        wine.description = self.request.get("description")
        wine.location = self.request.get("location")
        db.put(wine)
        self.redirect('/wine')
        
application = webapp.WSGIApplication([('/.*', WineHandler)])

def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()