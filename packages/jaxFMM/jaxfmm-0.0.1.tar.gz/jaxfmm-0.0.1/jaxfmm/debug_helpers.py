import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import jax.numpy as jnp
import jax.scipy as jsp
import jaxfmm.fmm as fmm
from math import isqrt

__all__ = ["print_stats", "plot_fmm_boxes"]

def print_stats(pts, idcs, rev_idcs, boxcenters, mpl_cnct, dir_cnct, n_split):
    r"""
    Print some basic information about the hierarchy.
    """
    print("----------------------------------------FMM Hierarchy Stats----------------------------------------")
    print("%i points, %i levels, %i children per box, %i charges per box"%(pts.shape[0],len(mpl_cnct)-1, 2**n_split, idcs.shape[1]))
    for i in range(len(mpl_cnct)):
        print("Total number of mpl interactions on level %i (with padding, fraction: %.2f): %i"%(i, mpl_cnct[i].size / (mpl_cnct[i]<mpl_cnct[i].shape[0]).sum(),mpl_cnct[i].size))
    print("Total number of dir interactions on max lvl (with padding, fraction: %.2f): %i"%(dir_cnct.size / (dir_cnct < dir_cnct.shape[0]).sum(),dir_cnct.size))
    print("Near field compression ratio (without padding):", (((dir_cnct<dir_cnct.shape[0]).sum()) * idcs.shape[1]**2) / (float(pts.shape[0])**2))
    memory_usage = idcs.nbytes + rev_idcs.nbytes + dir_cnct.nbytes
    for i in range(len(boxcenters)):
        memory_usage += boxcenters[i].nbytes + mpl_cnct[i].nbytes
    print("Total memory consumed by the hierarchy: %.2e Bytes"%memory_usage)
    print("---------------------------------------------------------------------------------------------------")

def plot_box(center, L, ax, facecolor='cyan', edgecolor='k', alpha=0.25):
    r"""
    Plot a single box in the given ax.
    """
    faces = []
    for perm in range(3):   # for the 3 coordinate axes
        faces.append([])
        faces.append([])
        for id in [(-1,-1), (1,-1), (1,1), (-1,1)]: # we generate 4 points on each side
            shift = jnp.array([-1,id[0],id[1]])
            shift2 = jnp.array([1,id[0],id[1]])

            start = center + L/2 * shift[(jnp.arange(3,dtype=int)+perm)%3]
            end = center + L/2 * shift2[(jnp.arange(3,dtype=int)+perm)%3]

            faces[-2].append(start)
            faces[-1].append(end)
        faces[-2].append(faces[-2][0])
        faces[-1].append(faces[-1][0])
    faces = jnp.array(faces)
    ax.add_collection3d(Poly3DCollection(faces, facecolors=facecolor, linewidths=0.5, edgecolors=edgecolor, alpha=alpha))

def plot_fmm_boxes(pts, boxcenters, boxlens, level, show_wellsep=None, mpl_cnct=None, dir_cnct=None, n_split=3, elev=45, azim=45, roll=0, fname=None, plot_all=False):
    r"""
    Plot the hierarchy.
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_box_aspect((jnp.ptp(pts[:,0]), jnp.ptp(pts[:,1]), jnp.ptp(pts[:,2])))    # setting equal aspect ratio so we see the true shape of objects

    nboxs = (2**n_split)**level
    colors = plt.cm.jet(jnp.linspace(0,1,nboxs))
    plot_all = plot_all or show_wellsep is None # if there is no show_wellsep set, we always plot everything
    for i in range(nboxs):
        if(show_wellsep is not None):
            if(i==show_wellsep):
                color = 'red'
            elif(show_wellsep in mpl_cnct[level][i]):
                color = 'green'
            elif(level==(len(boxcenters)-1) and dir_cnct is not None and show_wellsep in dir_cnct[i]):
                color = 'blue'
            else:
                color = 'gray'
        else:
            color = colors[i]
        if(plot_all or color == 'blue' or color == 'red' or color=="green"):
            plot_box(boxcenters[level][i],boxlens[level][i],ax,facecolor=color,alpha=0.5)
    
    plt.axis('off') 
    ax.view_init(elev=elev, azim=azim, roll=roll)
    plt.tight_layout()
    plt.show()
    if(fname is not None):
        fig.savefig(fname,transparent=True,bbox_inches='tight',dpi=300)
    return fig, ax

def eval_multipole(coeff, boxcenter, eval_pts):
    r"""
    Evaluate a single multipole expansion.
    """
    p = get_deg(coeff.shape[-1])
    sing = fmm.eval_singular_basis(eval_pts - boxcenter,p)
    res = jnp.zeros(eval_pts.shape[0])
    for n in range(p+1):
        for m in range(-n,n+1):
            if(m!=0):
                res += (-1)**n * 2 * coeff[...,fmm.mpl_idx(m,n)] * sing[...,fmm.mpl_idx(-m,n)]
            else:
                res += (-1)**n * coeff[...,fmm.mpl_idx(m,n)] * sing[...,fmm.mpl_idx(-m,n)] 
    res /= (4*jnp.pi)
    return res

def get_local_expansions(pts, chrgs, exp_centers, p):
    r"""
    Generate local expansions.
    """
    dist = pts[None,...] - exp_centers[:,None,:]
    coeff = (fmm.eval_singular_basis(dist,p) * chrgs[None,:,None]).sum(axis=1)
    return coeff

def binom(x, y):
  return jnp.exp(jsp.special.gammaln(x + 1) - jsp.special.gammaln(y + 1) - jsp.special.gammaln(x - y + 1))

def gen_multipole_dist(m, n, eps = 0.5):
    r"""
    Generate a point charge distribution corresponding to a specific multipole moment (Majic, Matt. (2022). Point charge representations of multipoles. European Journal of Physics. 43. 10.1088/1361-6404/ac578b.)
    """
    if(m == 0):   # axial
        k = jnp.arange(-n, n+1, 2)
        chrgs = (-1)**((n-k)/2) * binom(n, (n-k)/2.0) / (jsp.special.factorial(n) * (2*eps)**n)
        pts = jnp.zeros((k.shape[0],3))
        pts = pts.at[:,2].set(k*eps)
    else:         # (stacked) bracelet
        rotate = m < 0
        m = abs(m)      # we work with the real basis and rotate later
        knum = n-m+1
        jnum = 2*m
        j = jnp.tile(jnp.arange(jnum),knum)
        k = jnp.repeat(jnp.arange(-n+m,n-m+1,2),jnum)
        phi = (j-0.5) * jnp.pi/m if rotate else j * jnp.pi/m
        pts = jnp.array([eps*jnp.cos(phi), eps*jnp.sin(phi), k*eps]).T
        chrgs = 4**(m-1) * jsp.special.factorial(m-1) / ((2*eps)**n * jsp.special.factorial(n-m)) * (-1)**((n-m-k)/2 + j) * binom(n-m,(n-m-k)/2)
    return pts, chrgs

def get_deg(N_coeff):
    r"""
    Get the degree p of a multipole expansion from the number of coefficients.
    """
    return isqrt(N_coeff) - 1