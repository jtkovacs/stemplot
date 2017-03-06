
# coding: utf-8

# **Jacob Kovacs** | https://jtkovacs.com/



## IMPORT LIBRARY & GENERATE TEST DATA

import random  # to generate test data

pop_x = range(0,300,1)
xn = 50
x1 = random.sample(pop_x, xn) + random.sample(pop_x, xn)  # integer test data
x2 = random.sample(pop_x, xn) + random.sample(pop_x, xn)

pop_y = range(0,20,1)
yn=20
y1 = [i + random.uniform(0,10) for i in random.sample(pop_y, yn)]  # floats test data
y1 = [i + random.uniform(0,10) for i in y1]
y2 = [i + random.uniform(0,10) for i in random.sample(pop_y, yn)]



## STEMPLOT FUNCTIONS


def print_legend(integer_data=True, num_stemplots=1):
    """
    No return value; prints stemplot legend when called by create_stemplot() or compare_stemplots().
    
    Arguments: 
    integer_data is a Boolean reflecting the input datatype for create_stemplot(x) or compare_stemplots(x,y).
    num_stemplots is an integer: 1 if called by create_stemplot(), 2 if called by compare_stemplots().
    """
    
    print 'LEGEND'
    print '\t----------------'
    
    
    # create_stemplot(... integer_data=True)
    if integer_data and num_stemplots == 1:  
        print '\t00|1 shows that x contains the number 1' 
        print '\t12|25 shows that x contains 122, 125'
    
    
    # compare_stemplots(... integer_data=True)
    elif integer_data:  
        print '\t' + '1'.rjust(3) + '|00|1 shows that x and y both contain the number 1' 
        print '\t850|12|25 shows that x contains numbers 128, 125, 120 and y contains 122, 125'
    
    
    # create_stemplot(... integer_data=False)
    elif num_stemplots == 1: 
        print '\t12|25 shows that x contains 12.2, 12.5'
        print '\t1.2|25 shows that x contains 1.22, 1.25'
        
        
    # compare_stemplots(... integer_data=False)
    else:  
        print '\t' + '1'.rjust(3) + '|00|1 shows that x and y both contain the number 0.1' 
        print '\t850|1.2|25 shows that x contains numbers 1.28, 1.25, 1.20 and y contains 1.22, 1.25'
    print '\t----------------'      
    

def pad_with_zeros(x, integer_data=True, precision=2):
    """
    Return modified x as a list of strings when called by create_stemplot(). 
    Padding x with zeros is required to align stemplot outputs created by print_stemplot().
    
    Arguments: 
    x is a 1D list of integers or floats.
    integer_data is a Boolean reflecting the input datatype for create_stemplot(x).
    precision is an integer specifying #digits for rounding x when integer_data=False.
    """
    
    if integer_data:  
        offset = max([len(str(i)) for i in x])
        for i in range(len(x)):
            x[i] = str(x[i])
            
            # prepend zeros so len(x[i]) == len(x[j]) for all i,j
            while len(x[i]) < offset:
                x[i] = '0' + x[i]
    
    
    else:
        # need when create_float_stemplot() is called by compare_stemplots()
        x = [float(i) for i in x]
        
        offset = max([str(i).find('.') for i in x])
        for i in range(len(x)):
            
            # round data to desired precision, default = 2 decimal places 
            x[i] = str(round(x[i], precision))
            a,b = x[i].split('.')
            
            # pad with trailing zeros, e.g. 2.1 becomes 2.100 if precision=3
            while len(b) < precision:
                b = b + '0'
                
            # prepend zeros, e.g. 2.1 becomes 002.1
            while len(a) < offset:
                a = '0' + a
            
            x[i] = '.'.join([a, b]) 
        
    
    return x


def put_leaves_on_stems(x, precision, leaf_order):
    """ 
    Return stemplot, a dictionary based on x.
    The rightmost digit of each x[i] is a 'leaf'; remaining digits are the 'stem'.
    Leaves are appended to each other if they share a stem.
    E.g. if x[i]=001, x[j]=002, x[k]=006, then stemplot['00'] = '126'.
    
    Arguments:
    x is a list of integers or floats.
    precision is an integer formerly used for rounding x, here used to determine formatting.
    If precision == 1, the decimal falls at the stem-ends and is dropped (the stemplot legend clarifies).
    """
    
    # create dictionary from data: stemplot = {'stem': ['leaf', 'leaf']}
    stemplot = dict()
    for em in x:
        
        # if stem is already in dictionary
        if em[:-1] in stemplot:
            # append the new leaf
            stemplot[em[:-1]] = stemplot[em[:-1]] + em[-1]
        
        else:
            # create a stem with its first leaf
            stemplot[em[:-1]] = em[-1]
    
  
    # sort dictionary values; sort in descending order if leaf_order = True
    # make each dictionary value, currently a list of characters, into a string of characters
    # e.g. stemplot = {'00': ['1','2','6']} becomes stemplot = {'00': '126'}
    for key,value in stemplot.items():
        stemplot[key] = ''.join(sorted(value, reverse=leaf_order))

            
    # reformat dictionary keys when decimal place coincides with stem-ends 
    # e.g. stemplot['124.': '1'] becomes stemplot['124': '1']
    if precision == 1:
        for key in stemplot.keys(): stemplot[key[:-1]] = stemplot.pop(key) 
            
            
    return stemplot


