import unittest
import numpy as np

from playground.native_code import _lj
from pele.systems import LJCluster
from pele.potentials import LJ, LJpshift
from pele.optimize import mylbfgs

class TestLJ_CPP(unittest.TestCase):
    def setUp(self):
        self.natoms = 18
        self.pot = _lj.LJ() 
        
        self.pot_comp = LJ()
        x = np.random.uniform(-1,1, 3*self.natoms)
        ret = mylbfgs(x, self.pot_comp, tol=10.)
        self.x = ret.coords
        
    
    def test(self):
        eonly = self.pot.getEnergy(self.x)
        e, g = self.pot.getEnergyGradient(self.x)
        self.assertAlmostEqual(e, eonly, delta=1e-6)
        et, gt = self.pot_comp.getEnergyGradient(self.x)
        self.assertAlmostEqual(e, et, delta=1e-6)
        self.assertLess(np.max(np.abs(g - gt)), 1e-6)

class TestLJ_CPP_Periodic(TestLJ_CPP):
    def setUp(self):
        self.natoms = 18
        boxl = 1.
        self.boxvec = [boxl] * 3
        self.pot = _lj.LJ(boxvec=self.boxvec)
        
        self.pot_comp = LJ(boxl=boxl)
        x = np.random.uniform(-1,1, 3*self.natoms)
        ret = mylbfgs(x, self.pot_comp, tol=10.)
        self.x = ret.coords
        
    
    def test(self):
        eonly = self.pot.getEnergy(self.x)
        e, g = self.pot.getEnergyGradient(self.x)
        self.assertAlmostEqual(e, eonly, delta=1e-6)
        et, gt = self.pot_comp.getEnergyGradient(self.x)
        self.assertAlmostEqual(e, et, delta=1e-6)
        self.assertLess(np.max(np.abs(g - gt)), 1e-6)

class TestLJ_CPP_Cut(TestLJ_CPP):
    def setUp(self):
        self.natoms = 200
        rcut = 2.5
        self.pot = _lj.LJCut(rcut=rcut)
        
        self.pot_comp = LJpshift(self.natoms, self.natoms, rcut=rcut)
        x = np.random.uniform(-rcut*2,rcut*2, 3*self.natoms)
        ret = mylbfgs(x, self.pot_comp, tol=10.)
        self.x = ret.coords
        
    
    def test(self):
        eonly = self.pot.getEnergy(self.x)
        e, g = self.pot.getEnergyGradient(self.x)
        self.assertAlmostEqual(e, eonly, delta=1e-6)
        et, gt = self.pot_comp.getEnergyGradient(self.x)
        self.assertAlmostEqual(e, et, delta=1e-6)
        self.assertLess(np.max(np.abs(g - gt)), 1e-6)



if __name__ == "__main__":
    unittest.main()