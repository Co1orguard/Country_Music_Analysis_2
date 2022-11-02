import networkx as nx
from networkx import Graph
from bokeh.models import Range1d, Circle, TapTool, MultiLine, HoverTool, CustomJS, NodesAndLinkedEdges
from bokeh.plotting import figure, from_networkx
from bokeh.embed import components
from bokeh.palettes import d3


def render_graph(graph: Graph):
    """
    Renders the graph using Bokeh
    :param graph:
    :return:
    """
    colors = d3['Category10'][8]

    layout = nx.spring_layout(graph, k=0.20, scale=20, iterations=100)
    # layout = nx.spectral_layout(graph, scale=20)
    HOVER_TOOLTIPS = [("Name", "@artistName"),
                      ("ID", "@index"),
                      ("CC", "@closeness_centrality{0.00}"),
                      ("BC", "@betweenness_centrality{0.00}"),
                      ("DC", "@degree_centrality{0.00}")]
    #  Add measures here for display on graph
    plot = figure(tooltips=HOVER_TOOLTIPS, tools="pan,wheel_zoom,save,reset,tap",
                  active_scroll='wheel_zoom', x_range=Range1d(-10.5, 10.5),
                  y_range=Range1d(-10.5, 10.5), title="Title", sizing_mode="scale_width")
    network_graph = from_networkx(graph, layout, center=(0, 0))
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.node_renderer.glyph = Circle(size='size', fill_color='color')
    network_graph.edge_renderer.data_source.data["line_width"] = \
        [graph.get_edge_data(a, b)['weight'] for a, b in graph.edges()]
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5)
    network_graph.edge_renderer.glyph.line_width = {'field': 'line_width'}
    plot.renderers.append(network_graph)
    plot.xgrid.visible = False
    plot.ygrid.visible = False
    plot.axis.visible = False

    tap_tool = plot.select(type=TapTool)
    #tap_tool.callback = CustomJS(code="alert(cb_data.node_indices);")
    return components(plot)
