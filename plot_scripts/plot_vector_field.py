import pylab as pl
import numpy as np
import netCDF4
from scipy import stats
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point
'''
Use:

For plotting CESM/NorESM 2D wind vector data on pressure levels

For plotting climatology:
python plot_fields.py first_file  

For plotting difference (second_file-first_file):
python plot_fields.py first_file second_file
'''

# Manual settings

# Change level
plot_level=2

# Adjust density of vectors, 2 - every second, 3 - every third...
dens=4 

# Adjust vector length in plot
sc_len=200

############################################
# Scripts starts
############################################

first_file = pl.sys.argv[1]

var_u = 'U'
var_v = 'V'

# Read first netcdf file
id_nc1 = netCDF4.Dataset(first_file)
u1 = np.mean(id_nc1.variables[var_u][:,plot_level,:,:],axis=0)
v1 = np.mean(id_nc1.variables[var_v][:,plot_level,:,:],axis=0)
in_lat_nc1 =  id_nc1.variables['lat'][:]
in_lon_nc1 =  id_nc1.variables['lon'][:]
in_p_nc1   =  id_nc1.variables['lev'][:]

id_nc1.close()
# File closed

# Read second netcdf file
if len(pl.sys.argv) > 2:
   second_file = pl.sys.argv[2]
   print("File: " + second_file+"-"+ first_file+ ", variable: " + var_u,var_v )
   id_nc2 = netCDF4.Dataset(second_file)
   u2 = np.mean(id_nc2.variables[var_u][:,plot_level,:,:],axis=0)
   v2 = np.mean(id_nc2.variables[var_v][:,plot_level,:,:],axis=0)
   id_nc2.close()
else:
   print("File: " + first_file+ ", variable: " + var_u,var_v )



# If we are comparing files
if len(pl.sys.argv) > 2:
   u = u2-u1
   v = v2-v1
   # Calculate wind speed
   speed1=np.sqrt(u1*u1+v1*v1)
   speed2=np.sqrt(u2*u2+v2*v2)
   speed = speed2-speed1

# If there is only one file
else:
   u = u1
   v = v1
   # Calculate wind speed
   speed=np.sqrt(u1*u1+v1*v1)

# Pressure level in hPa, not Pa
lev = in_p_nc1[plot_level]/100.

# add cyclic point to avoid gap in plot
u_s,c_lon = add_cyclic_point(u,coord=in_lon_nc1)
v_s       = add_cyclic_point(v)
speed_s   = add_cyclic_point(speed)

# Create mesh for longitude and latitude
lons,lats=np.meshgrid(c_lon,in_lat_nc1)


# Adjust density of displayed vectors
yy=np.arange(0,len(in_lat_nc1)-1,dens)
xx=np.arange(0,len(c_lon)-1,dens)
# Indices of vectors to display
Y,X=np.meshgrid(yy,xx)


# For plotting monsoon region
y_min =-30 # -90
y_max = 60 #  90
x_min = 40 #-180
x_max =170 # 180


#======================================================================

def plot_vec(ax):

    # Plot contours for wind speed
    c = ax.contourf(lons,lats,speed_s,extend='both',transform=ccrs.PlateCarree())
    # Plot wind vectors
    q = ax.quiver(lons[Y,X],lats[Y,X],u_s[Y,X],v_s[Y,X],transform=ccrs.PlateCarree(),scale=sc_len)

    if len(pl.sys.argv) > 2:
        c.set_cmap('RdBu_r')
    else:
        c.set_cmap('Blues')
    # Add colourbar
    cb = plt.colorbar(c, orientation='horizontal')
    # Add key for vectors
    plt.quiverkey(q,0.9,1.03,10, '       10 m/s',labelpos='N')
    # Automatic title
    ax.set_title(str('%.0f'%lev)+'hPa wind speed (m/s)')



    # From cartopy ticker
    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
    ax.set_yticks([-90,-60,-30,0,30,60,90], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(number_format='.0f',degree_symbol='',dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.0f',degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    # Set area to plot
    ax.set_xlim(x_min,x_max)
    ax.set_ylim(y_min,y_max)

#-------------------------------------------------------------------------

# Create axes with cartopy map
ax=plt.subplot(1,1,1,projection=ccrs.PlateCarree())
ax.coastlines()
# Call plot_vec function
plot_vec(ax)
# Show plot
plt.show()
# Or save plot
#plt.savefig('fig.pdf')



