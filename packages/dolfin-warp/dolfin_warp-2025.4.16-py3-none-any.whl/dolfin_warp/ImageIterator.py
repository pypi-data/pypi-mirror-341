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
import vtk

import myPythonLibrary as mypy

import dolfin_mech as dmech
import dolfin_warp as dwarp

################################################################################

class ImageIterator():



    def __init__(self,
            problem,
            solver,
            parameters={}):

        self.problem = problem
        self.printer = self.problem.printer
        self.solver  = solver

        self.working_folder                              = parameters.get("working_folder"                             , "."           )
        self.working_basename                            = parameters.get("working_basename"                           , "sol"         )
        self.register_ref_frame                          = parameters.get("register_ref_frame"                         , False         )
        self.initialize_reduced_U_from_file              = parameters.get("initialize_reduced_U_from_file"             , False         )
        self.initialize_reduced_U_filename               = parameters.get("initialize_reduced_U_filename"              , "init"        )
        self.initialize_U_from_file                      = parameters.get("initialize_U_from_file"                     , False         )
        self.initialize_U_folder                         = parameters.get("initialize_U_folder"                        , "."           )
        self.initialize_U_basename                       = parameters.get("initialize_U_basename"                      , "init"        )
        self.initialize_U_ext                            = parameters.get("initialize_U_ext"                           , "vtu"         )
        self.initialize_U_array_name                     = parameters.get("initialize_U_array_name"                    , "displacement")
        self.initialize_U_method                         = parameters.get("initialize_U_method"                        , "dofs_transfer")
        self.write_qois_limited_precision                = parameters.get("write_qois_limited_precision"               , False         )
        self.write_VTU_files                             = parameters.get("write_VTU_files"                            , True          )
        self.write_VTU_files_with_preserved_connectivity = parameters.get("write_VTU_files_with_preserved_connectivity", False         )
        self.write_XML_files                             = parameters.get("write_XML_files"                            , False         )
        self.iteration_mode                              = parameters.get("iteration_mode"                             , "normal"      ) # MG20200616: This should be a bool
        self.continue_after_fail                         = parameters.get("continue_after_fail"                        , False         )



    def iterate(self):

        if not os.path.exists(self.working_folder):
            os.mkdir(self.working_folder)
        vtu_basename = self.working_folder+"/"+self.working_basename
        for vtu_filename in glob.glob(vtu_basename+"_[0-9]*.vtu"):
            os.remove(vtu_filename)

        dolfin.File(vtu_basename+"-mesh.xml") << self.problem.mesh # MG20230321: For warp_and_refine, need to save current mesh for next refine level

        self.printer.print_str("Initializing QOI file…")
        self.printer.inc()

        qoi_names = ["k_frame"]+self.problem.get_qoi_names()
        qoi_filebasename = self.working_folder+"/"+self.working_basename+"-qoi"
        qoi_printer = mypy.DataPrinter(
            names=qoi_names,
            filename=qoi_filebasename+".dat",
            limited_precision=self.write_qois_limited_precision)

        if not (self.register_ref_frame):
            self.printer.dec()
            self.printer.print_str("Writing initial solution…")
            self.printer.inc()

            if (self.write_VTU_files):
                dmech.write_VTU_file(
                    filebasename=vtu_basename,
                    function=self.problem.U,
                    time=self.problem.images_ref_frame,
                    preserve_connectivity=self.write_VTU_files_with_preserved_connectivity)
            if (self.write_XML_files):
                dolfin.File(vtu_basename+"_"+str(self.problem.images_ref_frame).zfill(3)+".xml") << self.problem.U

            # self.I = dolfin.Identity(2)
            # self.F = self.I + dolfin.grad(self.problem.U)
            # self.J = dolfin.det(self.F)
            # self.J_fe = dolfin.FiniteElement(
            #     family="DG",
            #     cell=self.problem.mesh.ufl_cell(),
            #     degree=0)
            # self.J_fs = dolfin.FunctionSpace(
            #     self.problem.mesh,
            #     self.J_fe)
            # self.J_func = dolfin.Function(self.J_fs)
            # dolfin.project(
            #     v=self.J,
            #     V=self.J_fs,
            #     function=self.J_func)
            # dmech.write_VTU_file(
            #     filebasename=vtu_basename+"-J",
            #     function=self.J_func,
            #     time=self.problem.images_ref_frame)

            self.printer.dec()
            self.printer.print_str("Writing initial QOI…")
            self.printer.inc()

            qoi_values = [self.problem.images_ref_frame]+self.problem.get_qoi_values()
            qoi_printer.write_line(
                values=qoi_values)

        self.printer.dec()
        self.printer.print_str("Looping over frames…")

        if (self.initialize_U_from_file):
            init_meshes_series = dwarp.MeshesSeries(
                folder=self.initialize_U_folder,
                basename=self.initialize_U_basename,
                ext=self.initialize_U_ext,
                printer=self.problem.printer)
            assert (init_meshes_series.n_frames <= self.problem.images_n_frames),\
                "init_meshes_series.n_frames ("+str(init_meshes_series.n_frames)+") < self.problem.images_n_frames ("+str(self.problem.images_n_frames)+"). Aborting."

            init_mesh_filename  = self.initialize_U_folder
            init_mesh_filename += "/"+self.initialize_U_basename
            init_mesh_filename += "-"+"mesh"
            init_mesh_filename += "."+"xml"
            init_mesh = dolfin.Mesh(init_mesh_filename)
            init_fe = dolfin.VectorElement(
                family="Lagrange",
                cell=self.problem.mesh.ufl_cell(),
                degree=1)
            init_fs = dolfin.FunctionSpace(
                init_mesh,
                init_fe)
            init_U = dolfin.Function(init_fs)
            init_U.set_allow_extrapolation(True)
            # init_dof_to_vertex_map = dolfin.dof_to_vertex_map(init_fs) # MG20230321: Somehow this is problematic when VTUs are saved with preserved connectivity…

        if (self.initialize_reduced_U_from_file):
            init_reduced_displacement = numpy.loadtxt(self.initialize_reduced_U_filename, ndmin=2)
            assert (init_reduced_displacement.shape[0] == self.problem.reduced_displacement_fs.dim()),\
                "\"init_reduced_displacement.shape[0]\" ("+str(init_reduced_displacement.shape[0])+") should match \"problem.reduced_displacement_fs.dim()\" (="+str(self.problem.reduced_displacement_fs.dim())+"). Aborting."
            assert (init_reduced_displacement.shape[1] == self.problem.images_n_frames),\
                "\"init_reduced_displacement.shape[1]\" ("+str(init_reduced_displacement.shape[1])+") should match \"problem.images_n_frames\" (="+str(self.problem.images_n_frames)+"). Aborting."

        n_iter_tot = 0
        for forward_or_backward in ["forward","backward"]:
            self.printer.print_var("forward_or_backward",forward_or_backward)

            if   (forward_or_backward == "forward"):
                if (self.register_ref_frame):
                    start = self.problem.images_ref_frame
                else:
                    start = self.problem.images_ref_frame + 1
                if   (self.iteration_mode == "normal"):
                    end = self.problem.images_n_frames
                elif (self.iteration_mode == "loop"):
                    end = self.problem.images_n_frames + self.problem.images_ref_frame
                else:
                    assert (0), \
                        "iteration_mode ("+str(self.iteration_mode)+") should be \"normal\" or \"loop\". Aborting."
                k_frames = range(start, end, +1)
            elif (forward_or_backward == "backward"):
                start = self.problem.images_ref_frame - 1
                if   (self.iteration_mode == "normal"):
                    end = -1
                elif (self.iteration_mode == "loop"):
                    end = self.problem.images_ref_frame - 1
                else:
                    assert (0), \
                        "iteration_mode ("+str(self.iteration_mode)+") should be \"normal\" or \"loop\". Aborting."
                k_frames = range(start, end, -1)
            self.printer.print_var("k_frames",k_frames)

            if (forward_or_backward == "backward"):
                self.problem.reinit()

            self.printer.inc()
            success = True
            for k_frame in k_frames:
                k_frame = k_frame%(self.problem.images_n_frames)
                self.printer.print_var("k_frame",k_frame,-1)

                if (self.initialize_U_from_file):
                    self.printer.print_str("Initializing displacement…")
                    init_mesh = init_meshes_series.get_mesh(k_frame=k_frame)
                    init_array_U = init_mesh.GetPointData().GetArray(self.initialize_U_array_name)
                    init_array_U = vtk.util.numpy_support.vtk_to_numpy(init_array_U)
                    init_array_U = init_array_U[:,:self.problem.mesh_dimension]
                    init_array_U = numpy.reshape(init_array_U, init_array_U.size)
                    init_U.vector()[:] = init_array_U
                    # init_U.vector()[:] = init_array_U[init_dof_to_vertex_map] # MG20230321: Somehow this is problematic when VTUs are saved with preserved connectivity…

                    if (self.initialize_U_method == "dofs_transfer"):
                        self.problem.U.vector()[:] = init_U.vector()
                    elif (self.initialize_U_method == "interpolation"):
                        self.problem.U.interpolate(init_U)
                    elif (self.initialize_U_method == "projection"):
                        dolfin.project(
                            v=init_U,
                            V=self.problem.U_fs,
                            function=self.problem.U)
                    self.problem.U_norm = self.problem.U.vector().norm("l2")

                elif (self.initialize_reduced_U_from_file):
                    self.problem.reduced_displacement.vector()[:] = init_reduced_displacement[k_frame-1,:]

                self.problem.call_before_solve(
                    k_frame=k_frame,
                    n_frames=self.problem.images_n_frames)

                self.printer.print_str("Running registration…")

                success, n_iter = self.solver.solve(
                    k_frame=k_frame)
                n_iter_tot += n_iter

                if not (success) and not (self.continue_after_fail):
                    break

                self.problem.call_after_solve(
                    k_frame=k_frame,
                    basename=vtu_basename)

                self.printer.print_str("Writing solution…")
                self.printer.inc()

                if (self.write_VTU_files):
                    dmech.write_VTU_file(
                        filebasename=vtu_basename,
                        function=self.problem.U,
                        time=k_frame,
                        preserve_connectivity=self.write_VTU_files_with_preserved_connectivity)
                if (self.write_XML_files):
                    dolfin.File(vtu_basename+"_"+str(k_frame).zfill(3)+".xml") << self.problem.U
                # dolfin.project(
                #     v=self.J,
                #     V=self.J_fs,
                #     function=self.J_func)
                # dmech.write_VTU_file(
                #     filebasename=vtu_basename+"-J",
                #     function=self.J_func,
                #     time=k_frame)

                self.printer.dec()
                self.printer.print_str("Writing QOI…")
                self.printer.inc()

                qoi_printer.write_line(
                    [k_frame]+self.problem.get_qoi_values())

                self.printer.dec()

            self.printer.dec()

            if not (success):
                break

        self.printer.print_str("Image iterator finished…")
        self.printer.inc()

        self.printer.print_var("n_iter_tot",n_iter_tot)

        self.printer.dec()
        self.printer.print_str("Plotting QOI…")

        qoi_printer.close()
        commandline  = "gnuplot -e \"set terminal pdf noenhanced;"
        commandline += " set output '"+qoi_filebasename+".pdf';"
        commandline += " set grid;"
        for k_qoi in range(1,len(qoi_names)):
            commandline += " plot '"+qoi_filebasename+".dat' u 1:"+str(1+k_qoi)+" lw 3 title '"+qoi_names[k_qoi]+"';"
        commandline += "\""
        os.system(commandline)

        return success
