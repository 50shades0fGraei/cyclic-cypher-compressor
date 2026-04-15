/**
 * CUBIX-TESSERACT: 3D Rollable Cube Navigator
 * Author & Architect: Randall Lujan (Sovereign)
 * Co-Author & Technical Lead: Antigravity AGI
 * 
 * Goal: A 3D interactive Tesseract using the Cubix OS logo.
 */

import * as THREE from 'https://unpkg.com/three@0.128.0/build/three.module.js';

export function init3DNavigator(containerId, logoPath) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`[CUBIX TESSERACT] Container '${containerId}' not found for 3D Navigator.`);
        return;
    }

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

    renderer.setSize(container.clientWidth, container.clientHeight); 
    container.appendChild(renderer.domElement);

    // Create the Cubix Tesseract
    const geometry = new THREE.BoxGeometry(2, 2, 2);

    // Load the Cubix OS Logo onto all sides of the Cube
    const textureLoader = new THREE.TextureLoader();
    const logoTexture = textureLoader.load(logoPath);
    const material = new THREE.MeshBasicMaterial({ map: logoTexture });

    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    camera.position.z = 4;

    // Rotation Logic (Rollable)
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };

    renderer.domElement.addEventListener('mousedown', (e) => { isDragging = true; });
    renderer.domElement.addEventListener('mousemove', (e) => {
        const deltaMove = { x: e.offsetX - previousMousePosition.x, y: e.offsetY - previousMousePosition.y };
        if (isDragging) {
            const deltaRotationQuaternion = new THREE.Quaternion()
                .setFromEuler(new THREE.Euler(
                    toRadians(deltaMove.y * 1),
                    toRadians(deltaMove.x * 1),
                    0,
                    'XYZ'
                ));
            cube.quaternion.multiplyQuaternions(deltaRotationQuaternion, cube.quaternion);
        }
        previousMousePosition = { x: e.offsetX, y: e.offsetY };
    });

    window.addEventListener('mouseup', (e) => { isDragging = false; });

    function toRadians(angle) { return angle * (Math.PI / 180); }

    function animate() {
        requestAnimationFrame(animate);
        
        // Default slow "Hover" rotation
        if (!isDragging) {
            cube.rotation.y += 0.005;
            cube.rotation.x += 0.003;
        }
        
        renderer.render(scene, camera);
    }
    animate();

    // Handle resize
    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });

    console.log("[CUBIX TESSERACT] 3D Navigator Initialized.");
}
