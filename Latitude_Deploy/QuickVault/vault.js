// (c) 2026 Randall James Lujan. ALL RIGHTS RESERVED.
// PATENT PENDING: Cyclic Cypher Deductive Metronome Architecture.
// This software is proprietary and subject to the terms of a specific License Agreement.

/**
 * Quick Vault — Sovereign Storage System
 * vault.js — Core Application Logic
 *
 * Features:
 *  - Drag & drop / browse file ingestion
 *  - Client-side compression simulation (LZ-string based)
 *  - LocalStorage persistence across sessions
 *  - Category tabs, search, file details modal
 *  - Export (download) and delete from vault
 *  - Real-time storage stats
 */

'use strict';

// =====================================================
//  LZ-String compression (embedded, no CDN needed)
//  © 2013 pieroxy.net — MIT License
// =====================================================
const LZString = (() => {
  const keyStrBase64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
  const baseReverseDic = {};
  for (let i = 0; i < keyStrBase64.length; i++) baseReverseDic[keyStrBase64[i]] = i;

  function _compress(uncompressed, bitsPerChar, getCharFromInt) {
    if (!uncompressed) return '';
    let i, value, contextDictionary = {}, contextDictionaryToCreate = {},
      contextC = '', contextWC = '', contextW = '',
      contextEnlargeIn = 2, contextDictSize = 3, contextNumBits = 2,
      contextData = [], contextDataVal = 0, contextDataPosition = 0, ii;

    for (ii = 0; ii < uncompressed.length; ii++) {
      contextC = uncompressed[ii];
      if (!Object.prototype.hasOwnProperty.call(contextDictionary, contextC)) {
        contextDictionary[contextC] = contextDictSize++;
        contextDictionaryToCreate[contextC] = true;
      }
      contextWC = contextW + contextC;
      if (Object.prototype.hasOwnProperty.call(contextDictionary, contextWC)) {
        contextW = contextWC;
      } else {
        if (Object.prototype.hasOwnProperty.call(contextDictionaryToCreate, contextW)) {
          if (contextW.charCodeAt(0) < 256) {
            for (i = 0; i < contextNumBits; i++) {
              contextDataVal = (contextDataVal << 1);
              if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
              else { contextDataPosition++; }
            }
            value = contextW.charCodeAt(0);
            for (i = 0; i < 8; i++) {
              contextDataVal = (contextDataVal << 1) | (value & 1);
              if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
              else { contextDataPosition++; }
              value = value >> 1;
            }
          } else {
            value = 1;
            for (i = 0; i < contextNumBits; i++) {
              contextDataVal = (contextDataVal << 1) | value;
              if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
              else { contextDataPosition++; }
              value = 0;
            }
            value = contextW.charCodeAt(0);
            for (i = 0; i < 16; i++) {
              contextDataVal = (contextDataVal << 1) | (value & 1);
              if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
              else { contextDataPosition++; }
              value = value >> 1;
            }
          }
          contextEnlargeIn--;
          if (contextEnlargeIn == 0) { contextEnlargeIn = Math.pow(2, contextNumBits); contextNumBits++; }
          delete contextDictionaryToCreate[contextW];
        } else {
          value = contextDictionary[contextW];
          for (i = 0; i < contextNumBits; i++) {
            contextDataVal = (contextDataVal << 1) | (value & 1);
            if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
            else { contextDataPosition++; }
            value = value >> 1;
          }
        }
        contextEnlargeIn--;
        if (contextEnlargeIn == 0) { contextEnlargeIn = Math.pow(2, contextNumBits); contextNumBits++; }
        contextDictionary[contextWC] = contextDictSize++;
        contextW = String(contextC);
      }
    }
    if (contextW !== '') {
      if (Object.prototype.hasOwnProperty.call(contextDictionaryToCreate, contextW)) {
        if (contextW.charCodeAt(0) < 256) {
          for (i = 0; i < contextNumBits; i++) {
            contextDataVal = (contextDataVal << 1);
            if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
            else { contextDataPosition++; }
          }
          value = contextW.charCodeAt(0);
          for (i = 0; i < 8; i++) {
            contextDataVal = (contextDataVal << 1) | (value & 1);
            if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
            else { contextDataPosition++; }
            value = value >> 1;
          }
        } else {
          value = 1;
          for (i = 0; i < contextNumBits; i++) {
            contextDataVal = (contextDataVal << 1) | value;
            if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
            else { contextDataPosition++; }
            value = 0;
          }
          value = contextW.charCodeAt(0);
          for (i = 0; i < 16; i++) {
            contextDataVal = (contextDataVal << 1) | (value & 1);
            if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
            else { contextDataPosition++; }
            value = value >> 1;
          }
        }
        contextEnlargeIn--;
        if (contextEnlargeIn == 0) { contextEnlargeIn = Math.pow(2, contextNumBits); contextNumBits++; }
        delete contextDictionaryToCreate[contextW];
      } else {
        value = contextDictionary[contextW];
        for (i = 0; i < contextNumBits; i++) {
          contextDataVal = (contextDataVal << 1) | (value & 1);
          if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
          else { contextDataPosition++; }
          value = value >> 1;
        }
      }
      contextEnlargeIn--;
      if (contextEnlargeIn == 0) { contextEnlargeIn = Math.pow(2, contextNumBits); contextNumBits++; }
    }
    value = 2;
    for (i = 0; i < contextNumBits; i++) {
      contextDataVal = (contextDataVal << 1) | (value & 1);
      if (contextDataPosition == bitsPerChar - 1) { contextDataPosition = 0; contextData.push(getCharFromInt(contextDataVal)); contextDataVal = 0; }
      else { contextDataPosition++; }
      value = value >> 1;
    }
    while (true) {
      contextDataVal = (contextDataVal << 1);
      if (contextDataPosition == bitsPerChar - 1) { contextData.push(getCharFromInt(contextDataVal)); break; }
      else { contextDataPosition++; }
    }
    return contextData.join('');
  }

  function _decompress(length, resetValue, getNextValue) {
    const dictionary = [];
    let next, enlargeIn = 4, dictSize = 4, numBits = 3, entry = '',
      result = [], i, w, bits, resb, maxpower, power, c,
      data = { val: getNextValue(0), position: resetValue, index: 1 };

    for (i = 0; i < 3; i++) dictionary[i] = i;

    bits = 0; maxpower = Math.pow(2, 2); power = 1;
    while (power != maxpower) {
      resb = data.val & data.position;
      data.position >>= 1;
      if (data.position == 0) { data.position = resetValue; data.val = getNextValue(data.index++); }
      bits |= (resb > 0 ? 1 : 0) * power;
      power <<= 1;
    }

    switch (next = bits) {
      case 0:
        bits = 0; maxpower = Math.pow(2, 8); power = 1;
        while (power != maxpower) {
          resb = data.val & data.position;
          data.position >>= 1;
          if (data.position == 0) { data.position = resetValue; data.val = getNextValue(data.index++); }
          bits |= (resb > 0 ? 1 : 0) * power;
          power <<= 1;
        }
        c = String.fromCharCode(bits); break;
      case 1:
        bits = 0; maxpower = Math.pow(2, 16); power = 1;
        while (power != maxpower) {
          resb = data.val & data.position;
          data.position >>= 1;
          if (data.position == 0) { data.position = resetValue; data.val = getNextValue(data.index++); }
          bits |= (resb > 0 ? 1 : 0) * power;
          power <<= 1;
        }
        c = String.fromCharCode(bits); break;
      case 2: return '';
    }

    dictionary[3] = c; w = c; result.push(c);
    while (true) {
      if (data.index > length) return '';
      bits = 0; maxpower = Math.pow(2, numBits); power = 1;
      while (power != maxpower) {
        resb = data.val & data.position;
        data.position >>= 1;
        if (data.position == 0) { data.position = resetValue; data.val = getNextValue(data.index++); }
        bits |= (resb > 0 ? 1 : 0) * power;
        power <<= 1;
      }
      switch (c = bits) {
        case 0:
          bits = 0; maxpower = Math.pow(2, 8); power = 1;
          while (power != maxpower) {
            resb = data.val & data.position;
            data.position >>= 1;
            if (data.position == 0) { data.position = resetValue; data.val = getNextValue(data.index++); }
            bits |= (resb > 0 ? 1 : 0) * power;
            power <<= 1;
          }
          dictionary[dictSize++] = String.fromCharCode(bits);
          c = dictSize - 1; enlargeIn--;
          break;
        case 1:
          bits = 0; maxpower = Math.pow(2, 16); power = 1;
          while (power != maxpower) {
            resb = data.val & data.position;
            data.position >>= 1;
            if (data.position == 0) { data.position = resetValue; data.val = getNextValue(data.index++); }
            bits |= (resb > 0 ? 1 : 0) * power;
            power <<= 1;
          }
          dictionary[dictSize++] = String.fromCharCode(bits);
          c = dictSize - 1; enlargeIn--;
          break;
        case 2: return result.join('');
      }
      if (enlargeIn == 0) { enlargeIn = Math.pow(2, numBits); numBits++; }
      if (dictionary[c]) { entry = dictionary[c]; } else { if (c === dictSize) { entry = w + w[0]; } else { return null; } }
      result.push(entry);
      dictionary[dictSize++] = w + entry[0];
      enlargeIn--;
      if (enlargeIn == 0) { enlargeIn = Math.pow(2, numBits); numBits++; }
      w = entry;
    }
  }

  return {
    compressToBase64(input) {
      if (!input) return '';
      const res = _compress(input, 6, a => keyStrBase64[a]);
      switch (res.length % 4) {
        default: case 0: return res;
        case 1: return res + '===';
        case 2: return res + '==';
        case 3: return res + '=';
      }
    },
    decompressFromBase64(input) {
      if (!input) return '';
      input = input.replace(/ /g, '+');
      return _decompress(input.length, 32, idx => baseReverseDic[input[idx]]);
    }
  };
})();


