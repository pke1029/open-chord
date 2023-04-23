# OpenChord

OpenChord is a Python library I am developing to plot beautiful chord diagrams for visualising networks and graphs. OpenChord uses the `drawsvg` library and can display figures in a Jupyter notebook or Jupyter lab. Other libraries for drawing chord diagram includes [PlotAPI](https://plotapi.com/) (paid), [Bokeh](https://holoviews.org/reference/elements/bokeh/Chord.html) (visible moire artifact), and [Plotly](https://plotly.com/python/v3/filled-chord-diagram/) (tedious). 

## Installation

OpenChord is now on PyPI.org! Install using the command
```
pip install openchord
```

## Usage

Currently, the function only support symmetric adjacency matricies (i.e. weighted graph, non-directed)
```python
import openchord as ocd

adjacency_matrix = [[ 3, 18,  9,  0, 23],
                    [18,  0, 12,  5, 29],
                    [ 9, 12,  0, 27, 10],
                    [ 0,  5, 27,  0,  0],
                    [23, 29, 10,  0,  0]]
labels = ['Emma', 'Isabella', 'Ava', 'Olivia', 'Sophia']

fig = ocd.Chord(adjacency_matrix, labels)
fig.show()
```
Color can be changed like so
```python
fig.colormap = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
fig.show()
```
You can export the figure as an .svg file and open it in a vector graphics software such as [Inkscape](https://inkscape.org/)
```python
fig.save_svg("figure.svg")
```
![Chord diagram using OpenChord](https://raw.githubusercontent.com/pke1029/open-chord/main/media/figure.png)

## More tutorials and examples
I wrote a few more tutorials available via the link below and in the `/example` directory
1. [Quick Start](https://github.com/pke1029/open-chord/blob/main/examples/01_quick_start.ipynb)
