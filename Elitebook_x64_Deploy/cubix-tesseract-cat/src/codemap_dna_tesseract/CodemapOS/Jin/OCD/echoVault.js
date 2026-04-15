import { saveToVault } from './vault';
export function logInvocation(segment, mode, biometric) {
    const echo = {
        segment,
        mode,
        timestamp: Date.now(),
        emotionalState: biometric.state,
        lineage: "CodemapDNA → Jin → Graei"
    };
    saveToVault(echo);
}
