# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 08:29:49 2019

@author: MEvans
"""

import numpy as np
import pandas as pd
#import plotly.plotly as py
import plotly.graph_objs as go
import functions as fxn

x = np.arange(0, 1.01, 0.01)
trace0 = go.Scatter(
        x = x,
        y = [fxn.sigmoid(i, 0.5, k = 10) for i in x],
        mode = 'lines',
        name = 'Logistic',
        line = {'color': 'blue'}
        )

trace1 = go.Scatter(
        x = x,
        y = [fxn.relu(i, 2) for i in x],
        mode = 'lines',
        name = 'Linear',
        line = {'color': 'black'}
        )

trace2 = go.Scatter(
        x = x,
        y = [i**5 for i in x],
        mode = 'lines',
        name = 'Exponential',
        line = {'color': 'orange'}
        )

trace3 = go.Scatter(
        x = x,
        y = [i**0.2 for i in x],
        mode = 'lines',
        name = 'Logarithmic',
        line = {'color': 'purple'}
        )

layout = go.Layout(xaxis = dict(title = 'Connectivity/Suitability',
                           titlefont = dict(size = 14, color = 'black')),
            yaxis = dict(title = 'Value',
                         titlefont = dict(size = 14, color = 'black')),
            legend = dict(x = 0.8, y = 0.1)
                         )

example = go.Figure(data = [trace0, trace1, trace2, trace3], layout = layout)

#View the plot in a local browser
#plotly.offline.plot(example)
#py.iplot(fig)
df = [[x,y] for x in np.arange(0, 1.01, 0.01) for y in np.arange(0, 1.01, 0.01)]
df = pd.DataFrame(df,columns = ['suitability', 'connectivity'])
df['test'] = df.suitability.apply(lambda x: x*2)
#print(df.groupby(['suitability']).groups.keys())
d = df.groupby(['suitability'], as_index = False).agg({'test': 'first', 'connectivity':'first'})

cols = d.columns

#traces = [go.Scatter(
#        x = d.test,
#        y = d.suitability,
#        mode = 'lines',
#        xaxis = 'x1',
#        yaxis = 'y1'
#        ),
#go.Scatter(
#        x = d.connectivity,
#        y = d.suitability,
#        mode = 'lines',
#        xaxis= 'x2',
#        yaxis = 'y2')]

traces = [go.Scatter(
            x = d[i],
            y = d.suitability,
            mode = 'lines',
            xaxis = 'x%s'%(cols.get_loc(i)),
            yaxis = 'y%s'%(cols.get_loc(i))) for i in cols[1:]]

def yparams(d1, d2, anchor = 'x1'):
    return dict(tickmode = 'array',
               tickvals = np.arange(0, 1.5, 0.5),
               ticktext = np.arange(0, 1.5, 0.5),
               showgrid = False,
               side = 'right',
               domain = [d1, d2],
               anchor = anchor) 

def xparams(d1, d2, anchor = 'y1'):
    return dict(tickmode = 'array',
               tickvals = np.arange(0, 2.5, 0.5),
               ticktext = np.arange(0, 2.5, 0.5),
               showgrid = False,
               domain = [d1, d2], 
               anchor = anchor)

layout = go.Layout(yaxis = yparams(0, 0.45),
                   xaxis = xparams(0, 0.45),
                   yaxis2 = yparams(0.55, 1, 'x2'),
                   xaxis2 = xparams(0.55, 1, 'y2'),
                   showlegend = False)
                
c = go.Figure(data = traces, layout = layout)                       