// =====================================================
//  APP STATE
// =====================================================
const STORAGE_KEY = 'quickvault_v2';

let state = {
  vault: [],       // { id, name, ext, tag, origSize, compSize, ratio, data, addedAt }
  queue: [],       // { file, name, size } — staged, not yet vaulted
  activeCategory: 'all',
  searchQuery: '',
  selectedId: null
};

// =====================================================
//  UTILITY FUNCTIONS
// =====================================================
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024, sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function formatDate(ts) {
  return new Date(ts).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

function getFileIcon(ext) {
  const map = {
    // Docs
    pdf: '📄', doc: '📝', docx: '📝', txt: '📃', md: '📃', rtf: '📃',
    // Spreadsheets
    xls: '📊', xlsx: '📊', csv: '📊',
    // Images
    png: '🖼', jpg: '🖼', jpeg: '🖼', gif: '🎞', webp: '🖼', svg: '🎨', bmp: '🖼',
    // Video
    mp4: '🎬', mov: '🎬', avi: '🎬', mkv: '🎬', webm: '🎬',
    // Audio
    mp3: '🎵', wav: '🎵', flac: '🎵', aac: '🎵', ogg: '🎵',
    // Code
    js: '💻', ts: '💻', py: '🐍', html: '🌐', css: '🎨', json: '📋',
    java: '☕', cpp: '💻', c: '💻', cs: '💻', go: '💻', rs: '💻',
    // Archives
    zip: '📦', tar: '📦', gz: '📦', rar: '📦', '7z': '📦',
    // Config
    env: '⚙', ini: '⚙', yaml: '⚙', yml: '⚙', toml: '⚙', xml: '⚙',
  };
  return map[ext?.toLowerCase()] || '📁';
}

function getFileColor(ext) {
  const map = {
    pdf: '#ff6b6b', doc: '#4e9af1', docx: '#4e9af1', txt: '#8892b0',
    xls: '#2bbc6e', xlsx: '#2bbc6e', csv: '#2bbc6e',
    png: '#f5c518', jpg: '#f5c518', jpeg: '#f5c518', gif: '#f5c518',
    mp4: '#a855f7', mp3: '#ec4899',
    js: '#f0db4f', ts: '#3178c6', py: '#306998', html: '#e44d26',
    css: '#264de4', json: '#5db85b', zip: '#ff9f43', rar: '#ff9f43',
  };
  return map[ext?.toLowerCase()] || '#7b61ff';
}

// =====================================================
//  PERSISTENCE
// =====================================================
function saveVault() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.vault));
  } catch (e) {
    showToast('⚠️ Storage limit reached — vault may be full', 'error');
  }
}

