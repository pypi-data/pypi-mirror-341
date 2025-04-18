#coding=utf8

################################################################################
###                                                                          ###
### Created by Martin Genet, 2016-2025                                       ###
###                                                                          ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

import dolfin
import typing

import dolfin_mech as dmech
import dolfin_warp as dwarp

from .Energy_Continuous import ContinuousEnergy
from .Problem           import Problem

################################################################################

class RegularizationContinuousEnergy(ContinuousEnergy):



    def __init__(self,
            problem: Problem,
            name: str = "reg",
            w: float = 1.,
            type: str = "equilibrated",
            model: str = "ogdenciarletgeymonatneohookean",
            young: float = 1.,
            poisson: float = 0.,
            b_fin: typing.Optional["list[float]"] = None,
            volume_subdomain_data = None,
            volume_subdomain_id = None,
            surface_subdomain_data = None,
            surface_subdomain_id = None,
            quadrature_degree: typing.Optional[int] = None): # MG20220815: This can be written "int | None" starting with python 3.10, but it is not readily available on the gitlab runners (Ubuntu 20.04)

        self.problem = problem
        self.printer = problem.printer

        self.name = name

        self.w = w

        type_lst = ("equilibrated", "elastic", "hyperelastic")
        assert (type in type_lst),\
            "\"type\" ("+str(type)+") must be in "+str(type_lst)+". Aborting."
        self.type = type

        model_lst = ("hooke", "kirchhoff", "neohookean", "mooneyrivlin", "neohookeanmooneyrivlin", "ciarletgeymonat", "ciarletgeymonatneohookean", "ciarletgeymonatneohookeanmooneyrivlin", "ogdenciarletgeymonat", "ogdenciarletgeymonatneohookean", "ogdenciarletgeymonatneohookeanmooneyrivlin")
        assert (model in model_lst),\
            "\"model\" ("+str(model)+") must be in "+str(model_lst)+". Aborting."
        self.model = model

        assert (young > 0.),\
            "\"young\" ("+str(young)+") must be > 0. Aborting."
        self.young = young

        assert (poisson > -1.),\
            "\"poisson\" ("+str(poisson)+") must be > -1. Aborting."
        assert (poisson < 0.5),\
            "\"poisson\" ("+str(poisson)+") must be < 0.5. Aborting."
        self.poisson = poisson

        self.quadrature_degree = quadrature_degree

        self.printer.print_str("Defining regularization energy…")
        self.printer.inc()

        self.printer.print_str("Defining measures…")

        self.form_compiler_parameters = {
            "quadrature_degree":self.quadrature_degree}
        self.dV = dolfin.Measure(
            "dx",
            domain=self.problem.mesh,
            subdomain_data=volume_subdomain_data,
            subdomain_id=volume_subdomain_id if volume_subdomain_id is not None else "everywhere",
            metadata=self.form_compiler_parameters)
        self.dF = dolfin.Measure(
            "dS",
            domain=self.problem.mesh,
            subdomain_data=volume_subdomain_data,
            subdomain_id=volume_subdomain_id if volume_subdomain_id is not None else "everywhere",
            metadata=self.form_compiler_parameters)
        self.dS = dolfin.Measure(
            "ds",
            domain=self.problem.mesh,
            subdomain_data=surface_subdomain_data,
            subdomain_id=surface_subdomain_id if (surface_subdomain_id is not None) else "everywhere",
            metadata=self.form_compiler_parameters)

        self.printer.print_str("Defining mechanical model…")

        if (self.model == "hooke"):
            kinematics = dmech.LinearizedKinematics(
                u=self.problem.U)
        elif (self.model in ("kirchhoff", "neohookean", "mooneyrivlin", "neohookeanmooneyrivlin", "ciarletgeymonat", "ciarletgeymonatneohookean", "ciarletgeymonatneohookeanmooneyrivlin", "ogdenciarletgeymonat", "ogdenciarletgeymonatneohookean", "ogdenciarletgeymonatneohookeanmooneyrivlin")):
            kinematics = dmech.Kinematics(
                U=self.problem.U)

        self.material = dmech.material_factory(
            kinematics=kinematics,
            model=self.model,
            parameters={
                "E":self.young,
                "nu":self.poisson,
                "checkJ":1})

        if (self.model == "hooke"):
            self.Psi   = self.material.psi
            self.Sigma = self.material.sigma
            self.P     = self.material.sigma
        elif (self.model in ("kirchhoff", "neohookean", "mooneyrivlin", "neohookeanmooneyrivlin", "ciarletgeymonat", "ciarletgeymonatneohookean", "ciarletgeymonatneohookeanmooneyrivlin", "ogdenciarletgeymonat", "ogdenciarletgeymonatneohookean", "ogdenciarletgeymonatneohookeanmooneyrivlin")):
            self.Psi   = self.material.Psi
            self.Sigma = self.material.Sigma
            self.P     = self.material.P

        self.printer.print_str("Defining regularization energy…")

        if (self.type in ("elastic", "hyperelastic")):
            self.Psi_V = self.Psi
            self.Psi_F = dolfin.Constant(0)
            self.Psi_S = dolfin.Constant(0)
        elif (self.type == "equilibrated"):
            self.Div_P = dolfin.div(self.P)
            self.Psi_V = dolfin.inner(self.Div_P, self.Div_P)
            self.N = dolfin.FacetNormal(self.problem.mesh)
            self.Jump_P_N = dolfin.jump(self.P, self.N)
            self.cell_h = dolfin.Constant(self.problem.mesh.hmin())
            self.Psi_F = dolfin.inner(self.Jump_P_N, self.Jump_P_N)/self.cell_h
            # self.P_N = dolfin.dot(self.P, self.N)
            # self.P_N_N = dolfin.inner(self.N, self.P_N)
            # self.P_N_T = self.P_N - self.P_N_N * self.N
            # self.Psi_S = dolfin.inner(self.P_N_T, self.P_N_T)/self.cell_h
            # self.Psi_S = dolfin.inner(self.P_N, self.P_N)/self.cell_h
            self.Psi_S = dolfin.Constant(0)

        self.DPsi_m_V  = dolfin.derivative( self.Psi_V  , self.problem.U, self.problem.dU_test )
        self.DPsi_m_F  = dolfin.derivative( self.Psi_F  , self.problem.U, self.problem.dU_test )
        self.DPsi_m_S  = dolfin.derivative( self.Psi_S  , self.problem.U, self.problem.dU_test )
        self.DDPsi_m_V = dolfin.derivative(self.DPsi_m_V, self.problem.U, self.problem.dU_trial)
        self.DDPsi_m_F = dolfin.derivative(self.DPsi_m_F, self.problem.U, self.problem.dU_trial)
        self.DDPsi_m_S = dolfin.derivative(self.DPsi_m_S, self.problem.U, self.problem.dU_trial)

        self.ener_form =   self.Psi_V   * self.dV +   self.Psi_F   * self.dF +   self.Psi_S   * self.dS
        self.res_form  =  self.DPsi_m_V * self.dV +  self.DPsi_m_F * self.dF +  self.DPsi_m_S * self.dS
        self.jac_form  = self.DDPsi_m_V * self.dV + self.DDPsi_m_F * self.dF + self.DDPsi_m_S * self.dS

        self.printer.dec()
