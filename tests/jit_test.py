from common import *
import collections


# From http://pythonhosted.org/pythran/MANUAL.html
def arc_distance(theta_1, phi_1, theta_2, phi_2):
    """
    Calculates the pairwise arc distance
    between all points in vector a and b.
    """
    temp = (np.sin((theta_2-theta_1)/2)**2
           + np.cos(theta_1)*np.cos(theta_2) * np.sin((phi_2-phi_1)/2)**2)
    distance_matrix = 2 * np.arctan2(np.sqrt(temp), np.sqrt(1-temp))
    return distance_matrix

@pytest.mark.skipif(sys.version_info < (3,6) and sys.version_info[0] != 2,
                    reason="no support for python3.5 (numba segfaults)")
def test_numba(ds):
    ds_original = ds.copy()
    #ds.columns['x'] = (ds.columns['x']*1).copy()  # convert non non-big endian for now
    expr = arc_distance(ds.y*1, ds.y*1, ds.y**2*ds.y, ds.x+ds.y)
    ds['arc_distance'] = expr
    print(expr)
    #assert ds.arc_distance.expression == expr.expression
    ds['arc_distance_jit'] = ds['arc_distance'].jit_numba()
    assert ds.arc_distance.tolist() == ds.arc_distance_jit.tolist()
    # TODO: make it such that they can be pickled
    ds_original.state_set(ds.state_get())
    ds = ds_original
    assert ds.arc_distance.tolist() == ds.arc_distance_jit.tolist()
