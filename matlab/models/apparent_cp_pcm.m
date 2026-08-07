function [cp_eff, alpha_melt] = apparent_cp_pcm(location, state, cfg)
% APPARENT_CP_PCM - Non-linear Apparent Heat Capacity method for PCM phase change
% Location and state structs supplied by MATLAB PDE Toolbox thermal solver

    T = state.u;
    T_m = cfg.pcm.tmelt;
    dT_m = cfg.pcm.twins;
    L = cfg.pcm.latent_heat;
    sigma = dT_m / 2.5;

    % Liquid fraction alpha(T) using smooth tanh transition
    alpha_melt = 0.5 * (1.0 + tanh((T - T_m) / (dT_m / 2.0)));
    alpha_melt = max(0.0, min(1.0, alpha_melt));

    % Derivative d(alpha)/dT using Gaussian pulse
    d_alpha_dT = (1.0 / (sqrt(2.0 * pi) * sigma)) * exp(-0.5 * min(((T - T_m) / sigma).^2, 50.0));

    % Effective Heat Capacity
    cp_base = (1.0 - alpha_melt) * cfg.pcm.cp_solid + alpha_melt * cfg.pcm.cp_liquid;
    cp_eff = cp_base + L * d_alpha_dT;
end
