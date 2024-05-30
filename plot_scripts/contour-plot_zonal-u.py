"""
plot zonal mean zonal wind (U)
"""
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from   matplotlib.pylab import *
import matplotlib.colors as colors   # palette and co.

data=Dataset("N1850AER-example-data-press.nc")

# read lats, levs.
lats = data.variables['lat'][:]
levs = data.variables['lev'][:]
# read zonal wind speed
u = data.variables['U'][:,:,:,:]
u_za = np.mean(np.mean(u[:,:,:,:],axis=0),axis=2)

# contour levels
clevs = np.arange(-30.,40.,4.)

# create figure.
fig=plt.figure(figsize=(8,4.5))
ax = fig.add_axes([0.15,0.1,0.85,0.85])

# coutour plots
cs1 = contour(lats,levs,u_za,clevs,colors='k',linewidths=1.)
cs2 = contourf(lats,levs,u_za,clevs,cmap=plt.cm.RdBu_r)
ax2 = axis([-90., 90., max(levs), min(levs)])
xlabel('Latitude')
ylabel('Pressure')

# add colorbar
cb = colorbar(cs2, ticks=clevs)
cb.set_label('m s-1')

plt.title('Mean zonal wind speed (m s-1)')
plt.show()
