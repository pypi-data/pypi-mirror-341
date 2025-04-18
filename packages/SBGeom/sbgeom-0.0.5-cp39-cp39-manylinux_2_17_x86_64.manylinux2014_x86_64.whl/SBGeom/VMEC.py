from .sbgeom_cpp import Flux_Surfaces, Flux_Surface_Settings, Flux_Surfaces_Fourier_Extended
import h5py
import numpy as np
import math
import plotly.graph_objects as go
import warnings
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_trapezoid
from typing import Callable
from functools import partial
def read_vmec(filename : str):
    '''
    Reads a VMEC nc4 file (or HDF5)

    Parameters:
        filename (str) : filename
    Returns:
        Rmnc (2D Array[Number of surfaces, vmec_i]): R array
        Zmns (2D Array[Number of surfaces, vmec_i]): Z array
        Flux_Surface_Settings: settings(number of surfaces, ntor, mpol, symmetry)

    
    '''
    with h5py.File(filename) as f:
        Rmnc     = np.array(f['rmnc'])
        Zmns     = np.array(f['zmns'])
        ntor_vec = np.array(f['xn'])
        
        
        m_pol    = int(np.array(f['mpol']))
        n_tor    = int(np.array(f['ntor']))
        no_surf  = int(np.array(f['ns']))
        symm     = int(ntor_vec[1])
    return Rmnc, Zmns, Flux_Surface_Settings(no_surf, n_tor, m_pol, symm)

def Flux_Surfaces_From_HDF5(filename : str):    
    '''
    Creates a Flux_Surfaces object from a file

    Parameters:
        filename(str) : VMEC nc4 filename
    Returns:
        Flux_Surfaces
    '''
    return Flux_Surfaces(*read_vmec(filename))


def mpol_vector(ntor : int, mpol : int):    
    return np.array([0 for i in range(ntor + 1)] + sum([[i for j in range(2 * ntor + 1)]for i in range(1, mpol )], []), dtype=int)

def ntor_vector(ntor : int, mpol : int, symm : int):
    return np.array(list(range(0, (ntor + 1) * symm , symm)) + sum([list(range(-ntor * symm, (ntor + 1) * symm, symm)) for i in range(mpol - 1)], []), dtype=int)

def ntor_mpol_vectors(ntor, mpol, symm):
    return ntor_vector(ntor, mpol,symm), mpol_vector(ntor,mpol)


def _Convert_CosSin_to_VMEC_R(xckl, xcmkl, xskl, xsmkl):
    mpol = xckl.shape[0]  # mpol needs to be 1 higher than maximum because vmec
    ntor = xckl.shape[1] - 1
        
    ntor_vec, mpol_vec = ntor_mpol_vectors(ntor, mpol, 1) # symm not necessary here
    
    R_a = np.zeros(mpol_vec.shape)
    
    for i, mi_ni in enumerate(zip(mpol_vec, ntor_vec)):
        m = mi_ni[0]
        n = mi_ni[1]
        if m == 0 and n == 0:
            R_a[i] = xckl[0,0] + xcmkl[0,0]
        elif m == 0 and n > 0:
            R_a[i] = xckl[0,n] + xcmkl[0,n]
        elif m > 0 and n < 0:
            R_a[i] = xckl[m,abs(n)]
        elif m >0 and n ==0:
            R_a[i] = xckl[m,0] + xcmkl[m,0]
        elif m > 0 and n  > 0 :
            R_a[i] = xcmkl[m, n]
        else:

            raise Exception("SHOULDN'T HAPPEN")
    return R_a,  ntor, mpol

