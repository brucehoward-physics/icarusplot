## ICARUS Plot Style Definitions
## 2024 - version 1.0, work in progress led by Bruce Howard, Jaesung Kim, Justin Mueller
##
## Thanks to the DUNE MPLSTYLE FILE for guidance in our mplstyle file
## Thanks to various other sources and documentation for help in using some of the functions

import matplotlib.pyplot as plt
import numpy as np
import os

#######################
## Load the style file

envvar=str(os.getenv('PYTHONPATH'))
pypath=envvar.split(':')
for i in pypath:
    if i.find('icarusplot')>=0:
        print("@@ Importing mplstyle from %s"%(i+'/icarus_style.mplstyle'))
        plt.style.use(i+'/icarus_style.mplstyle')
        break

#######################
## Plot labeling

def ICARUSMCPreliminary(_axis):
    _yrange = _axis.get_ylim()
    _use_y = _yrange[1] + 0.025*(_yrange[1] - _yrange[0])
    _xrange = _axis.get_xlim()
    _use_x = _xrange[0] + 0.025*(_xrange[1] - _xrange[0])    
    _axis.text( x=_use_x, y=_use_y, s=r'$\bf{ICARUS}$ Simulation Preliminary', fontsize=14, color='blue' )

def ICARUSDataPreliminary(_axis):
    _yrange = _axis.get_ylim()
    _use_y = _yrange[1] + 0.025*(_yrange[1] - _yrange[0])
    _xrange = _axis.get_xlim()
    _use_x = _xrange[0] + 0.025*(_xrange[1] - _xrange[0])    
    _axis.text( x=_use_x, y=_use_y, s=r'$\bf{ICARUS}$ Data Preliminary', fontsize=14, color='#d67a11' )

def ICARUSMC(_axis):
    _yrange = _axis.get_ylim()
    _use_y = _yrange[1] + 0.025*(_yrange[1] - _yrange[0])
    _xrange = _axis.get_xlim()
    _use_x = _xrange[0] + 0.025*(_xrange[1] - _xrange[0])    
    _axis.text( x=_use_x, y=_use_y, s=r'$\bf{ICARUS}$ Simulation', fontsize=14, color='blue' )

def ICARUSData(_axis):
    _yrange = _axis.get_ylim()
    _use_y = _yrange[1] + 0.025*(_yrange[1] - _yrange[0])
    _xrange = _axis.get_xlim()
    _use_x = _xrange[0] + 0.025*(_xrange[1] - _xrange[0])
    _axis.text( x=_use_x, y=_use_y, s=r'$\bf{ICARUS}$ Data', fontsize=14, color='#d67a11' )

def POT(_axis,_pot):
    _yrange = _axis.get_ylim()
    _use_y = _yrange[1] + 0.02*(_yrange[1] - _yrange[0])
    _xrange = _axis.get_xlim()
    _use_x = _xrange[1] - 0.02*(_xrange[1] - _xrange[0])
    _use_pot = _pot/1.0e20
    _axis.text( x=_use_x, y=_use_y, s='{:0.2}'.format(_use_pot)+r'$\times 10^{20}$'+' POT',\
                fontsize=13, color='black', horizontalalignment='right' )

#######################
## Ratio canvas

def RatioCanvas(_title='null'):
    fig, axs = plt.subplots(2, sharex=True, height_ratios=[0.7,0.3])
    fig.subplots_adjust(hspace=0)
    fig.align_ylabels()
    if _title!='null':
        axs[0].set_title(_title)
    axs[1].set_ylim(0.65,1.35)
    return fig, axs

def UnityLine(_axis):
    _xrange = _axis.get_xlim()
    _axis.plot(np.linspace(_xrange[0],_xrange[1],1001),np.ones(1001),'--',color='gray')

#######################
## RECO VS TRUE: column-normalized, sylized plots

def makeColumnNormHist(_inH2D):
    _entries = _inH2D[0]
    _xbins = _inH2D[1]
    _ybins = _inH2D[2]
    _halfDX = np.array([ (_xbins[i+1]-_xbins[i])/2. for i in range(len(_xbins)-1) ])
    _halfDY = np.array([ (_ybins[i+1]-_ybins[i])/2. for i in range(len(_ybins)-1) ])
    _xentries = []
    _yentries = []
    _weights = []
    for i in range(len(_xbins)-1):
        wts = _entries[i]/np.sum(_entries[i])
        for j in range(len(wts)):
            _weights.append(wts[j])
    for i in range(len(_xbins)-1):
        for j in range(len(_ybins)-1):
            _xentries.append(_xbins[i]+_halfDX[i])
            _yentries.append(_ybins[j]+_halfDY[j])
    return _xentries, _yentries, _weights, _xbins, _ybins

