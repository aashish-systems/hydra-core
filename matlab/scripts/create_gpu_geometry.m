function [model, face_ids, total_height] = create_gpu_geometry(cfg)
% CREATE_GPU_GEOMETRY - Programmatically creates 2D multi-domain package geometry with HBM stacks
% 
% Package Layout across x-axis (32 mm total):
% Face 1: HBM Stack 1 (0 to 6 mm)
% Face 2: GPU Die (6 to 26 mm)
% Face 3: HBM Stack 2 (26 to 32 mm)
% Face 4: TIM Layer (0 to 32 mm)
% Face 5: PCM Buffer (0 to 32 mm)
% Face 6: Cold Plate (0 to 32 mm)

    model = createpde('thermal', 'transient');

    L_hbm = 0.006;                  % 6 mm HBM stack width
    L_gpu = cfg.gpu.length - 2*L_hbm; % 20 mm GPU die width
    L_tot = cfg.gpu.length;          % 32 mm total package length

    d1 = cfg.gpu.thick;
    d2 = cfg.tim.thick;
    d3 = cfg.pcm.thick;
    d4 = cfg.cp.thick;

    z0 = 0.0;
    z1 = z0 + d1;
    z2 = z1 + d2;
    z3 = z2 + d3;
    z4 = z3 + d4;
    total_height = z4;

    % Rectangles for 2D Package [3; 4; x1; x2; x3; x4; y1; y2; y3; y4]
    r_hbm1 = [3; 4; 0; L_hbm; L_hbm; 0; z0; z0; z1; z1];
    r_gpu  = [3; 4; L_hbm; L_hbm+L_gpu; L_hbm+L_gpu; L_hbm; z0; z0; z1; z1];
    r_hbm2 = [3; 4; L_hbm+L_gpu; L_tot; L_tot; L_hbm+L_gpu; z0; z0; z1; z1];
    r_tim  = [3; 4; 0; L_tot; L_tot; 0; z1; z1; z2; z2];
    r_pcm  = [3; 4; 0; L_tot; L_tot; 0; z2; z2; z3; z3];
    r_cp   = [3; 4; 0; L_tot; L_tot; 0; z3; z3; z4; z4];

    gd = [r_hbm1, r_gpu, r_hbm2, r_tim, r_pcm, r_cp];
    ns = char('R1', 'R2', 'R3', 'R4', 'R5', 'R6')';
    sf = 'R1 + R2 + R3 + R4 + R5 + R6';

    [g, ~] = decsg(gd, sf, ns);
    geometryFromEdges(model, g);

    face_ids.hbm1 = 1;
    face_ids.gpu  = 2;
    face_ids.hbm2 = 3;
    face_ids.tim  = 4;
    face_ids.pcm  = 5;
    face_ids.cp   = 6;
end
