% MAIN.M - Master MATLAB PDE Toolbox Thermal Simulation Entrypoint for Hydra-Core
% 
% Executes 2D Transient FEM thermal simulations across cooling architectures,
% generates publication figures, validates against Python model, and exports results.

clear; clc; close all;

% Add paths for subdirectories
addpath(genpath(fileparts(mfilename('fullpath'))));

fprintf('================================================================================\n');
fprintf('   HYDRA-CORE: MATLAB PDE Toolbox 2D Transient Thermal Simulation Engine\n');
fprintf('================================================================================\n\n');

% Load Configuration
cfg = config_hydra_matlab();

% Time and Power Trace (LLM Inference Bursts)
sim_time = cfg.sim.t_end;
dt = cfg.sim.dt;
t_arr = 0:dt:sim_time;

% Synthesize LLM Inference Power Trace P(t)
p_arr = zeros(size(t_arr));
base_tdp = cfg.gpu.power;
for i = 1:length(t_arr)
    t = t_arr(i);
    cycle_time = mod(t, 10.0);
    if cycle_time < 1.5
        p_arr(i) = base_tdp * 1.25 + 20.0 * sin(2.0 * pi * 5.0 * t);
    elseif mod(cycle_time - 1.5, 0.5) < 0.15
        p_arr(i) = base_tdp * 1.0;
    else
        p_arr(i) = base_tdp * 0.55;
    end
    p_arr(i) = max(100.0, p_arr(i));
end

% 1. Run Case 1: No PCM (Solid Copper Spreader Baseline)
fprintf('[Step 1/4] Running MATLAB PDE Thermal Simulation: Case 1 (No PCM Baseline)...\n');
res_nopcm = run_pde_thermal_simulation('No_PCM', t_arr, p_arr, cfg);

% 2. Run Case 2: Uniform PCM Layer
fprintf('[Step 2/4] Running MATLAB PDE Thermal Simulation: Case 2 (Uniform PCM Layer)...\n');
res_uniform = run_pde_thermal_simulation('Uniform_PCM', t_arr, p_arr, cfg);

% 3. Run Case 3: Hydra-Core Workload-Aware Composite PCM
fprintf('[Step 3/4] Running MATLAB PDE Thermal Simulation: Case 3 (Hydra-Core Composite PCM)...\n');
res_hydra = run_pde_thermal_simulation('Hydra_Core', t_arr, p_arr, cfg);

% 4. Plot Figures and Validate against Python Model
fprintf('[Step 4/4] Generating MATLAB publication figures and cross-validating...\n');
plot_pde_results(res_nopcm, res_uniform, res_hydra);
validate_python_vs_matlab(res_hydra);

% Export MATLAB Simulation Results
if ~exist('results/matlab', 'dir')
    mkdir('results/matlab');
end

save('results/matlab/pde_thermal_results.mat', 'res_nopcm', 'res_uniform', 'res_hydra', 'cfg');

matlab_export_table = table(t_arr', p_arr', res_nopcm.gpu_temp_array, res_uniform.gpu_temp_array, res_hydra.gpu_temp_array, ...
    'VariableNames', {'Time_s', 'Power_W', 'GPU_Temp_NoPCM_degC', 'GPU_Temp_Uniform_degC', 'GPU_Temp_HydraCore_degC'});
writetable(matlab_export_table, 'results/matlab/pde_junction_temps.csv');

fprintf('[Export] Saved MATLAB results to results/matlab/pde_thermal_results.mat and pde_junction_temps.csv\n\n');

fprintf('=======================================================\n');
fprintf('  MATLAB PDE TOOLBOX SIMULATION SUMMARY\n');
fprintf('=======================================================\n');
fprintf('  Baseline Peak Junction Temp:     %.2f °C\n', res_nopcm.peak_temp);
fprintf('  Uniform PCM Peak Junction Temp:  %.2f °C\n', res_uniform.peak_temp);
fprintf('  Hydra-Core Peak Junction Temp:   %.2f °C\n', res_hydra.peak_temp);
fprintf('  Thermal Uniformity Index (TUI):  %.2f °C\n', res_hydra.tui);
fprintf('=======================================================\n');
fprintf('MATLAB SIMULATION ENGINE COMPLETE!\n\n');
