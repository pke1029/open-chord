# OpenChord

OpenChord is a Python library I am developing to plot beautiful chord diagrams for free. OpenChord uses the `drawsvg` library and can display figures in a Jupyter notebook or Jupyter lab. Other libraries for drawing chord diagram includes [PlotAPI](https://plotapi.com/) (paid), [Bokeh](https://holoviews.org/reference/elements/bokeh/Chord.html) (visible moire artifact), and [Plotly](https://plotly.com/python/v3/filled-chord-diagram/) (tedious). 

## Installation

I am working on hosting the library on PyPI.org. At the meantime, you can download the `openchord.py` file into your working directory/folder and use it that way. You will also need to install the `drawsvg` library (https://github.com/cduck/drawsvg) using the command
```
python3 -m pip install "drawsvg[all]~=2.0"
```

## Usage

Currently, the function only support a symmetric adjacency matrix (i.e. weighted graph, non-directed)
```python
import openchord as oc

adjacency_matrix = [[ 3, 18,  9,  0, 23],
                    [18,  0, 12,  5, 29],
                    [ 9, 12,  0, 27, 10],
                    [ 0,  5, 27,  0,  0],
                    [23, 29, 10,  0,  0]]
labels = [Emma', 'Isabella', 'Ava', 'Olivia', 'Sophia']

fig = oc.Chord(adjacency_matrix, labels)
fig.show()
```
Color can be changed with
```
fig.color_map = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
fig.show()
```
You can export the figure as an .svg file and open it in a vector graphics software such as [Inkscape](https://inkscape.org/)
```
fig.save_svg("figure.svg")
```
![Chord diagram using OpenChord](https://github.com/pke1029/open-chord/blob/main/figure.png)