def _Convert_CosSin_to_VMEC_Z(xckl, xcmkl, xskl, xsmkl):
    mpol = xckl.shape[0]  # mpol needs to be 1 higher than maximum because vmec
    ntor = xckl.shape[1] - 1
        
    ntor_vec, mpol_vec = ntor_mpol_vectors(ntor, mpol, 1) # symm not necessary here
    
    Z_a = np.zeros(mpol_vec.shape)    
    
    for i, mi_ni in enumerate(zip(mpol_vec, ntor_vec)):
        m = mi_ni[0]
        n = mi_ni[1]
        if m == 0 and n == 0:
            Z_a[i] = 0
        elif m == 0 and n > 0:            
            Z_a[i] = - xskl[0,n] + xsmkl[0,n]
        elif m > 0 and n < 0:            
            Z_a[i] =  xskl[m,abs(n)]
        elif m >0 and n ==0:            
            Z_a[i] = xskl[m,0] + xsmkl[m,0]
        elif m > 0 and n  > 0 :
            Z_a[i] = xsmkl[m, n]
        else:

            raise Exception("SHOULDN'T HAPPEN")
    return Z_a,  ntor, mpol



def _Calculate_CosSin_From_DFT(DFT_coefficients, N, M):
    N_h = math.floor(N/2) + 1
    M_h = math.floor(M/2) + 1    
    # x^c_{kl}
    def Divide_Nyquist(arr, N, M):
        if N%2 == 0:
            arr[-1, :] = arr[-1, :] / 2.0
        if M%2 == 0:
            arr[:, -1] = arr[:,-1] / 2.0
        return arr

    # x^c_{kl}
    xckl  = 2 * np.real(DFT_coefficients[:N_h, :M_h])
    xckl[0,0] = xckl[0,0] / 2.0
    xckl = Divide_Nyquist(xckl, N , M)
    
    # x^{c-}_{kl}
    xcmkl  = np.zeros_like(xckl)
    xcmkl[1:, 1:] = 2 * np.real(DFT_coefficients[:, ::-1])[1:N_h , :M_h - 1 ]
    xcmkl = Divide_Nyquist(xcmkl, N, M)
    
    # x^s_{kl} 
    xskl = - 2 * np.imag(DFT_coefficients[:N_h,:M_h])
    # the corners are already zero by virtue of the Nyquist sampling
    xskl = Divide_Nyquist(xskl, N, M)
    

    # x^{s-}_{kl}
    xsmkl = np.zeros_like(xskl)
    xsmkl[1:, 1:] = - 2 * np.imag(DFT_coefficients[:,::-1])[1:N_h,:M_h - 1]
    xsmkl = Divide_Nyquist(xsmkl, N, M)
    if N%2 == 0:
        xsmkl[-1, :] = xsmkl[-1, :] * -1.0
    return xckl, xcmkl, xskl, xsmkl

def _Scaled_DFT(points):
    fft_s = np.fft.fft2(points)
    N = fft_s.shape[0]
    M = fft_s.shape[1]
    return np.fft.fft2(points) / N /M, N, M

def _CosSin_DFT(points):
    return _Calculate_CosSin_From_DFT(*_Scaled_DFT(points))


def RZ_Points_to_VMEC(points_2D_R, points_2D_Z, ntor = None, mpol = None):
    '''
    Creates Rmnc and Zmns coefficients in the VMEC format for an RZ point cloud.

        Parameters:
            points_2D_R(2D Array): R points
            points_2D_Z(2D Array): Z points
            ntor(int)            : ntor desired
            mpol(int)            : mpol desired
        Returns:
            Rmnc (1D array), Zmns (1D array), ntor (int), mpol(int)

    It is assumed that the first index corresponds to the poloidal angle, and the second to the toroidal angle. 
    Furthermore, since the discrete fourier transform is used, it is assumed that the points are uniformly spaced in both 
    angles. If not, the result will not exactly match the input point cloud.

    The resulting fourier coefficients are truncated to ntor, mpol if given.

    '''
    if(points_2D_R.shape != points_2D_Z.shape):
        raise Exception("Shape of R points " + str( points_2D_R.shape) +  " does not match shape of Z points " + str( points_2D_Z.shape)+"")
    Rmnc, ntor_obtained, mpol_obtained = _Convert_CosSin_to_VMEC_R(*_CosSin_DFT(points_2D_R))
    Zmns, ntor_obtained, mpol_obtained = _Convert_CosSin_to_VMEC_Z(*_CosSin_DFT(points_2D_Z))

    if ntor is None:
        ntor = ntor_obtained
        mpol = mpol_obtained

    Rmnc_conv = Convert_to_different_ntor_mpol(Rmnc[np.newaxis, :], ntor_obtained, mpol_obtained, ntor, mpol)[0,:]
    Zmns_conv = Convert_to_different_ntor_mpol(Zmns[np.newaxis, :], ntor_obtained, mpol_obtained, ntor, mpol)[0,:]

    return Rmnc_conv, Zmns_conv, ntor, mpol


