import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const BLOCK_TYPES = {
    "grass": { "texture": "../common/textures/grass.png" },
    "dirt": { "texture": "../common/textures/dirt.png" },
    "stone": { "texture": "../common/textures/stone.png" },
    "wood": { "texture": "../common/textures/wood.png" }
};

let scene, camera, renderer, controls;
let raycaster, pointer;
const objects = [];
let currentBlockType = Object.keys(BLOCK_TYPES)[0];
const rollOverMesh = createRollOverMesh();
const plane = createPlane();
const textureLoader = new THREE.TextureLoader();
const textureCache = {};

// ★追加: ドラッグ操作で同じ場所に連続配置しないように、最後に置いた場所を記録
let lastPlacedPos = null;

function init() {
    preloadTextures();
    setupScene();
    createBlockSelector();

    // ★変更点: イベントリスナーを更新
    document.addEventListener('pointermove', onPointerMove);
    document.addEventListener('pointerdown', onPointerDown);
    document.addEventListener('pointerup', onPointerUp); // マウスボタンを離した時のイベントを追加
    window.addEventListener('resize', onWindowResize);
    document.getElementById('export-btn').addEventListener('click', exportScene);
    const importBtn = document.getElementById('import-btn');
    const fileImporter = document.getElementById('file-importer');
    importBtn.addEventListener('click', () => fileImporter.click());
    fileImporter.addEventListener('change', importScene);
    animate();
}

function setupScene() { /* ...変更なし... */ }

// ★変更点: ドラッグ操作のロジックを追加
function onPointerMove(event) {
    pointer.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1);
    raycaster.setFromCamera(pointer, camera);
    const intersects = raycaster.intersectObjects(objects, false);

    if (intersects.length > 0) {
        const intersect = intersects[0];
        const newPos = new THREE.Vector3().copy(intersect.point).add(intersect.face.normal);
        const voxelPos = new THREE.Vector3(Math.floor(newPos.x), Math.floor(newPos.y), Math.floor(newPos.z));
        
        rollOverMesh.position.copy(voxelPos).addScalar(0.5);
        rollOverMesh.visible = true;

        // event.buttons === 1 は左ボタンが押されている状態を示す
        if (event.buttons === 1) {
             if (!lastPlacedPos || !lastPlacedPos.equals(voxelPos)) {
                 addBlock(voxelPos, currentBlockType);
                 lastPlacedPos = voxelPos.clone();
             }
        }
    } else {
        rollOverMesh.visible = false;
    }
}

function onPointerDown(event) {
    // onPointerMoveで処理されるので、pointerdownでは最初の一個を置くだけ
    onPointerMove(event);
}

// ★追加: マウスボタンを離したら、最後の位置記録をリセット
function onPointerUp() {
    lastPlacedPos = null;
}


function onWindowResize() { /* ...変更なし... */ }
function addBlock(position, type) { /* ...変更なし... */ }
function removeBlock(object) { /* ...変更なし... */ }
function preloadTextures() { /* ...変更なし... */ }
function importScene(event) { /* ...変更なし... */ }
function clearScene() { /* ...変更なし... */ }
function exportScene() { /* ...変更なし... */ }
function createRollOverMesh() { /* ...変更なし... */ }
function createPlane() { /* ...変更なし... */ }
function createBlockSelector() { /* ...変更なし... */ }
function updateStatus(message, color) { /* ...変更なし... */ }
function animate() { /* ...変更なし... */ }

init();