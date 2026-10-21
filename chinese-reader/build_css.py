# -*- coding: utf-8 -*-

CSS_CONTENT = """
:root {
  --accent: #E8344E;
  --accent-hover: #D02B43;
  --accent-subtle: rgba(232, 52, 78, 0.1);
  --accent-glow: rgba(232, 52, 78, 0.25);
  --accent-text: #FFFFFF;
  --success: #2EA043;
  --warning: #F59E0B;
  --info: #0969DA;
  
  --bg-base: #F8F9FA;
  --bg-surface: #FFFFFF;
  --bg-card: #FFFFFF;
  --bg-muted: #F1F3F5;
  --bg-input: #FFFFFF;
  --text-primary: #1F2328;
  --text-secondary: #57606A;
  --text-muted: #8C959F;
  --border-color: #E1E4E8;
  --border-light: #ECEFF2;
  --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  --sheet-shadow: 0 -8px 32px rgba(0, 0, 0, 0.12);
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-xl: 28px;
  
  --font-hanzi: "Noto Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  --font-kanji: "Noto Sans JP", "Yu Gothic", sans-serif;
  --font-ui: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  
  --reader-font-size: 28px;
  --top-bar-height: 56px;
  --bottom-bar-height: 64px;
}

[data-theme="dark"] {
  --bg-base: #0D1117;
  --bg-surface: #161B22;
  --bg-card: #1B2129;
  --bg-muted: #21262D;
  --bg-input: #12161C;
  --text-primary: #F0F6FC;
  --text-secondary: #8B949E;
  --text-muted: #6E7681;
  --border-color: #30363D;
  --border-light: #21262D;
  --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
  --sheet-shadow: 0 -8px 32px rgba(0, 0, 0, 0.55);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  -webkit-tap-highlight-color: transparent;
}

html, body {
  width: 100%;
  height: 100%;
  height: 100dvh;
  overflow: hidden;
  background-color: var(--bg-base);
  color: var(--text-primary);
  font-family: var(--font-ui);
  font-size: 15px;
  line-height: 1.5;
  user-select: none;
  -webkit-font-smoothing: antialiased;
}

button, input, textarea, select {
  font-family: inherit;
  color: inherit;
}

/* App Shell Layout */
#app-shell {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  height: 100dvh;
  max-width: 860px;
  margin: 0 auto;
  position: relative;
  background-color: var(--bg-base);
  border-left: 1px solid var(--border-light);
  border-right: 1px solid var(--border-light);
}

/* Top Bar */
#top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--top-bar-height);
  padding: 0 16px;
  padding-top: env(safe-area-inset-top, 0);
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  z-index: 100;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.brand-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #E8344E, #FF5A73);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-hanzi);
  font-weight: 700;
  font-size: 18px;
  box-shadow: 0 2px 8px var(--accent-glow);
}

.brand-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.3px;
  color: var(--text-primary);
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-btn {
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: var(--bg-surface);
}

.icon-btn:hover {
  background-color: var(--bg-muted);
  color: var(--text-primary);
}

.icon-btn:active {
  transform: scale(0.94);
}

.lang-pill-btn {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  background: var(--bg-muted);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s;
}

/* Main Content Area */
#main-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  -webkit-overflow-scrolling: touch;
  padding-bottom: calc(var(--bottom-bar-height) + env(safe-area-inset-bottom, 0) + 16px);
}

/* View Container */
.view {
  display: none;
  padding: 16px;
  animation: fadeIn 0.2s ease;
}

.view.active {
  display: block;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Cards & Panels */
.card {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 18px;
  box-shadow: var(--card-shadow);
  margin-bottom: 16px;
}

/* Primary Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 600;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  text-decoration: none;
}

.btn-primary {
  background-color: var(--accent);
  color: var(--accent-text);
  box-shadow: 0 3px 12px var(--accent-glow);
}

.btn-primary:hover {
  background-color: var(--accent-hover);
  box-shadow: 0 4px 16px var(--accent-glow);
}

.btn-secondary {
  background-color: var(--bg-muted);
  border-color: var(--border-color);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background-color: var(--border-color);
}

.btn-outline {
  background: transparent;
  border-color: var(--accent);
  color: var(--accent);
}

.btn-outline:hover {
  background-color: var(--accent-subtle);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 13px;
  border-radius: var(--radius-sm);
}

.btn:active {
  transform: scale(0.97);
}

/* View: Input */
.input-header {
  margin-bottom: 14px;
}
.input-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}
.input-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.textarea-box {
  width: 100%;
  height: 180px;
  padding: 14px;
  font-size: 18px;
  font-family: var(--font-hanzi);
  line-height: 1.6;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background-color: var(--bg-input);
  color: var(--text-primary);
  resize: vertical;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  user-select: text;
}

.textarea-box:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}

.action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.samples-container {
  margin-top: 20px;
}
.section-title {
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-secondary);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sample-chips {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 6px;
}

.sample-chip {
  padding: 8px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
  font-size: 13px;
  color: var(--text-primary);
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s;
}

.sample-chip:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-subtle);
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recent-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: border-color 0.2s;
}

.recent-item:hover {
  border-color: var(--accent);
}

.recent-text {
  font-family: var(--font-hanzi);
  font-size: 15px;
  max-width: 80%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.recent-meta {
  font-size: 12px;
  color: var(--text-muted);
}

/* View: Reader */
.reader-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 14px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  margin-bottom: 14px;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.toggle-btn {
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  background: var(--bg-muted);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.sentence-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px 20px;
  box-shadow: var(--card-shadow);
  margin-bottom: 16px;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

.sentence-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.sentence-index {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-muted);
}

.sentence-content {
  font-size: var(--reader-font-size);
  line-height: 2.2;
  font-family: var(--font-hanzi);
  word-break: break-word;
  user-select: text;
}

/* Word Token / Ruby Styling */
.word-token {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  vertical-align: bottom;
  margin: 0 3px;
  padding: 2px 4px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  position: relative;
}

.word-token:hover {
  background-color: var(--accent-subtle);
  transform: translateY(-2px);
}

.word-token:active {
  transform: scale(0.95);
}

.word-token.saved-star::after {
  content: "★";
  position: absolute;
  top: -4px;
  right: -2px;
  font-size: 10px;
  color: #F59E0B;
}

.token-pinyin {
  font-size: 0.45em;
  line-height: 1.1;
  font-weight: 600;
  color: var(--accent);
  user-select: none;
  letter-spacing: -0.2px;
}

.token-chars {
  font-size: 1em;
  line-height: 1.1;
  color: var(--text-primary);
}

.token-mini-meaning {
  font-size: 0.35em;
  line-height: 1;
  color: var(--text-muted);
  max-width: 60px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hide-pinyin .token-pinyin {
  display: none;
}

.hide-meaning .token-mini-meaning {
  display: none;
}

/* Sentence Translation Box */
.translation-box {
  margin-top: 16px;
  padding: 14px;
  border-radius: var(--radius-md);
  background-color: var(--bg-muted);
  border-left: 3px solid var(--accent);
  font-size: 14px;
  color: var(--text-primary);
  user-select: text;
  display: none;
}

.translation-box.show {
  display: block;
}

.sentence-nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 18px;
}

/* Full Text Mode */
.full-text-container {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  font-size: var(--reader-font-size);
  line-height: 2.3;
}

.sentence-paragraph {
  margin-bottom: 20px;
  padding: 6px;
  border-radius: var(--radius-sm);
  transition: background-color 0.2s;
}

.sentence-paragraph.active-sentence {
  background-color: var(--accent-subtle);
  border-left: 3px solid var(--accent);
}

/* View: Dictionary */
.search-bar-wrap {
  position: relative;
  margin-bottom: 14px;
}

.search-input {
  width: 100%;
  padding: 12px 14px 12px 42px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-surface);
  font-size: 15px;
  outline: none;
  transition: all 0.2s;
}

.search-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.filter-chips {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.filter-chip {
  padding: 5px 12px;
  border-radius: var(--radius-xl);
  font-size: 12px;
  font-weight: 600;
  border: 1px solid var(--border-color);
  background: var(--bg-surface);
  color: var(--text-secondary);
  cursor: pointer;
  white-space: nowrap;
}

.filter-chip.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.dict-results-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.dict-item-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.dict-item-card:hover {
  border-color: var(--accent);
  transform: translateX(2px);
}

.dict-item-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.dict-hanzi {
  font-family: var(--font-hanzi);
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.dict-pinyin {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent);
}

.dict-hanviet {
  font-size: 13px;
  color: var(--info);
  font-weight: 500;
}

.dict-meaning {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  background: var(--bg-muted);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.badge-hsk {
  background: rgba(232, 52, 78, 0.1);
  color: var(--accent);
  border-color: rgba(232, 52, 78, 0.25);
}

/* View: Saved Words */
.stats-banner {
  display: flex;
  justify-content: space-around;
  padding: 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  margin-bottom: 16px;
  text-align: center;
}

.stat-num {
  font-size: 22px;
  font-weight: 800;
  color: var(--accent);
}

.stat-label {
  font-size: 11px;
  text-transform: uppercase;
  color: var(--text-secondary);
  font-weight: 600;
  margin-top: 2px;
}

.saved-actions-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

/* View: Settings */
.settings-section {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: 16px;
}

.settings-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-light);
}

.settings-row:last-child {
  border-bottom: none;
}

.settings-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.settings-sublabel {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.settings-control select {
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  background: var(--bg-muted);
  outline: none;
}

/* Bottom Navigation */
#bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 860px;
  margin: 0 auto;
  height: calc(var(--bottom-bar-height) + env(safe-area-inset-bottom, 0));
  padding-bottom: env(safe-area-inset-bottom, 0);
  background-color: var(--bg-surface);
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 100;
  backdrop-filter: blur(12px);
}

.nav-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  flex: 1;
  height: 100%;
  border: none;
  background: none;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.nav-tab.active {
  color: var(--accent);
}

.nav-tab svg {
  width: 22px;
  height: 22px;
  stroke-width: 2;
  transition: transform 0.2s;
}

.nav-tab.active svg {
  transform: translateY(-2px);
}

.nav-tab span {
  font-size: 11px;
  font-weight: 600;
}

/* Bottom Sheet Modal */
.sheet-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  z-index: 998;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}

.sheet-backdrop.active {
  opacity: 1;
  pointer-events: auto;
}

.bottom-sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 640px;
  margin: 0 auto;
  background: var(--bg-surface);
  border-top-left-radius: 24px;
  border-top-right-radius: 24px;
  padding: 20px 24px;
  padding-bottom: calc(24px + env(safe-area-inset-bottom, 0));
  box-shadow: var(--sheet-shadow);
  z-index: 999;
  transform: translateY(100%);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 86vh;
  overflow-y: auto;
}

.bottom-sheet.active {
  transform: translateY(0);
}

.sheet-handle {
  width: 40px;
  height: 5px;
  background: var(--border-color);
  border-radius: 3px;
  margin: 0 auto 16px auto;
}

.sheet-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}

.sheet-hanzi-title {
  font-family: var(--font-hanzi);
  font-size: 40px;
  font-weight: 800;
  line-height: 1.1;
  color: var(--text-primary);
}

.sheet-pinyin {
  font-size: 18px;
  font-weight: 700;
  color: var(--accent);
  margin-top: 4px;
}

.sheet-hanviet {
  font-size: 15px;
  font-weight: 600;
  color: var(--info);
  margin-top: 2px;
}

.sheet-actions-top {
  display: flex;
  gap: 8px;
}

/* Hanzi Writer Container */
.hanzi-writer-container {
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
  margin: 16px 0;
  flex-wrap: wrap;
  min-height: 120px;
}

.writer-char-box {
  width: 130px;
  height: 130px;
  border: 1px dashed var(--border-color);
  border-radius: 12px;
  background: var(--bg-base);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.writer-controls {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 16px;
}

.sheet-definitions {
  margin-top: 14px;
}

.def-section {
  margin-bottom: 12px;
}

.def-label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.def-text {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.5;
}

.external-links {
  display: flex;
  gap: 8px;
  margin-top: 18px;
  flex-wrap: wrap;
}

/* Flashcard Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s;
}

.modal-overlay.active {
  opacity: 1;
  pointer-events: auto;
}

.modal-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  max-width: 480px;
  width: 100%;
  padding: 24px;
  box-shadow: var(--sheet-shadow);
  max-height: 90vh;
  overflow-y: auto;
}

.flashcard-3d-scene {
  perspective: 1000px;
  width: 100%;
  height: 260px;
  margin: 16px 0;
  cursor: pointer;
}

.flashcard-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  border-radius: var(--radius-md);
  box-shadow: var(--card-shadow);
}

.flashcard-inner.is-flipped {
  transform: rotateY(180deg);
}

.flashcard-front, .flashcard-back {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: var(--radius-md);
  border: 2px solid var(--border-color);
  background: var(--bg-card);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  text-align: center;
}

.flashcard-front {
  background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-muted) 100%);
}

.flashcard-back {
  transform: rotateY(180deg);
  background: var(--bg-surface);
}

.flashcard-hanzi {
  font-family: var(--font-hanzi);
  font-size: 58px;
  font-weight: 800;
  color: var(--text-primary);
}

.flashcard-hint {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 12px;
}

.flashcard-btn-row {
  display: flex;
  gap: 12px;
  width: 100%;
  margin-top: 12px;
}

/* Toast System */
#toast-container {
  position: fixed;
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 2000;
  pointer-events: none;
}

.toast {
  background: rgba(30, 32, 38, 0.92);
  color: white;
  padding: 8px 16px;
  border-radius: var(--radius-xl);
  font-size: 13px;
  font-weight: 600;
  box-shadow: 0 4px 14px rgba(0,0,0,0.2);
  backdrop-filter: blur(8px);
  animation: toastIn 0.25s ease, toastOut 0.25s ease 2.75s forwards;
}

@keyframes toastIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes toastOut {
  from { opacity: 1; }
  to { opacity: 0; transform: translateY(-8px); }
}

/* Desktop Responsiveness */
@media (min-width: 768px) {
  #app-shell {
    margin-top: 12px;
    margin-bottom: 12px;
    height: calc(100dvh - 24px);
    border-radius: var(--radius-lg);
    box-shadow: 0 8px 40px rgba(0,0,0,0.08);
    overflow: hidden;
  }
  
  #bottom-nav {
    position: static;
    border-top: none;
    border-bottom: 1px solid var(--border-color);
    order: -1;
    height: 48px;
    padding-bottom: 0;
  }
  
  .nav-tab {
    flex-direction: row;
    gap: 8px;
  }
  
  .nav-tab span {
    font-size: 13px;
  }
  
  #main-content {
    padding-bottom: 24px;
  }
}
"""

print("CSS module defined successfully.")
