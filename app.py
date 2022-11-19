from flask import Flask, render_template, session
from guilayer.artistform import ArtistForm
from flask_bootstrap import Bootstrap
from applayer.artistlist import ArtistList
from bokeh.resources import INLINE
from guilayer.render import render_graph
from applayer.artistgraph import ArtistGraph

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jerrygthesupremeleader'
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def main_page():
    """
    Sets up the page used to display the application; Uses a single form
    in a two-div structured page. The page is styled minimally using bootstrap
    :return: rendered page
    """
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render graph
    the_graph, script, div = None, None, None
    debug = False # False displays graph

    form = ArtistForm()
    session['select'] = None
    artist_list = None

    if form.validate_on_submit():
        session['select'] = form.select.data
        # Use the selected data to build a graph by getting the list
        # of objects and passing them to an ArtistGraph object
        artist_list = ArtistList(session['select'])
        script = None
        div = None
        # Uncomment the next two lines to do system tests
        ag = ArtistGraph(artist_list, int(form.depth.data))
        script, div = render_graph(ag.graph)

    html = render_template('index.html', title='Home', formtitle='Artist Social Network',
                           form=form, select=artist_list, plot_script=script, debug=debug,
                           plot_div=div, js_resources=js_resources, css_resources=css_resources)
    return html


if __name__ == '__main__':
    app.run()