def RecoVTrue(_axis, _inNPH2D, _xlabel='', _ylabel=''):
    _xvals, _yvals, _weights, _xbins, _ybins = makeColumnNormHist(_inNPH2D)

    _cts, _xb, _yb, _im = _axis.hist2d( _xvals, _yvals, weights=_weights, bins=[_xbins,_ybins], cmap='Reds' )
    _axis.set_xlabel(_xlabel)
    _axis.set_ylabel(_ylabel)

    # Draw the lines...
    _x_arr = np.linspace(_xb[0],_xb[-1],1001)
    _y_arr = np.linspace(_yb[0],_yb[-1],1001)

    for i in range(len(_xb)):
        _axis.plot(_xb[i]*np.ones(1001),_y_arr,color='black')
    for i in range(len(_yb)):
        _axis.plot(_x_arr,_yb[i]*np.ones(1001),color='black')

    # Write the numbers
    for idxX in range(len(_xb)-1):
        for idxY in range(len(_yb)-1):
            xtxt = _xb[idxX]+(0.2*(_xb[idxX+1]-_xb[idxX]))
            ytxt = _yb[idxY]+(0.2*(_yb[idxY+1]-_yb[idxY]))
            # if the bin is more than 20% of the total x-span, instead use 0.4 scale
            if (_xb[idxX+1]-_xb[idxX])/(_xb[-1]-_xb[0]) > 0.2:
                xtxt = _xb[idxX]+(0.4*(_xb[idxX+1]-_xb[idxX]))
            if (_yb[idxY+1]-_yb[idxY])/(_yb[-1]-_yb[0]) > 0.2:
                ytxt = _yb[idxY]+(0.4*(_yb[idxY+1]-_yb[idxY]))
            if _cts[idxX][idxY] < 0.65*np.max(_cts):
                _axis.text( x=xtxt, y=ytxt, s='{:.1%}'.format(_cts[idxX][idxY]), color='black', fontsize=16 )
            else:
                _axis.text( x=xtxt, y=ytxt, s='{:.1%}'.format(_cts[idxX][idxY]), color='white', fontsize=16 )

    _axis.set_xlim(_xb[0],_xb[-1])
    _axis.set_ylim(_yb[0],_yb[-1])

def RecoVTrue_ReturnIm(_axis, _inNPH2D, _xlabel='', _ylabel=''):
    _xvals, _yvals, _weights, _xbins, _ybins = makeColumnNormHist(_inNPH2D)

    _cts, _xb, _yb, _im = _axis.hist2d( _xvals, _yvals, weights=_weights, bins=[_xbins,_ybins], cmap='Reds' )
    _axis.set_xlabel(_xlabel)
    _axis.set_ylabel(_ylabel)

    # Draw the lines...
    _x_arr = np.linspace(_xb[0],_xb[-1],1001)
    _y_arr = np.linspace(_yb[0],_yb[-1],1001)

    for i in range(len(_xb)):
        _axis.plot(_xb[i]*np.ones(1001),_y_arr,color='black')
    for i in range(len(_yb)):
        _axis.plot(_x_arr,_yb[i]*np.ones(1001),color='black')

    # Write the numbers
    for idxX in range(len(_xb)-1):
        for idxY in range(len(_yb)-1):
            xtxt = _xb[idxX]+(0.2*(_xb[idxX+1]-_xb[idxX]))
            ytxt = _yb[idxY]+(0.2*(_yb[idxY+1]-_yb[idxY]))
            # if the bin is more than 20% of the total x-span, instead use 0.4 scale
            if (_xb[idxX+1]-_xb[idxX])/(_xb[-1]-_xb[0]) > 0.2:
                xtxt = _xb[idxX]+(0.4*(_xb[idxX+1]-_xb[idxX]))
            if (_yb[idxY+1]-_yb[idxY])/(_yb[-1]-_yb[0]) > 0.2:
                ytxt = _yb[idxY]+(0.4*(_yb[idxY+1]-_yb[idxY]))
            if _cts[idxX][idxY] < 0.65*np.max(_cts):
                _axis.text( x=xtxt, y=ytxt, s='{:.1%}'.format(_cts[idxX][idxY]), color='black', fontsize=16 )
            else:
                _axis.text( x=xtxt, y=ytxt, s='{:.1%}'.format(_cts[idxX][idxY]), color='white', fontsize=16 )

    _axis.set_xlim(_xb[0],_xb[-1])
    _axis.set_ylim(_yb[0],_yb[-1])

    return _im
