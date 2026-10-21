# -*- coding: utf-8 -*-

JS_LOGIC = """
// === Chinese Reader Web Application Logic ===

// App State
const state = {
  currentView: 'input',
  uiLang: localStorage.getItem('cr_uiLang') || 'vi',
  meaningLang: localStorage.getItem('cr_meaningLang') || 'vi',
  meaningLang2: localStorage.getItem('cr_meaningLang2') || null,
  darkMode: localStorage.getItem('cr_darkMode') || 'system',
  fontSize: parseInt(localStorage.getItem('cr_fontSize') || '28', 10),
  showPinyin: localStorage.getItem('cr_showPinyin') !== 'false',
  showMeaning: localStorage.getItem('cr_showMeaning') === 'true',
  currentText: '',
  sentences: [],
  currentSentenceIndex: 0,
  viewMode: 'sentence', // 'sentence' | 'all'
  savedWords: JSON.parse(localStorage.getItem('cr_savedWords') || '{}'),
  recentTexts: JSON.parse(localStorage.getItem('cr_recentTexts') || '[]'),
  cachedTranslations: {},
  activeWord: null,
  activeWriters: [],
  flashcards: [],
  flashcardIndex: 0,
  flashcardFlipped: false,
  hskFilter: 'all',
  searchQuery: '',
  dictFilterHSK: 'all',
  savedSort: 'date',
  savedFilterHSK: 'all',
  savedFilterStatus: 'all',
};

// --- Module: i18n ---
function t(key) {
  const lang = state.uiLang;
  return (I18N_DATA[lang] && I18N_DATA[lang][key]) ||
         (I18N_DATA.en && I18N_DATA.en[key]) ||
         key;
}

function setUiLang(lang) {
  if (!I18N_DATA[lang]) return;
  state.uiLang = lang;
  localStorage.setItem('cr_uiLang', lang);
  updateThemeAndUI();
  renderCurrentView();
  showToast(t('language') + ': ' + lang.toUpperCase());
}

function cycleUiLang() {
  const langs = ['vi', 'en', 'ja'];
  const next = langs[(langs.indexOf(state.uiLang) + 1) % langs.length];
  setUiLang(next);
}

// --- Module: Theme Management ---
function applyTheme() {
  let theme = state.darkMode;
  if (theme === 'system') {
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    theme = prefersDark ? 'dark' : 'light';
  }
  document.documentElement.setAttribute('data-theme', theme);
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  if (themeMeta) {
    themeMeta.setAttribute('content', theme === 'dark' ? '#161B22' : '#E8344E');
  }
}

function toggleTheme() {
  if (state.darkMode === 'light') state.darkMode = 'dark';
  else if (state.darkMode === 'dark') state.darkMode = 'system';
  else state.darkMode = 'light';
  localStorage.setItem('cr_darkMode', state.darkMode);
  applyTheme();
  updateThemeAndUI();
  showToast(t('darkMode') + ': ' + state.darkMode);
}

// --- Module: Toast Notifications ---
function showToast(msg) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => {
    if (toast.parentNode) toast.parentNode.removeChild(toast);
  }, 3000);
}

// --- Module: IndexedDB Caching ---
let dbInstance = null;
function initDB() {
  return new Promise((resolve) => {
    if (!window.indexedDB) {
      resolve(null);
      return;
    }
    const req = window.indexedDB.open('ChineseReaderCacheDB', 1);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains('translations')) {
        db.createObjectStore('translations', { keyPath: 'q' });
      }
      if (!db.objectStoreNames.contains('onlineWords')) {
        db.createObjectStore('onlineWords', { keyPath: 'word' });
      }
    };
    req.onsuccess = (e) => {
      dbInstance = e.target.result;
      resolve(dbInstance);
    };
    req.onerror = () => {
      resolve(null);
    };
  });
}

function getFromDB(storeName, key) {
  return new Promise((resolve) => {
    if (!dbInstance) return resolve(null);
    try {
      const tx = dbInstance.transaction(storeName, 'readonly');
      const store = tx.objectStore(storeName);
      const req = store.get(key);
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => resolve(null);
    } catch (err) {
      resolve(null);
    }
  });
}

function putToDB(storeName, data) {
  return new Promise((resolve) => {
    if (!dbInstance) return resolve(false);
    try {
      const tx = dbInstance.transaction(storeName, 'readwrite');
      const store = tx.objectStore(storeName);
      store.put(data);
      tx.oncomplete = () => resolve(true);
      tx.onerror = () => resolve(false);
    } catch (err) {
      resolve(false);
    }
  });
}

// --- Module: Word Segmentation & Tokenization ---
function segmentSentence(text) {
  if (!text) return [];
  // Use Intl.Segmenter if supported
  if ('Segmenter' in Intl) {
    try {
      const segmenter = new Intl.Segmenter('zh', { granularity: 'word' });
      return [...segmenter.segment(text)].map(s => s.segment);
    } catch (e) {
      console.warn('Intl.Segmenter fallback', e);
    }
  }
  // Greedy Forward Match Fallback with MINI_DICT
  const tokens = [];
  let i = 0;
  const maxLen = 4;
  while (i < text.length) {
    let matched = null;
    for (let l = maxLen; l >= 1; l--) {
      if (i + l <= text.length) {
        const sub = text.slice(i, i + l);
        if (MINI_DICT[sub]) {
          matched = sub;
          break;
        }
      }
    }
    if (matched) {
      tokens.push(matched);
      i += matched.length;
    } else {
      tokens.push(text[i]);
      i += 1;
    }
  }
  return tokens;
}

// --- Module: Pinyin & Phonetics ---
function getWordPinyin(word) {
  if (!word) return '';
  // Check if pinyin-pro is loaded on window
  if (window.pinyinPro && typeof window.pinyinPro.pinyin === 'function') {
    try {
      return window.pinyinPro.pinyin(word, { toneType: 'symbol' });
    } catch (e) {}
  }
  // Check embedded dictionary
  if (MINI_DICT[word] && MINI_DICT[word].pinyin) {
    return MINI_DICT[word].pinyin;
  }
  // Check single characters in dictionary
  const parts = [];
  for (const ch of word) {
    if (MINI_DICT[ch] && MINI_DICT[ch].pinyin) {
      parts.push(MINI_DICT[ch].pinyin);
    } else {
      parts.push(ch);
    }
  }
  return parts.join(' ');
}

function getWordHanViet(word) {
  if (!word) return '';
  const parts = [];
  for (const ch of word) {
    parts.push(HAN_VIET[ch] || '');
  }
  const filtered = parts.filter(Boolean);
  return filtered.length > 0 ? filtered.join(' ') : '';
}

function getWordKanji(word) {
  if (!word) return null;
  for (const ch of word) {
    if (KANJI_DATA[ch]) return KANJI_DATA[ch];
  }
  return null;
}

function isChinese(text) {
  return /[\\u4e00-\\u9fff]/.test(text);
}

// Split text into coherent sentences while preserving delimiters
function splitSentences(rawText) {
  if (!rawText) return [];
  const normalized = rawText.replace(/\\r\\n/g, '\\n').replace(/\\r/g, '\\n');
  const rawList = normalized.split(/([。！？；!?;\\n]+)/);
  const result = [];
  let current = '';
  for (let i = 0; i < rawList.length; i++) {
    const chunk = rawList[i];
    if (!chunk) continue;
    current += chunk;
    if (/[。！？；!?;\\n]/.test(chunk) || i === rawList.length - 1) {
      const trimmed = current.trim();
      if (trimmed) result.push(trimmed);
      current = '';
    }
  }
  if (current.trim()) result.push(current.trim());
  return result.length > 0 ? result : [rawText.trim()];
}

// --- Module: Audio TTS ---
function speakText(text) {
  if (!text || !('speechSynthesis' in window)) return;
  try {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    utterance.rate = 0.88;
    const voices = window.speechSynthesis.getVoices();
    const zhVoice = voices.find(v => v.lang.startsWith('zh') || v.lang.includes('cmn'));
    if (zhVoice) {
      utterance.voice = zhVoice;
    } else if (voices.length > 0) {
      console.warn("No Chinese TTS voice found");
    }
    window.speechSynthesis.speak(utterance);
  } catch (err) {
    console.error("Speech error", err);
  }
}

function testSpeechVoices() {
  if (!('speechSynthesis' in window)) {
    alert("Speech Synthesis is not supported in this browser.");
    return;
  }
  const voices = window.speechSynthesis.getVoices();
  const zhVoices = voices.filter(v => v.lang.startsWith('zh') || v.lang.includes('cmn'));
  if (zhVoices.length > 0) {
    const names = zhVoices.map(v => v.name + " (" + v.lang + ")").join('\\n');
    alert("Found " + zhVoices.length + " Chinese voice(s):\\n" + names);
    speakText("你好，欢迎使用汉读！");
  } else {
    alert(t('noVoice'));
  }
}

// --- Module: Translation API (MyMemory) ---
async function translateTextOnline(text, targetLang) {
  if (!text) return '';
  const langPair = targetLang === 'vi' ? 'zh|vi' : (targetLang === 'ja' ? 'zh|ja' : 'zh|en');
  const cacheKey = langPair + ':' + text;
  
  if (state.cachedTranslations[cacheKey]) {
    return state.cachedTranslations[cacheKey];
  }
  const fromDB = await getFromDB('translations', cacheKey);
  if (fromDB && fromDB.result) {
    state.cachedTranslations[cacheKey] = fromDB.result;
    return fromDB.result;
  }
  
  try {
    const url = 'https://api.mymemory.translated.net/get?q=' + encodeURIComponent(text) + '&langpair=' + langPair;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error("HTTP error " + resp.status);
    const data = await resp.json();
    if (data && data.responseData && data.responseData.translatedText) {
      let result = data.responseData.translatedText;
      // Filter out automated matches if quality is bad or error string
      if (result.includes("MYMEMORY WARNING")) {
        result = data.responseData.translatedText.split('\\n')[0];
      }
      state.cachedTranslations[cacheKey] = result;
      await putToDB('translations', { q: cacheKey, result });
      return result;
    }
  } catch (err) {
    console.warn("Online translation request failed", err);
  }
  return '';
}

// --- Module: Navigation & Views ---
function switchView(viewName) {
  state.currentView = viewName;
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const targetView = document.getElementById('view-' + viewName);
  if (targetView) targetView.classList.add('active');

  document.querySelectorAll('.nav-tab').forEach(tab => {
    if (tab.getAttribute('data-view') === viewName) {
      tab.classList.add('active');
    } else {
      tab.classList.remove('active');
    }
  });

  const titles = {
    input: t('inputTitle'),
    reader: t('readTitle'),
    dict: t('dictTitle'),
    saved: t('savedTitle'),
    settings: t('settingsTitle'),
  };
  const topTitleEl = document.getElementById('top-bar-title');
  if (topTitleEl) topTitleEl.textContent = titles[viewName] || t('appName');

  renderCurrentView();
}

function renderCurrentView() {
  switch (state.currentView) {
    case 'input':
      renderInputView();
      break;
    case 'reader':
      renderReaderView();
      break;
    case 'dict':
      renderDictView();
      break;
    case 'saved':
      renderSavedView();
      break;
    case 'settings':
      renderSettingsView();
      break;
  }
}

// --- Module: Input View ---
function renderInputView() {
  const recentListEl = document.getElementById('recent-texts-list');
  if (!recentListEl) return;
  if (!state.recentTexts || state.recentTexts.length === 0) {
    recentListEl.innerHTML = '<div style="color:var(--text-muted); font-size:13px; padding:8px;">' + t('noHistory') + '</div>';
    return;
  }
  let html = '';
  state.recentTexts.slice(0, 5).forEach((item, idx) => {
    html += `
      <div class="recent-item" onclick="loadRecentText(${idx})">
        <div class="recent-text">${escapeHtml(item.preview)}</div>
        <div class="recent-meta">${new Date(item.date).toLocaleDateString()}</div>
      </div>
    `;
  });
  recentListEl.innerHTML = html;
}

function loadRecentText(idx) {
  const item = state.recentTexts[idx];
  if (!item) return;
  document.getElementById('input-textarea').value = item.text;
  analyzeText();
}

function loadSample(sampleType) {
  const samples = {
    daily: "你好！很高兴认识你。今天天气非常好，我们一起去公园散步吧。你想喝中国茶还是咖啡？",
    story: "从前有一只聪明的猫，它住在一个美丽的大城市里。每天早上，它都在窗户旁边看太阳升起。朋友们都很喜欢它。",
    business: "王经理，您好！关于下周一的会议，我们已经准备好了所有材料。如果您有时间，请查看附件中的文件。祝工作顺利！"
  };
  const text = samples[sampleType] || samples.daily;
  document.getElementById('input-textarea').value = text;
}

async function pasteFromClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    if (text) {
      document.getElementById('input-textarea').value = text;
      showToast(t('copied'));
    }
  } catch (err) {
    alert("Vui lòng cấp quyền clipboard hoặc dán thủ công vào ô văn bản.");
  }
}

function analyzeText() {
  const textarea = document.getElementById('input-textarea');
  const text = textarea ? textarea.value.trim() : '';
  if (!text) {
    showToast("Vui lòng nhập văn bản tiếng Trung!");
    return;
  }

  state.currentText = text;
  state.sentences = splitSentences(text);
  state.currentSentenceIndex = 0;

  // Add to recent texts
  const existingIdx = state.recentTexts.findIndex(r => r.text === text);
  if (existingIdx >= 0) state.recentTexts.splice(existingIdx, 1);
  state.recentTexts.unshift({
    text: text,
    preview: text.length > 35 ? text.slice(0, 35) + '...' : text,
    date: Date.now()
  });
  if (state.recentTexts.length > 20) state.recentTexts.pop();
  localStorage.setItem('cr_recentTexts', JSON.stringify(state.recentTexts));

  switchView('reader');
}

// --- Module: Reader View ---
function renderReaderView() {
  const container = document.getElementById('reader-content-area');
  if (!container) return;
  
  document.documentElement.style.setProperty('--reader-font-size', state.fontSize + 'px');
  
  // Update toggle button states
  const pinyinBtn = document.getElementById('btn-toggle-pinyin');
  if (pinyinBtn) pinyinBtn.classList.toggle('active', state.showPinyin);
  const meaningBtn = document.getElementById('btn-toggle-meaning');
  if (meaningBtn) meaningBtn.classList.toggle('active', state.showMeaning);
  const viewModeBtn = document.getElementById('btn-toggle-viewmode');
  if (viewModeBtn) {
    viewModeBtn.textContent = state.viewMode === 'sentence' ? t('viewSingle') : t('viewAll');
  }

  if (state.sentences.length === 0) {
    container.innerHTML = '<div class="card" style="text-align:center; padding:30px;">Chưa có văn bản. Nhấn Quay lại để nhập văn bản.</div>';
    return;
  }

  if (state.viewMode === 'sentence') {
    renderSentenceMode(container);
  } else {
    renderFullTextMode(container);
  }
}

function renderSentenceMode(container) {
  const total = state.sentences.length;
  const currIdx = Math.min(Math.max(0, state.currentSentenceIndex), total - 1);
  state.currentSentenceIndex = currIdx;
  const sentence = state.sentences[currIdx];
  const tokens = segmentSentence(sentence);

  let tokensHtml = '';
  tokens.forEach(tok => {
    if (!isChinese(tok)) {
      tokensHtml += `<span class="punctuation-token">${escapeHtml(tok)}</span>`;
    } else {
      const pinyin = getWordPinyin(tok);
      const dictInfo = MINI_DICT[tok];
      let miniMeaning = '';
      if (state.showMeaning) {
        miniMeaning = dictInfo ? (state.meaningLang === 'en' ? dictInfo.en[0] : dictInfo.vi) : '';
      }
      const isSaved = !!state.savedWords[tok];
      tokensHtml += `
        <div class="word-token ${isSaved ? 'saved-star' : ''}" onclick="openWordSheet('${escapeHtml(tok)}')">
          <span class="token-pinyin">${escapeHtml(pinyin)}</span>
          <span class="token-chars">${escapeHtml(tok)}</span>
          ${miniMeaning ? `<span class="token-mini-meaning">${escapeHtml(miniMeaning)}</span>` : ''}
        </div>
      `;
    }
  });

  const pinyinClass = state.showPinyin ? '' : 'hide-pinyin';
  const meaningClass = state.showMeaning ? '' : 'hide-meaning';

  container.innerHTML = `
    <div class="sentence-card">
      <div class="sentence-header">
        <span class="sentence-index">${t('translateSentence').split(' ')[1] || 'Câu'} ${currIdx + 1} / ${total}</span>
        <div style="display:flex; gap:8px;">
          <button class="icon-btn" onclick="speakText('${escapeQuotes(sentence)}')">
            <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path></svg>
          </button>
          <button class="btn btn-secondary btn-sm" onclick="translateCurrentSentence()">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path></svg>
            ${t('translateSentence')}
          </button>
        </div>
      </div>
      <div class="sentence-content ${pinyinClass} ${meaningClass}">
        ${tokensHtml}
      </div>
      <div id="sentence-trans-box" class="translation-box"></div>
      <div class="sentence-nav-bar">
        <button class="btn btn-secondary" onclick="prevSentence()" ${currIdx === 0 ? 'disabled style="opacity:0.5;"' : ''}>
          ← ${t('prevSentence')}
        </button>
        <button class="btn btn-primary" onclick="nextSentence()" ${currIdx === total - 1 ? 'disabled style="opacity:0.5;"' : ''}>
          ${t('nextSentence')} →
        </button>
      </div>
    </div>
  `;
}

function renderFullTextMode(container) {
  const pinyinClass = state.showPinyin ? '' : 'hide-pinyin';
  const meaningClass = state.showMeaning ? '' : 'hide-meaning';

  let html = '<div class="full-text-container">';
  state.sentences.forEach((sentence, sIdx) => {
    const tokens = segmentSentence(sentence);
    let tokensHtml = '';
    tokens.forEach(tok => {
      if (!isChinese(tok)) {
        tokensHtml += `<span class="punctuation-token">${escapeHtml(tok)}</span>`;
      } else {
        const pinyin = getWordPinyin(tok);
        const dictInfo = MINI_DICT[tok];
        let miniMeaning = '';
        if (state.showMeaning) {
          miniMeaning = dictInfo ? (state.meaningLang === 'en' ? dictInfo.en[0] : dictInfo.vi) : '';
        }
        const isSaved = !!state.savedWords[tok];
        tokensHtml += `
          <div class="word-token ${isSaved ? 'saved-star' : ''}" onclick="openWordSheet('${escapeHtml(tok)}')">
            <span class="token-pinyin">${escapeHtml(pinyin)}</span>
            <span class="token-chars">${escapeHtml(tok)}</span>
            ${miniMeaning ? `<span class="token-mini-meaning">${escapeHtml(miniMeaning)}</span>` : ''}
          </div>
        `;
      }
    });

    html += `
      <div class="sentence-paragraph ${sIdx === state.currentSentenceIndex ? 'active-sentence' : ''}" onclick="state.currentSentenceIndex = ${sIdx}">
        <span style="font-size:12px; font-weight:700; color:var(--text-muted); margin-right:8px; cursor:pointer;" onclick="speakText('${escapeQuotes(sentence)}')">🔊 [${sIdx + 1}]</span>
        <div style="display:inline;" class="${pinyinClass} ${meaningClass}">
          ${tokensHtml}
        </div>
      </div>
    `;
  });
  html += '</div>';
  container.innerHTML = html;
}

function prevSentence() {
  if (state.currentSentenceIndex > 0) {
    state.currentSentenceIndex--;
    renderReaderView();
  }
}

function nextSentence() {
  if (state.currentSentenceIndex < state.sentences.length - 1) {
    state.currentSentenceIndex++;
    renderReaderView();
  }
}

function togglePinyin() {
  state.showPinyin = !state.showPinyin;
  localStorage.setItem('cr_showPinyin', state.showPinyin);
  renderReaderView();
}

function toggleMeaning() {
  state.showMeaning = !state.showMeaning;
  localStorage.setItem('cr_showMeaning', state.showMeaning);
  renderReaderView();
}

function toggleViewMode() {
  state.viewMode = state.viewMode === 'sentence' ? 'all' : 'sentence';
  renderReaderView();
}

function changeFontSize(delta) {
  state.fontSize = Math.min(48, Math.max(18, state.fontSize + delta));
  localStorage.setItem('cr_fontSize', state.fontSize);
  renderReaderView();
}

async function translateCurrentSentence() {
  const box = document.getElementById('sentence-trans-box');
  if (!box) return;
  const sentence = state.sentences[state.currentSentenceIndex];
  if (!sentence) return;

  box.classList.add('show');
  box.innerHTML = '<em>' + t('translating') + '</em>';

  const trans = await translateTextOnline(sentence, state.meaningLang);
  if (trans) {
    box.innerHTML = `<strong>${escapeHtml(trans)}</strong>`;
  } else {
    box.innerHTML = '<span style="color:var(--text-muted);">' + t('noMeaning') + '</span>';
  }
}

// --- Module: Word Sheet Modal & Hanzi Writer ---
async function openWordSheet(word) {
  if (!word) return;
  state.activeWord = word;
  
  const backdrop = document.getElementById('sheet-backdrop');
  const sheet = document.getElementById('word-sheet');
  if (!backdrop || !sheet) return;

  const pinyin = getWordPinyin(word);
  const hanviet = getWordHanViet(word);
  const dictEntry = MINI_DICT[word];
  const kanjiInfo = getWordKanji(word);
  const isSaved = !!state.savedWords[word];

  // Header info
  document.getElementById('sheet-hanzi-title').textContent = word;
  document.getElementById('sheet-pinyin').textContent = pinyin;
  const hanvietEl = document.getElementById('sheet-hanviet');
  if (hanvietEl) {
    hanvietEl.textContent = hanviet ? (t('hanViet') + ': ' + hanviet) : '';
  }

  // Save / Bookmark button state
  updateSheetSaveButton(isSaved);

  // Badges
  const badgesContainer = document.getElementById('sheet-badges');
  badgesContainer.innerHTML = '';
  if (dictEntry && dictEntry.hsk) {
    badgesContainer.innerHTML += `<span class="badge badge-hsk">HSK ${dictEntry.hsk}</span>`;
  }
  if (dictEntry && dictEntry.type) {
    badgesContainer.innerHTML += `<span class="badge">${escapeHtml(dictEntry.type)}</span>`;
  }

  // Meanings
  const defViEl = document.getElementById('sheet-def-vi');
  const defEnEl = document.getElementById('sheet-def-en');
  const defJaEl = document.getElementById('sheet-def-ja');
  
  if (dictEntry) {
    if (defViEl) defViEl.innerHTML = escapeHtml(dictEntry.vi);
    if (defEnEl) defEnEl.innerHTML = escapeHtml(dictEntry.en.join('; '));
  } else {
    if (defViEl) defViEl.innerHTML = '<em>' + t('loadingDict') + '</em>';
    if (defEnEl) defEnEl.innerHTML = '';
    
    // Fetch online translation for unknown word
    translateTextOnline(word, 'vi').then(trans => {
      if (state.activeWord === word && defViEl) {
        defViEl.innerHTML = trans ? escapeHtml(trans) : ('<span style="color:var(--text-muted);">' + t('noMeaning') + '</span>');
      }
    });
    translateTextOnline(word, 'en').then(trans => {
      if (state.activeWord === word && defEnEl) {
        defEnEl.innerHTML = trans ? escapeHtml(trans) : '';
      }
    });
  }

  // Japanese Kanji info
  if (defJaEl) {
    if (kanjiInfo) {
      defJaEl.parentElement.style.display = 'block';
      defJaEl.innerHTML = `
        <div><strong>${t('kanjiOn')}:</strong> ${escapeHtml(kanjiInfo.on)}</div>
        <div><strong>${t('kanjiKun')}:</strong> ${escapeHtml(kanjiInfo.kun || '-')}</div>
        <div><strong>${t('kanjiMeaning')}:</strong> ${escapeHtml(kanjiInfo.ja_meaning)}</div>
      `;
    } else {
      defJaEl.parentElement.style.display = 'none';
    }
  }

  // External Dictionary Links
  const extContainer = document.getElementById('sheet-external-links');
  if (extContainer) {
    extContainer.innerHTML = `
      <a class="btn btn-secondary btn-sm" href="https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb=${encodeURIComponent(word)}" target="_blank" rel="noopener">MDBG</a>
      <a class="btn btn-secondary btn-sm" href="https://baike.baidu.com/item/${encodeURIComponent(word)}" target="_blank" rel="noopener">Baidu</a>
      <a class="btn btn-secondary btn-sm" href="https://hanzicraft.com/character/${encodeURIComponent(word)}" target="_blank" rel="noopener">HanziCraft</a>
    `;
  }

  // Render Hanzi Writer
  renderHanziWriterForWord(word);

  backdrop.classList.add('active');
  sheet.classList.add('active');
}

function closeWordSheet() {
  const backdrop = document.getElementById('sheet-backdrop');
  const sheet = document.getElementById('word-sheet');
  if (backdrop) backdrop.classList.remove('active');
  if (sheet) sheet.classList.remove('active');
  state.activeWriters = [];
}

function updateSheetSaveButton(isSaved) {
  const btn = document.getElementById('sheet-btn-save');
  if (!btn) return;
  if (isSaved) {
    btn.innerHTML = `
      <svg width="20" height="20" fill="#F59E0B" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
    `;
    btn.title = t('savedWord');
  } else {
    btn.innerHTML = `
      <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>
    `;
    btn.title = t('saveWord');
  }
}

function toggleSaveActiveWord() {
  const word = state.activeWord;
  if (!word) return;
  
  if (state.savedWords[word]) {
    delete state.savedWords[word];
    localStorage.setItem('cr_savedWords', JSON.stringify(state.savedWords));
    updateSheetSaveButton(false);
    showToast(t('wordRemoved'));
  } else {
    const pinyin = getWordPinyin(word);
    const hanviet = getWordHanViet(word);
    const dict = MINI_DICT[word];
    state.savedWords[word] = {
      word: word,
      pinyin: pinyin,
      hanviet: hanviet,
      vi: dict ? dict.vi : '',
      en: dict ? dict.en.join('; ') : '',
      hsk: dict ? dict.hsk : null,
      remembered: false,
      dateSaved: Date.now()
    };
    localStorage.setItem('cr_savedWords', JSON.stringify(state.savedWords));
    updateSheetSaveButton(true);
    showToast(t('wordSaved'));
  }
  
  if (state.currentView === 'reader') renderReaderView();
  if (state.currentView === 'saved') renderSavedView();
}

function renderHanziWriterForWord(word) {
  const container = document.getElementById('hanzi-writer-box');
  if (!container) return;
  container.innerHTML = '';
  state.activeWriters = [];

  const chars = [...word].filter(ch => /[\\u4e00-\\u9fff]/.test(ch));
  if (chars.length === 0) return;

  chars.forEach((ch, idx) => {
    const targetDiv = document.createElement('div');
    targetDiv.className = 'writer-char-box';
    targetDiv.id = 'writer-target-' + idx;
    container.appendChild(targetDiv);

    if (window.HanziWriter && typeof window.HanziWriter.create === 'function') {
      try {
        const writer = window.HanziWriter.create(targetDiv.id, ch, {
          width: 120,
          height: 120,
          padding: 5,
          showOutline: true,
          strokeAnimationSpeed: 1.2,
          delayBetweenStrokes: 120,
          strokeColor: '#E8344E',
          outlineColor: '#DDD',
          drawingColor: '#2EA043'
        });
        state.activeWriters.push(writer);
        writer.animateCharacter();
      } catch (e) {
        targetDiv.innerHTML = `<span style="font-family:var(--font-hanzi); font-size:64px;">${escapeHtml(ch)}</span>`;
      }
    } else {
      // Fallback offline SVG box
      targetDiv.innerHTML = `
        <svg width="120" height="120" viewBox="0 0 120 120">
          <line x1="0" y1="0" x2="120" y2="120" stroke="#eee" stroke-dasharray="3,3"/>
          <line x1="120" y1="0" x2="0" y2="120" stroke="#eee" stroke-dasharray="3,3"/>
          <line x1="60" y1="0" x2="60" y2="120" stroke="#eee" stroke-dasharray="3,3"/>
          <line x1="0" y1="60" x2="120" y2="60" stroke="#eee" stroke-dasharray="3,3"/>
          <text x="60" y="80" font-size="64" font-family="Noto Sans SC, sans-serif" text-anchor="middle" fill="#E8344E">${escapeHtml(ch)}</text>
        </svg>
      `;
    }
  });
}

function animateActiveWriters() {
  if (state.activeWriters && state.activeWriters.length > 0) {
    state.activeWriters.forEach(w => w.animateCharacter());
  }
}

function quizActiveWriters() {
  if (state.activeWriters && state.activeWriters.length > 0) {
    state.activeWriters.forEach(w => w.quiz({
      onComplete: (summary) => {
        showToast(t('remember') + '! Mistakes: ' + summary.totalMistakes);
      }
    }));
  }
}

function splitActiveWord() {
  const word = state.activeWord;
  if (!word || word.length <= 1) return;
  const chars = [...word];
  closeWordSheet();
  // Open first character
  openWordSheet(chars[0]);
}

// --- Module: Dictionary View ---
function renderDictView() {
  const container = document.getElementById('dict-results-container');
  if (!container) return;

  const query = state.searchQuery.trim().toLowerCase();
  const filterHSK = state.dictFilterHSK;

  let matches = [];
  const allWords = Object.keys(MINI_DICT);

  for (const w of allWords) {
    const entry = MINI_DICT[w];
    if (filterHSK !== 'all' && String(entry.hsk) !== filterHSK) {
      continue;
    }
    if (!query) {
      matches.push({ word: w, ...entry });
      if (matches.length >= 60) break;
      continue;
    }

    const matchesHanzi = w.includes(query);
    const matchesPinyin = entry.pinyin.toLowerCase().includes(query);
    const matchesVi = entry.vi && entry.vi.toLowerCase().includes(query);
    const matchesEn = entry.en && entry.en.some(e => e.toLowerCase().includes(query));
    const matchesHanViet = entry.hanviet && entry.hanviet.toLowerCase().includes(query);

    if (matchesHanzi || matchesPinyin || matchesVi || matchesEn || matchesHanViet) {
      matches.push({ word: w, ...entry });
      if (matches.length >= 80) break;
    }
  }

  if (matches.length === 0) {
    container.innerHTML = `
      <div class="card" style="text-align:center; padding:30px;">
        <div style="font-size:16px; font-weight:600; color:var(--text-secondary);">${t('noResults')}</div>
        ${query ? `
          <button class="btn btn-outline" style="margin-top:14px;" onclick="searchOnline('${escapeQuotes(query)}')">
            🔍 ${t('onlineLookup')}: "${escapeHtml(query)}"
          </button>
        ` : ''}
      </div>
    `;
    return;
  }

  let html = '<div class="dict-results-list">';
  matches.forEach(item => {
    const meaning = state.meaningLang === 'en' ? item.en.join('; ') : item.vi;
    html += `
      <div class="dict-item-card" onclick="openWordSheet('${escapeHtml(item.word)}')">
        <div>
          <div class="dict-item-left">
            <span class="dict-hanzi">${escapeHtml(item.word)}</span>
            <span class="dict-pinyin">${escapeHtml(item.pinyin)}</span>
            ${item.hanviet ? `<span class="dict-hanviet">${escapeHtml(item.hanviet)}</span>` : ''}
          </div>
          <div class="dict-meaning">${escapeHtml(meaning)}</div>
        </div>
        <div>
          ${item.hsk ? `<span class="badge badge-hsk">HSK ${item.hsk}</span>` : ''}
        </div>
      </div>
    `;
  });
  html += '</div>';
  container.innerHTML = html;
}

function handleDictSearch(val) {
  state.searchQuery = val;
  renderDictView();
}

function setDictFilter(hskVal) {
  state.dictFilterHSK = hskVal;
  document.querySelectorAll('.dict-filter-chip').forEach(el => {
    el.classList.toggle('active', el.getAttribute('data-hsk') === hskVal);
  });
  renderDictView();
}

function searchOnline(query) {
  openWordSheet(query);
}

// --- Module: Saved Words & Flashcard Review ---
function renderSavedView() {
  const container = document.getElementById('saved-words-container');
  if (!container) return;

  const words = Object.values(state.savedWords);
  const totalCount = words.length;
  const rememberedCount = words.filter(w => w.remembered).length;
  const unknownCount = totalCount - rememberedCount;

  document.getElementById('stat-total-count').textContent = totalCount;
  document.getElementById('stat-knew-count').textContent = rememberedCount;
  document.getElementById('stat-unknown-count').textContent = unknownCount;

  let filtered = [...words];

  // HSK Filter
  if (state.savedFilterHSK !== 'all') {
    filtered = filtered.filter(w => String(w.hsk) === state.savedFilterHSK);
  }

  // Status Filter
  if (state.savedFilterStatus === 'remembered') {
    filtered = filtered.filter(w => w.remembered);
  } else if (state.savedFilterStatus === 'unknown') {
    filtered = filtered.filter(w => !w.remembered);
  }

  // Sort
  if (state.savedSort === 'alpha') {
    filtered.sort((a, b) => a.word.localeCompare(b.word));
  } else {
    filtered.sort((a, b) => (b.dateSaved || 0) - (a.dateSaved || 0));
  }

  if (filtered.length === 0) {
    container.innerHTML = `<div class="card" style="text-align:center; padding:30px; color:var(--text-muted);">${t('noSavedWords')}</div>`;
    return;
  }

  let html = '<div class="dict-results-list">';
  filtered.forEach(item => {
    const meaning = state.meaningLang === 'en' ? item.en : (item.vi || item.en);
    html += `
      <div class="dict-item-card">
        <div style="flex:1; cursor:pointer;" onclick="openWordSheet('${escapeHtml(item.word)}')">
          <div class="dict-item-left">
            <span class="dict-hanzi">${escapeHtml(item.word)}</span>
            <span class="dict-pinyin">${escapeHtml(item.pinyin)}</span>
            ${item.hanviet ? `<span class="dict-hanviet">${escapeHtml(item.hanviet)}</span>` : ''}
          </div>
          <div class="dict-meaning">${escapeHtml(meaning || t('noMeaning'))}</div>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <button class="btn btn-sm ${item.remembered ? 'btn-primary' : 'btn-secondary'}" onclick="toggleRememberWord('${escapeHtml(item.word)}')">
            ${item.remembered ? '✓ ' + t('remember') : t('notRemember')}
          </button>
          <button class="icon-btn" onclick="speakText('${escapeQuotes(item.word)}')">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
          </button>
          <button class="icon-btn" style="color:var(--accent);" onclick="deleteSavedWord('${escapeHtml(item.word)}')">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </div>
    `;
  });
  html += '</div>';
  container.innerHTML = html;
}

function toggleRememberWord(word) {
  if (state.savedWords[word]) {
    state.savedWords[word].remembered = !state.savedWords[word].remembered;
    localStorage.setItem('cr_savedWords', JSON.stringify(state.savedWords));
    renderSavedView();
  }
}

function deleteSavedWord(word) {
  if (state.savedWords[word]) {
    delete state.savedWords[word];
    localStorage.setItem('cr_savedWords', JSON.stringify(state.savedWords));
    renderSavedView();
    showToast(t('wordRemoved'));
  }
}

function setSavedFilterHSK(hskVal) {
  state.savedFilterHSK = hskVal;
  renderSavedView();
}

function setSavedFilterStatus(status) {
  state.savedFilterStatus = status;
  renderSavedView();
}

function setSavedSort(sortMode) {
  state.savedSort = sortMode;
  renderSavedView();
}

// Flashcard Review
function startFlashcardReview() {
  const words = Object.values(state.savedWords);
  if (words.length === 0) {
    showToast(t('noSavedWords'));
    return;
  }
  state.flashcards = [...words].sort(() => Math.random() - 0.5);
  state.flashcardIndex = 0;
  state.flashcardFlipped = false;

  const modal = document.getElementById('flashcard-modal');
  if (modal) modal.classList.add('active');
  renderCurrentFlashcard();
}

function closeFlashcardModal() {
  const modal = document.getElementById('flashcard-modal');
  if (modal) modal.classList.remove('active');
  renderSavedView();
}

function renderCurrentFlashcard() {
  const total = state.flashcards.length;
  if (state.flashcardIndex >= total) {
    // Review complete
    const scene = document.getElementById('flashcard-scene-container');
    scene.innerHTML = `
      <div class="card" style="text-align:center; padding:40px 20px;">
        <h2 style="font-size:24px; color:var(--accent); margin-bottom:12px;">🎉 ${t('flashcardDone')}</h2>
        <p style="color:var(--text-secondary); margin-bottom:20px;">Bạn đã hoàn thành xem qua ${total} từ.</p>
        <button class="btn btn-primary" onclick="startFlashcardReview()">${t('flashcard')}</button>
      </div>
    `;
    document.getElementById('flashcard-controls-row').style.display = 'none';
    return;
  }

  document.getElementById('flashcard-controls-row').style.display = 'flex';
  const curr = state.flashcards[state.flashcardIndex];
  state.flashcardFlipped = false;

  const progressEl = document.getElementById('flashcard-progress');
  if (progressEl) progressEl.textContent = (state.flashcardIndex + 1) + ' / ' + total;

  const meaning = state.meaningLang === 'en' ? curr.en : (curr.vi || curr.en);

  const scene = document.getElementById('flashcard-scene-container');
  scene.innerHTML = `
    <div class="flashcard-3d-scene" onclick="toggleFlashcardFlip()">
      <div id="flashcard-inner-card" class="flashcard-inner">
        <div class="flashcard-front">
          <div class="flashcard-hanzi">${escapeHtml(curr.word)}</div>
          <div class="flashcard-hint">${t('flipCard')}</div>
        </div>
        <div class="flashcard-back">
          <div style="font-size:24px; font-weight:700; color:var(--accent);">${escapeHtml(curr.pinyin)}</div>
          ${curr.hanviet ? `<div style="font-size:16px; color:var(--info); font-weight:600; margin-top:4px;">${escapeHtml(curr.hanviet)}</div>` : ''}
          <div style="font-size:16px; margin-top:10px; color:var(--text-primary); font-weight:500;">${escapeHtml(meaning || t('noMeaning'))}</div>
          <button class="btn btn-secondary btn-sm" style="margin-top:16px;" onclick="event.stopPropagation(); speakText('${escapeQuotes(curr.word)}')">
            🔊 ${t('play')}
          </button>
        </div>
      </div>
    </div>
  `;
}

function toggleFlashcardFlip() {
  const card = document.getElementById('flashcard-inner-card');
  if (!card) return;
  state.flashcardFlipped = !state.flashcardFlipped;
  card.classList.toggle('is-flipped', state.flashcardFlipped);
}

function answerFlashcard(remembered) {
  const curr = state.flashcards[state.flashcardIndex];
  if (curr && state.savedWords[curr.word]) {
    state.savedWords[curr.word].remembered = remembered;
    localStorage.setItem('cr_savedWords', JSON.stringify(state.savedWords));
  }
  state.flashcardIndex++;
  renderCurrentFlashcard();
}

// Export CSV
function exportSavedCSV() {
  const words = Object.values(state.savedWords);
  if (words.length === 0) {
    showToast(t('noSavedWords'));
    return;
  }
  let csv = "\\uFEFFHán Tự,Phiên Âm,Hán Việt,Nghĩa Tiếng Việt,Nghĩa Tiếng Anh,HSK,Trạng Thái\\n";
  words.forEach(w => {
    csv += `"${w.word}","${w.pinyin || ''}","${w.hanviet || ''}","${(w.vi || '').replace(/"/g, '""')}","${(w.en || '').replace(/"/g, '""')}","${w.hsk || ''}","${w.remembered ? 'Đã nhớ' : 'Chưa nhớ'}"\\n`;
  });
  downloadFile(csv, "chinese_reader_words.csv", "text/csv;charset=utf-8;");
}

// Export JSON
function exportSavedJSON() {
  const jsonStr = JSON.stringify(state.savedWords, null, 2);
  downloadFile(jsonStr, "chinese_reader_saved_words.json", "application/json");
}

// Full Backup & Restore
function backupAllData() {
  const fullBackup = {
    version: 1,
    savedWords: state.savedWords,
    recentTexts: state.recentTexts,
    settings: {
      uiLang: state.uiLang,
      meaningLang: state.meaningLang,
      darkMode: state.darkMode,
      fontSize: state.fontSize,
      showPinyin: state.showPinyin,
      showMeaning: state.showMeaning,
    }
  };
  downloadFile(JSON.stringify(fullBackup, null, 2), "chinese_reader_backup.json", "application/json");
}

function restoreDataFromFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      if (data.savedWords) {
        state.savedWords = data.savedWords;
        localStorage.setItem('cr_savedWords', JSON.stringify(state.savedWords));
      }
      if (data.recentTexts) {
        state.recentTexts = data.recentTexts;
        localStorage.setItem('cr_recentTexts', JSON.stringify(state.recentTexts));
      }
      if (data.settings) {
        if (data.settings.uiLang) state.uiLang = data.settings.uiLang;
        if (data.settings.meaningLang) state.meaningLang = data.settings.meaningLang;
        if (data.settings.darkMode) state.darkMode = data.settings.darkMode;
        if (data.settings.fontSize) state.fontSize = data.settings.fontSize;
      }
      showToast("Khôi phục thành công!");
      updateThemeAndUI();
      renderCurrentView();
    } catch (err) {
      alert("Tệp sao lưu không hợp lệ.");
    }
  };
  reader.readAsText(file);
}

function clearAllAppData() {
  if (confirm(t('confirmClear'))) {
    state.savedWords = {};
    state.recentTexts = [];
    localStorage.removeItem('cr_savedWords');
    localStorage.removeItem('cr_recentTexts');
    showToast("Đã xóa toàn bộ dữ liệu.");
    renderCurrentView();
  }
}

function downloadFile(content, fileName, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// --- Module: OCR (Tesseract.js) ---
async function handleImageUpload(file) {
  if (!file) return;
  
  const modal = document.getElementById('ocr-modal');
  const progressContainer = document.getElementById('ocr-progress-container');
  const progressBar = document.getElementById('ocr-progress-bar');
  const progressText = document.getElementById('ocr-progress-text');
  const editArea = document.getElementById('ocr-edit-textarea');
  
  if (!modal) return;
  modal.classList.add('active');
  progressContainer.style.display = 'block';
  progressBar.style.width = '0%';
  progressText.textContent = t('loadingOCR');
  editArea.value = '';

  try {
    // Resize image using offscreen canvas to avoid memory overflow & speed up recognition
    const img = await loadImageFromFile(file);
    const canvas = document.createElement('canvas');
    const maxDim = 1200;
    let w = img.width;
    let h = img.height;
    if (w > maxDim || h > maxDim) {
      if (w > h) {
        h = Math.round((h * maxDim) / w);
        w = maxDim;
      } else {
        w = Math.round((w * maxDim) / h);
        h = maxDim;
      }
    }
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, w, h);

    if (window.Tesseract && typeof window.Tesseract.recognize === 'function') {
      const res = await window.Tesseract.recognize(canvas, 'chi_sim', {
        logger: (m) => {
          if (m.status === 'recognizing text') {
            const pct = Math.round((m.progress || 0) * 100);
            progressBar.style.width = pct + '%';
            progressText.textContent = t('loadingOCR') + ' (' + pct + '%)';
          }
        }
      });
      progressContainer.style.display = 'none';
      editArea.value = (res.data && res.data.text) ? res.data.text.trim() : '';
    } else {
      progressContainer.style.display = 'none';
      editArea.value = "Thư viện Tesseract.js chưa được tải (vui lòng kiểm tra kết nối mạng). Bạn có thể gõ hoặc dán chữ Hán vào đây.";
    }
  } catch (err) {
    console.error("OCR error", err);
    progressContainer.style.display = 'none';
    alert("Lỗi nhận diện ảnh: " + err.message);
  }
}

function loadImageFromFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = e.target.result;
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function confirmOcrResult() {
  const text = document.getElementById('ocr-edit-textarea').value.trim();
  const modal = document.getElementById('ocr-modal');
  if (modal) modal.classList.remove('active');
  if (text) {
    document.getElementById('input-textarea').value = text;
    analyzeText();
  }
}

function closeOcrModal() {
  const modal = document.getElementById('ocr-modal');
  if (modal) modal.classList.remove('active');
}

// --- Module: Settings View ---
function renderSettingsView() {
  const uiSelect = document.getElementById('setting-ui-lang');
  if (uiSelect) uiSelect.value = state.uiLang;

  const meaningSelect = document.getElementById('setting-meaning-lang');
  if (meaningSelect) meaningSelect.value = state.meaningLang;

  const darkSelect = document.getElementById('setting-dark-mode');
  if (darkSelect) darkSelect.value = state.darkMode;

  const fontSlider = document.getElementById('setting-font-size');
  const fontValText = document.getElementById('setting-font-val');
  if (fontSlider) fontSlider.value = state.fontSize;
  if (fontValText) fontValText.textContent = state.fontSize + 'px';
}

function handleSettingChange(key, val) {
  if (key === 'uiLang') {
    setUiLang(val);
  } else if (key === 'meaningLang') {
    state.meaningLang = val;
    localStorage.setItem('cr_meaningLang', val);
    showToast(t('meaningLang') + ': ' + val.toUpperCase());
  } else if (key === 'darkMode') {
    state.darkMode = val;
    localStorage.setItem('cr_darkMode', val);
    applyTheme();
  } else if (key === 'fontSize') {
    state.fontSize = parseInt(val, 10);
    localStorage.setItem('cr_fontSize', state.fontSize);
    document.getElementById('setting-font-val').textContent = state.fontSize + 'px';
    document.documentElement.style.setProperty('--reader-font-size', state.fontSize + 'px');
  }
}

// --- Module: Onboarding ---
let onboardingStep = 1;
function checkOnboarding() {
  const seen = localStorage.getItem('cr_onboarding_seen');
  if (!seen) {
    const overlay = document.getElementById('onboarding-overlay');
    if (overlay) overlay.classList.add('active');
    showOnboardingStep(1);
  }
}

function showOnboardingStep(step) {
  onboardingStep = step;
  document.querySelectorAll('.onboarding-slide').forEach(s => s.style.display = 'none');
  const slide = document.getElementById('onboarding-step-' + step);
  if (slide) slide.style.display = 'block';

  document.querySelectorAll('.onboarding-dot').forEach((dot, idx) => {
    dot.classList.toggle('active', idx + 1 === step);
  });
}

function nextOnboarding() {
  if (onboardingStep < 3) {
    showOnboardingStep(onboardingStep + 1);
  } else {
    finishOnboarding();
  }
}

function finishOnboarding() {
  localStorage.setItem('cr_onboarding_seen', 'true');
  const overlay = document.getElementById('onboarding-overlay');
  if (overlay) overlay.classList.remove('active');
}

// --- Module: Keyboard Shortcuts ---
function setupKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    // If active element is input or textarea, don't trigger global navigation keys
    const tag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
    const isTyping = tag === 'input' || tag === 'textarea';

    if (e.key === 'Escape') {
      closeWordSheet();
      closeFlashcardModal();
      closeOcrModal();
      return;
    }

    if (isTyping) return;

    if (e.key === '/') {
      e.preventDefault();
      switchView('dict');
      const searchInp = document.getElementById('dict-search-input');
      if (searchInp) searchInp.focus();
    } else if (e.key === 'ArrowLeft') {
      if (state.currentView === 'reader') prevSentence();
    } else if (e.key === 'ArrowRight') {
      if (state.currentView === 'reader') nextSentence();
    } else if (e.key.toLowerCase() === 'p') {
      togglePinyin();
    } else if (e.key.toLowerCase() === 'l') {
      cycleUiLang();
    }
  });
}

// --- Module: UI Updates & DOM Binding ---
function updateThemeAndUI() {
  applyTheme();
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = t(key);
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    el.placeholder = t(key);
  });

  const langPill = document.getElementById('top-lang-pill');
  if (langPill) langPill.textContent = state.uiLang.toUpperCase();
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeQuotes(str) {
  if (!str) return '';
  return String(str).replace(/'/g, "\\\\'").replace(/"/g, '&quot;');
}

// --- App Initialization ---
window.addEventListener('DOMContentLoaded', async () => {
  await initDB();
  applyTheme();
  updateThemeAndUI();
  setupKeyboardShortcuts();
  checkOnboarding();
  switchView('input');
});
"""

print("JS logic module defined successfully.")
