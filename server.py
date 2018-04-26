from flask import Flask, redirect, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Getting our list of MOST LOVED MELONS
MOST_LOVED_MELONS = {
    'cren': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimRegular/crenshaw.jpg',
        'name': 'Crenshaw',
        'num_loves': 584,
    },
    'jubi': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Jubilee-Watermelon-web.jpg',
        'name': 'Jubilee Watermelon',
        'num_loves': 601,
    },
    'sugb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Sugar-Baby-Watermelon-web.jpg',
        'name': 'Sugar Baby Watermelon',
        'num_loves': 587,
    },
    'texb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Texas-Golden-2-Watermelon-web.jpg',
        'name': 'Texas Golden Watermelon',
        'num_loves': 598,
    },
}

@app.route("/")
def index():

    if "name" in session:
        return render_template("top-melons.html", melons=MOST_LOVED_MELONS)


    return render_template("homepage.html")


@app.route("/top-melons")
def top_melons():
    """returns top melons"""

    if "name" not in session: 
        return render_template("homepage.html")

    return render_template("top-melons.html", melons=MOST_LOVED_MELONS)

@app.route("/get-name")
def get_name():

    name = request.args.get("name")
    session["name"] = name 

    return redirect("/top-melons")
    # I get this message when I redirect:
    # The Flask Debug Toolbar has intercepted a redirect to the above URL for debug viewing purposes. You can click the above link to continue with the redirect as normal. If you'd like to disable this feature, you can set the config variable DEBUG_TB_INTERCEPT_REDIRECTS to False.

@app.route("/love-melon", methods=["POST"])
def love_melon():

    # Attempt to complete using dictionary
    #loved_melon = request.args.get("melon")
    # print loved_melon
    # MOST_LOVED_MELONS[loved_melon]['num_loves'] += 1 

    loved_melon = request.form.get('melon')
    # melon_name = request.form.get('melon')
    # when using jinja for loop.got this response error: list indices must be integers, not unicode




    # if 'cren' == request.form.get('cren'):
    #     loved_melon = 'cren'
    # elif 'jubi' == request.form.get('jubi'):
    #     loved_melon = 'jubi'
    # elif 'sugb' == request.form.get('sugb'):
    #     loved_melon = 'sugb'
    # elif 'texb' == request.form.get('texb'):
    #     loved_melon = 'texb'

    # if loved_melon == True:
    [MOST_LOVED_MELONS][loved_melon]['num_loves'] += 1 


    if "name" in session:
        name = session["name"]

    return render_template("thank-you.html", loved_melon=loved_melon)

@app.route("/thank-you")
def thank_you():

    return render_template("thank-you.html")




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
