#coding=utf8

################################################################################
###                                                                          ###
### Created by Mahdi Manoochehrtayebi, 2020-2024                             ###
###                                                                          ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

import dolfin

import dolfin_mech as dmech
from .Material_Elastic import ElasticMaterial

################################################################################

class ExponentialNeoHookeanElasticMaterial(ElasticMaterial):



    def __init__(self,
            kinematics,
            parameters):

        self.kinematics = kinematics

        self.beta1 = dolfin.Constant(parameters["beta1"])
        self.beta2 = dolfin.Constant(parameters["beta2"])
        self.beta3 = dolfin.Constant(parameters["beta3"])
        self.beta4 = dolfin.Constant(parameters["beta4"])
        self.alpha = dolfin.Constant(parameters["alpha"])


        if   (self.kinematics.dim == 2):
                self.Psi   =  self.beta1/self.beta2/self.alpha/2 * (dolfin.exp(self.beta2*(self.kinematics.IC - 2 - 2*dolfin.ln(self.kinematics.J))**self.alpha) - 1) \
                           +  self.beta3 * (self.kinematics.IC - 2 - 2*dolfin.ln(self.kinematics.J))\
                           +  self.beta4 * (self.kinematics.J**2 - 1 - 2*dolfin.ln(self.kinematics.J))
                self.Sigma =  self.beta1 * (self.kinematics.I - self.kinematics.C_inv) * (self.kinematics.IC - 2 - 2*dolfin.ln(self.kinematics.J))**(self.alpha - 1) * dolfin.exp(self.beta2*(self.kinematics.IC - 2 - 2*dolfin.ln(self.kinematics.J))**self.alpha) \
                           +  2 * self.beta3 * (self.kinematics.I - self.kinematics.C_inv)\
                           +  2*self.beta4 * (self.kinematics.J**2 - 1) * self.kinematics.C_inv 
        
        elif (self.kinematics.dim == 3):
            self.Psi   =  self.beta1/self.beta2/self.alpha/2 * (dolfin.exp(self.beta2*(self.kinematics.IC - 3 - 2*dolfin.ln(self.kinematics.J))**self.alpha) - 1) \
                           +  self.beta3 * (self.kinematics.IC - 3 - 2*dolfin.ln(self.kinematics.J))\
                           +  self.beta4 * (self.kinematics.J**2 - 1 - 2*dolfin.ln(self.kinematics.J))
            self.Sigma =  self.beta1 * (self.kinematics.I - self.kinematics.C_inv) * (self.kinematics.IC - 3 - 2*dolfin.ln(self.kinematics.J))**(self.alpha - 1) * dolfin.exp(self.beta2*(self.kinematics.IC - 3 - 2*dolfin.ln(self.kinematics.J))**self.alpha) \
                        +  2 * self.beta3 * (self.kinematics.I - self.kinematics.C_inv)\
                        +  2*self.beta4 * (self.kinematics.J**2 - 1) * self.kinematics.C_inv 


        self.P = self.kinematics.F * self.Sigma
        self.sigma = self.P * self.kinematics.F.T / self.kinematics.J