import * as THREE from 'https://unpkg.com/three@0.128.0/build/three.module.js';

function initSpiralVisualizer() {
    const container = document.getElementById('forge-spiral');
    if (!container) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // Create a particle spiral
    const geometry = new THREE.BufferGeometry();
    const particleCount = 1000;
    const posArray = new Float32Array(particleCount * 3);

    for(let i = 0; i < particleCount; i++) {
        // Parametric equation for a 3D spiral (Codemap DNA structure)
        const t = i * 0.1;
        const x = Math.cos(t) * (t * 0.05);
        const y = t * 0.05 - 15;
        const z = Math.sin(t) * (t * 0.05);
        posArray[i*3] = x;
        posArray[i*3+1] = y;
        posArray[i*3+2] = z;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const material = new THREE.PointsMaterial({ size: 0.1, color: 0xA1C1D1 });
    const pointsMesh = new THREE.Points(geometry, material);
    scene.add(pointsMesh);

    camera.position.z = 20;

    function animateSpiral() {
        requestAnimationFrame(animateSpiral);
        pointsMesh.rotation.y += 0.005;
        pointsMesh.rotation.x += 0.001;
        renderer.render(scene, camera);
    }
    animateSpiral();
}

export function initCubixEnvironment() {
    initSpiralVisualizer();
    
    const navContainer = document.getElementById('bottom-navigator');
    const world = document.getElementById('world');
    const envCube = document.getElementById('environment-cube'); // Inner AGI
    const outerCube = document.getElementById('outer-cube'); // Outer External

    // --- SYSTEM TIME UPDATER ---
    const timeNode = document.getElementById('sys-time');
    setInterval(() => {
        const now = new Date();
        timeNode.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }, 1000);
    timeNode.innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    // --- THREE.JS BOTTOM NAVIGATOR ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, navContainer.clientWidth / navContainer.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

    renderer.setSize(navContainer.clientWidth, navContainer.clientHeight); 
    navContainer.appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry(2, 2, 2);

    // Dynamically generate an HD Canvas Texture for the CUBIX Logo
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');

    // Background Panel
    ctx.fillStyle = '#0d1117';
    ctx.fillRect(0, 0, 512, 512);
    // Glowing border
    ctx.strokeStyle = '#A1C1D1';
    ctx.lineWidth = 15;
    ctx.strokeRect(15, 15, 482, 482);
    // Radial Core Glow
    const gradient = ctx.createRadialGradient(256, 256, 20, 256, 256, 300);
    gradient.addColorStop(0, 'rgba(112, 225, 0, 0.4)'); // Green AGI glow in center
    gradient.addColorStop(0.5, 'rgba(161, 193, 209, 0.1)'); // Blue mid
    gradient.addColorStop(1, '#0d1117');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 512, 512);
    // Text Logo
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 90px "Outfit", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('CUBIX', 256, 210);
    ctx.fillStyle = '#8892B0';
    ctx.font = '400 50px "Outfit", sans-serif';
    ctx.fillText('TESSERACT', 256, 290);
    ctx.fillStyle = '#70E100';
    ctx.font = '900 30px "Outfit", sans-serif';
    ctx.fillText('• SOVEREIGN •', 256, 420);

    const logoTexture = new THREE.CanvasTexture(canvas);
    
    // Physical material to look like glowing machinery
    const material = new THREE.MeshStandardMaterial({ 
        map: logoTexture,
        metalness: 0.8,
        roughness: 0.2,
        emissive: 0x112233
    });

    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    
    // Add lighting to make the cube visible and shiny
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    const pointLight = new THREE.PointLight(0xA1C1D1, 2, 50);
    pointLight.position.set(5, 5, 5);
    scene.add(ambientLight);
    scene.add(pointLight);

    camera.position.z = 3.5;

    // --- INTERACTION LOGIC (Dual Layer Matrix) ---
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    
    let targetRotationYInner = 0; 
    let targetRotationYOuter = 0; 
    
    let currentZLevel = -50; 
    const Z_LEVELS = {
        outer: -280, // Far back to see the giant outer cube
        inner: -50   // Locked inside the inner AGI room
    };
    let targetRotationX = 0;
    let dragDistanceY = 0;

    navContainer.addEventListener('mousedown', (e) => { 
        isDragging = true; 
        dragDistanceY = 0; 
        previousMousePosition = { x: e.clientX, y: e.clientY };
        navContainer.style.cursor = 'grabbing';
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const deltaX = e.clientX - previousMousePosition.x;
        const deltaY = e.clientY - previousMousePosition.y;
        dragDistanceY += deltaY;

        // Rotate the mini-cube instantly with drag Y
        cube.rotation.y += deltaX * 0.01;
        cube.rotation.x += deltaY * 0.005; 
        previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', (e) => {
        if (!isDragging) return;
        isDragging = false;
        navContainer.style.cursor = 'grab';

        // Snap Y-axis of the mini-cube to nearest 90 degrees
        const snapAngle = Math.PI / 2;
        const lockedY = Math.round(cube.rotation.y / snapAngle) * snapAngle;
        
        // Snap X-axis strictly to 0 to keep the room level
        targetRotationX = 0;

        // Quick Zoom Out Logic
        if (dragDistanceY > 100) {
            currentZLevel = Z_LEVELS.outer; // Move world away
        } else if (dragDistanceY < -100) {
            currentZLevel = Z_LEVELS.inner; // Move world closer
        }

        // Determine which layer's rotation to update based on Zoom State 
        // Note: The navigator mini-cube visually matches the currently active layer
        if (currentZLevel === Z_LEVELS.inner) {
            targetRotationYInner = lockedY;
            // Align mini-cube natively with the inner layer logic
            cube.rotation.y = targetRotationYInner;
        } else {
            targetRotationYOuter = lockedY;
            // Align mini-cube natively with the outer layer logic
            cube.rotation.y = targetRotationYOuter;
        }

        // Apply transformations globally
        // 1. Move World backward or forward
        world.style.transform = `translateZ(${currentZLevel}vw)`;

        // 2. Spin the specific cubes independently!
        const cssRotationInner = -(targetRotationYInner * (180 / Math.PI));
        envCube.style.transform = `rotateY(${cssRotationInner}deg)`;

        const cssRotationOuter = -(targetRotationYOuter * (180 / Math.PI));
        outerCube.style.transform = `rotateY(${cssRotationOuter}deg)`;
    });

    // --- CUBIX RUBYS (QUICK NAV) LOGIC ---
    function applyMatrixState() {
        world.style.transform = `translateZ(${currentZLevel}vw)`;
        envCube.style.transform = `rotateY(${-(targetRotationYInner * (180 / Math.PI))}deg)`;
        outerCube.style.transform = `rotateY(${-(targetRotationYOuter * (180 / Math.PI))}deg)`;
        
        // Sync navigator cube to current active layer
        const targetNavY = (currentZLevel === Z_LEVELS.inner) ? targetRotationYInner : targetRotationYOuter;
        cube.rotation.y = targetNavY;

        // Reset X (pitch) to level
        targetRotationX = 0;
        cube.rotation.x = 0;
    }

    document.getElementById('ruby-c')?.addEventListener('click', () => {
        if (currentZLevel === Z_LEVELS.inner) targetRotationYInner = 0; else targetRotationYOuter = 0;
        applyMatrixState();
    });
    document.getElementById('ruby-u')?.addEventListener('click', () => {
        if (currentZLevel === Z_LEVELS.inner) targetRotationYInner = Math.PI / 2; else targetRotationYOuter = Math.PI / 2;
        applyMatrixState();
    });
    document.getElementById('ruby-b')?.addEventListener('click', () => {
        if (currentZLevel === Z_LEVELS.inner) targetRotationYInner = Math.PI; else targetRotationYOuter = Math.PI;
        applyMatrixState();
    });
    document.getElementById('ruby-i')?.addEventListener('click', () => {
        if (currentZLevel === Z_LEVELS.inner) targetRotationYInner = -Math.PI / 2; else targetRotationYOuter = -Math.PI / 2;
        applyMatrixState();
    });
    document.getElementById('ruby-x')?.addEventListener('click', () => {
        currentZLevel = (currentZLevel === Z_LEVELS.inner) ? Z_LEVELS.outer : Z_LEVELS.inner;
        applyMatrixState();
    });

    function animate() {
        requestAnimationFrame(animate);
        
        // Smoothly snap the mini cube to its designated layer rotation
        if (!isDragging) {
            const activeTargetY = (currentZLevel === Z_LEVELS.inner) ? targetRotationYInner : targetRotationYOuter;
            cube.rotation.y += (activeTargetY - cube.rotation.y) * 0.1;
            cube.rotation.x += (targetRotationX - cube.rotation.x) * 0.1;
        }
        
        renderer.render(scene, camera);
    }
    animate();

    // --- SOVEREIGN BRIDGE (SYNC UI <-> PYTHON) ---
    const BRIDGE_URL = "http://localhost:8081";

    function initOmniBridge() {
        const chatFeed = document.getElementById('omni-chat-feed');
        
        // Poll for security/system alerts from GAPCI/Librarian
        setInterval(async () => {
            try {
                const res = await fetch(`${BRIDGE_URL}/omni/alerts`);
                const data = await res.json();
                if (data.alerts && data.alerts.length > 0) {
                    data.alerts.forEach(alert => {
                        const div = document.createElement('div');
                        div.className = "chat-msg msg-ai";
                        div.style.color = "#FF4B2B"; // Security Alert Red
                        div.innerText = `[ALERT] ${alert}`;
                        chatFeed.appendChild(div);
                        chatFeed.scrollTop = chatFeed.scrollHeight;
                    });
                }
            } catch(e) {}
        }, 3000);
    }

    function initVaultBridge() {
        const terminalInput = document.getElementById('terminal-input');
        const terminalFeed = document.getElementById('terminal-feed');

        terminalInput?.addEventListener('keydown', async (e) => {
            if (e.key === 'Enter') {
                const cmd = terminalInput.value.trim();
                terminalInput.value = "";
                
                // Append local command to feed
                const line = document.createElement('div');
                line.innerHTML = `<span style="color:#70E100;">randall@tesseract:~$</span> ${cmd}`;
                terminalFeed.appendChild(line);

                // Check for Summon command logic (e.g., "summon 0x0001,0x0002")
                if (cmd.startsWith('summon ')) {
                    const addresses = cmd.replace('summon ', '').split(',').map(s => s.trim());
                    try {
                        const res = await fetch(`${BRIDGE_URL}/librarian/summon`, {
                            method: "POST",
                            body: JSON.stringify({ sequence: addresses })
                        });
                        const data = await res.json();
                        const out = document.createElement('div');
                        out.style.color = "#8892B0";
                        out.innerText = `[SYSTEM] Execution Result: ${data.result}`;
                        terminalFeed.appendChild(out);
                    } catch(err) {
                        const errLine = document.createElement('div');
                        errLine.style.color = "red";
                        errLine.innerText = "[ERROR] Bridge Offline.";
                        terminalFeed.appendChild(errLine);
                    }
                } else if (cmd === "ls") {
                    const out = document.createElement('div');
                    out.style.color = "#8892B0";
                    out.innerText = "drwxr-xr-x  -  . \n-rw-r--r--  -  garuda_v6.bin\n-rw-r--r--  -  dna_store.vlt";
                    terminalFeed.appendChild(out);
                }
                
                terminalFeed.parentElement.scrollTop = terminalFeed.parentElement.scrollHeight;
            }
        });
    }

    initOmniBridge();
    initVaultBridge();

    console.log("[CUBIX TESSERACT] Multi-Layer Tesseract + Sovereign Bridge Initialized.");
}