def print_stemplot(x_stemplot, y_stemplot=None):
    """
    No return value. Prints stemplot when called by create_stemplot() or compare_stemplots().
    
    Arguments: 
    x_stemplot is a dictionary: {'x_stem': 'x_leaves'}.
    y_stemplot is a dictionary: {'y_stem': 'y_leaves'}. Only supplied by create_stemplot().
    """

    print 'DATA'
    

    if y_stemplot:
        # print two stemplots as column of x_leaves|stem|y_leaves
        # if x has no leaves but y does, print **|00|114
        
        # combine and sort dictionary keys from both x_stemplot and y_stemplot
        for em in sorted(set(x_stemplot.keys()).union(set(y_stemplot.keys()))):  
            
            # offset, spacer used to justify print output
            offset = max([len(val) for val in x_stemplot.values()])  
            spacer = '*'*offset
            
            try: 
                # x_leaves|stem|y_values
                print '\t', x_stemplot[em].rjust(offset) + '|' + em + '|' + y_stemplot[em] 
                
            except: 
                try: 
                    # x_leaves|stem|*****
                    print x_stemplot[em].rjust(offset) + '|' + em + '|' + spacer  
                    
                except: 
                    # ****|stem|y_values 
                    print spacer.rjust(offset) + '|' + em + '|' + y_stemplot[em]  
    

    else:
        # print single stemplot as column of stem|leaves
        for key in sorted(x_stemplot.keys()):
            print '\t' + key + '|' + x_stemplot[key]
    


def create_stemplot(x, integer_data=True, precision=2, l=True, p=True, leaf_order=False):
    """ 
    Return a dictionary where each key is a 'stem' and its associated value is a string of ordered 'leaves'. 
    
    Arguments: 
    x, the data, is a 1D list of integers or floats.
    integer_data is a Boolean denoting the datatype of x[i]; datatype is integer by default.
    precision is an integer specifying #digits for rounding x when integer_data=False. 
    l is a Boolean where l=True means to print a legend.
    p is a Boolean where p=True means to print the stemplot.
    leaf_order is a Boolean used only when create_stemplot() is called by compare_stemplots().
    """ 
    
    # converts data to integers by default
    if integer_data:
        x = [int(i) for i in x]
    
    
    # print legend for plot
    if l: print_legend(integer_data=integer_data)
        
        
    # pad x with leading or trailing zeros to align print_stemplot() output
    # round x to desired precision if integer_data = False
    x = pad_with_zeros(x, integer_data, precision=precision)    
    
    
    # construct stemplot from data
    stemplot = put_leaves_on_stems(x, precision, leaf_order)
      
        
    # print stemplot
    if p: print_stemplot(x_stemplot=stemplot)
        
        
    return stemplot
    
    
def compare_stemplots(x, y, integer_data=True, precision=2, l=True):
    """ No return value; function prints two stemplots that share their stem.
    
    Arguments: 
    x and y are two 1D lists of integers; can be floats or ints.
    integer_data is a Boolean denoting the datatype of x[i] and y[i].
    precision is an integer specifying #digits for rounding x, y when integer_data=False.
    l is a Boolean where l=True means to print a legend.
    """      
        
    # print legend for plot
    if l: print_legend(integer_data=integer_data, num_stemplots=2)
        
        
    # create stemplots
    # leaf_order is a Boolean used to mirror x data around the stem it shares with y
    x_stemplot = create_stemplot(x, integer_data=integer_data, precision=precision, p=False, l=False, leaf_order=True)
    y_stemplot = create_stemplot(y, integer_data=integer_data, precision=precision, p=False, l=False)
        
        
    # print stemplots together
    print_stemplot(x_stemplot, y_stemplot)
    


## CALL FUNCTIONS ON TEST DATA

#def create_stemplot(x, integer_data=True, precision=2, l=True, p=True, leaf_order=False):
x1_stemplot = create_stemplot(x1)

#def compare_stemplots(x, y, integer_data=True, precision=2, l=True):
x1_x2_stemplot = compare_stemplots(x1, x2)

#def create_stemplot(x, integer_data=True, precision=2, l=True, p=True, leaf_order=False):
y1_stemplot = create_stemplot(y1, integer_data=False, precision=2)

#def compare_stemplots(x, y, integer_data=True, precision=2, l=True):
y1_y2_stemplot = compare_stemplots(y1, y2, integer_data=False, precision=1)

