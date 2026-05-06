export function validateEmotion(segment, biometric) {
    // Check typing rhythm, pressure, mistake handling, proofreading
    return biometric.traits.includes("discernment") && biometric.rhythm === "reflective";
}
