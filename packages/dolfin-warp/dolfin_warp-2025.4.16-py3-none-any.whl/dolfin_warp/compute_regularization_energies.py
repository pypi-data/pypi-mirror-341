#coding=utf8

################################################################################
###                                                                          ###
### Created by Martin Genet, 2016-2024                                       ###
###                                                                          ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

import dolfin
import math
import matplotlib.pyplot                   as mpl
import meshio
import numpy
import pandas
import random
import typing
import vtk.numpy_interface.dataset_adapter as dsa

import dolfin_mech as dmech
import dolfin_warp as dwarp

################################################################################

def compute_regularization_energies(
        dim                             : str,
        working_folder                  : str,
        working_basename                : str,
        working_ext                     : str                          = "vtu"                           ,
        working_displacement_array_name : str                          = "displacement"                  ,
        noise_type                      : typing.Optional[str]         = None                            , # MG20220815: This can be written "str | None" starting with python 3.10, but it is not readily available on the gitlab runners (Ubuntu 20.04)
        noise_level                     : float                        = 0.                              , 
        regul_types                     : list                         = []                              ,
        regul_model_for_lin             : str                          = "hooke"                         ,
        regul_model_for_nl              : str                          = "ogdenciarletgeymonatneohookean",
        regul_poisson                   : float                        = 0.                              ,
        regul_quadrature                : typing.Optional[int]         = None                            , # MG20220815: This can be written "int | None" starting with python 3.10, but it is not readily available on the gitlab runners (Ubuntu 20.04)
        normalize_energies              : bool                         = True                            ,
        write_regularization_energy_file: bool                         = True                            ,
        plot_regularization_energy      : bool                         = True                            ,
        verbose                         : bool                         = True                            ):

    working_series = dwarp.MeshesSeries(
        folder=working_folder,
        basename=working_basename,
        ext=working_ext,
        verbose=verbose)

    meshio_mesh = meshio.read(working_series.get_mesh_filename(k_frame=0))
    if (dim == 2):
        meshio_mesh.points = meshio_mesh.points[:, :2]
    meshio.write(working_series.get_mesh_filename(k_frame=None, ext="xdmf"), meshio_mesh)

    mesh = dolfin.Mesh()
    dolfin.parameters['reorder_dofs_serial'] = False
    dolfin.XDMFFile(working_series.get_mesh_filename(k_frame=None, ext="xdmf")).read(mesh)
    # print (mesh)
    # print (mesh.num_vertices())
    # print (mesh.num_cells())

    problem = dwarp.FullKinematicsWarpingProblem(
        mesh=mesh,
        U_family="Lagrange",
        U_degree=1)
    # print (len(problem.U.vector()))

    for regul_type in regul_types:
        regul_name = regul_type
        if regul_type.startswith("continuous"):
            regularization_energy_type = dwarp.RegularizationContinuousEnergy
            if regul_type.startswith("continuous-linear"):
                regul_type_ = regul_type.split("-",2)[2]
                regul_model = regul_model_for_lin
            else:
                regul_type_ = regul_type.split("-",1)[1]
                regul_model = regul_model_for_nl
        elif regul_type.startswith("discrete-simple"):
            regularization_energy_type = dwarp.SimpleRegularizationDiscreteEnergy
            regul_type_ = regul_type.split("-",2)[2]
            regul_model = regul_model_for_lin
        elif regul_type.startswith("discrete"):
            if ("equilibrated" in regul_type):
                regularization_energy_type = dwarp.VolumeRegularizationDiscreteEnergy
            elif ("tractions" in regul_type):
                regularization_energy_type = dwarp.SurfaceRegularizationDiscreteEnergy
            else: assert (0), "regul_type (= "+str(regul_type)+") unknown. Aborting."
            if regul_type.startswith("discrete-linear"):
                regul_type_ = regul_type.split("-",2)[2]
                regul_model = regul_model_for_lin
            else:
                regul_type_ = regul_type.split("-",1)[1]
                regul_model = regul_model_for_nl
        else: assert (0), "regul_type (= "+str(regul_type)+") unknown. Aborting."
        regularization_energy = regularization_energy_type(
            name=regul_name,
            problem=problem,
            w=1.,
            type=regul_type_,
            model=regul_model,
            poisson=regul_poisson,
            quadrature_degree=regul_quadrature)
        problem.add_regul_energy(
            energy=regularization_energy,
            order_by_type=False)

    # print (regul_types)
    # print ([energy.name for energy in problem.energies])
    # print ([energy.type for energy in problem.energies])

    if (normalize_energies):
        dwarp.compute_energies_normalization(
            problem=problem,
            verbose=verbose)

    if (write_regularization_energy_file):
        regul_ener_filebasename = working_folder+"/"+working_basename+"-regul_ener"
        if (noise_type is not None): regul_ener_filebasename += "-noise_level="+str(noise_level)
        # regul_ener_filebasename += "-".join(regul_types)
        regul_ener_file = open(regul_ener_filebasename+".dat", "w")
        regul_ener_file.write("#k_frame "+" ".join(regul_types)+"\n")

    regul_ener_lst = numpy.zeros((working_series.n_frames, len(regul_types)))

    for k_frame in range(working_series.n_frames):
        if (verbose): print ("k_frame = "+str(k_frame))

        vtk_mesh = working_series.get_mesh(k_frame=k_frame)
        # print (vtk_mesh)
        # print (vtk_mesh.GetNumberOfPoints())
        # print (vtk_mesh.GetNumberOfCells())
        np_mesh = dsa.WrapDataObject(vtk_mesh)
        # print (np_mesh)

        np_disp = np_mesh.PointData[working_displacement_array_name]
        if (dim == 2):
            np_disp = np_disp[:,:2]
        # print (np_disp)
        # print (np_disp.shape)
        # print (np_disp.flatten().shape)

        problem.U.vector()[:] = np_disp.flatten(order="F")
        if (noise_type is not None):
            if (noise_type == "random"):
                problem.U.vector()[:] += numpy.random.normal(
                    loc=0.,
                    scale=noise_level,
                    size=problem.U.vector().get_local().shape)
            elif (noise_type == "random_gaussian_field"):
                U_tmp = problem.U.copy(deepcopy=True)
                beta_min  = 2*math.pi/0.6
                beta_max  = 2*math.pi/0.6
                theta_min = 0.
                theta_max = 2*math.pi
                gamma_min = 0.
                gamma_max = 2*math.pi
                N = 10
                for _ in range(N):
                    if (dim == 2):
                        betax  = random.uniform( beta_min,  beta_max)
                        betay  = random.uniform( beta_min,  beta_max)
                        thetax = random.uniform(theta_min, theta_max)
                        thetay = random.uniform(theta_min, theta_max)
                        gammax = random.uniform(gamma_min, gamma_max)
                        gammay = random.uniform(gamma_min, gamma_max)
                        U_expr = dolfin.Expression(
                            ("cos(betax * (x[0]*nxx + x[1]*nxy) - gammax)",
                             "cos(betay * (x[0]*nyx + x[1]*nyy) - gammay)"),
                            betax=betax, betay=betay,
                            nxx=math.cos(thetax), nyx=math.cos(thetay),
                            nxy=math.sin(thetax), nyy=math.sin(thetay),
                            gammax=gammax, gammay=gammay,
                            element=problem.U_fe)
                    elif (dim == 3):
                        assert (0), "ToDo. Aborting."
                    U_tmp.interpolate(U_expr)
                    # print (problem.U.vector().get_local())
                    # print (U_tmp.vector().get_local())
                    problem.U.vector().axpy(noise_level/N, U_tmp.vector())
                    # print (problem.U.vector().get_local())
            filebasename  = working_series.get_mesh_filebasename(k_frame=None)
            filebasename += "-noise_type="+noise_type
            filebasename += "-noise_level="+str(noise_level)
            dmech.write_VTU_file(
                filebasename = filebasename,
                function = problem.U,
                time = k_frame)

        for k_ener, energy in enumerate(problem.energies):
            regul_ener_lst[k_frame, k_ener] = (energy.assemble_ener()/problem.mesh_V0)**(1/2)
            if (verbose): print (energy.name, ":", regul_ener_lst[k_frame, k_ener])

        if (write_regularization_energy_file): regul_ener_file.write(" ".join([str(val) for val in [k_frame]+list(regul_ener_lst[k_frame,:])])+"\n")

    if (write_regularization_energy_file): regul_ener_file.close()

    if (plot_regularization_energy):
        ener_data = pandas.read_csv(
            regul_ener_filebasename+".dat",
            delim_whitespace=True,
            comment="#",
            names=open(regul_ener_filebasename+".dat").readline()[1:].split())

        # mpl.xkcd()
        ener_fig, ener_axes = mpl.subplots()
        # ener_data.plot(x="k_frame", y=regul_types, linestyle="dashed", ax=ener_axes, ylabel="regularization energy")
        # print (ener_axes.get_sketch_params())
        # ener_axes.set_sketch_params(1., 100., 2.) # Does nothing
        # print (ener_axes.get_sketch_params())
        # matplotlib.rcParams['path.sketch'] = (1., 100., 2.) # Applies to all lines!
        # print (ener_axes.get_sketch_params())
        for k, regul_type in enumerate(regul_types):
            ener_data.plot(x="k_frame", y=regul_type, dashes=[len(regul_types)-k, 2], ax=ener_axes, ylabel="regularization energy")
            # ener_data.plot(x="k_frame", y=regul_type, dashes=[len(regul_types)-k, 2], sketch_params=0.3, ax=ener_axes, ylabel="regularization energy")
        # ener_axes.set_ylim([-0.001,0.1])
        # ener_axes.set_sketch_params(1.) # Does nothing
        ener_fig.savefig(regul_ener_filebasename+".pdf")

    return numpy.mean(regul_ener_lst, axis=0)
