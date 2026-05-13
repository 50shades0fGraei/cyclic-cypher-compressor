import * as THREE from './lib/three.module.js';

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
        // Parametric equation for a 3D spiral (CubixOS DNA structure)
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
    
    // --- THREE.JS BOTTOM NAVIGATOR (Bottom-Center Slot) ---
    const navContainer = document.getElementById('nav-center-slot') || document.getElementById('bottom-navigator');
    const world = document.getElementById('world');
    const envCube = document.getElementById('environment-cube'); // Inner GRAEI
    const outerCube = document.getElementById('outer-cube'); // Outer External

    // CRITICAL: world must pass clicks through to face panels
    if (world) world.style.pointerEvents = 'none';

    // --- SYSTEM TIME UPDATER ---
    const timeNode = document.getElementById('sys-time');
    setInterval(() => {
        const now = new Date();
        timeNode.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }, 1000);
    timeNode.innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    // --- THREE.JS BOTTOM NAVIGATOR ---
    const scene = new THREE.Scene();
    const NAV_SIZE = navContainer ? (navContainer.clientWidth || 60) : 60;
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

    renderer.setSize(NAV_SIZE, NAV_SIZE);
    if (navContainer) navContainer.appendChild(renderer.domElement);

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
    gradient.addColorStop(0, 'rgba(112, 225, 0, 0.4)'); // Green GRAEI glow in center
    gradient.addColorStop(0.5, 'rgba(161, 193, 209, 0.1)'); // Blue mid
    gradient.addColorStop(1, '#0d1117');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 512, 512);
    // Text Logo
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 90px "Outfit", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('LUJAN', 256, 210);
    ctx.fillStyle = '#00f2ff';
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

    // --- INTERACTION LOGIC: Mouse + Touch (Swipe = rotate) ---
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let touchStartX = 0;
    let touchHeld = false;
    
    let targetRotationYInner = 0; 
    let targetRotationYOuter = 0; 
    
    let currentZLevel = -75; 
    const Z_LEVELS = {
        outer: -180,
        inner: -75
    };
    let targetRotationX = 0;

    // --- MOUSE DRAG ---
    if (navContainer) navContainer.addEventListener('mousedown', (e) => { 
        isDragging = true; 
        previousMousePosition = { x: e.clientX, y: e.clientY };
        navContainer.style.cursor = 'grabbing';
        e.stopPropagation();
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const deltaX = e.clientX - previousMousePosition.x;
        const deltaY = e.clientY - previousMousePosition.y;
        cube.rotation.y += deltaX * 0.01;
        cube.rotation.x += deltaY * 0.005; 
        previousMousePosition = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', (e) => {
        if (!isDragging) return;
        isDragging = false;
        if (navContainer) navContainer.style.cursor = 'grab';
        const snapAngle = Math.PI / 2;
        const lockedY = Math.round(cube.rotation.y / snapAngle) * snapAngle;
        targetRotationX = 0;
        if (currentZLevel === Z_LEVELS.inner) {
            targetRotationYInner = lockedY;
            cube.rotation.y = targetRotationYInner;
        } else {
            targetRotationYOuter = lockedY;
            cube.rotation.y = targetRotationYOuter;
        }
        applyMatrixState();
    });

    // --- TOUCH: hold & swipe left/right to rotate ---
    if (navContainer) {
        navContainer.addEventListener('touchstart', (e) => {
            touchHeld = true;
            touchStartX = e.touches[0].clientX;
            previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
            e.preventDefault();
        }, { passive: false });

        navContainer.addEventListener('touchmove', (e) => {
            if (!touchHeld) return;
            const deltaX = e.touches[0].clientX - previousMousePosition.x;
            const deltaY = e.touches[0].clientY - previousMousePosition.y;
            cube.rotation.y += deltaX * 0.015;
            cube.rotation.x += deltaY * 0.005;
            previousMousePosition = { x: e.touches[0].clientX, y: e.touches[0].clientY };
            e.preventDefault();
        }, { passive: false });

        navContainer.addEventListener('touchend', (e) => {
            if (!touchHeld) return;
            touchHeld = false;
            // Snap to nearest 90-degree face
            const snapAngle = Math.PI / 2;
            const lockedY = Math.round(cube.rotation.y / snapAngle) * snapAngle;
            targetRotationX = 0;
            if (currentZLevel === Z_LEVELS.inner) {
                targetRotationYInner = lockedY;
            } else {
                targetRotationYOuter = lockedY;
            }
            applyMatrixState();
            e.preventDefault();
        }, { passive: false });
    }

    // --- SCROLL WHEEL ZOOM (scene element, does NOT interfere with widgets) ---
    let zoomCooldown = false;
    document.querySelector('.scene')?.addEventListener('wheel', (e) => {
        // Only zoom if not over a widget (input, button, select, textarea, iframe)
        const tag = e.target.tagName.toLowerCase();
        if (['input','button','select','textarea','iframe','a'].includes(tag)) return;
        if (zoomCooldown) return;
        zoomCooldown = true;
        setTimeout(() => { zoomCooldown = false; }, 600);

        if (e.deltaY > 0) {
            // Scroll down = zoom OUT to outer layer
            currentZLevel = Z_LEVELS.outer;
        } else {
            // Scroll up = zoom INTO inner layer
            currentZLevel = Z_LEVELS.inner;
        }
        applyMatrixState();
        e.preventDefault();
    }, { passive: false });

    // --- CUBIX RUBYS (QUICK NAV) LOGIC ---
    function applyMatrixState() {
        world.style.transform = `translateZ(${currentZLevel}vw)`;
        envCube.style.transform = `rotateY(${-(targetRotationYInner * (180 / Math.PI))}deg)`;
        outerCube.style.transform = `rotateY(${-(targetRotationYOuter * (180 / Math.PI))}deg)`;
        
        // Ensure world has correct matrix class
        if (currentZLevel === Z_LEVELS.inner) {
            world.classList.add('matrix-inner-active');
            world.classList.remove('matrix-outer-active');
        } else {
            world.classList.add('matrix-outer-active');
            world.classList.remove('matrix-inner-active');
        }

        // Sync navigator cube to current active layer
        const targetNavY = (currentZLevel === Z_LEVELS.inner) ? targetRotationYInner : targetRotationYOuter;
        cube.rotation.y = targetNavY;

        // Reset X (pitch) to level
        targetRotationX = 0;
        cube.rotation.x = 0;
    }
    
    // Set initial state
    applyMatrixState();

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
        const rubyX = document.getElementById('ruby-x');
        
        // Toggle the layer
        currentZLevel = (currentZLevel === Z_LEVELS.inner) ? Z_LEVELS.outer : Z_LEVELS.inner;
        
        // Update Ruby X active state
        if (currentZLevel === Z_LEVELS.outer) {
            rubyX.classList.add('active');
            world.classList.add('matrix-outer-active');
            world.classList.remove('matrix-inner-active');
            console.log("[MATRIX] Switching to MACRO (Outer) Environment");
        } else {
            rubyX.classList.remove('active');
            world.classList.add('matrix-inner-active');
            world.classList.remove('matrix-outer-active');
            console.log("[MATRIX] Switching to MICRO (Inner) Environment");
        }
        
        applyMatrixState();
    });

    // --- TASKBAR ICON NAVIGATION ---
    const appIcons = document.querySelectorAll('.app-icon');
    appIcons.forEach((icon, index) => {
        icon.addEventListener('click', () => {
            // Remove active class from all
            appIcons.forEach(i => i.classList.remove('active'));
            icon.classList.add('active');

            // Map index to rotation (Front, Right, Back, Left)
            if (currentZLevel === Z_LEVELS.inner) {
                targetRotationYInner = (index * Math.PI / 2);
            } else {
                targetRotationYOuter = (index * Math.PI / 2);
            }
            console.log(`[CUBIX NAV] Icon clicked: ${index}, Target Rotation: ${currentZLevel === Z_LEVELS.inner ? targetRotationYInner : targetRotationYOuter}`);
            applyMatrixState();
        });
    });

    function animate() {
        requestAnimationFrame(animate);
        
        // Smoothly snap the mini cube to its designated layer rotation
        if (!isDragging && !touchHeld) {
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

        // Omni Chat Send Logic
        const omniInput = document.getElementById('omni-input');
        const omniSend = document.getElementById('omni-send');
        const handleOmniSubmit = async () => {
            const text = omniInput.value.trim();
            if(!text) return;
            
            // Add user message
            const div = document.createElement('div');
            div.className = "chat-msg msg-user";
            div.innerText = text;
            chatFeed.appendChild(div);
            omniInput.value = "";
            chatFeed.scrollTop = chatFeed.scrollHeight;

            try {
                const res = await fetch(`${BRIDGE_URL}/omni/chat`, {
                    method: "POST",
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await res.json();
                const aiDiv = document.createElement('div');
                aiDiv.className = "chat-msg msg-ai";
                aiDiv.innerText = data.reply || data.error;
                chatFeed.appendChild(aiDiv);
                chatFeed.scrollTop = chatFeed.scrollHeight;
            } catch (e) {
                const aiDiv = document.createElement('div');
                aiDiv.className = "chat-msg msg-ai";
                aiDiv.style.color = "#FF4B2B";
                aiDiv.innerText = "[ERROR] Bridge Offline.";
                chatFeed.appendChild(aiDiv);
            }
        };
        omniSend?.addEventListener('click', handleOmniSubmit);
        omniInput?.addEventListener('keydown', (e) => { if(e.key === 'Enter') handleOmniSubmit(); });
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
        
        // Librarian Chat — powered by Gemini 1.5 Pro via Sovereign Bridge
        const librarianInput = document.getElementById('librarian-input');
        const librarianSend = document.getElementById('librarian-send');
        const librarianFeed = document.querySelector('.librarian-chat > div:nth-child(2)');
        const handleLibrarianSubmit = async () => {
            const text = librarianInput.value.trim();
            if (!text) return;
            // User message
            const userDiv = document.createElement('div');
            userDiv.style.cssText = "margin-bottom:10px;color:#A1C1D1;";
            userDiv.innerHTML = `<b>You:</b> ${text}`;
            librarianFeed.appendChild(userDiv);
            librarianInput.value = "";
            librarianFeed.scrollTop = librarianFeed.scrollHeight;
            // Thinking indicator
            const thinkDiv = document.createElement('div');
            thinkDiv.style.cssText = "margin-bottom:10px;color:#8892B0;font-style:italic;";
            thinkDiv.innerText = "📚 Librarian is searching the vault...";
            librarianFeed.appendChild(thinkDiv);
            try {
                const res = await fetch(`${BRIDGE_URL}/librarian/gemini`, {
                    method: "POST",
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await res.json();
                thinkDiv.remove();
                const aiDiv = document.createElement('div');
                aiDiv.style.cssText = "margin-bottom:10px;color:#E2E2E2;";
                aiDiv.innerHTML = `<b style="color:#00f2ff;">📚 Librarian (Gemini):</b> ${data.reply || data.error}`;
                librarianFeed.appendChild(aiDiv);
            } catch (e) {
                thinkDiv.innerText = "[ERROR] Bridge offline — start sovereign_bridge.py";
                thinkDiv.style.color = "#FF4B2B";
            }
            librarianFeed.scrollTop = librarianFeed.scrollHeight;
        };
        librarianSend?.addEventListener('click', handleLibrarianSubmit);
        librarianInput?.addEventListener('keydown', (e) => { if(e.key === 'Enter') handleLibrarianSubmit(); });

        // Builder/Forge Thread logic
        const builderInput = document.getElementById('builder-input');
        const builderSend = document.getElementById('builder-send');
        const builderFeed = document.querySelector('.chat-thread-container > div:nth-child(2)');
        const handleBuilderSubmit = () => {
            if(!builderInput.value.trim()) return;
            const div = document.createElement('div');
            div.style.marginBottom = "10px";
            div.style.color = "#70E100";
            div.innerHTML = `<b>Randall (Architect):</b> ${builderInput.value}`;
            builderFeed.appendChild(div);
            builderInput.value = "";
            builderFeed.scrollTop = builderFeed.scrollHeight;
        };
        builderSend?.addEventListener('click', handleBuilderSubmit);
        builderInput?.addEventListener('keydown', (e) => { if(e.key === 'Enter') handleBuilderSubmit(); });
    }

    initOmniBridge();
    initVaultBridge();

    // --- INNER APP VIEW SWITCHING ---
    window.switchInnerView = function(viewId, element) {
        // Remove active class from all nav items
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
        // Add active class to clicked item
        element.classList.add('active');

        // Hide all views
        document.querySelectorAll('.inner-view').forEach(view => view.classList.remove('active'));
        // Show target view
        const targetView = document.getElementById(`view-${viewId}`);
        if (targetView) targetView.classList.add('active');

        console.log(`[SOVEREIGN] Switched to view: ${viewId}`);
    };

    // --- SIDEBAR TOGGLE LOGIC ---
    window.toggleSidebar = function() {
        const sidebar = document.getElementById('inner-sidebar');
        if (sidebar) {
            sidebar.classList.toggle('collapsed');
            console.log(`[SOVEREIGN] Sidebar ${sidebar.classList.contains('collapsed') ? 'collapsed' : 'expanded'}`);
        }
    };

    // --- OPACITY CYCLING LOGIC ---
    let currentOpacityLevel = 0;
    const opacityClasses = ['bg-opaque', 'bg-soft', 'bg-glass', 'bg-clear'];
    
    window.cycleOpacity = function() {
        const container = document.querySelector('.inner-app-container');
        if (!container) return;

        // Remove old class
        container.classList.remove(opacityClasses[currentOpacityLevel]);
        
        // Cycle level
        currentOpacityLevel = (currentOpacityLevel + 1) % opacityClasses.length;
        
        // Add new class
        container.classList.add(opacityClasses[currentOpacityLevel]);
        
        // Update Ruby O active state
        const rubyO = document.getElementById('ruby-o');
        if (rubyO) {
            if (currentOpacityLevel > 0) rubyO.classList.add('active');
            else rubyO.classList.remove('active');
        }

        console.log(`[SOVEREIGN] Visibility Mode: ${opacityClasses[currentOpacityLevel]}`);
    };

    // --- SIDEBAR OPACITY CONTROL ---
    window.setOpacity = function(level) {
        const container = document.querySelector('.inner-app-container');
        if (!container) return;

        // Update levels
        container.classList.remove(...opacityClasses);
        container.classList.add(opacityClasses[level]);
        currentOpacityLevel = level;

        // Update UI pills
        document.querySelectorAll('.pill').forEach((pill, idx) => {
            if (idx === level) pill.classList.add('active');
            else pill.classList.remove('active');
        });

        // Update Ruby O state
        const rubyO = document.getElementById('ruby-o');
        if (rubyO) {
            if (level > 0) rubyO.classList.add('active');
            else rubyO.classList.remove('active');
        }

        console.log(`[SOVEREIGN] Visibility Mode set to: ${opacityClasses[level]}`);
    };

    // --- SIDEBAR AI CHAT LOGIC ---
    window.sendSidebarChat = function() {
        const input = document.getElementById('sidebar-ai-input');
        const feed = document.getElementById('sidebar-chat-feed');
        if (!input || !feed || !input.value.trim()) return;

        const userMsg = input.value.trim();
        
        // Add User Message
        const userDiv = document.createElement('div');
        userDiv.className = 'mini-msg msg-user';
        userDiv.textContent = userMsg;
        feed.appendChild(userDiv);
        
        // Clear input
        input.value = '';
        feed.scrollTop = feed.scrollHeight;

        // Simulated AI Response (In production, this would hit the Bridge)
        setTimeout(() => {
            const aiDiv = document.createElement('div');
            aiDiv.className = 'mini-msg msg-ai';
            aiDiv.textContent = "Processing sovereign request... Command acknowledged.";
            feed.appendChild(aiDiv);
            feed.scrollTop = feed.scrollHeight;
        }, 1000);
    };

    // Add Enter listener for chat
    document.getElementById('sidebar-ai-input')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendSidebarChat();
    });

    // --- IN-PAGE APP DOCKING ---
    window.dockApp = function(appName, icon) {
        const portal = document.getElementById('library-portal');
        if (!portal) return;

        portal.innerHTML = `
            <div style="width:100%; height:100%; display:flex; flex-direction:column;">
                <div style="background:rgba(255,255,255,0.05); padding:10px 20px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1);">
                    <div style="font-weight:800; font-size:0.8rem; color:#00f2ff;">${icon} ${appName.toUpperCase()}</div>
                    <button onclick="closeDock()" style="background:none; border:none; color:#8892B0; cursor:pointer; font-weight:900;">✕</button>
                </div>
                <div style="flex:1; padding:20px; color:#E2E2E2; overflow-y:auto;">
                    <h3>Sovereign Application Portal</h3>
                    <p>Executing ${appName} in protected memory space...</p>
                    <div style="margin-top:20px; padding:15px; background:rgba(0,0,0,0.3); border-radius:10px; border-left:4px solid #70E100;">
                        <div style="font-family:monospace; font-size:0.85rem; color:#70E100;">
                            > Initializing bridge connection...<br>
                            > Validating CyberDNA handshake...<br>
                            > Application ${appName} is now ACTIVE.
                        </div>
                    </div>
                </div>
            </div>
        `;
        console.log(`[SOVEREIGN] Docked app: ${appName}`);
    };

    window.closeDock = function() {
        const portal = document.getElementById('library-portal');
        if (portal) {
            portal.innerHTML = '<div class="portal-placeholder">SELECT A FUNCTION TO DOCK INTO THIS VIEW</div>';
        }
    };

    console.log("[CUBIX TESSERACT] Multi-Layer Tesseract + Sovereign Bridge Initialized.");
}

