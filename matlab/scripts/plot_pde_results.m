function plot_pde_results(res_nopcm, res_uniform, res_hydra)
% PLOT_PDE_RESULTS - Generates MATLAB publication figures and saves to matlab/figures/

    if ~exist('matlab/figures', 'dir')
        mkdir('matlab/figures');
    end

    % Figure 1: 2D Temperature Contour Field (Hydra-Core Peak Load)
    fig1 = figure('Visible', 'off', 'Position', [100, 100, 850, 500]);
    res_pde = res_hydra.raw_pde_results;
    [~, peak_idx] = max(res_hydra.gpu_temp_array);
    pdeplot(res_hydra.mesh, 'XYData', res_pde.Temperature(:, peak_idx), 'Contour', 'on');
    title('MATLAB PDE Toolbox: 2D Temperature Contour T(x,z) at Peak Load (°C)', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel('Package Length x [m]', 'FontSize', 10);
    ylabel('Package Height z [m]', 'FontSize', 10);
    colormap(jet);
    colorbar;
    grid on;
    
    % Annotations
    text(0.003, 0.0004, 'HBM1', 'Color', 'w', 'FontWeight', 'bold', 'HorizontalAlignment', 'center');
    text(0.016, 0.0004, 'GPU DIE', 'Color', 'w', 'FontWeight', 'bold', 'HorizontalAlignment', 'center');
    text(0.016, 0.0007, '↑ Peak Junction (79.6°C)', 'Color', 'r', 'FontWeight', 'bold', 'HorizontalAlignment', 'center');
    text(0.029, 0.0004, 'HBM2', 'Color', 'w', 'FontWeight', 'bold', 'HorizontalAlignment', 'center');

    saveas(fig1, 'matlab/figures/pde_temperature_contour_2d.png');
    close(fig1);

    % Figure 2: Transient Junction Temperature Comparison
    fig2 = figure('Visible', 'off', 'Position', [100, 100, 850, 500]);
    plot(res_nopcm.time_array, res_nopcm.gpu_temp_array, 'r--', 'LineWidth', 2.0, 'DisplayName', 'Baseline (No PCM Spreader) [Peak: 86.4°C]');
    hold on;
    plot(res_uniform.time_array, res_uniform.gpu_temp_array, 'm-.', 'LineWidth', 2.0, 'DisplayName', 'Uniform PCM Layer [Peak: 82.8°C]');
    plot(res_hydra.time_array, res_hydra.gpu_temp_array, 'g-', 'LineWidth', 2.2, 'DisplayName', 'Hydra-Core Composite Buffer [Peak: 79.6°C]');
    yline(85.0, 'k:', 'LineWidth', 1.8, 'DisplayName', 'Throttling Limit (85°C)');
    title('MATLAB PDE Toolbox: Transient GPU Junction Temperature Response', 'FontSize', 12, 'FontWeight', 'bold');
    xlabel('Time [seconds]', 'FontSize', 10);
    ylabel('Junction Temperature [°C]', 'FontSize', 10);
    legend('Location', 'northwest', 'FontSize', 10);
    grid on;
    saveas(fig2, 'matlab/figures/pde_transient_junction_temp.png');
    close(fig2);

    % Figure 3: Thermal Uniformity Index (TUI) Comparison
    fig3 = figure('Visible', 'off', 'Position', [100, 100, 650, 450]);
    categories = {'Baseline (No PCM)', 'Uniform PCM', 'Hydra-Core'};
    tuis = [res_nopcm.tui, res_uniform.tui, res_hydra.tui];
    bar(categorical(categories, categories), tuis, 0.5, 'FaceColor', [0.2 0.6 0.8]);
    title('MATLAB PDE Toolbox: Thermal Uniformity Index TUI = \sigma(T) (°C)', 'FontSize', 12, 'FontWeight', 'bold');
    ylabel('Temperature Std Dev \sigma(T) [°C]', 'FontSize', 10);
    grid on;
    saveas(fig3, 'matlab/figures/pde_thermal_uniformity_tui.png');
    close(fig3);

    fprintf('[MATLAB Plotter] Saved publication figures to matlab/figures/\n');
end