def _truncate_VMEC(vmec_array, ntor_old, mpol_old, ntor_trunc, mpol_trunc):    
    symm_num = 1
    ntor_vec_old, mpol_vec_old = ntor_mpol_vectors(ntor_old, mpol_old, symm_num)
    boolean_arr = np.logical_and(np.abs(ntor_vec_old) <= ntor_trunc, np.abs(mpol_vec_old) < mpol_trunc)

    return vmec_array[:, boolean_arr]    

def _extend_VMEC(vmec_points, ntor_old, mpol_old, ntor_new, mpol_new):
    ntorv, mpolv = ntor_mpol_vectors(ntor_new, mpol_new, 1)
    mnarray = np.zeros((vmec_points.shape[0], ntorv.shape[0]), dtype= float)
    mnarray[:, np.logical_and(np.abs(ntorv) <= ntor_old, mpolv < mpol_old)] = vmec_points[:,:]
    return mnarray

def Convert_to_different_ntor_mpol(vmec_array, ntor_old : int, mpol_old : int, ntor_new : int, mpol_new : int):
    '''
    Converts a VMEC array (Rmnc, Zmns) to a different ntor, mpol number

        Parameters:
            vmec_array (1D array): array in VMEC format
            ntor_old (int): ntor of input array
            mpol_old (int): mpol of input array
            ntor_new (int): ntor of output array
            mpol_new (int): mpol of output array
        Returns:
            vmec_array (1D array): array in VMEC with ntor_new, mpol_new 
    '''
    if ntor_new >= ntor_old and mpol_new >= mpol_old:
        return _extend_VMEC(vmec_array, ntor_old, mpol_old, ntor_new, mpol_new)
    elif ntor_new < ntor_old and mpol_new < mpol_old:
        return _truncate_VMEC(vmec_array, ntor_old, mpol_old, ntor_new, mpol_new)
    elif ntor_new >= ntor_old and mpol_new < mpol_old:
        extended_ntor = _extend_VMEC(vmec_array, ntor_old, mpol_old, ntor_new, mpol_old)
        return _truncate_VMEC(extended_ntor, ntor_new, mpol_old, ntor_new, mpol_new)
    elif ntor_new < ntor_old and mpol_new >= mpol_old:
        extended_mpol = _extend_VMEC(vmec_array, ntor_old, mpol_old, ntor_old, mpol_new)
        return _truncate_VMEC(extended_ntor, ntor_new, mpol_new, ntor_old, mpol_new)
    else:
        raise Exception("Should not happen")
    