function loadVault() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) state.vault = JSON.parse(raw);
  } catch (e) {
    state.vault = [];
  }
}

// =====================================================
//  TOAST
// =====================================================
function showToast(msg, type = 'success', duration = 3500) {
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span class="toast-icon">${icons[type]}</span><span class="toast-msg">${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.transition = 'all 0.4s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(40px)';
    setTimeout(() => toast.remove(), 400);
  }, duration);
}

// =====================================================
//  COMPRESSION ENGINE
// =====================================================
function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = e => resolve(e.target.result); // data URL
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

async function compressAndVault(file, tag, level) {
  const dataUrl = await readFileAsBase64(file);

  // Simulate compression: LZ compress the base64 string
  // Higher level = more aggressive compression (via repeated passes simulation)
  let compressed = LZString.compressToBase64(dataUrl);

  // For text-heavy files, we do more passes
  let passes = Math.max(1, Math.floor(level / 3));
  for (let p = 1; p < passes; p++) {
    const again = LZString.compressToBase64(compressed);
    if (again.length < compressed.length) compressed = again;
  }

  const origSize  = file.size;
  const compSize  = Math.ceil(compressed.length * 0.75); // base64 → bytes approx
  const ratio     = origSize > 0 ? Math.round((1 - compSize / origSize) * 100) : 0;
  const ext       = file.name.split('.').pop();

  return {
    id:       uid(),
    name:     file.name,
    ext:      ext,
    tag:      tag || 'General',
    origSize: origSize,
    compSize: Math.max(compSize, 1),
    ratio:    Math.max(0, ratio),
    data:     compressed,
    addedAt:  Date.now()
  };
}

