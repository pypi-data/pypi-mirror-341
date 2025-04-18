#coding=utf8

################################################################################
###                                                                          ###
### Created by Martin Genet, 2018-2025                                       ###
###                                                                          ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

import dolfin
import matplotlib.pyplot as mpl
import pandas
import numpy

import dolfin_mech as dmech

################################################################################

def run_RivlinCube_PoroHyperelasticity(
        dim=3,
        inverse=0,
        cube_params={},
        porosity_params={},
        move_params={},
        mat_params={},
        step_params={},
        load_params={},
        inertia_params={"applied": False},
        res_basename="run_RivlinCube_PoroHyperelasticity",
        plot_curves=False,
        get_results=0,
        verbose=0):

    ################################################################### Mesh ###

    if ("path_and_mesh_name" in cube_params):
        mesh = dolfin.Mesh()
        mesh_name = str(cube_params["path_and_mesh_name"])
        dolfin.XDMFFile(mesh_name).read(mesh)
        if ("refine" in cube_params):
            mesh=dolfin.refine(mesh)
        boundaries_mf = dolfin.MeshFunction("size_t", mesh, mesh.topology().dim()-1) # MG20180418: size_t looks like unsigned int, but more robust wrt architecture and os
        boundaries_mf.set_all(0)
    else:
        if   (dim==2):
            mesh, boundaries_mf, xmin_id, xmax_id, ymin_id, ymax_id = dmech.run_RivlinCube_Mesh(dim=dim, params=cube_params)
        elif (dim==3):
            mesh, boundaries_mf, xmin_id, xmax_id, ymin_id, ymax_id, zmin_id, zmax_id = dmech.run_RivlinCube_Mesh(dim=dim, params=cube_params)

    domains_mf = None
    if ("generic_zones" in cube_params):
        if len(mat_params)>1 :
            ymin = mesh.coordinates()[:, 1].min()
            ymax = mesh.coordinates()[:, 1].max()
            delta_y = ymax - ymin
            tol = 1E-14
            number_zones = len(mat_params)
            length_zone = delta_y/number_zones
            domains_mf = dolfin.MeshFunction('size_t', mesh, mesh.topology().dim())
            domains_mf.set_all(0)
            subdomain_lst = []
            for mat_id in range(number_zones-1, -1, -1):
                subdomain_lst.append(dolfin.CompiledSubDomain("x[1] <= y1 - tol",  y1=ymax-length_zone*(number_zones-1-mat_id), tol=tol))
                subdomain_lst[number_zones-1-mat_id].mark(domains_mf, mat_id)
                mat_params[mat_id]["subdomain_id"] = mat_id

    if move_params.get("move", False) == True :
        Umove = move_params.get("U")
        dolfin.ALE.move(mesh, Umove)

    ################################################################ Porosity ###

    porosity_type = porosity_params.get("type", "constant")
    porosity_val  = porosity_params.get("val", 0.5)

    if (porosity_type == "constant"):
        porosity_fun = None
    elif (porosity_type=="from_file"):
        porosity_filename = porosity_val
        porosity_mf = dolfin.MeshFunction(
            "double",
            mesh,
            porosity_filename)       
        porosity_expr = dolfin.CompiledExpression(getattr(dolfin.compile_cpp_code(dmech.get_ExprMeshFunction_cpp_pybind()), "MeshExpr")(), mf=porosity_mf, degree=0)
        porosity_fs = dolfin.FunctionSpace(mesh, 'DG', 0)
        porosity_fun = dolfin.interpolate(porosity_expr, porosity_fs)
        porosity_val = None
    elif (porosity_type.startswith("mesh_function")):
        if (porosity_type == "mesh_function_constant"):
            porosity_mf = dolfin.MeshFunction(
                value_type="double",
                mesh=mesh,
                dim=dim,
                value=porosity_val)
        elif (porosity_type == "mesh_function_xml"):
            porosity_filename = res_basename+"-poro.xml"
            n_cells = len(mesh.cells())
            with open(porosity_filename, "w") as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('<dolfin xmlns:dolfin="http://fenicsproject.org">\n')
                file.write('  <mesh_function type="double" dim="'+str(dim)+'" size="'+str(n_cells)+'">\n')
                for k_cell in range(n_cells):
                    file.write('    <entity index="'+str(k_cell)+'" value="'+str(porosity_val)+'"/>\n')
                file.write('  </mesh_function>\n')
                file.write('</dolfin>\n')
                file.close()
            porosity_mf = dolfin.MeshFunction(
                "double",
                mesh,
                porosity_filename)
        elif (porosity_type == "mesh_function_random_xml"):
            # print("mesh_function xml")
            porosity_filename = res_basename+"-poro.xml"
            n_cells = len(mesh.cells())
            with open(porosity_filename, "w") as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('<dolfin xmlns:dolfin="http://fenicsproject.org">\n')
                file.write('  <mesh_function type="double" dim="'+str(dim)+'" size="'+str(n_cells)+'">\n')
                for k_cell in range(n_cells):
                    value = numpy.random.uniform(low=0.4, high=0.6)
                            # positive_value = True
                    file.write('    <entity index="'+str(k_cell)+'" value="'+str(value)+'"/>\n')
                file.write('  </mesh_function>\n')
                file.write('</dolfin>\n')
                file.close()
            porosity_mf = dolfin.MeshFunction(
                "double",
                mesh,
                porosity_filename)
        porosity_expr = dolfin.CompiledExpression(getattr(dolfin.compile_cpp_code(dmech.get_ExprMeshFunction_cpp_pybind()), "MeshExpr")(), mf=porosity_mf, degree=0)
        porosity_fs = dolfin.FunctionSpace(mesh, 'DG', 0)
        porosity_fun = dolfin.interpolate(porosity_expr, porosity_fs)
        porosity_val = None
    elif (porosity_type.startswith("function")):
        porosity_fs = dolfin.FunctionSpace(mesh, 'DG', 0)
        if (porosity_type == "function_constant"):
            porosity_fun = dolfin.Function(porosity_fs)
            porosity_fun.vector()[:] = porosity_val
        elif (porosity_type == "function_xml"):
            porosity_filename = res_basename+"-poro.xml"
            n_cells = len(mesh.cells())
            with open(porosity_filename, "w") as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('<dolfin xmlns:dolfin="http://fenicsproject.org">\n')
                file.write('  <function_data size="'+str(n_cells)+'">\n')
                for k_cell in range(n_cells):
                    file.write('    <dof index="'+str(k_cell)+'" value="'+str(porosity_val)+'" cell_index="'+str(k_cell)+'" cell_dof_index="0"/>\n')
                file.write('  </function_data>\n')
                file.write('</dolfin>\n')
                file.close()
            porosity_fun = dolfin.Function(
                porosity_fs,
                porosity_filename)
        elif (porosity_type == "function_xml_from_array"):
            # print("function xml")
            porosity_filename = res_basename+"-poro.xml"
            # print("porosity_filename=", porosity_filename)
            n_cells = len(mesh.cells())
            with open(porosity_filename, "w") as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('<dolfin xmlns:dolfin="http://fenicsproject.org">\n')
                file.write('  <function_data size="'+str(n_cells)+'">\n')
                for k_cell in range(n_cells):
                    # print("kcell=", k_cell)
                    # print("porosity for kcell", porosity_val[k_cell])
                    file.write('    <dof index="'+str(k_cell)+'" value="'+str(porosity_val[k_cell])+'" cell_index="'+str(k_cell)+'" cell_dof_index="0"/>\n')
                file.write('  </function_data>\n')
                file.write('</dolfin>\n')
                file.close()
            porosity_fun = dolfin.Function(
                porosity_fs,
                porosity_filename)
        porosity_val = None

    ################################################################ Problem ###
    load_type = load_params.get("type", "internal")

    if load_type=="p_boundary_condition0":
        gradient_operators="inverse"
    elif load_type=="p_boundary_condition":
        gradient_operators="direct"
    else:
        gradient_operators=None

    if (type(mat_params) == list):
        skel_behavior=None
        skel_behaviors=mat_params
        bulk_behavior=None
        bulk_behaviors=mat_params
        pore_behavior=None
        pore_behaviors=mat_params
    else:
        skel_behavior=mat_params
        skel_behaviors=[]
        bulk_behavior=mat_params
        bulk_behaviors=[]
        pore_behavior=mat_params
        pore_behaviors=[]
    
    if (inverse):
        problem = dmech.InversePoroHyperelasticityProblem(
            mesh=mesh,
            define_facet_normals=1,
            boundaries_mf=boundaries_mf,
            domains_mf = domains_mf,
            displacement_degree=1,
            quadrature_degree = 6,
            porosity_init_val=porosity_val,
            porosity_init_fun=porosity_fun,
            skel_behavior=skel_behavior,
            skel_behaviors=skel_behaviors,
            bulk_behavior=bulk_behavior,
            bulk_behaviors=bulk_behaviors,
            pore_behavior=pore_behavior,
            pore_behaviors=pore_behaviors,
            gradient_operators=gradient_operators)
    else:
        problem = dmech.PoroHyperelasticityProblem(
            mesh=mesh,
            define_facet_normals=1,
            boundaries_mf=boundaries_mf,
            domains_mf = domains_mf,
            displacement_degree=1,
            quadrature_degree = 6,
            porosity_init_val=porosity_val,
            porosity_init_fun=porosity_fun,
            skel_behavior=skel_behavior,
            skel_behaviors=skel_behaviors,
            bulk_behavior=bulk_behavior,
            bulk_behaviors=bulk_behaviors,
            pore_behavior=pore_behavior,
            pore_behaviors=pore_behaviors,
            gradient_operators=gradient_operators)

    ########################################## Boundary conditions & Loading ###
    
    n_steps = step_params.get("n_steps", 1)
    Deltat_lst = step_params.get("Deltat_lst", [step_params.get("Deltat", 1.)/n_steps]*n_steps)
    dt_ini_lst = step_params.get("dt_ini_lst", [step_params.get("dt_ini", 1.)/n_steps]*n_steps)
    dt_min_lst = step_params.get("dt_min_lst", [step_params.get("dt_min", 1.)/n_steps]*n_steps)

    load_type = load_params.get("type", "internal")

    if   (load_type == "internal"):
        pf_lst = load_params.get("pf_lst", [(k_step+1)*load_params.get("pf", +0.5)/n_steps for k_step in range(n_steps)])
    elif (load_type in ("external0", "external")):
        P_lst = load_params.get("P_lst", [(k_step+1)*load_params.get("P", -0.5)/n_steps for k_step in range(n_steps)])
    elif (load_type in ("p_boundary_condition0", "p_boundary_condition")):
        f_lst = load_params.get("f_lst", [(k_step+1)*load_params.get("f", 1e4)/n_steps for k_step in range(n_steps)])
        P0_lst = load_params.get("P0_lst", [(k_step+1)*load_params.get("P0", -0.50)/n_steps for k_step in range(n_steps)])
    
    for k_step in range(n_steps):

        Deltat = Deltat_lst[k_step]
        dt_ini = dt_ini_lst[k_step]
        dt_min = dt_min_lst[k_step]

        k_step = problem.add_step(
            Deltat=Deltat,
            dt_ini=dt_ini,
            dt_min=dt_min)

        if (load_type == "internal"):
            pf = pf_lst[k_step]
            pf_old = pf_lst[k_step-1] if (k_step > 0) else 0.
            problem.add_pf_operator(
                measure=problem.dV,
                pf_ini=pf_old, pf_fin=pf,
                k_step=k_step)
        elif (load_type == "external"):
            problem.add_pf_operator(
                measure=problem.dV,
                pf_ini=0., pf_fin=0.,
                k_step=k_step)
            P = P_lst[k_step]
            P_old = P_lst[k_step-1] if (k_step > 0) else 0.
            problem.add_surface_pressure_loading_operator(
                measure=problem.dS(xmax_id),
                P_ini=P_old, P_fin=P,
                k_step=k_step)
            problem.add_surface_pressure_loading_operator(
                measure=problem.dS(ymax_id),
                P_ini=P_old, P_fin=P,
                k_step=k_step)
            if (dim==3): problem.add_surface_pressure_loading_operator(
                measure=problem.dS(zmax_id),
                P_ini=P_old, P_fin=P,
                k_step=k_step)
        elif (load_type == "external0"):
            problem.add_pf_operator(
                measure=problem.dV,
                pf_ini=0., pf_fin=0.,
                k_step=k_step)
            P = P_lst[k_step]
            P_old = P_lst[k_step-1] if (k_step > 0) else 0.
            problem.add_surface_pressure0_loading_operator(
                measure=problem.dS(xmax_id),
                P_ini=P_old, P_fin=P,
                k_step=k_step)
            problem.add_surface_pressure0_loading_operator(
                measure=problem.dS(ymax_id),
                P_ini=P_old, P_fin=P,
                k_step=k_step)
            if (dim==3): problem.add_surface_pressure0_loading_operator(
                measure=problem.dS(zmax_id),
                P_ini=P_old, P_fin=P,
                k_step=k_step)
        elif (load_type == "p_boundary_condition0"):
            problem.add_pf_operator(
                measure=problem.dV,
                pf_ini=0.,
                pf_fin=0.,
                k_step=k_step)
            f = f_lst[k_step]
            f_old = f_lst[k_step-1] if (k_step > 0) else 0.
            P0 = P0_lst[k_step]
            P0_old = P0_lst[k_step-1] if (k_step > 0) else 0.
            if type(mat_params)==list:
                rho_solid = mat_params[0].get("parameters").get("rho_solid", 1e-6)
            else:
                rho_solid = mat_params.get("parameters").get("rho_solid", 1e-6)
            problem.add_pressure_balancing_gravity0_loading_operator(
                dV=problem.dV,
                dS=problem.dS,
                f_ini=[0., f_old, 0.],
                # f_fin=[f, 0., 0.],
                f_fin=[0., f, 0],
                rho_solid=rho_solid,
                phis=problem.phis,
                P0_ini=P0_old,
                P0_fin=P0,
                breathing_constant=load_params.get("H", 0.),
                k_step=k_step)
        elif (load_type == "p_boundary_condition"):
            problem.add_pf_operator(
                measure=problem.dV,
                pf_ini=0.,
                pf_fin=0.,
                k_step=k_step)
            f = f_lst[k_step]
            f_old = f_lst[k_step-1] if (k_step > 0) else 0.
            P0 = P0_lst[k_step]
            P0_old = P0_lst[k_step-1] if (k_step > 0) else 0.
            if type(mat_params)==list:
                rho_solid = mat_params[0].get("parameters").get("rho_solid", 1e-6)
            else:
                rho_solid = mat_params.get("parameters").get("rho_solid", 1e-6)

            problem.add_pressure_balancing_gravity_loading_operator(
                dV=problem.dV,
                dS=problem.dS,
                f_ini=[0., f_old, 0],
                # f_fin=[f, 0., 0.],
                f_fin=[0., f, 0],
                rho_solid=rho_solid,
                P0_ini=P0_old,
                P0_fin=P0,
                breathing_constant=load_params.get("H", 0.),
                k_step=k_step)
        
        if not inertia_params["applied"]:
            problem.add_constraint(V=problem.get_displacement_function_space().sub(0), sub_domains=boundaries_mf, sub_domain_id=xmin_id, val=0.)
            problem.add_constraint(V=problem.get_displacement_function_space().sub(1), sub_domains=boundaries_mf, sub_domain_id=ymin_id, val=0.)
            if (dim==3):
                problem.add_constraint(V=problem.get_displacement_function_space().sub(2), sub_domains=boundaries_mf, sub_domain_id=zmin_id, val=0.)
        else:
            rho_val=inertia_params.get("rho_val", 1e-6)
            problem.add_inertia_operator(
            measure=problem.dV,
            rho_val=rho_val,
            k_step=k_step)

    ################################################# Quantities of Interest ###

    problem.add_deformed_volume_qoi()
    problem.add_global_strain_qois()
    problem.add_global_stress_qois()
    problem.add_global_porosity_qois()
    problem.add_global_fluid_pressure_qoi()

    ################################################################# Solver ###

    solver = dmech.NonlinearSolver(
        problem=problem,
        parameters={
            "sol_tol":[1e-6]*len(problem.subsols),
            "n_iter_max":32},
        relax_type="constant",
        write_iter=0)

    integrator = dmech.TimeIntegrator(
        problem=problem,
        solver=solver,
        parameters={
            "n_iter_for_accel":4,
            "n_iter_for_decel":16,
            "accel_coeff":2,
            "decel_coeff":2},
        print_out=res_basename*verbose,
        print_sta=res_basename*verbose,
        write_qois=res_basename+"-qois",
        write_qois_limited_precision=1,
        write_sol=res_basename*verbose)

    success = integrator.integrate()
    assert (success),\
        "Integration failed. Aborting."

    integrator.close()

    ################################################################## Plots ###

    if (plot_curves):
        qois_data = pandas.read_csv(
            res_basename+"-qois.dat",
            delim_whitespace=True,
            comment="#",
            names=open(res_basename+"-qois.dat").readline()[1:].split())

        qois_fig, qois_axes = mpl.subplots()
        all_strains = ["E_XX", "E_YY"]
        if (dim == 3): all_strains += ["E_ZZ"]
        all_strains += ["E_XY"]
        if (dim == 3): all_strains += ["E_YZ", "E_ZX"]
        qois_data.plot(x="t", y=all_strains, ax=qois_axes, ylabel="Green-Lagrange strain")
        qois_fig.savefig(res_basename+"-strains-vs-time.pdf")

        for comp in ["skel", "bulk", "tot"]:
            qois_fig, qois_axes = mpl.subplots()
            all_stresses = ["s_"+comp+"_XX", "s_"+comp+"_YY"]
            if (dim == 3): all_stresses += ["s_"+comp+"_ZZ"]
            all_stresses += ["s_"+comp+"_XY"]
            if (dim == 3): all_stresses += ["s_"+comp+"_YZ", "s_"+comp+"_ZX"]
            qois_data.plot(x="t", y=all_stresses, ax=qois_axes, ylabel="Cauchy stress")
            qois_fig.savefig(res_basename+"-stresses-"+comp+"-vs-time.pdf")

        qois_fig, qois_axes = mpl.subplots()
        all_porosities = []
        if (inverse):
            all_porosities += ["phis0", "phif0", "Phis0", "Phif0"]
        else:
            all_porosities += ["Phis", "Phif", "phis", "phif"]
        qois_data.plot(x="t", y=all_porosities, ax=qois_axes, ylim=[0,1], ylabel="porosity")
        qois_fig.savefig(res_basename+"-porosities-vs-time.pdf")

        qois_fig, qois_axes = mpl.subplots()
        qois_data.plot(x="pf", y=all_porosities, ax=qois_axes, ylim=[0,1], ylabel="porosity")
        qois_fig.savefig(res_basename+"-porosities-vs-pressure.pdf")
    
    if get_results:
        if inverse:
            phi = problem.get_foi(name="Phis0").func.vector().get_local()
        else:
            phi = problem.get_foi(name="phis").func.vector().get_local()
        return (problem.get_displacement_subsol().func, phi, dolfin.Measure("dx", domain=mesh))
