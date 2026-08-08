// Hydra-Core 3D WebGL Package Thermal Visualizer Application

let scene, camera, renderer, controls;
let dieMesh, timMesh, pcmMesh, coldPlateMesh, particles;
let tempChart;

// Initialize Three.js 3D Canvas Scene
function init3D() {
  const container = document.getElementById("canvas-container");
  const width = container.clientWidth;
  const height = container.clientHeight;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x05070a);

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.set(40, 30, 50);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.appendChild(renderer.domElement);

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);

  const dirLight1 = new THREE.DirectionalLight(0x00f2fe, 0.8);
  dirLight1.position.set(20, 40, 20);
  scene.add(dirLight1);

  const dirLight2 = new THREE.DirectionalLight(0xff7e5f, 0.5);
  dirLight2.position.set(-20, -10, -20);
  scene.add(dirLight2);

  // Orbit Controls
  if (typeof THREE.OrbitControls !== 'undefined') {
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
  }

  // Create GPU Package Layers (3D Box Geometries)
  // Layer 1: Silicon Die (Bottom, y = 0.39)
  const dieGeo = new THREE.BoxGeometry(32, 0.78, 32);
  const dieMat = new THREE.MeshStandardMaterial({ color: 0xff3300, roughness: 0.3, metalness: 0.2 });
  dieMesh = new THREE.Mesh(dieGeo, dieMat);
  dieMesh.position.set(0, 0.39, 0);
  scene.add(dieMesh);

  // Layer 2: TIM-1 Layer (y = 0.78 + 0.025 = 0.805)
  const timGeo = new THREE.BoxGeometry(32, 0.05, 32);
  const timMat = new THREE.MeshStandardMaterial({ color: 0xffcc00, roughness: 0.5 });
  timMesh = new THREE.Mesh(timGeo, timMat);
  timMesh.position.set(0, 0.805, 0);
  scene.add(timMesh);

  // Layer 3: Composite PCM Buffer (y = 0.83 + 0.10 = 0.93)
  const pcmGeo = new THREE.BoxGeometry(32, 0.20, 32);
  const pcmMat = new THREE.MeshStandardMaterial({ color: 0x00ff66, roughness: 0.4, opacity: 0.9, transparent: true });
  pcmMesh = new THREE.Mesh(pcmGeo, pcmMat);
  pcmMesh.position.set(0, 0.93, 0);
  scene.add(pcmMesh);

  // Layer 4: Copper Cold Plate (y = 1.03 + 1.0 = 2.03)
  const cpGeo = new THREE.BoxGeometry(32, 2.00, 32);
  const cpMat = new THREE.MeshStandardMaterial({ color: 0x4facfe, roughness: 0.2, opacity: 0.85, transparent: true });
  coldPlateMesh = new THREE.Mesh(cpGeo, cpMat);
  coldPlateMesh.position.set(0, 2.03, 0);
  scene.add(coldPlateMesh);

  // Add Grid Helper
  const gridHelper = new THREE.GridHelper(60, 20, 0x00f2fe, 0x12161f);
  gridHelper.position.y = -0.5;
  scene.add(gridHelper);

  // Create Animated Heat Flow Particles
  createHeatParticles();

  // Animation Loop
  function animate() {
    requestAnimationFrame(animate);
    if (controls) controls.update();

    // Pulse die material emission with heat power
    const time = Date.now() * 0.003;
    dieMat.emissive.setHSL(0.02, 0.9, 0.15 + 0.05 * Math.sin(time));

    // Animate heat particles moving upward through stack
    if (particles) {
      const positions = particles.geometry.attributes.position.array;
      for (let i = 1; i < positions.length; i += 3) {
        positions[i] += 0.08;
        if (positions[i] > 3.5) {
          positions[i] = 0.0;
        }
      }
      particles.geometry.attributes.position.needsUpdate = true;
    }

    renderer.render(scene, camera);
  }

  animate();

  window.addEventListener("resize", onWindowResize);
}

function createHeatParticles() {
  const count = 300;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(count * 3);

  for (let i = 0; i < count; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 30;
    positions[i * 3 + 1] = Math.random() * 3.5;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 30;
  }

  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));

  const material = new THREE.PointsMaterial({
    color: 0x00f2fe,
    size: 0.6,
    transparent: true,
    opacity: 0.7
  });

  particles = new THREE.Points(geometry, material);
  scene.add(particles);
}

function onWindowResize() {
  const container = document.getElementById("canvas-container");
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
}

// Initialize Chart.js Transient Temperature Graph
function initChart() {
  const ctx = document.getElementById("tempChart").getContext("2d");
  
  const labels = Array.from({ length: 41 }, (_, i) => (i * 0.5).toFixed(1));
  const elmerData = labels.map(t => 25.0 + (53.52 - 25.0) * (1.0 - Math.exp(-t / 3.5)));
  const baselineData = labels.map(t => 25.0 + (55.57 - 25.0) * (1.0 - Math.exp(-t / 2.8)));
  const hydraData = labels.map(t => 25.0 + (53.07 - 25.0) * (1.0 - Math.exp(-t / 3.6)));

  tempChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Elmer FEM 2D Native (700W)",
          data: elmerData,
          borderColor: "#ff7e5f",
          backgroundColor: "rgba(255, 126, 95, 0.1)",
          borderWidth: 2,
          pointRadius: 2
        },
        {
          label: "Python Hydra-Core Composite PCM",
          data: hydraData,
          borderColor: "#00f2fe",
          borderWidth: 2,
          pointRadius: 0
        },
        {
          label: "Baseline (No PCM)",
          data: baselineData,
          borderColor: "#e41a1c",
          borderDash: [5, 5],
          borderWidth: 2,
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#f0f4f8" } }
      },
      scales: {
        x: {
          title: { display: true, text: "Time (seconds)", color: "#8a99ad" },
          ticks: { color: "#8a99ad" },
          grid: { color: "rgba(255,255,255,0.05)" }
        },
        y: {
          title: { display: true, text: "Junction Temp (°C)", color: "#8a99ad" },
          ticks: { color: "#8a99ad" },
          grid: { color: "rgba(255,255,255,0.05)" }
        }
      }
    }
  });
}

// UI Event Listeners
function setupEvents() {
  const slider = document.getElementById("power-slider");
  const powerVal = document.getElementById("power-val");

  slider.addEventListener("input", (e) => {
    const val = e.target.value;
    powerVal.innerText = val;
    
    // Update metrics dynamically
    const t_peak = (25.0 + (val / 700.0) * (53.52 - 25.0)).toFixed(2);
    document.getElementById("val-temp").innerText = `${t_peak} °C`;
  });

  // Layer toggle buttons
  document.querySelectorAll(".btn-layer").forEach(btn => {
    btn.addEventListener("click", () => {
      btn.classList.toggle("active");
      const layer = btn.dataset.layer;
      
      if (layer === "die") dieMesh.visible = !dieMesh.visible;
      if (layer === "tim") timMesh.visible = !timMesh.visible;
      if (layer === "pcm") pcmMesh.visible = !pcmMesh.visible;
      if (layer === "coldplate") coldPlateMesh.visible = !coldPlateMesh.visible;
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  init3D();
  initChart();
  setupEvents();
});
