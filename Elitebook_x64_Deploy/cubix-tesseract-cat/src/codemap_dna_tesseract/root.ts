// Copyright ©️ Randall Lujan, Emurica co GRAEI integrations

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Define interfaces for the configuration files
interface Trait {
  name: string;
  description: string;
}

interface Cyclone {
  name: string;
  description: string;
  entrypoint: string;
}

// Function to read the configuration files
const readConfig = (): { traits: Trait[], cyclones: Cyclone[] } => {
  try {
    const traitsJsonPath = path.join(__dirname, 'traits.json');
    const traitsData = fs.readFileSync(traitsJsonPath, 'utf-8');
    const { traits } = JSON.parse(traitsData);

    const cycloneJsonPath = path.join(__dirname, 'cyclone.json');
    const cycloneData = fs.readFileSync(cycloneJsonPath, 'utf-8');
    const { cyclones } = JSON.parse(cycloneData);

    return { traits, cyclones };
  } catch (error) {
    console.error('Error reading configuration files:', error);
    return { traits: [], cyclones: [] };
  }
};

// Main function for the root process
const runRoot = () => {
  console.log('Initializing Codemap DNA Tesseract OS...');

  const { traits, cyclones } = readConfig();

  if (traits.length === 0 || cyclones.length === 0) {
    console.error('Configuration files are missing or empty. Please run the architect first.');
    return;
  }

  console.log('Traits loaded:', traits.map(t => t.name));
  console.log('Cyclones loaded:', cyclones.map(c => c.name));

  const initialCyclone = cyclones.find(c => c.name === 'InitialCyclone');

  if (initialCyclone) {
    console.log(`Summoning the initial cyclone: ${initialCyclone.name}`);
    console.log(`Description: ${initialCyclone.description}`);
    console.log(`Entrypoint: ${initialCyclone.entrypoint}`);
    // Here you would add the logic to actually execute the entrypoint
    console.log('The DNA spiral begins to weave...');
  } else {
    console.error('Initial cyclone not found. The OS cannot start.');
  }

  console.log('Codemap DNA Tesseract OS initialized.');
};

runRoot();