function decompressEntry(entry) {
  return LZString.decompressFromBase64(entry.data);
}

// =====================================================
//  QUEUE MANAGEMENT
// =====================================================
function addFilesToQueue(files) {
  const maxSize = 50 * 1024 * 1024; // 50MB per file
  let added = 0;
  for (const file of files) {
    if (file.size > maxSize) {
      showToast(`${file.name} exceeds 50MB limit`, 'error');
      continue;
    }
    if (state.queue.some(q => q.name === file.name && q.size === file.size)) continue;
    state.queue.push({ file, name: file.name, size: file.size });
    added++;
  }
  if (added) showToast(`${added} file${added > 1 ? 's' : ''} queued for vaulting`, 'info');
  renderQueue();
  document.getElementById('btn-vault').disabled = state.queue.length === 0;
}

function removeFromQueue(idx) {
  state.queue.splice(idx, 1);
  renderQueue();
  document.getElementById('btn-vault').disabled = state.queue.length === 0;
}

function renderQueue() {
  // Remove old queue section if exists
  const existing = document.getElementById('queue-section');
  if (existing) existing.remove();

  if (state.queue.length === 0) return;

  const section = document.createElement('div');
  section.className = 'queue-section';
  section.id = 'queue-section';
  section.innerHTML = `
    <div class="queue-header">
      <span class="queue-title">Queued <span class="queue-badge">${state.queue.length}</span></span>
      <button class="queue-clear" id="queue-clear-btn">Clear All</button>
    </div>
    <div id="queue-items"></div>
  `;

  const leftPanel = document.querySelector('.left-panel');
  const vaultBtn  = document.getElementById('btn-vault');
  leftPanel.insertBefore(section, vaultBtn);

  document.getElementById('queue-clear-btn').addEventListener('click', () => {
    state.queue = [];
    renderQueue();
    document.getElementById('btn-vault').disabled = true;
  });

  const queueItems = document.getElementById('queue-items');
  state.queue.forEach((item, idx) => {
    const el = document.createElement('div');
    el.className = 'queue-item';
    el.innerHTML = `
      <span>${getFileIcon(item.name.split('.').pop())}</span>
      <span class="queue-item-name">${item.name}</span>
      <span class="queue-item-size">${formatBytes(item.size)}</span>
      <button class="queue-item-remove" data-idx="${idx}">✕</button>
    `;
    el.querySelector('.queue-item-remove').addEventListener('click', e => {
      e.stopPropagation();
      removeFromQueue(idx);
    });
    queueItems.appendChild(el);
  });
}

