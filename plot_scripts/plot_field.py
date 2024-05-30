import pylab as pylab
import numpy as np
import netCDF4
from scipy import stats
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point
'''
Use:

For plotting 2D scalar data

For plotting climatology:
python plot_fields.py first_file variable 

For plotting difference (second_file-first_file):
python plot_fields.py first_file variable second_file
'''

# Some manual settings

# Manual plotting/colourbar range
#opm=True
opm=False

# Max/min range/colourbar
# These are only active if opm=True
p_max_m=1
p_min_m=-p_max_m

# Manual figure title settings
title_m = False
# Only active if title_m = True
var_name_m = 'string'
unit_m = 'Wm$^{-2}$'

#############################################
# Script starts
#############################################

def frexp10(x):
   # Function for automatic colourbar range
   exp = pylab.rint(pylab.math.log10(abs(x)))
   mant = x/10**exp
   if int(mant)==0:
      mant=mant*10
      exp=exp-1
   return mant, exp

# Read command-line arguments
first_file = pylab.sys.argv[1]
var_name = pylab.sys.argv[2]

# Read first netcdf file
id_nc1 = netCDF4.Dataset(first_file)
in_var1 = np.mean(id_nc1.variables[var_name][:,:,:],axis=0)
in_lat_nc1 =  id_nc1.variables['lat'][:]
in_lon_nc1 =  id_nc1.variables['lon'][:]
in_unit =  id_nc1.variables[var_name].units
id_nc1.close()
# File closed

# Print variable dimensions
print(in_var1.shape)

# Read second netcdf file if there are 3 command line arguments
if len(pylab.sys.argv) > 3:
   second_file = plab.sys.argv[3]
   print("File: " + second_file+"-"+ first_file+ ", variable: " + var_name )
   id_nc2 = netCDF4.Dataset(second_file)
   in_var2 = np.mean(id_nc2.variables[var_name][:,:,:],axis=0)
   id_nc2.close()
else:
   print("File: " + first_file+ ", variable: " + var_name )

# Calculate global average and range

# If 2 files, calculate difference
if len(pylab.sys.argv) > 3:
   var = (in_var2 - in_var1)
   var_ave = np.average(np.average(var,1),weights=np.cos(np.pi*in_lat_nc1/180.))
   var_min = np.amin(var)
   var_max = np.amax(var)
   if abs(var_max)>abs(var_min):
      mant, exo = frexp10(var_max)
   else:
      mant1, exo = frexp10(var_min)
      mant = -mant1

# If 1 file, plot field
else:
   var = in_var1.copy()
   var_ave = np.average(np.average(var,1),weights=np.cos(np.pi*in_lat_nc1/180.))
   var_max = np.amax(var)
   mant, exo = frexp10(var_max)
   var_min = np.amin(var)
   if var_min == 0:
      mant2=0
      exo2=0
   else:
      mant2, exo2 = frexp10(var_min)

# add cyclic point to avoid gap in plot
c_var,c_lon = add_cyclic_point(var,coord=in_lon_nc1)


#======================================================================
# Define PLOT: 2D plot with map
def plot_map(ax_in, var_in):

    # Range for diffplot
    if len(pylab.sys.argv) > 3:
       if mant > 0:
          p_max = np.fix(mant)*np.power(10,exo)
          p_min =-p_max
          p_delta = float( p_max/5.)
       else:
          p_min = np.fix(mant)*np.power(10,exo)
          p_max =-p_min

    # Range for climatology
    else:
       p_max = np.fix(mant)*np.power(10,exo)
       p_min = np.fix(mant2)*np.power(10,exo2)

    # If range is set manually
    if opm == True:
       p_max=p_max_m  
       p_min=p_min_m  
    # Contour levels

    # Contour levels
    lvls = np.linspace(p_min,p_max,11)

    # Plot contours
    c = ax_in.contourf(c_lon,in_lat_nc1,var_in,levels=lvls,extend='both',transform=ccrs.PlateCarree())

    # If manual title
    if title_m:
        var_name_t = var_name_m
        unit_t =unit_m
    # Automatic title
    else:
        var_name_t = var_name
        unit_t =in_unit
    if len(pylab.sys.argv) > 3:
        c.set_cmap('RdBu_r')
        title("$\Delta$"+ var_name_t+': '+str('%.2f'%var_ave)+' '+unit_t)
    else:
        c.set_cmap('Blues')
        plt.title(var_name_t+': '+str('%.2f'%var_ave)+' '+unit_t)

    # Add colourbar
    cb = pylab.colorbar(c, orientation='horizontal')
    #colorbar_lab = ''
    #cb.set_label(colorbar_lab)



    # From cartopy ticker
    ax_in.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
    ax_in.set_yticks([-90,-60,-30,0,30,60,90], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(number_format='.0f',degree_symbol='',dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.0f',degree_symbol='')
    ax_in.xaxis.set_major_formatter(lon_formatter)
    ax_in.yaxis.set_major_formatter(lat_formatter)
#-----------------------------------------------------------------------------------



# Creat axes with cartopy map
ax=plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=0))
ax.coastlines()
# Call plot_map function
plot_map(ax,c_var)
# Show plot
plt.show()
# Or save plot
#plt.savefig('fig.pdf')