def Convert_VMEC_Extension_ntor_mpol(fs_ext : Flux_Surfaces_Fourier_Extended, ntor_new : int, mpol_new : int):
    '''
    Converts a Flux_Surfaces_Fourier_Extended to another ntor, mpol 

        Parameters:
            fs_ext: Flux_Surfaces_Fourier_Extended
            ntor_new (int): desired ntor
            mpol_new (int): desired mpol
        Returns:
            Flux_Surfaces_Fourier_Extended with ntor_new, mpol_new
    '''
    Rmnc_old = fs_ext.Rmnc_Extension()
    Zmns_old = fs_ext.Zmns_Extension()
    fs_settings = fs_ext.Flux_Surface_Settings_Extension()
    d_ext    = fs_ext.Extension_Labels()
    ntor_old = fs_settings.n_tor
    mpol_old = fs_settings.m_pol
    
    rmnc_new = Convert_to_different_ntor_mpol(Rmnc_old, ntor_old, mpol_old, ntor_new, mpol_new)
    zmns_new = Convert_to_different_ntor_mpol(Zmns_old, ntor_old, mpol_old, ntor_new, mpol_new)

    zmns_base = fs_ext.Zmns()
    rmnc_base = fs_ext.Rmnc()
    fs_settings_base   = fs_ext.flux_surface_settings()
    return Flux_Surfaces_Fourier_Extended(rmnc_base, zmns_base, fs_settings_base, d_ext, rmnc_new, zmns_new, Flux_Surface_Settings(rmnc_new.shape[0], ntor_new, mpol_new, fs_settings.symmetry))
    


def _VMEC_R(vmec_r, ntor, mpol, uu, vv, SYMM):
    mpvector, ntvector = ntor_mpol_vectors(ntor, mpol, SYMM)
    return np.sum(vmec_r[:, np.newaxis, np.newaxis] * np.cos( mpvector[:, np.newaxis, np.newaxis] * uu[np.newaxis, : , : ] - ntvector[:, np.newaxis, np.newaxis] * vv[np.newaxis, : , : ] ), axis=0)

def _VMEC_Z(vmec_z, ntor, mpol, uu, vv, SYMM):
    mpvector, ntvector = ntor_mpol_vectors(ntor, mpol, SYMM)
    return np.sum(vmec_z[:, np.newaxis, np.newaxis] * np.cos( mpvector[:, np.newaxis, np.newaxis] * uu[np.newaxis, : , : ] - ntvector[:, np.newaxis, np.newaxis] * vv[np.newaxis, : , : ] ), axis=0)


def Plot_Poloidal_Slice(fig, fs : Flux_Surfaces, s : float, LCFS_distance_label : float, phi : float, nu = 200,  line_kwargs = {}, **kwargs):
    '''
    Plot a poloidal slice using Plotly

    Parameters:
        fig         (Plotly figure): figure to plot in
        fs          (Flux_Surfaces): Flux_Surfaces to use
        s                   (float): s coordinate of slice
        LCFS_distance_label (float): distance label of slice
        phi                 (float): phi coordinate of slice
        nu              (int = 200): number of samples
        line_kwargs          (dict): dictionary of line options for plotly
        **kwargs                   : passed directly to the add_trace method


    {name, showlegend, mode} of the kwargs will be passed to the scatter graph object instead.
    '''

    RZPhi = fs.Return_Cylindrical_Position(s,LCFS_distance_label, np.linspace(0, 2 * np.pi,nu), phi )
    name_dict = {}
    mesh_prop = {"name" : "", "showlegend" : False, "mode" : "lines"}
    for key in mesh_prop.keys():        
        if key in kwargs:
            mesh_prop[key] = kwargs[key]
            kwargs.pop(key)
    fig.add_trace(go.Scatter(x=RZPhi[:,0], y=RZPhi[:,1], line = line_kwargs, **mesh_prop), **kwargs)

def Plot_Poloidal_Slice_Fig(fs : Flux_Surfaces, s : float, LCFS_distance_label : float, phi : float, fig_kwargs = {}, nu = 200, line_kwargs = {}, **kwargs):
    fig = go.Figure()
    fig_prop = {"autosize" : False, "width" : 600, "height" : 500}
    print(type(fig_kwargs))
    for key in fig_prop.keys():
        if key in fig_kwargs:
            fig_prop[key] = kwargs[key]
            fig_kwargs.pop(key)


    fig.update_layout(**fig_prop) 
    fig.update_xaxes(scaleanchor = "y", scaleratio = 1)
    
    Plot_Poloidal_Slice(fig, fs, s, LCFS_distance_label, phi, nu, line_kwargs, **kwargs)
    return fig