// =====================================================
//  VAULT OPERATIONS
// =====================================================
async function vaultAllQueued() {
  if (state.queue.length === 0) return;

  const btn   = document.getElementById('btn-vault');
  const level = parseInt(document.getElementById('compress-level').value);
  const tag   = document.getElementById('vault-tag').value.trim() || 'General';

  btn.textContent = '⏳ Vaulting...';
  btn.disabled = true;

  let successCount = 0;

  for (const item of state.queue) {
    try {
      const entry = await compressAndVault(item.file, tag, level);
      state.vault.unshift(entry); // newest first
      successCount++;
    } catch (e) {
      showToast(`Failed to vault: ${item.name}`, 'error');
    }
  }

  state.queue = [];
  renderQueue();
  saveVault();
  renderVault();
  updateStats();

  btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><polygon points="9,1 17,5 17,13 9,17 1,13 1,5" stroke="currentColor" stroke-width="1.5"/><circle cx="9" cy="9" r="3" fill="currentColor"/></svg> Vault Selected Files`;
  btn.disabled = true;

  if (successCount > 0) showToast(`${successCount} file${successCount > 1 ? 's' : ''} vaulted successfully! 🔐`);
}

function deleteEntry(id) {
  state.vault = state.vault.filter(e => e.id !== id);
  saveVault();
  renderVault();
  updateStats();
  showToast('File removed from vault', 'info');
  closeModal();
}

function extractEntry(entry) {
  try {
    const dataUrl = decompressEntry(entry);
    if (!dataUrl) { showToast('Could not decompress — data may be corrupted', 'error'); return; }
    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = entry.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    showToast(`Extracting ${entry.name}...`, 'info');
  } catch (e) {
    showToast('Extraction failed', 'error');
  }
}

// =====================================================
//  RENDER VAULT
// =====================================================
function getFilteredVault() {
  let items = [...state.vault];
  if (state.activeCategory !== 'all') {
    items = items.filter(e => e.tag.toLowerCase() === state.activeCategory.toLowerCase());
  }
  if (state.searchQuery) {
    const q = state.searchQuery.toLowerCase();
    items = items.filter(e => e.name.toLowerCase().includes(q) || e.tag.toLowerCase().includes(q));
  }
  return items;
}

function renderVault() {
  renderTabs();
  const filtered = getFilteredVault();
  const list = document.getElementById('vault-list');
  const empty = document.getElementById('empty-state');

  // Clear existing cards (but keep empty state)
  [...list.querySelectorAll('.file-card')].forEach(c => c.remove());

  if (filtered.length === 0) {
    empty.style.display = '';
    return;
  }
  empty.style.display = 'none';

  filtered.forEach(entry => {
    const card = createFileCard(entry);
    list.appendChild(card);
  });
}

function createFileCard(entry) {
  const card = document.createElement('div');
  card.className = 'file-card';
  card.dataset.id = entry.id;

  const color = getFileColor(entry.ext);
  const icon  = getFileIcon(entry.ext);
  const saved = entry.origSize - entry.compSize;

  card.innerHTML = `
    <div class="file-type-badge" style="background:${color}22; color:${color}">${icon}</div>
    <div class="file-info">
      <div class="file-name">${entry.name}</div>
      <div class="file-meta">
        <span>${formatBytes(entry.origSize)}</span>
        <span>→</span>
        <span>${formatBytes(entry.compSize)}</span>
        <span class="tag">${entry.tag}</span>
        <span>${formatDate(entry.addedAt)}</span>
      </div>
      <div class="compress-bar">
        <div class="compress-fill" style="width:${Math.min(entry.ratio, 100)}%"></div>
      </div>
    </div>
    <div class="file-savings">
      <span class="savings-val">-${entry.ratio}%</span>
      <span class="savings-label">${formatBytes(saved)} saved</span>
    </div>
  `;

  card.addEventListener('click', () => openModal(entry));
  return card;
}

function renderTabs() {
  const tabsEl = document.getElementById('category-tabs');

  // Extract unique categories
  const cats = [...new Set(state.vault.map(e => e.tag))].sort();

  tabsEl.innerHTML = '';
  const allTab = createTab('All', 'all');
  tabsEl.appendChild(allTab);

  cats.forEach(cat => {
    tabsEl.appendChild(createTab(cat, cat));
  });
}

function createTab(label, value) {
  const btn = document.createElement('button');
  btn.className = 'tab' + (state.activeCategory === value ? ' active' : '');
  btn.textContent = label;
  const count = value === 'all' ? state.vault.length : state.vault.filter(e => e.tag === value).length;
  if (count > 0) btn.textContent += ` (${count})`;
  btn.addEventListener('click', () => {
    state.activeCategory = value;
    renderVault();
  });
  return btn;
}

// =====================================================
//  STATS
// =====================================================
function updateStats() {
  const totalFiles = state.vault.length;
  const totalOrig  = state.vault.reduce((s, e) => s + e.origSize, 0);
  const totalComp  = state.vault.reduce((s, e) => s + e.compSize, 0);
  const totalSaved = totalOrig - totalComp;
  const avgRatio   = totalOrig > 0 ? Math.round((1 - totalComp / totalOrig) * 100) : 0;

  document.getElementById('total-files').textContent = totalFiles;
  document.getElementById('total-saved').textContent  = formatBytes(Math.max(0, totalSaved));
  document.getElementById('compress-ratio').textContent = avgRatio + '%';
  document.getElementById('storage-used-label').textContent = formatBytes(totalComp);

  // Fill bar based on 100MB "soft" cap for display
  const cappedPct = Math.min((totalComp / (100 * 1024 * 1024)) * 100, 100);
  document.getElementById('storage-fill').style.width = cappedPct + '%';
}

// =====================================================
//  MODAL
// =====================================================
let modalEntry = null;

function openModal(entry) {
  modalEntry = entry;
  const overlay = document.getElementById('modal-overlay');
  const saved   = entry.origSize - entry.compSize;

  document.getElementById('modal-title').textContent = entry.name;
  document.getElementById('modal-body').innerHTML = `
    <div class="savings-badge">
      <span class="big">-${entry.ratio}%</span>
      <span class="sub">compressed · ${formatBytes(saved)} saved</span>
    </div>
    <div class="modal-detail-row">
      <span>Original Size</span><span>${formatBytes(entry.origSize)}</span>
    </div>
    <div class="modal-detail-row">
      <span>Vaulted Size</span><span>${formatBytes(entry.compSize)}</span>
    </div>
    <div class="modal-detail-row">
      <span>Extension</span><span>.${entry.ext}</span>
    </div>
    <div class="modal-detail-row">
      <span>Category Tag</span><span>${entry.tag}</span>
    </div>
    <div class="modal-detail-row">
      <span>Added</span><span>${formatDate(entry.addedAt)}</span>
    </div>
    <div class="modal-detail-row">
      <span>Vault ID</span><span>${entry.id}</span>
    </div>
  `;

  overlay.hidden = false;
}

function closeModal() {
  document.getElementById('modal-overlay').hidden = true;
  modalEntry = null;
}

// =====================================================
//  EXPORT ALL
// =====================================================
function exportAllEntries() {
  if (state.vault.length === 0) { showToast('Vault is empty', 'info'); return; }
  const data     = JSON.stringify(state.vault, null, 2);
  const blob     = new Blob([data], { type: 'application/json' });
  const url      = URL.createObjectURL(blob);
  const a        = document.createElement('a');
  a.href         = url;
  a.download     = `quickvault_export_${Date.now()}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('Vault exported as JSON backup', 'success');
}

