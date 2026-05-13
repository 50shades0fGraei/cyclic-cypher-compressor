# EliteBook Sovereign Build: UI Interactivity Checklist

This checklist outlines the remaining tasks to make the **Cubix OS** UI fully interactive and integrated with the **Sovereign Bridge** (Python backend).

## 1. Core System & Navigation
- [x] **Boot-to-Login Flow**: (Initialized)
- [x] **Profile Selection**: (Basic implementation)
- [x] **Cube Assembly Animation**: (Wired)
- [x] **3D Navigator (Bottom Center)**:
    - [x] Rotate cube (Wired)
    - [x] **FIX**: Applied `pointer-events` optimization to prevent interaction dead-zones.
- [x] **Ruby Quick-Nav**: (Wired to rotation/zoom)

## 2. Inner Cube (Micro Environments)
### Dashboard (Front Face)
- [x] **Real-time Telemetry**: Wired to `/telemetry/energy`.
    - [x] Update **NPU Sync** (CPU load).
    - [x] Update **Energy Profile** (P-State status).
### Omni Chat / AGI (Left Face)
- [x] **Chat Connectivity**: Wired to `/omni/chat`.
- [x] **System Alerts**: (Wired polling)
### Vault / Librarian (Back Face)
- [x] **Librarian Chat**: (Wired to Gemini)
- [x] **Terminal Commands**: (Wired to `/system/exec`)
### Forge / Builder (Right Face)
- [x] **Ability Execution**: (Wired to `/omni/execute_mapped_dna`)
- [x] **Spiral Visualizer**: (Initialized)

## 3. Outer Cube (Macro Environments)
### Network Manager (Left Face)
- [x] **WiFi Scanning**: Wired to `/network/scan`.
- [x] **Connection Logic**: Wired to `/network/connect`.
- [x] **Advanced Settings**: Wired to `/system/launch`.
### Sovereign Browser (Front Face)
- [x] **URL Navigation**: Wired.
- [x] **Internal Hub**: Wired to `LUJAN_VAULT_MVP.html`.

## 4. Device & System Management
- [x] **Taskbar Integration**: 
    - [x] Wired **Battery**, **Network**, **Bluetooth**, **Task Manager** to `/system/launch`.
- [x] **Global Shell**: Wired to `/system/exec` (Bridge now supports arbitrary commands).

## 5. Security & Encryption
- [ ] **Ephemeral Cypher**:
    - [ ] Add dedicated UI panel in the "Dark Encryptor" face (WIP).
- [x] **GAPCI Sandbox**:
    - [x] Integration with `/gapci/assess` (Wired in bridge).

## 6. Hardware Optimization (EliteBook Specific)
- [x] **Left-Click Responsiveness**: Fixed via CSS `pointer-events` and `will-change` hints.
- [x] **Energy Savings Verification**: Dashboard now displays real-time savings from P-State locking.