def _d_arc_length_8(line, u_line):    
    ''' 
    Uses 8th order central finite difference.
    No forward or backward is needed because it forms a closed loop.
    '''
    # assumes equispaced in u!
    du = u_line[1] - u_line[0]
    x = [np.roll(line,i, axis=0) for i in [0,1,2,3,4,-4,-3,-2,-1]]        
    result =  np.linalg.norm(1 /280 * x[-4] + -4 / 105 * x[-3] +  1/5 * x[-2] + -4/5 * x[-1] + 4/5 * x[1] + -1/5 * x[2] + 4/105 * x[3] + -1/280 * x[4], axis=1)  / du    
    return result 


def _transform_u_coords_equal_arclength_functions(fs : Flux_Surfaces, ntheta : int, phi : float, s : float, d : Callable, n_samples : int = None):
    '''
    Transforms theta coordinates to an equal-arclength theta coordinate.

    Parameters:
        fs (Flux_Surfaces): 
        ntheta (theta)    : number of theta required
        phi    (float)    : phi 
        s      (float)    : s coordinate
        d      (Callable) : LCFS distance label function, should have as signature d(u,v) with u,v arraylike.
        n_samples (int)   : Number of samples used for constructing interpolating function in integrand

    Returns:
        u_required        : required theta for equal-arc lengths.
    

    Arc length is |f'(x)|, with this derivative computed using 8th order finite differences using the samples that were computed in any case for the integration of the total arclength.

    Then, |f'(x)| is integrated using a cumulative trapezoid method, thus obtaining the total arc length as a function of theta. 

    To compute the set of theta that results in equal arc-length, the interpolating function is constructed, taking the total arclength as x and the input theta as y.
    This is then evaluated at linearly spaced arc lengths, yielding the required theta for equal arc lengths.
    '''
    if n_samples is None:
        # n_samples is used to reconstruct the arc-length function: this arbitrary 4 seems to resolve it fairly well.
        n_samples = 4 * ntheta    
    
    u_samples   = np.linspace(0,2 * np.pi, n_samples, endpoint=False)        
    phi_samples = np.ones_like(u_samples) * phi
    s_samples   = np.ones_like(u_samples) * s
    d_samples   = d(u_samples, phi_samples)    

    uline                    = fs.Return_Position(s_samples, d_samples, u_samples, phi_samples)                
    arc_length_samples       = _d_arc_length_8(uline, u_samples)
    total_u_samples          = np.concatenate([u_samples, [2 * np.pi]])    
    total_arc_length_samples = np.concatenate([arc_length_samples,[arc_length_samples[0]]])
    cumulative_arclength     = cumulative_trapezoid(total_arc_length_samples, total_u_samples, initial=0.0)    

    interpolated_inverse     = CubicSpline(cumulative_arclength, total_u_samples)
        
    desired_arclengths       = np.linspace(0,cumulative_arclength[-1],ntheta, endpoint=False) 
    required_theta           = interpolated_inverse(desired_arclengths)            
    return required_theta



