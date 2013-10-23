cimport _pele
import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
cdef double _python_grad(_pele.Array x, _pele.Array grad, void *userdata) except *:
    cdef double *xdata = x.data()
    cdef double *gdata = grad.data()
    cdef np.ndarray[double, ndim=1, mode="c"] px = np.zeros(x.size())
    cdef size_t i
    for i in xrange(x.size()):
        px[i] = xdata[i]

    pot = <PythonPotential>(userdata)
    
    e, g = pot.getEnergyGradient(px)
    
    for i in xrange(x.size()):
        gdata[i] = g[i]
        
    return e

# energy callback not yet implemented
@cython.boundscheck(False)
cdef double _python_energy(_pele.Array x, void *userdata) except *:
    cdef double *xdata = x.data()
    cdef np.ndarray[double, ndim=1, mode="c"] px = np.zeros(x.size())
    cdef size_t i
    for i in xrange(x.size()):
        px[i] = xdata[i]

    pot = <PythonPotential>(userdata)
    return pot.getEnergy(px)

# define the potential class
cdef class PythonPotential(_pele.BasePotential):   
    def __cinit__(self):
        self.thisptr = <_pele.cBasePotential*>new _pele.cPotentialFunction(
                                           &_python_energy,
                                           &_python_grad,
                                           <void*>self)
        
    def getEnergy(self, x):
        raise NotImplementedError        

    def getEnergyGradient(self, x):
        raise NotImplementedError        