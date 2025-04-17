#coding=utf8

################################################################################
###                                                                          ###
### Created by Martin Genet, 2016-2024                                       ###
###                                                                          ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

import dolfin
import glob
import numpy
import os
import time

import myPythonLibrary as mypy

import dolfin_mech as dmech
import dolfin_warp as dwarp

from .NonlinearSolver            import           NonlinearSolver
from .NonlinearSolver_Relaxation import RelaxationNonlinearSolver

################################################################################

class NewtonNonlinearSolver(RelaxationNonlinearSolver):



    def __init__(self,
            problem,
            parameters={}):

        self.problem = problem
        self.printer = self.problem.printer

        # linear solver
        self.linear_solver_name = parameters["linear_solver_name"] if ("linear_solver_name" in parameters) and (parameters["linear_solver_name"] is not None) else "mumps"

        # self.res_vec = dolfin.PETScVector()
        # self.jac_mat = dolfin.PETScMatrix()
        self.res_vec = dolfin.Vector()
        self.jac_mat = dolfin.Matrix()

        self.linear_solver = dolfin.LUSolver(
            self.jac_mat,
            self.linear_solver_name)
        self.linear_solver.parameters['report']               = bool(0)
        # self.linear_solver.parameters['reuse_factorization']  = bool(0)
        # self.linear_solver.parameters['same_nonzero_pattern'] = bool(1)
        self.linear_solver.parameters['symmetric']            = bool(1)
        self.linear_solver.parameters['verbose']              = bool(0)

        # relaxation
        RelaxationNonlinearSolver.__init__(self, parameters=parameters)

        # iterations control
        self.tol_dU      = parameters.get("tol_dU"     , None)
        self.tol_dU_rel  = parameters.get("tol_dU_rel" , None)
        self.tol_res_rel = parameters.get("tol_res_rel", None)
        self.n_iter_max  = parameters.get("n_iter_max" , 32  )

        # write iterations
        self.write_iterations = parameters["write_iterations"] if ("write_iterations" in parameters) and (parameters["write_iterations"] is not None) else False

        if (self.write_iterations):
            self.working_folder   = parameters["working_folder"]
            self.working_basename = parameters["working_basename"]

            for filename in glob.glob(self.working_folder+"/"+self.working_basename+"-frame=[0-9]*.*"):
                os.remove(filename)



    def solve(self,
            k_frame=None):

        self.k_frame = k_frame

        if (self.write_iterations):
            self.frame_filebasename = self.working_folder+"/"+self.working_basename+"-frame="+str(self.k_frame).zfill(len(str(self.problem.images_n_frames)))

            self.frame_printer = mypy.DataPrinter(
                names=["k_iter", "res_norm", "res_err_rel", "relax", "dU_norm", "U_norm", "dU_err"],
                filename=self.frame_filebasename+".dat")

            dmech.write_VTU_file(
                filebasename=self.frame_filebasename,
                function=self.problem.U,
                time=0)
        else:
            self.frame_filebasename = None

        self.k_iter = 0
        self.problem.DU.vector().zero()
        self.success = False
        self.printer.inc()
        while (True):
            self.k_iter += 1
            self.printer.print_var("k_iter",self.k_iter,-1)

            # linear problem
            self.linear_success = self.linear_solve()
            if not (self.linear_success):
                break

            # relaxation
            self.compute_relax()

            # solution update
            self.problem.update_displacement(relax=self.relax)
            self.printer.print_sci("U_norm",self.problem.U_norm)

            self.problem.DU.vector()[:] = self.problem.U.vector() - self.problem.Uold.vector()
            self.problem.DU_norm = self.problem.DU.vector().norm("l2")
            self.printer.print_sci("DU_norm",self.problem.DU_norm)

            if (self.write_iterations):
                dmech.write_VTU_file(
                    filebasename=self.frame_filebasename,
                    function=self.problem.U,
                    time=self.k_iter)

            # displacement error
            if (self.problem.U_norm == 0.):
                if (self.problem.Uold_norm == 0.):
                    self.problem.dU_err = 0.
                else:
                    self.problem.dU_err = abs(self.relax)*self.problem.dU_norm/self.problem.Uold_norm
            else:
                self.problem.dU_err = abs(self.relax)*self.problem.dU_norm/self.problem.U_norm
            self.printer.print_sci("dU_err",self.problem.dU_err)

            if (self.problem.DU_norm == 0.):
                self.problem.dU_err_rel = 1.
            else:
                self.problem.dU_err_rel = abs(self.relax)*self.problem.dU_norm/self.problem.DU_norm
            self.printer.print_sci("dU_err_rel",self.problem.dU_err_rel)

            if (self.write_iterations):
                self.frame_printer.write_line([self.k_iter, self.res_norm, self.res_err_rel, self.relax, self.problem.dU_norm, self.problem.U_norm, self.problem.dU_err])

            # exit test
            self.success = True
            if (self.tol_res_rel is not None) and (self.res_err_rel        > self.tol_res_rel):
                self.success = False
            if (self.tol_dU      is not None) and (self.problem.dU_err     > self.tol_dU     ):
                self.success = False
            if (self.tol_dU_rel  is not None) and (self.problem.dU_err_rel > self.tol_dU_rel ):
                self.success = False

            # exit
            if (self.success):
                self.printer.print_str("Nonlinear solver converged…")
                break

            if (self.k_iter == self.n_iter_max):
                self.printer.print_str("Warning! Nonlinear solver failed to converge… (k_frame = "+str(self.k_frame)+")")
                break

        self.printer.dec()

        if (self.write_iterations):
            self.frame_printer.close()
            commandline  = "gnuplot -e \"set terminal pdf noenhanced;"
            commandline += " set output '"+self.frame_filebasename+".pdf';"
            commandline += " set key box textcolor variable;"
            commandline += " set grid;"
            commandline += " set logscale y;"
            commandline += " set yrange [1e-3:1e0];"
            commandline += " plot '"+self.frame_filebasename+".dat' u 1:7 pt 1 lw 3 title 'dU_err', "+str(self.tol_dU)+" lt -1 notitle;"
            commandline += " unset logscale y;"
            commandline += " set yrange [*:*];"
            commandline += " plot '' u 1:4 pt 1 lw 3 title 'relax'\""
            os.system(commandline)

        return self.success, self.k_iter



    def linear_solve(self):

        # res_old
        if (self.k_iter > 1):
            if (hasattr(self, "res_old_vec")):
                self.res_old_vec[:] = self.res_vec[:]
            else:
                self.res_old_vec = self.res_vec.copy()
            self.res_old_norm = self.res_norm

        self.problem.call_before_assembly(
            write_iterations=self.write_iterations,
            basename=self.frame_filebasename,
            k_iter=self.k_iter)

        # linear system: residual assembly
        self.printer.print_str("Residual assembly…",newline=False)
        timer = time.time()
        self.problem.assemble_res(
            res_vec=self.res_vec)
        timer = time.time() - timer
        self.printer.print_str(" "+str(timer)+" s",tab=False)
        # self.printer.print_var("res_vec",self.res_vec.get_local())

        self.printer.inc()

        # res_norm
        self.res_norm = self.res_vec.norm("l2")
        self.printer.print_sci("res_norm",self.res_norm)
        if not (numpy.isfinite(self.res_norm)):
            self.printer.print_str("Warning! Residual is NaN!",tab=False)
            return False

        # dres
        if (self.k_iter > 1):
            if (hasattr(self, "dres_vec")):
                self.dres_vec[:] = self.res_vec[:] - self.res_old_vec[:]
            else:
                self.dres_vec = self.res_vec - self.res_old_vec
            self.dres_norm = self.dres_vec.norm("l2")
            self.printer.print_sci("dres_norm",self.dres_norm)

        # res_err_rel
        if (self.k_iter == 1):
            self.res_err_rel = 1.
        else:
            self.res_err_rel = self.dres_norm / self.res_old_norm
            self.printer.print_sci("res_err_rel",self.res_err_rel)

        self.printer.dec()

        # linear system: matrix assembly
        self.printer.print_str("Jacobian assembly…",newline=False)
        timer = time.time()
        self.problem.assemble_jac(
            jac_mat=self.jac_mat)
        timer = time.time() - timer
        self.printer.print_str(" "+str(timer)+" s",tab=False)
        # self.printer.print_var("jac_mat",self.jac_mat.array())

        # linear system: solve
        try:
            self.printer.print_str("Solve…",newline=False)
            timer = time.time()
            if (type(self.problem) is dwarp.FullKinematicsWarpingProblem):
                self.linear_solver.solve(
                    self.problem.dU.vector(),
                    -self.res_vec)
                # self.printer.print_var("dU",dU.vector().get_local())
            elif (type(self.problem) is dwarp.ReducedKinematicsWarpingProblem):
                self.linear_solver.solve(
                    self.problem.dreduced_displacement.vector(),
                    -self.res_vec)
                # self.problem.dreduced_displacement.vector()[:] = numpy.linalg.solve(
                #     self.jac_mat.array(),
                #     -self.res_vec.get_local())
                # self.printer.print_var("dreduced_displacement",self.problem.dreduced_displacement.vector().get_local())
            timer = time.time() - timer
            self.printer.print_str(" "+str(timer)+" s",tab=False)
        except:
            self.printer.print_str("Warning! Linear solver failed!",tab=False)
            return False

        self.printer.inc()

        if (type(self.problem) is dwarp.FullKinematicsWarpingProblem):
            self.problem.dU_norm = self.problem.dU.vector().norm("l2")
            self.printer.print_sci("dU_norm",self.problem.dU_norm)
            if not (numpy.isfinite(self.problem.dU_norm)):
                self.printer.print_str("Warning! Solution increment is NaN! Setting it to 0.",tab=False)
                self.problem.dU.vector().zero()
                return False
        elif (type(self.problem) is dwarp.ReducedKinematicsWarpingProblem):
            self.problem.dreduced_displacement_norm = self.problem.dreduced_displacement.vector().norm("l2")
            self.printer.print_sci("dreduced_displacement_norm",self.problem.dreduced_displacement_norm)
            if not (numpy.isfinite(self.problem.dreduced_displacement_norm)):
                self.printer.print_str("Warning! Solution increment is NaN! Setting it to 0.",tab=False)
                self.problem.dreduced_displacement.vector().zero()
                return False

        self.printer.dec()

        return True
