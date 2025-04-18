from .sbgeom_cpp import * 
import h5py
import numpy as np
import plotly.graph_objects as go
from .VMEC import _d_arc_length_8
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_trapezoid

def Discrete_Coil_Set_From_HDF5(filename : str, dataset = "Dataset1"):
    '''
    Creates a coil set from an HDF5 file

    Parameters:
        filename (str) : HDF5 file
        dataset        : Dataset in HDF5 file
    Returns:
        Coil_Set : Coil_Set with Discrete Coil objects

    The HDF5 is expected to have a structure where in the 'dataset' is 
    a 3D array as (coil, vertex, cartesian coordinate).

    '''
    with h5py.File(filename,"r") as f:
        vertices = np.array(f[dataset])
    coils = []
    for i in range(vertices.shape[0]):
        coils.append(Discrete_Coil(vertices[i,:,:]))
    return Coil_Set(coils)

def Fourier_Coil_Set_From_HDF5(filename : str):
    '''
    Creates a Fourier coil set from an HDF5 file

    Parameters:
        filename (str) : HDF5 file

    Returns:
        Coil_Set: Coil_Set with Fourier_Coil objects

    The HDF5 is expected to contain a dataset 'Number_of_Coils'
    with the number of coils. Then, it is expected to have that number of datasets
    [Coil_0, Coil_1, ... ], 
    which should contain:
        - A 2D array Fourier_Cos (fourier, cartesian coordinate)
        - A 2D array Fourier_Sin (fourier, cartesian coordinate)
        - A vector (1D) array Centre (cartesian coordinate).
    
    '''
    coils = []
    with h5py.File(filename) as f:
        for i in range(np.array(f['Number_of_Coils'])[0]):
            coili = f['Coil_' + str(i)]
            coils.append(Fourier_Coil(np.array(coili['Fourier_Cos']), np.array(coili["Fourier_Sin"]), np.array(coili["Centre"])))
    return Coil_Set(coils)

def Transform_Equal_Arclength(coil : Coil, ns : int , n_samples : int = None):
    '''
    Returns an equal-arclength sampled coordinate for a given coil.

    Parameters:
        coil (Coil) : coil to transform
        ns (int)    : number of samples required
        n_samples (int, optional) : number of samples used to reconstruct the arc-length function (default: None = 4*ns)
    Returns:
        required_theta (np.ndarray) : theta values for the equal-arclength sampling
    '''
    if n_samples is None:
        # n_samples is used to reconstruct the arc-length function: this arbitrary 4 seems to resolve it fairly well.
        n_samples = 4 * ns
    u_samples   = np.linspace(0,1, n_samples, endpoint=False)
    positions = coil.Position(u_samples)
    arc_length_samples = _d_arc_length_8(positions, u_samples)
    total_u_samples          = np.concatenate([u_samples, [1.0]])    
    total_arc_length_samples = np.concatenate([arc_length_samples,[arc_length_samples[0]]])
    cumulative_arclength     = cumulative_trapezoid(total_arc_length_samples, total_u_samples, initial=0.0)    

    interpolated_inverse     = CubicSpline(cumulative_arclength, total_u_samples)
        
    desired_arclengths       = np.linspace(0, cumulative_arclength[-1], ns, endpoint=False) 
    required_theta           = interpolated_inverse(desired_arclengths)            
    return required_theta


def Convert_to_Fourier_Coils(coilset_cpp : Coil_Set, Nftrunc : int = None, equal_arclength : bool = False):
    '''
    Converts a Coil_Set to a Fourier representation

    Parameters:
        coilset_cpp (Coil_Set)  : original Coil_Set
        Nftrunc (int, optional) : number of harmonics kept (default: None = all harmonics)
    Returns:
        Coil_Set                : Coil_Set with Fourier_Coil objects.
    
    The number of samples is given by the original coil set, as with 
    Discrete_Coil objects the maximum is set by the number of vertices.
    '''
    coils = []
    for i in range(coilset_cpp.Number_of_Coils()):
        xyz = coilset_cpp[i].Return_Sampling_Curve()
        nsamples = xyz.shape[0]
        
        if equal_arclength:
            # Get the new theta values
            nsamples = nsamples * 2
            required_theta = Transform_Equal_Arclength(coilset_cpp[i], nsamples)
            # Interpolate the original coil to get the new positions
            xyz = coilset_cpp[i].Position(required_theta)

        def convert_to_cos_sin_centre(loc):
            loc_f = np.fft.rfft(loc)
            N = loc.shape[0]
            loc_f_cos = np.real( 2 * loc_f[1:] / N)[:Nftrunc]
            loc_f_sin = - np.imag( 2 * loc_f[1:] / N)[:Nftrunc]
            if N%2 == 0 and Nftrunc is None:                
                loc_f_cos[-1] = loc_f_cos[-1] / 2.0
                loc_f_sin[-1] = loc_f_sin[-1] / 2.0
            loc_centre    = np.real(loc_f[0] / N)
            return loc_f_cos, loc_f_sin, loc_centre

        x_cos, x_sin, x_centre =convert_to_cos_sin_centre(xyz[:,0])
        y_cos, y_sin, y_centre =convert_to_cos_sin_centre(xyz[:,1])
        z_cos, z_sin, z_centre =convert_to_cos_sin_centre(xyz[:,2])

        xyz_c = np.vstack([x_cos, y_cos, z_cos]).T
        xyz_s = np.vstack([x_sin, y_sin, z_sin]).T
        centr = np.array([x_centre, y_centre, z_centre])

        coils.append(Fourier_Coil(xyz_c, xyz_s, centr))
    return Coil_Set(coils)

def Plot(fig, coil : Coil, nt_samples = 100, line= {}, marker = {}, **kwargs):
    '''
    Plot the filament of a single Coil.
    Parameters:
        fig  (plotly figure) : figure to plot in
        coil (Coil)          : Coil to plot
        nt_samples (int, optional) : number of points in filament (default 100)
        line (dict)          : line dictionary for Scatter3d
        marker(dict)         : marker dictionary for Scatter3d
        kwargs               : kwargs for add_trace method of the plotly figure
    
    The {name, showlegend,mode} kwargs are passed to the Scatter3d directly. 
    '''
    posxyz = coil.Position(np.linspace(0,1, nt_samples))
    name_dict = {}
    scatter_prop = {"name" : "", "showlegend" : False, "mode" : "lines"}
    for key in scatter_prop.keys():        
        if key in kwargs:
            scatter_prop[key] = kwargs[key]
            kwargs.pop(key)
    fig.add_trace(go.Scatter3d( x = posxyz[:,0], y = posxyz[:,1], z = posxyz[:,2], line=line, marker=marker, **scatter_prop, ), **kwargs)

def Plot_Set(fig, coilset : Coil_Set, nt_samples = 100, line ={}, marker ={}, **kwargs):
    '''
    Plot the filament of all Coils in the Coil_Set.
    Parameters:
        fig  (plotly figure) : figure to plot in
        coil (Coil_Set)      : Coil to plot
        nt_samples (int, optional) : number of points in filament (default 100)
        line (dict)          : line dictionary for Scatter3d
        marker(dict)         : marker dictionary for Scatter3d
        kwargs               : kwargs for add_trace method of the plotly figure
    
    The {name, showlegend,mode} kwargs are passed to the Scatter3d directly. 
    '''
    for coil in coilset:
        Plot(fig, coil,nt_samples, line, marker, **kwargs)