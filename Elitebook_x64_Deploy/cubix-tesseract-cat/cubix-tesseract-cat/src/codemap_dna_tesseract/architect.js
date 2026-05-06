// Copyright ©️ Randall Lujan, Emurica co GRAEI integrations
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Function to parse the README.md and extract core concepts
const parseReadme = (readmeContent) => {
    const traits = [];
    const cyclones = [];
    // A simple parsing logic to extract traits and cyclones from the README.
    // This can be made more robust with more complex parsing rules.
    const lines = readmeContent.split('\n');
    let currentSection = '';
    for (const line of lines) {
        if (line.startsWith('*   **')) {
            const match = line.match(/\*\s+\*\*(.*?):\*\*/);
            if (match) {
                currentSection = match[1].trim();
            }
        }
        if (currentSection) {
            if (currentSection === 'The DNA Spiral System') {
                // You can add more logic here to parse specific details about the DNA spiral system
            }
            else if (currentSection === 'Function Library & Trait-Locking') {
                traits.push({ name: 'Trait-Locking', description: 'Ensures predictable and secure execution.' });
            }
            else if (currentSection === 'Cyclone-Based Execution') {
                cyclones.push({ name: 'InitialCyclone', description: 'The first cyclone to be invoked.', entrypoint: 'root.ts' });
            }
        }
    }
    return { traits, cyclones };
};
// Main function for the architect
const runArchitect = () => {
    try {
        const readmePath = path.join(__dirname, 'README.md');
        const readmeContent = fs.readFileSync(readmePath, 'utf-8');
        const { traits, cyclones } = parseReadme(readmeContent);
        // Create the traits.json file
        const traitsJsonPath = path.join(__dirname, 'traits.json');
        fs.writeFileSync(traitsJsonPath, JSON.stringify({ traits }, null, 2));
        console.log('Successfully created traits.json');
        // Create the cyclone.json file
        const cycloneJsonPath = path.join(__dirname, 'cyclone.json');
        fs.writeFileSync(cycloneJsonPath, JSON.stringify({ cyclones }, null, 2));
        console.log('Successfully created cyclone.json');
    }
    catch (error) {
        console.error('Error running the architect:', error);
    }
};
runArchitect();
