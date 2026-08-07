// Gmsh CAD Geometry Script for GPU Package Elmer FEM Simulation
// Dimensions in meters

SetFactory("OpenCASCADE");

L_gpu = 0.032;   // 32 mm
d_die = 0.00078; // 0.78 mm
d_tim = 0.00005; // 0.05 mm
d_pcm = 0.0002;  // 0.2 mm
d_cp  = 0.002;   // 2 mm

Rectangle(1) = {0, 0, 0, L_gpu, d_die};
Rectangle(2) = {0, d_die, 0, L_gpu, d_tim};
Rectangle(3) = {0, d_die + d_tim, 0, L_gpu, d_pcm};
Rectangle(4) = {0, d_die + d_tim + d_pcm, 0, L_gpu, d_cp};

Physical Surface("GPU_Die") = {1};
Physical Surface("TIM_Layer") = {2};
Physical Surface("PCM_Buffer") = {3};
Physical Surface("Cold_Plate") = {4};

Physical Line("Coolant_Top") = {4};
Physical Line("Insulated_Sides") = {1, 2, 3};

Mesh.CharacteristicLengthMax = 0.0005;
Mesh 2;
