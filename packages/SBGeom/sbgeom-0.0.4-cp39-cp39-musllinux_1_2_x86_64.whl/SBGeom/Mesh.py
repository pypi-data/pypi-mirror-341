from .sbgeom_cpp import Mesh
import meshio
import plotly.graph_objects as go
import numpy as np
def Meshio(mesh : Mesh):
    '''
    Converts SBGeom mesh to meshio Mesh.

    Parameters:
        mesh (SBGeom.Mesh): mesh to convert
    Returns:
        mesh (meshio.Mesh): output mesh
    '''
    mesh_names = ['0', 'vertex', 'line','triangle', 'tetra']
    vertices = mesh.vertices()
    return meshio.Mesh(mesh.positions(), [(mesh_names[vertices.shape[1]], vertices)])

def Plot(fig, mesh : Mesh, wireframe=False, surface=True, **kwargs):
    '''
    Plots a triangular mesh in a 3D plotly figure

    Parameters:
        fig : plotly figure
        mesh (SBGeom.Mesh)        : mesh to plot
        wireframe (bool,optional, default = False) : whether to plot wireframe of mesh (can be costly)
        surface (bool, optional, default = True) : whether to plot the surface
        **kwargs                  : are passed to fig.add_trace 

    The kwargs {name, color, opacity, showlegend} are passed to Scatter3d instead.
    '''
    pos = mesh.positions()
    verts = mesh.vertices()
    triangles = pos[verts]    

    mesh_prop = {"name" : "", "color" : 'lightblue', "opacity" : 1.0, "showlegend" : True}
    for key in mesh_prop.keys():        
        if key in kwargs:
            mesh_prop[key] = kwargs[key]
            kwargs.pop(key)
    if wireframe:
        list_x = np.full((triangles.shape[0], triangles.shape[1] + 1), np.nan)
        list_y = np.full((triangles.shape[0], triangles.shape[1] + 1), np.nan)
        list_z = np.full((triangles.shape[0], triangles.shape[1] + 1), np.nan)

        list_x[:,:-1] = triangles[:, :, 0]
        list_y[:,:-1] = triangles[:, :, 1]
        list_z[:,:-1] = triangles[:, :, 2]
        fig.add_trace(go.Scatter3d(x= list_x.ravel(), y = list_y.ravel(), z = list_z.ravel(), mode = 'lines', line =dict(color='black', width=3), showlegend=False), **kwargs)
    if surface:
        fig.add_trace(go.Mesh3d(x = pos[:,0], y = pos[:,1], z = pos[:,2], i = verts[:,0], j = verts[:,1], k = verts[:,2], **mesh_prop), **kwargs)
    