def Get_Sampling_Curve(flux_surface, nus, nvs, distance_function, equal_arclength = False):                
    '''
        Returns a sampling curve for converting to VMEC format

            Parameters:
                flux_surface (Flux_Surfaces) : Flux Surfaces from which to sample
                nus  (int)                   : Number of poloidal samples
                nvs  (int)                   : Number of toroidal samples
                distance_function (Callable, float, int): function signifying distance from LCFS at u,v. Signature is d(u,v) with u,v arraylike. Passing float or int just uses that value for all u,v
                equal_arclength   (bool)     : whether the theta samples are transformed to yield equal arc lengths


            Returns:
                points_2D_R (Array[nus, nvs]): R points
                points_2D_Z (Array[nus, nvs]): Z points
                uu (Array[nus, nvs])         : u samples
                vv (Array[nus, nvs])         : v samples

        Note that the actual phi coordinate might not match the sampled toroidal angle. This is the case
        when using the naively normal extended surface : the curvature of the surface ensures that the normal
        vector has a component in the phi direction, such that the toroidal angle of the generated point does not match 
        the input toroidal angle. The surface will thus not exactly match the equi-distant normal surface if converted to VMEC format (since actual phi is different from equispaced phi
        as used in the DFT).
        
        If using the constant phi version of the normally extended surface, this is no issue (but this is considerably slower due to the need for Newton iterations on the point, although in most cases
        this is the difference between half a second or 2 seconds, so not an issue.)

        Stellarator symmetry is exploited:

        R(theta, phi) =   R(-theta, 2 * pi / symmetry - phi)
        Z(theta, phi) = - Z(-theta, 2 * pi / symmetry - phi)
        
    '''        
    s = 1.0
    if isinstance(distance_function, float) or isinstance(distance_function, int):
        dlabel = distance_function
        distance_function = lambda uu,vv: np.ones_like(uu) * dlabel
    
    
    symm = flux_surface.flux_surface_settings().symmetry

    u = np.linspace(0, 2 *np.pi, nus, endpoint = False)
    v = np.linspace(0, 2 *np.pi / symm, nvs, endpoint = False)
    # If nvs is even, the half module boundary is included and thus:    int(nvs/2) + 1
    # If nvs is odd, the half module boundary is not included and thus: int(nvs/2) + 1
    v_stellsymm = v[:int(nvs / 2) + 1] 
    
    uu, vv = np.meshgrid(u,v, indexing="ij")        

    uu_ss, vv_ss = np.meshgrid(u,v_stellsymm, indexing="ij")        
            
    if equal_arclength:
        for i, vi in enumerate(v_stellsymm):
            uu_ss[:,i] = _transform_u_coords_equal_arclength_functions(flux_surface, nus, vi, s, distance_function)                                

    points_ss        = flux_surface.Return_Position( (np.ones_like(uu_ss) * s).ravel(), distance_function(uu_ss.ravel(), vv_ss.ravel()),  uu_ss.ravel(), vv_ss.ravel()).reshape((vv_ss.shape[0],vv_ss.shape[-1], 3))        
    points_2D_R_ss   = np.sqrt(points_ss[:,:,0] ** 2 + points_ss[:,:,1] ** 2)
    points_2D_Z_ss   = points_ss[:,:,2]
    points_2D_phi_ss = np.arctan2(points_ss[:,:,1], points_ss[:,:,0])
    points_2D_R      = np.zeros((nus,nvs))
    points_2D_Z      = np.zeros((nus,nvs))
    points_2D_phi    = np.zeros((nus,nvs))
    
    for i, _ in enumerate(v_stellsymm):
        points_2D_R[:,i]   = points_2D_R_ss[:,i]
        points_2D_R[0,-i]  = points_2D_R_ss[0,i]
        points_2D_R[1:,-i] = points_2D_R_ss[::-1,i][:-1]

        points_2D_Z[:,i]   = points_2D_Z_ss[:,i]
        points_2D_Z[0,-i]  = -points_2D_Z_ss[0,i]
        points_2D_Z[1:,-i] = -points_2D_Z_ss[::-1,i][:-1]
        

        points_2D_phi[:,i]   = points_2D_phi_ss[:,i]
        if i > 0:
            points_2D_phi[0,-i]  = 2 * np.pi / symm - points_2D_phi_ss[0,i]
            points_2D_phi[1:,-i] = 2 * np.pi / symm - points_2D_phi_ss[::-1,i][:-1]        


    return points_2D_R, points_2D_Z, points_2D_phi, uu, vv
    

