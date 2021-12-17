# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 20:56:16 2019

@author: MEvans
"""
import numpy as np
import math

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
  y = (1 - np.exp(-b*array))/(1 - np.exp(-b))
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