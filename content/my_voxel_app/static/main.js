import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let scene, camera, renderer, controls;
let raycaster, pointer;
const objects = [];
let blockTypes = {};
let currentBlockType = '';
const rollOverMesh = createRollOverMesh();
const plane = createPlane();
const textureLoader = new THREE.TextureLoader();
const textureCache = {};

async function init() {
    await fetchBlockTypes();
    preloadTextures();
    setupScene();
    createBlockSelector();
    document.addEventListener('pointermove', onPointerMove);
    document.addEventListener('pointerdown', onPointerDown);
    window.addEventListener('resize', onWindowResize);
    document.getElementById('export-btn').addEventListener('click', exportScene);
    document.getElementById('save-btn').addEventListener('click', saveSceneToServer);
    animate();
}

function setupScene() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87ceeb);
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(2, 5, 10);
    camera.lookAt(0, 0, 0);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('canvas-container').appendChild(renderer.domElement);
    const ambientLight = new THREE.AmbientLight(0x606060);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
    directionalLight.position.set(1, 0.75, 0.5).normalize();
    scene.add(directionalLight);
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    raycaster = new THREE.Raycaster();
    pointer = new THREE.Vector2();
    scene.add(rollOverMesh);
    scene.add(plane);
    objects.push(plane);
    const gridHelper = new THREE.GridHelper(50, 50);
    scene.add(gridHelper);
}

function onPointerMove(event) {
    pointer.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1);
    raycaster.setFromCamera(pointer, camera);
    const intersects = raycaster.intersectObjects(objects, false);
    if (intersects.length > 0) {
        const intersect = intersects[0];
        const newPos = new THREE.Vector3().copy(intersect.point).add(intersect.face.normal);
        rollOverMesh.position.set(Math.floor(newPos.x) + 0.5, Math.floor(newPos.y) + 0.5, Math.floor(newPos.z) + 0.5);
        rollOverMesh.visible = true;
    } else {
        rollOverMesh.visible = false;
    }
}

function onPointerDown(event) {
    pointer.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1);
    raycaster.setFromCamera(pointer, camera);
    const intersects = raycaster.intersectObjects(objects, false);
    if (intersects.length > 0) {
        const intersect = intersects[0];
        if (event.button === 0) {
            const newPos = new THREE.Vector3().copy(intersect.point).add(intersect.face.normal);
            addBlock({ x: Math.floor(newPos.x), y: Math.floor(newPos.y), z: Math.floor(newPos.z) }, currentBlockType);
        } else if (event.button === 2 && intersect.object !== plane) {
            removeBlock(intersect.object);
        }
    }
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function addBlock(position, type) {
    if (!blockTypes[type] || !textureCache[type]) return;
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshLambertMaterial({ map: textureCache[type] });
    const cube = new THREE.Mesh(geometry, material);
    cube.position.set(position.x + 0.5, position.y + 0.5, position.z + 0.5);
    cube.userData = { type, position };
    scene.add(cube);
    objects.push(cube);
}

function removeBlock(object) {
    scene.remove(object);
    objects.splice(objects.indexOf(object), 1);
    object.geometry.dispose();
    object.material.dispose();
}

async function fetchBlockTypes() {
    try {
        const response = await fetch('/api/block_types');
        blockTypes = await response.json();
        currentBlockType = Object.keys(blockTypes)[0];
    } catch (error) {
        console.error('ブロック定義の取得に失敗:', error);
    }
}

function preloadTextures() {
    for (const type in blockTypes) {
        const texture = textureLoader.load(blockTypes[type].texture);
        texture.magFilter = THREE.NearestFilter;
        textureCache[type] = texture;
    }
}

function exportScene() {
    const sceneData = { blocks: objects.filter(o => o.userData.type).map(o => o.userData) };
    const blob = new Blob([JSON.stringify(sceneData, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'scene.json';
    a.click();
    URL.revokeObjectURL(a.href);
    updateStatus('シーンがファイルにエクスポートされました。', 'green');
}

async function saveSceneToServer() {
    const sceneData = { blocks: objects.filter(o => o.userData.type).map(o => o.userData) };
    updateStatus('サーバーに保存中...', 'blue');
    try {
        const response = await fetch('/api/save_scene', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sceneData)
        });
        const result = await response.json();
        if (response.ok) {
            updateStatus(`サーバーに ${result.filename} として保存しました。`, 'green');
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        updateStatus(`保存エラー: ${error.message}`, 'red');
    }
}

function createRollOverMesh() {
    const geo = new THREE.BoxGeometry(1, 1, 1);
    const mat = new THREE.MeshBasicMaterial({ color: 0xff0000, opacity: 0.5, transparent: true });
    return new THREE.Mesh(geo, mat);
}

function createPlane() {
    const geo = new THREE.PlaneGeometry(50, 50);
    geo.rotateX(-Math.PI / 2);
    const mat = new THREE.MeshToonMaterial({ color: 0xcccccc });
    const plane = new THREE.Mesh(geo, mat);
    plane.receiveShadow = true;
    return plane;
}

function createBlockSelector() {
    const selector = document.getElementById('block-selector');
    selector.innerHTML = '';
    for (const type in blockTypes) {
        const item = document.createElement('div');
        item.innerHTML = `
            <input type="radio" name="blocktype" id="type-${type}" value="${type}">
            <label for="type-${type}">
                <img src="${blockTypes[type].texture}" class="block-preview"> ${type}
            </label>`;
        item.querySelector('input').addEventListener('change', e => currentBlockType = e.target.value);
        selector.appendChild(item);
    }
    selector.querySelector('input').checked = true;
}

function updateStatus(message, color) {
    const statusEl = document.getElementById('status-message');
    statusEl.textContent = message;
    statusEl.style.color = color;
    setTimeout(() => statusEl.textContent = '', 5000);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

init();