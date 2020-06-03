# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:49:58 2019

@author: MEvans
"""
import math
import pandas as pd
import numpy as np
import plotly
#import plotly.plotly as ply
import plotly.graph_objs as go
    
suit = 2
conn = 2

df = [[x,y] for x in np.arange(0, 1.01, 0.01) for y in np.arange(0, 1.01, 0.01)]
df = pd.DataFrame(df, columns = ['suitability', 'connectivity'])
df['exp_suit'] = df['suitability']**suit
df['exp_conn'] = df['connectivity']**conn       #exp_conn = connectivity^conn,
df['root_suit'] = df['suitability']**(1/suit) #root_suit = suitability^(1/suit),
df['root_conn'] = df['connectivity']**(1/suit) #root_conn = connectivity^(1/conn),
df['log_suit'] = sigmoid(df.suitability, 0.5, suit*10) #log_suit = sigmoid(suitability, 0.5, suit*10),
df['log_conn'] = sigmoid(df.connectivity, 0.5, suit*10) #log_conn = sigmoid(connectivity, 0.5, conn*10),
df['lin_suit'] = relu(df.suitability, suit) #lin_suit = relu(suitability, suit),
df['lin_conn'] = relu(df.connectivity, conn) #lin_conn = relu(connectivity, conn)

c = (df
    .groupby(['connectivity'], as_index = False)
    .agg({'exp_conn': 'first',
          'root_conn':'first',
          'log_conn':'first',
          'lin_conn':'first'})
    )
    
s = (df
     .groupby(['suitability'], as_index = False)
     .agg({'exp_suit':'first',
           'root_suit':'first',
           'log_suit':'first',
           'lin_suit':'first'})
    )


c_traces = [go.Scatter(
        y = c['connectivity'],
        x = c[i],
        showlegend = False,
        mode = 'lines',
        line = dict(color = 'black'),
        xaxis = 'x%s'%((c.columns.get_loc(i)*5)+1),
        yaxis = 'y%s'%((c.columns.get_loc(i)*5)+1)) for i in c.columns[1:]]


s_traces = [go.Scatter(
        x = s['suitability'],
        y = s[i],
        mode = 'lines',
        line = dict(color = 'black'),
        showlegend = False,
        xaxis = 'x%s'%(s.columns.get_loc(i)+1),
        yaxis = 'y%s'%(s.columns.get_loc(i)+1)) for i in s.columns[1:]]

y_layout = {'yaxis%s' %(i+1): dict(showgrid = False,
            domain = [0, 0.1],
            anchor = 'x%s' %(i+1),
            tickmode = 'auto',
            nticks = 3) for i in range(1, len(s.columns))}
x_layout = {'xaxis%s' %(i+1): dict(showgrid = False,
            domain = [0.1+(0.02*i)+((i-1)/5), (i/5)+0.1+(0.02*i)],
            anchor = 'y%s' %(i+1),
            tickmode = 'auto',
            nticks = 3) for i in range(1, len(s.columns))}

y_layout.update({'yaxis%s' %((i*5)+1): dict(showgrid = False,
                 domain = [0.1+(0.02*i)+((i-1)/5), (i/5)+0.1+(0.02*i)],
                 anchor = 'x%s' %((i*5)+1),
                 tickmode = 'auto',
                 nticks = 3) for i in range(1, len(c.columns))})
x_layout.update({'xaxis%s' %((i*5)+1): dict(showgrid = False,
                 domain = [0, 0.1],
                 anchor = 'y%s' %((i*5)+1),
                 tickmode = 'auto',
                 nticks = 3) for i in range(1, len(c.columns))})

h_traces = []

for i in c.columns[1:]:
    for j in s.columns[1:]:
        J = s.columns.get_loc(j)
        I = c.columns.get_loc(i)
        index = ((I)*5)+J+1
        df['test'] = df[i] + df[j]
        
        mat = np.array(df.test.values).reshape(101, 101)
        
        trace = go.Contour(z = mat,
                           autocontour = False,
                           contours = dict(start = 0.666,
                                           end = 2,
                                           size = 0.666,
                                           coloring = 'heatmap'),
                           colorbar = dict(len = 0.2,
                                           x = 0, 
                                           y = 0,
                                           title = 'Value',
                                           tickmode = 'array',
                                           tickvals = [0, 0.667, 1.333],
                                           ticktext = ['Low', 'Medium', 'High']),
                           xaxis = 'x%s' %index,
                           yaxis = 'y%s' %index)
                         
        h_traces.append(trace)
        
        xpar = dict(visible = False, domain = [0.1+(0.02*J)+((J-1)/5), (J/5)+0.1+(0.02*J)], anchor = 'y%s' %index)
        ypar = dict(visible = False, domain = [0.1+(0.02*I)+((I-1)/5), (I/5)+0.1+(0.02*I)], anchor = 'x%s' %index)
        
        x_layout.update({'xaxis%s' %index: xpar})
        y_layout.update({'yaxis%s' %index: ypar})
        
        
layout = {**x_layout, **y_layout}
layout['xaxis3'].update({'title':'Suitability'})
layout['yaxis11'].update({'title':'Connectivity'})
        
fig = go.Figure(data = h_traces+c_traces+s_traces, layout = layout)                       
plotly.offline.plot(fig)

xs = join.Xconn.unique()
ys = join.Yconn.unique()
join = join.sort_values(['Xconn', 'Yconn'])
z = np.array(join['Suitability']).reshape(len(xs), len(ys))
trace = go.Heatmap(
            z = z,
            x = xs,
            y = ys)


print(10478*5876)