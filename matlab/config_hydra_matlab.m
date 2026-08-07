function cfg = config_hydra_matlab()
% CONFIG_HYDRA_MATLAB - Returns thermal parameters for GPU Package PDE Toolbox simulation
% 
% Architecture: GPU Die -> TIM -> PCM Buffer -> Microchannel Cold Plate

    % GPU Package Envelope (NVIDIA H100)
    cfg.gpu.length = 0.032;        % m (32 mm)
    cfg.gpu.width  = 0.025;        % m (25 mm)
    cfg.gpu.thick  = 0.00078;      % m (0.78 mm Silicon)
    cfg.gpu.power  = 700.0;        % W TDP
    cfg.gpu.k      = 130.0;        % W/m*K
    cfg.gpu.rho    = 2330.0;       % kg/m^3
    cfg.gpu.cp     = 700.0;        % J/kg*K

    % Thermal Interface Material (TIM)
    cfg.tim.thick  = 0.00005;      % m (0.05 mm)
    cfg.tim.k      = 15.0;         % W/m*K
    cfg.tim.rho    = 2500.0;       % kg/m^3
    cfg.tim.cp     = 500.0;        % J/kg*K

    % Phase Change Material (PCM) Buffer
    cfg.pcm.thick        = 0.0004;      % m (0.4 mm)
    cfg.pcm.tmelt        = 65.0;        % °C
    cfg.pcm.twins        = 2.0;         % °C
    cfg.pcm.latent_heat  = 220000.0;   % J/kg
    cfg.pcm.rho          = 1200.0;      % kg/m^3
    cfg.pcm.k_solid      = 65.0;        % W/m*K
    cfg.pcm.k_liquid     = 60.0;        % W/m*K
    cfg.pcm.k_hydracore  = 95.0;        % W/m*K (High-K Composite Matrix)
    cfg.pcm.cp_solid     = 1800.0;      % J/kg*K
    cfg.pcm.cp_liquid    = 2000.0;      % J/kg*K

    % Baseline Spreader (No PCM)
    cfg.spreader.k   = 400.0;       % W/m*K (Copper)
    cfg.spreader.rho = 8960.0;      % kg/m^3
    cfg.spreader.cp  = 385.0;       % J/kg*K

    % Microchannel Cold Plate
    cfg.cp.thick     = 0.002;       % m (2 mm Copper)
    cfg.cp.k         = 400.0;       % W/m*K
    cfg.cp.rho       = 8960.0;      % kg/m^3
    cfg.cp.cp        = 385.0;       % J/kg*K
    cfg.cp.h_conv    = 25000.0;     % W/m^2*K (Liquid Cooling)
    cfg.cp.t_coolant = 25.0;        % °C

    % Simulation Time Discretization
    cfg.sim.t_end    = 60.0;        % seconds
    cfg.sim.dt       = 0.1;         % seconds
    cfg.sim.t_init   = 25.0;        % °C
end