def Convert_to_Fourier_Extended(flux_surfaces : Flux_Surfaces, LCFS_distance_labels_list, nu_sample : int, nv_sample : int, LCFS_distance_labels_functions = None,  ntor = None, mpol = None, equal_arclength = False):
    '''
    Creates Fourier extende flux surfaces from a set of surfaces defined by distances from the LCFS, possibly functions of (theta, phi).

    Parameters:
        flux_surfaces (Flux_Surfaces)          : Flux_Surfaces of which LCFS is used
        LCFS_distance_labels_list (List[float]): List of LCFS distance labels. These are used for evaluating in the Return_Position like methods. 
                                                 i.e., if [0.2,1.0,2.0], evaluating Return_Position(1.0, 1.5, theta, phi) will yield the surface halfway between
                                                 the second and third LCFS_distance_labels_functions function.
        nu_sample (int)                        : poloidal samples (direct relation with resulting harmonics: mpol = ceil(nu_sample / 2))
        nv_sample (int)                        : toroidal samples (direct relation with resulting harmonics: ntor = ceil(nv_sample / 2))
        LCFS_distance_labels_functions (List[]): List of distance functions for each label in LCFS_distance_labels_list. Signature should be d(u,v), with u,v arraylike, or just a float. If not given, the labels are directly used as distances.
        ntor     (int)                         : output ntor
        mpol     (int)                         : output mpol
        equal_arglength : bool                 : whether the equal arc length transformation is used.

    
    '''
    if LCFS_distance_labels_functions is None:
        LCFS_distance_labels_functions = LCFS_distance_labels_list
    rmnc_list = []
    zmns_list = []
    for d_label, d_function in zip(LCFS_distance_labels_list, LCFS_distance_labels_functions):
        points_2D_R, points_2D_Z, points_2D_Phi, uu, vv = Get_Sampling_Curve(flux_surfaces, nus =nu_sample, nvs= nv_sample,  distance_function=d_function, equal_arclength=equal_arclength)
        if(np.max(np.abs(points_2D_Phi - vv)) > 1e-8):
            warnings.warn("Warning: sampling points phi differ from resulting phi (max = " + str(np.max(np.abs(points_2D_Phi - vv)))+"). Can result in poor Fourier fit.")
        
        Rmnc, Zmns, ntor_fit, mpol_fit = RZ_Points_to_VMEC(points_2D_R, points_2D_Z, ntor, mpol)
        rmnc_list.append(Rmnc)
        zmns_list.append(Zmns)
    return Flux_Surfaces_Fourier_Extended(flux_surfaces, np.array(LCFS_distance_labels_list), np.array(rmnc_list), np.array(zmns_list), Flux_Surface_Settings(len(LCFS_distance_labels_list), ntor_fit, mpol_fit, flux_surfaces.flux_surface_settings().symmetry))

from scipy.interpolate import CloughTocher2DInterpolator, RegularGridInterpolator

def Fit_From_Thickness_Points(points_theta, points_phi, thickness):
    '''
    Interpolator for thicknesses given as discrete  points in theta,phi space.
    Can be passed directly as a distance function for Convert_to_Fourier_Extended

    Parameters:
        points_theta : poloidal sample points
        points_phi   : toroidal sample points
        thickness    : value of distance from LCFS at each of the points

    Returns:
        d_function  : Callable(u,v) returning distance as a function of u,v
    '''
    points = np.stack([points_theta, points_phi], axis=-1)
    linpor = CloughTocher2DInterpolator(points, thickness)
    return linpor


def Fit_From_Thickness_Matrix(points_theta_1D, points_phi_1D, thickness_matrix, **kwargs):
    '''
    Interpolator for thicknesses given on a regular 2D grid
    Can be passed directly as a distance function for Convert_to_Fourier_Extended

    Parameters:
        points_theta_1D : poloidal sample points in 1D
        points_phi_1D   : toroidal sample points in 1D
        thickness       : value of distance from LCFS on the meshgrid of points_theta_1D, points_phi_1D
        **kwargs        : kwargs to be passed to the RegularGridInterpolator

    Returns:
        d_function  : Callable(u,v) returning distance as a function of u,v
    '''
    interpolate_func = RegularGridInterpolator((points_theta_1D, points_phi_1D), values=thickness_matrix, **kwargs)
    def Interpolator(u,v):
        return interpolate_func(np.stack([u,v], axis=-1))
    return Interpolator