// =====================================================
//  AMBIENT PARTICLES
// =====================================================
function initParticles() {
  const ambient = document.getElementById('ambient');
  // Handled purely by CSS radial gradients + animations
}

// =====================================================
//  EVENT LISTENERS
// =====================================================
function initEvents() {
  // Drop zone
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');

  dropZone.addEventListener('dragover', e => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });

  dropZone.addEventListener('dragleave', e => {
    if (!dropZone.contains(e.relatedTarget)) dropZone.classList.remove('drag-over');
  });

  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    if (e.dataTransfer.files.length) addFilesToQueue([...e.dataTransfer.files]);
  });

  dropZone.addEventListener('click', () => fileInput.click());

  document.getElementById('btn-browse').addEventListener('click', e => {
    e.stopPropagation();
    fileInput.click();
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length) addFilesToQueue([...fileInput.files]);
    fileInput.value = '';
  });

  // Vault button
  document.getElementById('btn-vault').addEventListener('click', vaultAllQueued);

  // Compression slider
  const slider = document.getElementById('compress-level');
  const sliderVal = document.getElementById('compress-val');
  slider.addEventListener('input', () => { sliderVal.textContent = slider.value; });

  // Search
  document.getElementById('search-vault').addEventListener('input', e => {
    state.searchQuery = e.target.value.trim();
    renderVault();
  });

  // Export all
  document.getElementById('btn-export-all').addEventListener('click', exportAllEntries);

  // Clear all
  document.getElementById('btn-clear-all').addEventListener('click', () => {
    if (state.vault.length === 0) { showToast('Vault is already empty', 'info'); return; }
    if (!confirm(`Remove all ${state.vault.length} file(s) from the vault?`)) return;
    state.vault = [];
    saveVault();
    renderVault();
    updateStats();
    showToast('Vault cleared', 'info');
  });

  // Modal
  document.getElementById('modal-close').addEventListener('click', closeModal);
  document.getElementById('modal-overlay').addEventListener('click', e => {
    if (e.target === document.getElementById('modal-overlay')) closeModal();
  });

  document.getElementById('modal-extract').addEventListener('click', () => {
    if (modalEntry) extractEntry(modalEntry);
  });

  document.getElementById('modal-delete').addEventListener('click', () => {
    if (modalEntry) {
      if (confirm(`Remove "${modalEntry.name}" from vault permanently?`)) {
        deleteEntry(modalEntry.id);
      }
    }
  });

  // Keyboard shortcut
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
  });
}

// =====================================================
//  BOOT
// =====================================================
function init() {
  loadVault();
  initEvents();
  initParticles();
  renderVault();
  updateStats();

  // Welcome toast on first load
  if (state.vault.length === 0) {
    setTimeout(() => showToast('Welcome to Quick Vault! Drop files to compress & store them. 🔐', 'info', 5000), 800);
  } else {
    setTimeout(() => showToast(`Vault loaded — ${state.vault.length} file${state.vault.length !== 1 ? 's' : ''} stored`, 'info'), 600);
  }
}

document.addEventListener('DOMContentLoaded', init);
