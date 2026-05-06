import { BiometricData, saveToVault, echo } from './vault';

export function logInvocation(segment: string, mode: string, biometric: BiometricData) {
  const echo: echo = {
    segment,
    mode,
    timestamp: Date.now(),
    emotionalState: biometric.state,
    lineage: "CodemapDNA → Jin → Graei"
  };
  saveToVault(echo);
}
