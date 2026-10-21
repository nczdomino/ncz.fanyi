# -*- coding: utf-8 -*-
import json
import os
import sys

# Import components
sys.path.append('/Users/thanhtrung/.gemini/antigravity/scratch/chinese-reader')
from build_dict_data import MINI_DICT, HAN_VIET, KANJI_DATA
from build_i18n import I18N_DATA
from build_css import CSS_CONTENT
from build_js import JS_LOGIC

OUTPUT_PATH = "/Users/thanhtrung/.gemini/antigravity/scratch/chinese-reader/index.html"

# SVG Icons
ICON_READ = '''<svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>'''
ICON_DICT = '''<svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>'''
ICON_SAVED = '''<svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>'''
ICON_SETTINGS = '''<svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><circle cx="12" cy="12" r="3" stroke-width="2"/></svg>'''

html_content = f'''<!DOCTYPE html>
<html lang="vi" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, maximum-scale=1.0, user-scalable=no">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="漢讀">
  <meta name="theme-color" content="#E8344E">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%23E8344E%22/><text y=%2268%22 x=%2250%22 font-family=%22sans-serif%22 font-weight=%22bold%22 font-size=%2260%22 text-anchor=%22middle%22 fill=%22white%22>漢</text></svg>">
  <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2220%22 fill=%22%23E8344E%22/><text y=%2268%22 x=%2250%22 font-family=%22sans-serif%22 font-weight=%22bold%22 font-size=%2260%22 text-anchor=%22middle%22 fill=%22white%22>漢</text></svg>">
  
  <title>漢讀 - Chinese Reader</title>

  <!-- Google Fonts: Noto Sans SC (Simplified Chinese) & Noto Sans JP (Japanese Kanji) & Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Sans+SC:wght@400;500;700;800&display=swap" rel="stylesheet">

  <!-- CDN Libraries -->
  <script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/pinyin-pro@3.24.2/dist/index.js"></script>

  <style>
{CSS_CONTENT}
  </style>

  <!-- Dynamic PWA Manifest Blob Injection -->
  <script>
    (function() {{
      try {{
        const manifest = {{
          name: "漢讀 - Chinese Reader",
          short_name: "漢讀",
          description: "Học và đọc tiếng Trung thông minh với phân tích từ vựng, phiên âm và thứ tự nét.",
          start_url: "./index.html",
          display: "standalone",
          background_color: "#F8F9FA",
          theme_color: "#E8344E",
          icons: [
            {{
              src: "data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 192 192%22><rect width=%22192%22 height=%22192%22 rx=%2240%22 fill=%22%23E8344E%22/><text y=%22130%22 x=%2296%22 font-family=%22sans-serif%22 font-weight=%22bold%22 font-size=%22115%22 text-anchor=%22middle%22 fill=%22white%22>漢</text></svg>",
              sizes: "192x192",
              type: "image/svg+xml"
            }}
          ]
        }};
        const blob = new Blob([JSON.stringify(manifest)], {{ type: 'application/json' }});
        const manifestUrl = URL.createObjectURL(blob);
        const link = document.createElement('link');
        link.rel = 'manifest';
        link.href = manifestUrl;
        document.head.appendChild(link);
      }} catch(e) {{
        console.warn("Manifest injection warning", e);
      }}
    }})();
  </script>
</head>
<body>

<div id="app-shell">
  <!-- Top Bar -->
  <header id="top-bar">
    <div class="brand-badge" onclick="switchView('input')">
      <div class="brand-icon">漢</div>
      <div class="brand-title" id="top-bar-title">漢讀</div>
    </div>
    <div class="top-actions">
      <button class="lang-pill-btn" id="top-lang-pill" onclick="cycleUiLang()" title="Đổi ngôn ngữ">VI</button>
      <button class="icon-btn" id="btn-toggle-theme" onclick="toggleTheme()" title="Đổi giao diện">
        <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
      </button>
    </div>
  </header>

  <!-- Main Views Container -->
  <main id="main-content">
    
    <!-- VIEW: Input -->
    <section id="view-input" class="view active">
      <div class="card">
        <div class="input-header">
          <div class="input-title" data-i18n="inputTitle">Nhập văn bản</div>
          <div class="input-subtitle" data-i18n="onboarding2Desc">Dán văn bản tiếng Trung hoặc chụp ảnh chứa chữ Hán. App sẽ nhận diện và phân tích cho bạn.</div>
        </div>
        
        <textarea id="input-textarea" class="textarea-box" data-i18n-ph="pasteText" placeholder="Dán văn bản tiếng Trung vào đây..."></textarea>
        
        <input type="file" id="ocr-file-input" accept="image/*" style="display:none;" onchange="handleImageUpload(this.files[0])">
        
        <div class="action-row">
          <button class="btn btn-primary" id="btn-analyze" onclick="analyzeText()">
            <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/></svg>
            <span data-i18n="btnAnalyze">Phân tích văn bản</span>
          </button>
          
          <button class="btn btn-secondary" onclick="pasteFromClipboard()">
            <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
            <span data-i18n="btnPaste">Dán từ clipboard</span>
          </button>
          
          <button class="btn btn-secondary" onclick="document.getElementById('ocr-file-input').click()">
            <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            <span data-i18n="btnCamera">Chụp / Chọn ảnh</span>
          </button>
        </div>
      </div>

      <!-- Sample Texts -->
      <div class="samples-container">
        <div class="section-title" data-i18n="sampleTexts">Văn bản mẫu</div>
        <div class="sample-chips">
          <div class="sample-chip" onclick="loadSample('daily')">💬 Giao tiếp hàng ngày (HSK 1-2)</div>
          <div class="sample-chip" onclick="loadSample('story')">📖 Mẩu chuyện ngắn (HSK 2-3)</div>
          <div class="sample-chip" onclick="loadSample('business')">💼 Thư từ công việc (HSK 3)</div>
        </div>
      </div>

      <!-- Recent Texts -->
      <div class="samples-container">
        <div class="section-title" data-i18n="recentTexts">Văn bản gần đây</div>
        <div id="recent-texts-list" class="recent-list"></div>
      </div>
    </section>

    <!-- VIEW: Reader -->
    <section id="view-reader" class="view">
      <div class="reader-toolbar">
        <div class="toolbar-group">
          <button class="btn btn-secondary btn-sm" onclick="switchView('input')">
            ← <span data-i18n="back">Quay lại</span>
          </button>
          <button id="btn-toggle-viewmode" class="toggle-btn" onclick="toggleViewMode()" data-i18n="viewSingle">
            Từng câu
          </button>
        </div>
        
        <div class="toolbar-group">
          <button id="btn-toggle-pinyin" class="toggle-btn active" onclick="togglePinyin()">
            <span data-i18n="pinyin">Phiên âm</span>
          </button>
          <button id="btn-toggle-meaning" class="toggle-btn" onclick="toggleMeaning()">
            <span data-i18n="meaning">Nghĩa</span>
          </button>
          <button class="icon-btn" onclick="changeFontSize(-2)" title="Giảm cỡ chữ">A-</button>
          <button class="icon-btn" onclick="changeFontSize(2)" title="Tăng cỡ chữ">A+</button>
        </div>
      </div>

      <div id="reader-content-area"></div>
    </section>

    <!-- VIEW: Dictionary -->
    <section id="view-dict" class="view">
      <div class="search-bar-wrap">
        <svg class="search-icon" width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input type="search" id="dict-search-input" class="search-input" data-i18n-ph="searchHint" placeholder="Nhập chữ Hán, pinyin, hoặc nghĩa..." oninput="handleDictSearch(this.value)">
      </div>

      <div class="filter-chips">
        <div class="filter-chip dict-filter-chip active" data-hsk="all" onclick="setDictFilter('all')" data-i18n="hskAll">Tất cả HSK</div>
        <div class="filter-chip dict-filter-chip" data-hsk="1" onclick="setDictFilter('1')">HSK 1</div>
        <div class="filter-chip dict-filter-chip" data-hsk="2" onclick="setDictFilter('2')">HSK 2</div>
        <div class="filter-chip dict-filter-chip" data-hsk="3" onclick="setDictFilter('3')">HSK 3</div>
      </div>

      <div id="dict-results-container"></div>
    </section>

    <!-- VIEW: Saved Words -->
    <section id="view-saved" class="view">
      <!-- Stats Banner -->
      <div class="stats-banner">
        <div>
          <div class="stat-num" id="stat-total-count">0</div>
          <div class="stat-label" data-i18n="totalSaved">Tổng số từ</div>
        </div>
        <div>
          <div class="stat-num" style="color:var(--success);" id="stat-knew-count">0</div>
          <div class="stat-label" data-i18n="knewCount">Đã nhớ</div>
        </div>
        <div>
          <div class="stat-num" style="color:var(--warning);" id="stat-unknown-count">0</div>
          <div class="stat-label" data-i18n="unknown">Chưa nhớ</div>
        </div>
      </div>

      <div class="saved-actions-row">
        <button class="btn btn-primary btn-sm" onclick="startFlashcardReview()">
          🗂️ <span data-i18n="flashcard">Ôn tập Flashcard</span>
        </button>
        <button class="btn btn-secondary btn-sm" onclick="exportSavedCSV()">
          📊 <span data-i18n="exportCSV">Xuất CSV</span>
        </button>
        <button class="btn btn-secondary btn-sm" onclick="exportSavedJSON()">
          💾 <span data-i18n="exportJSON">Xuất JSON</span>
        </button>
      </div>

      <div class="filter-chips">
        <div class="filter-chip active" onclick="setSavedFilterHSK('all')" data-i18n="hskAll">Tất cả HSK</div>
        <div class="filter-chip" onclick="setSavedFilterHSK('1')">HSK 1</div>
        <div class="filter-chip" onclick="setSavedFilterHSK('2')">HSK 2</div>
        <div class="filter-chip" onclick="setSavedFilterHSK('3')">HSK 3</div>
        <div class="filter-chip" onclick="setSavedFilterStatus('remembered')" data-i18n="remember">Đã nhớ</div>
        <div class="filter-chip" onclick="setSavedFilterStatus('unknown')" data-i18n="notRemember">Chưa nhớ</div>
      </div>

      <div id="saved-words-container"></div>
    </section>

    <!-- VIEW: Settings -->
    <section id="view-settings" class="view">
      <div class="settings-section">
        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="language">Ngôn ngữ giao diện</div>
            <div class="settings-sublabel">Chọn ngôn ngữ hiển thị hệ thống</div>
          </div>
          <div class="settings-control">
            <select id="setting-ui-lang" onchange="handleSettingChange('uiLang', this.value)">
              <option value="vi">Tiếng Việt</option>
              <option value="en">English</option>
              <option value="ja">日本語</option>
            </select>
          </div>
        </div>

        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="meaningLang">Ngôn ngữ nghĩa</div>
            <div class="settings-sublabel">Hiển thị giải nghĩa từ và dịch câu</div>
          </div>
          <div class="settings-control">
            <select id="setting-meaning-lang" onchange="handleSettingChange('meaningLang', this.value)">
              <option value="vi">Tiếng Việt</option>
              <option value="en">English</option>
            </select>
          </div>
        </div>

        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="darkMode">Chế độ tối</div>
            <div class="settings-sublabel">Tự động theo hệ thống hoặc cố định</div>
          </div>
          <div class="settings-control">
            <select id="setting-dark-mode" onchange="handleSettingChange('darkMode', this.value)">
              <option value="system">Hệ thống</option>
              <option value="light">Sáng</option>
              <option value="dark">Tối</option>
            </select>
          </div>
        </div>

        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="fontSize">Cỡ chữ văn bản</div>
            <div class="settings-sublabel" id="setting-font-val">28px</div>
          </div>
          <div class="settings-control">
            <input type="range" id="setting-font-size" min="18" max="44" step="2" value="28" oninput="handleSettingChange('fontSize', this.value)">
          </div>
        </div>
      </div>

      <div class="settings-section">
        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="dictOffline">Từ điển offline</div>
            <div class="settings-sublabel">Bộ từ điển tích hợp sẵn 570 từ HSK 1-3 & 690+ âm Hán Việt</div>
          </div>
          <span class="badge" style="background:#2EA043; color:white;">Sẵn sàng</span>
        </div>

        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="testVoice">Kiểm tra giọng phát âm</div>
            <div class="settings-sublabel">Kiểm tra bộ giọng đọc tiếng Trung (Web Speech API)</div>
          </div>
          <button class="btn btn-secondary btn-sm" onclick="testSpeechVoices()">
            🔊 Kiểm tra
          </button>
        </div>

        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="backup">Sao lưu & Khôi phục</div>
            <div class="settings-sublabel">Xuất hoặc nhập toàn bộ từ đã lưu và cài đặt</div>
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn btn-secondary btn-sm" onclick="backupAllData()">
              <span data-i18n="backup">Sao lưu</span>
            </button>
            <input type="file" id="restore-file-input" accept=".json" style="display:none;" onchange="restoreDataFromFile(this.files[0])">
            <button class="btn btn-secondary btn-sm" onclick="document.getElementById('restore-file-input').click()">
              <span data-i18n="restore">Khôi phục</span>
            </button>
          </div>
        </div>

        <div class="settings-row">
          <div>
            <div class="settings-label" style="color:var(--accent);" data-i18n="clearAllData">Xóa toàn bộ dữ liệu</div>
            <div class="settings-sublabel">Xóa tất cả từ đã lưu và văn bản gần đây</div>
          </div>
          <button class="btn btn-outline btn-sm" style="color:var(--accent); border-color:var(--accent);" onclick="clearAllAppData()">
            <span data-i18n="delete">Xóa</span>
          </button>
        </div>
      </div>
    </section>

  </main>

  <!-- Bottom Navigation -->
  <nav id="bottom-nav">
    <button class="nav-tab active" data-view="input" onclick="switchView('input')">
      {ICON_READ}
      <span data-i18n="tabRead">Đọc</span>
    </button>
    <button class="nav-tab" data-view="dict" onclick="switchView('dict')">
      {ICON_DICT}
      <span data-i18n="tabDict">Từ điển</span>
    </button>
    <button class="nav-tab" data-view="saved" onclick="switchView('saved')">
      {ICON_SAVED}
      <span data-i18n="tabSaved">Đã lưu</span>
    </button>
    <button class="nav-tab" data-view="settings" onclick="switchView('settings')">
      {ICON_SETTINGS}
      <span data-i18n="tabSettings">Cài đặt</span>
    </button>
  </nav>
</div>

<!-- Bottom Sheet Popup (Word Inspector) -->
<div id="sheet-backdrop" class="sheet-backdrop" onclick="closeWordSheet()"></div>
<div id="word-sheet" class="bottom-sheet">
  <div class="sheet-handle"></div>
  
  <div class="sheet-header">
    <div>
      <div id="sheet-hanzi-title" class="sheet-hanzi-title">你好</div>
      <div id="sheet-pinyin" class="sheet-pinyin">nǐ hǎo</div>
      <div id="sheet-hanviet" class="sheet-hanviet">Nhĩ Hảo</div>
    </div>
    <div class="sheet-actions-top">
      <button class="icon-btn" onclick="speakText(state.activeWord)" title="Phát âm">
        <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
      </button>
      <button id="sheet-btn-save" class="icon-btn" onclick="toggleSaveActiveWord()" title="Lưu từ">
        <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>
      </button>
      <button class="icon-btn" onclick="closeWordSheet()" title="Đóng">✕</button>
    </div>
  </div>

  <div id="sheet-badges" style="display:flex; gap:6px; margin-bottom:12px;"></div>

  <!-- Hanzi Writer stroke order canvas container -->
  <div id="hanzi-writer-box" class="hanzi-writer-container"></div>
  
  <div class="writer-controls">
    <button class="btn btn-secondary btn-sm" onclick="animateActiveWriters()">
      ▶ <span data-i18n="animateStrokes">Phát nét</span>
    </button>
    <button class="btn btn-secondary btn-sm" onclick="quizActiveWriters()">
      ✏️ <span data-i18n="quizMode">Tập viết</span>
    </button>
    <button class="btn btn-outline btn-sm" onclick="splitActiveWord()">
      🔤 <span data-i18n="splitWord">Tách thành chữ đơn</span>
    </button>
  </div>

  <div class="sheet-definitions">
    <div class="def-section">
      <div class="def-label">Tiếng Việt</div>
      <div id="sheet-def-vi" class="def-text"></div>
    </div>
    
    <div class="def-section">
      <div class="def-label">English</div>
      <div id="sheet-def-en" class="def-text"></div>
    </div>

    <div class="def-section" style="display:none;">
      <div class="def-label">日本語 (Kanji)</div>
      <div id="sheet-def-ja" class="def-text"></div>
    </div>
  </div>

  <div class="def-label" style="margin-top:16px;" data-i18n="openExternal">Mở từ điển ngoài</div>
  <div id="sheet-external-links" class="external-links"></div>
</div>

<!-- Flashcard Modal -->
<div id="flashcard-modal" class="modal-overlay">
  <div class="modal-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
      <div style="font-size:16px; font-weight:700;" data-i18n="flashcard">Ôn tập Flashcard</div>
      <div style="display:flex; align-items:center; gap:12px;">
        <span id="flashcard-progress" style="font-size:13px; font-weight:600; color:var(--text-muted);">1 / 10</span>
        <button class="icon-btn" onclick="closeFlashcardModal()">✕</button>
      </div>
    </div>
    
    <div id="flashcard-scene-container"></div>
    
    <div id="flashcard-controls-row" class="flashcard-btn-row">
      <button class="btn btn-secondary" style="flex:1;" onclick="answerFlashcard(false)">
        ❌ <span data-i18n="notRemember">Chưa nhớ</span>
      </button>
      <button class="btn btn-primary" style="flex:1;" onclick="answerFlashcard(true)">
        ✅ <span data-i18n="remember">Đã nhớ</span>
      </button>
    </div>
  </div>
</div>

<!-- OCR Modal -->
<div id="ocr-modal" class="modal-overlay">
  <div class="modal-card">
    <div style="font-size:18px; font-weight:700; margin-bottom:12px;" data-i18n="ocrEdit">Chỉnh sửa văn bản nhận diện</div>
    
    <div id="ocr-progress-container" style="display:none; margin-bottom:14px;">
      <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;" id="ocr-progress-text">Đang nhận diện chữ...</div>
      <div style="width:100%; height:8px; background:var(--bg-muted); border-radius:4px; overflow:hidden;">
        <div id="ocr-progress-bar" style="width:0%; height:100%; background:var(--accent); transition:width 0.2s;"></div>
      </div>
    </div>
    
    <textarea id="ocr-edit-textarea" class="textarea-box" style="height:160px; font-size:16px;" placeholder="Văn bản nhận diện sẽ hiển thị ở đây..."></textarea>
    
    <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:16px;">
      <button class="btn btn-secondary" onclick="closeOcrModal()">
        <span data-i18n="cancel">Hủy</span>
      </button>
      <button class="btn btn-primary" onclick="confirmOcrResult()">
        <span data-i18n="ocrConfirm">Xác nhận và đọc</span>
      </button>
    </div>
  </div>
</div>

<!-- Onboarding Modal -->
<div id="onboarding-overlay" class="modal-overlay">
  <div class="modal-card" style="text-align:center;">
    <div id="onboarding-step-1" class="onboarding-slide">
      <div style="font-size:42px; margin-bottom:10px;">👋</div>
      <h2 style="font-size:22px; font-weight:800; margin-bottom:8px;" data-i18n="onboarding1Title">Chào mừng đến 漢讀</h2>
      <p style="color:var(--text-secondary); font-size:14px; margin-bottom:20px;" data-i18n="onboarding1Desc">Ứng dụng đọc và học tiếng Trung. Đầu tiên, hãy chọn ngôn ngữ của bạn:</p>
      <div style="display:flex; flex-direction:column; gap:10px; max-width:240px; margin:0 auto 20px auto;">
        <button class="btn btn-secondary" onclick="setUiLang('vi'); nextOnboarding();">🇻🇳 Tiếng Việt</button>
        <button class="btn btn-secondary" onclick="setUiLang('en'); nextOnboarding();">🇺🇸 English</button>
        <button class="btn btn-secondary" onclick="setUiLang('ja'); nextOnboarding();">🇯🇵 日本語</button>
      </div>
    </div>

    <div id="onboarding-step-2" class="onboarding-slide" style="display:none;">
      <div style="font-size:42px; margin-bottom:10px;">📸</div>
      <h2 style="font-size:22px; font-weight:800; margin-bottom:8px;" data-i18n="onboarding2Title">Dán hoặc chụp ảnh</h2>
      <p style="color:var(--text-secondary); font-size:14px; margin-bottom:24px;" data-i18n="onboarding2Desc">Dán văn bản tiếng Trung hoặc chụp ảnh chứa chữ Hán. App sẽ nhận diện và phân tích cho bạn.</p>
      <button class="btn btn-primary" onclick="nextOnboarding()" data-i18n="next">Tiếp tục</button>
    </div>

    <div id="onboarding-step-3" class="onboarding-slide" style="display:none;">
      <div style="font-size:42px; margin-bottom:10px;">⭐</div>
      <h2 style="font-size:22px; font-weight:800; margin-bottom:8px;" data-i18n="onboarding3Title">Chạm để tra nghĩa</h2>
      <p style="color:var(--text-secondary); font-size:14px; margin-bottom:24px;" data-i18n="onboarding3Desc">Chạm vào bất kỳ từ nào để xem pinyin, nghĩa, và phát âm. Lưu từ bằng nút ⭐</p>
      <button class="btn btn-primary" onclick="finishOnboarding()" data-i18n="getStarted">Bắt đầu</button>
    </div>

    <div style="display:flex; justify-content:center; gap:6px; margin-top:16px;">
      <div class="onboarding-dot active" style="width:8px; height:8px; border-radius:4px; background:var(--accent);"></div>
      <div class="onboarding-dot" style="width:8px; height:8px; border-radius:4px; background:var(--border-color);"></div>
      <div class="onboarding-dot" style="width:8px; height:8px; border-radius:4px; background:var(--border-color);"></div>
    </div>
  </div>
</div>

<!-- Toast Container -->
<div id="toast-container"></div>

<!-- Embedded Datasets & App Engine -->
<script>
// --- Embedded i18n Data ---
const I18N_DATA = {json.dumps(I18N_DATA, ensure_ascii=False, indent=2)};

// --- Embedded Mini Dictionary (570 words covering HSK 1-3) ---
const MINI_DICT = {json.dumps(MINI_DICT, ensure_ascii=False, indent=2)};

// --- Embedded Han Viet Table (691 characters) ---
const HAN_VIET = {json.dumps(HAN_VIET, ensure_ascii=False, indent=2)};

// --- Embedded Kanji Data (230 characters) ---
const KANJI_DATA = {json.dumps(KANJI_DATA, ensure_ascii=False, indent=2)};

{JS_LOGIC}
</script>

</body>
</html>
'''

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"File successfully created at: {OUTPUT_PATH}")
line_count = len(html_content.splitlines())
byte_size = len(html_content.encode('utf-8'))
print(f"Total lines: {line_count}")
print(f"File size: {byte_size / 1024:.2f} KB")
