# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 20:56:16 2019

@author: MEvans
"""
import math
import numpy as np
import pandas as pd
import plotly.graph_objs as go

def normalize(array):
    """ 
    Normalize array to [0, 1]
    Args:
      array (ndarray): 2D array of values to be transformed
    Return:
      ndarray: transformed values
    """
  minimum = np.nanmin(array)
  maximum = np.nanmax(array)
  y = maximum - array/(maximum - minimum)
  return(y)

def relu(array, b):
    """ 
    Perform rectified linear unit transformation on array
    Args:
      b (int): slope parameter of linear rescaling
    Return:
      ndarray: transformed values
    """
    y = array*b
    return np.where(y>1, 1, y)
        
def sigmoid(array, x0, b):
    """Sigmoid function

    Args:
      array (ndarray): 2D array of values to be transformed
      x0 (int): inflection point
      b (int): scale parameter

    Returns:
      ndarray: image containing transformed values
    """
    y = 1/(1 + np.exp(-b*(array - x0)))
    return(y) 

def logarithmic(array, b):
  """Log-like function bounded [0,1]

  1-exp(-3*x)

  Args:
    array (ndarray): 2D array of values to be transformed
    b (int): scale parameter

  Returns:
    ndarray: log transformed values
  """  
  y = 1 - np.exp(-b*array)
  return(y)

def exponential(array, b):
  """Exponential function bounded 

  Args:
    array (ndarray): 2D array of values to be transformed
    b (int): scale parameter

  Returns:
    ndarray: exponentially transformed values
  """  
  y = array**b 
  return(y)

    
def block(raster, weight, mode):
  if(mode == 'Linear'):
      out = relu(raster, weight)
  elif(mode == 'Exponential'):
      out = raster.pow(weight)
  elif(mode == 'Sigmoid'):
      out = sigmoid(raster, 0.5, weight*10)
  elif(mode == 'Logarithmic'):
      out = logarithmic(raster, weight)
  else:
      out = raster
  return out

class rasterCalculator:
  def __init__(self, rasters, modes, weights):
    self.rasters = rasters
    self.modes = modes
    self.weights = weights
    self.n = len(rasters)

  def calculate(self):
    combined = sum([block(self.rasters[x], self.weights[x], self.modes[x]) for x in range(self.n)])
    return combined

def plot_grid(suit, conn):
    df = [[x,y] for x in np.arange(0, 1.01, 0.01) for y in np.arange(0, 1.01, 0.01)]
    df = pd.DataFrame(df, columns = ['suitability', 'connectivity'])
    df['exp_suit'] = df['suitability']**suit
    df['exp_conn'] = df['connectivity']**conn       #exp_conn = connectivity^conn,
    df['root_suit'] = df['suitability']**(1/suit) #root_suit = suitability^(1/suit),
    df['root_conn'] = df['connectivity']**(1/suit) #root_conn = connectivity^(1/conn),
    df['log_suit'] = sigmoid(df.suitability, 0.5, suit*10) #log_suit = sigmoid(suitability, 0.5, suit*10),
    df['log_conn'] = sigmoid(df.connectivity, 0.5, suit*10) #log_conn = sigmoid(connectivity, 0.5, conn*10),
    df['lin_suit'] = relu(df.suitability, suit) #lin_suit = relu(suitability, suit),
    df['lin_conn'] = relu(df.connectivity, conn) #lin_conn = relu(connectivity, conn) #lin_conn = relu(connectivity, conn)
    
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
                                               y = 0),
                               xaxis = 'x%s' %index,
                               yaxis = 'y%s' %index)
                             
            xpar = dict(visible = False, domain = [0.1+(0.02*J)+((J-1)/5), (J/5)+0.1+(0.02*J)], anchor = 'y%s' %index)
            ypar = dict(visible = False, domain = [0.1+(0.02*I)+((I-1)/5), (I/5)+0.1+(0.02*I)], anchor = 'x%s' %index)
            h_traces.append(trace)
            x_layout.update({'xaxis%s' %index: xpar})
            y_layout.update({'yaxis%s' %index: ypar})
            
            
    layout = {**x_layout, **y_layout}
    layout['xaxis3'].update({'title':'Suitability'})
    layout['yaxis11'].update({'title':'Connectivity'}) 
       
    fig = go.Figure(data = h_traces+c_traces+s_traces, layout = layout)       
    return fig

def calc_value(suit_rast, conn_rast, suit, conn, suitMode, connMode):
    """Transform and combine two rasters
    
    Keyword arguments:
    suit_rast -- raster representing habitat suitability
    conn_rast -- raster representing habitat conectivity
    suit -- integer weight for suitability value functions
    conn -- integer weight for connectivity value functions
    suitMode -- string specifying suitability value function
    connMode -- string specifying connectivity value funtion
    
    Returns:
    raster (ndarray) of transformed and combined values
    """
    if(suitMode == 'linear'):
        suitability = relu(suit_rast, suit)
    elif(suitMode == 'exponential'):
        suitability = suit_rast**suit
    elif(suitMode == 'logistic'):
        suitability = sigmoid(suit_rast, 0.5, suit*10)
    elif(suitMode == 'logarithmic'):
        suitability = suit_rast**(1/suit)
    else:
        suitability = df.Suitability
        
    if(connMode == 'linear'):
        connectivity = relu(conn_rast, conn)
    elif(connMode == 'exponential'):
        connectivity = conn_rast**conn
    elif(connMode == 'logistic'):
        connectivity = sigmoid(conn_rast, 0.5, conn*10)
    elif(connMode == 'logarithmic'):
        connectivity = conn_rast**(1/conn)
    else:
        connectivity = df.Connectivity
        
    value = connectivity + suitability
    del(connectivity, suitability)
    return value