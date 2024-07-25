#include "setup.hpp"
const uint lbm_T = 10000u; // number of LBM time steps to simulate
void main_setup() { //Case 1: Bucket JOHNS; required extensions in defines.hpp: FP16S, EQUILIBRIUM_BOUNDARIES, SUBGRID, INTERACTIVE_GRAPHICS or GRAPHICS
	// ################################################################## define simulation box size, viscosity and volume force ###################################################################
	const uint3 lbm_N = resolution(float3(0.2f, 1.0f, 0.2f), 1000u); // input: simulation box aspect ratio and VRAM occupation in MB, output: grid resolution
	const float si_u = 1.0f;
	const float si_length = 8.2f;
	const float si_T = 30.0f;
	const float si_nu=1.48E-5f, si_rho=1.225f;
	const float lbm_length = 0.2f*(float)lbm_N.y;
	const float lbm_u = 0.05f;
	units.set_m_kg_s(lbm_length, lbm_u, 1.0f, si_length, si_u, si_rho);
	print_info("Re = "+to_string(to_uint(units.si_Re(si_length, si_u, si_nu))));
	LBM lbm(lbm_N, units.nu(si_nu));
	// ###################################################################################### define geometry ######################################################################################
	const float3x3 rotation = float3x3(float3(1, 0, 0), radians(180.0f))*float3x3(float3(0, 0, 1), radians(180.0f));
	Mesh* mesh = read_stl(get_exe_path()+"/stl/SimpleBucket.stl", lbm.size(), lbm.center(), rotation, lbm_length);
	mesh->translate(float3(0.0f, mesh->pmin.y-4.2f*lbm_length, 0.0f));
	lbm.voxelize_mesh_on_device(mesh);
	Mesh* wmesh = read_stl(get_exe_path()+"/stl/Wall.stl", lbm.size(), lbm.center(), rotation, lbm_length);
	wmesh->translate(float3(0.0f, wmesh->pmin.y-4.2f*lbm_length, 0.0f));
	const uint Nx=lbm.get_Nx(), Ny=lbm.get_Ny(), Nz=lbm.get_Nz(); parallel_for(lbm.get_N(), [&](ulong n) { uint x=0u, y=0u, z=0u; lbm.coordinates(n, x, y, z);
		//if(z==0u) lbm.flags[n] = TYPE_S; // solid floor
		if(x==0u||x==Nx-1u||y==0u||y==Ny-1u||z==Nz-1u) lbm.flags[n] = TYPE_E; // all other simulation box boundaries are
		if(lbm.flags[n] == TYPE_E && y==0u) lbm.u.y[n] = lbm_u; // initialize y-velocity everywhere except in solid cellsinflow/outflow
		
	}); // ####################################################################### run simulation, export images and data ##########################################################################
	lbm.graphics.visualization_modes = VIS_FLAG_SURFACE|VIS_Q_CRITERION;
#if defined(GRAPHICS) && !defined(INTERACTIVE_GRAPHICS)
	lbm.graphics.set_camera_centered(-40.0f, 20.0f, 78.0f, 1.25f);
	lbm.run(0u); // initialize simulation
	while(lbm.get_t()<=units.t(si_T)) { // main simulation loop
		if(lbm.graphics.next_frame(units.t(si_T), 10.0f)) lbm.graphics.write_frame();
		lbm.run(1u);
	}
#else // GRAPHICS && !INTERACTIVE_GRAPHICS
        bool OBJSET = false;
	while(lbm.get_t()<lbm_T){
	lbm.run(1u);
        if(lbm.get_t()>=1000u && !OBJSET){
	lbm.voxelize_mesh_on_device(wmesh);
	OBJSET=true;
        }
	}
#endif // GRAPHICS && !INTERACTIVE_GRAPHICS
} /**/
