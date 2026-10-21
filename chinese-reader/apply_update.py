# -*- coding: utf-8 -*-
"""
Script to apply HSK 4-6 dictionary expansion and 3-Tier TTS engine upgrade
to /Users/thanhtrung/.gemini/antigravity/scratch/chinese-reader/index.html
"""

import sys
import os
import json
import shutil

scratch_dir = '/Users/thanhtrung/.gemini/antigravity/scratch/chinese-reader'
sys.path.insert(0, scratch_dir)

from hsk4_data import HSK4
from hsk5_data import HSK5
from hsk6_data import HSK6

html_path = os.path.join(scratch_dir, 'index.html')
backup_path = os.path.join(scratch_dir, 'index.html.bak')

# 1. Clean duplicates across sets
d4 = dict(HSK4)
d5 = dict(HSK5)
d6 = dict(HSK6)

# Specific overlaps resolved to most appropriate HSK level
del d4['概念']  # In prompt under HSK 6
del d5['道德']  # In prompt under HSK 6
del d5['策略']  # In prompt under HSK 6
del d5['诚恳']  # In prompt under HSK 6
del d5['独特']  # In prompt under HSK 6
del d6['文明']  # In prompt under HSK 4 & 6 -> assigned to HSK 4
del d6['格外']  # Assigned to HSK 4
del d6['大厦']  # Assigned to HSK 5

print(f"HSK 4 entries: {len(d4)}")
print(f"HSK 5 entries: {len(d5)}")
print(f"HSK 6 entries: {len(d6)}")
total_added = len(d4) + len(d5) + len(d6)
print(f"Total HSK 4-6 entries to add: {total_added}")

# 2. Format entries
def format_entry(word, data):
    pinyin_str = json.dumps(data["pinyin"], ensure_ascii=False)
    en_str = json.dumps(data["en"], ensure_ascii=False)
    vi_str = json.dumps(data["vi"], ensure_ascii=False)
    hanviet_str = json.dumps(data["hanviet"], ensure_ascii=False)
    type_str = json.dumps(data["type"], ensure_ascii=False)
    hsk_val = data["hsk"]
    return f'  "{word}": {{ "pinyin": {pinyin_str}, "en": {en_str}, "vi": {vi_str}, "hanviet": {hanviet_str}, "type": {type_str}, "hsk": {hsk_val} }},'

hsk_lines = []
hsk_lines.append("\n  // --- HSK 4 Expanded Dictionary (329 words) ---")
for w, d in d4.items():
    hsk_lines.append(format_entry(w, d))

hsk_lines.append("\n  // --- HSK 5 Expanded Dictionary (293 words) ---")
for w, d in d5.items():
    hsk_lines.append(format_entry(w, d))

hsk_lines.append("\n  // --- HSK 6 Expanded Dictionary (282 words) ---")
for w, d in d6.items():
    hsk_lines.append(format_entry(w, d))

new_dict_entries = "\n".join(hsk_lines)

# Read original file
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
shutil.copyfile(html_path, backup_path)
print(f"Backed up original index.html to {backup_path}")

# Anchor 1: End of MINI_DICT
target_dict_end = '    "hsk": 3\n  }\n};\n\n// --- Embedded Han Viet Table (691 characters) ---'
replacement_dict_end = f'    "hsk": 3\n  }},\n{new_dict_entries}\n}};\n\n// --- Embedded Han Viet Table (691 characters) ---'

assert target_dict_end in content, "Anchor 1 (target_dict_end) not found!"
content = content.replace(target_dict_end, replacement_dict_end, 1)
print("Anchor 1 (MINI_DICT expansion) successfully applied.")

# Anchor 2: I18N additions
target_i18n_vi = '    "sampleTexts": "Văn bản mẫu",'
replacement_i18n_vi = '    "sampleTexts": "Văn bản mẫu",\n    "ttsEngine": "Công cụ phát âm (TTS)",'
assert target_i18n_vi in content, "Anchor 2a (i18n vi) not found!"
content = content.replace(target_i18n_vi, replacement_i18n_vi, 1)

target_i18n_en = '    "sampleTexts": "Sample texts",'
replacement_i18n_en = '    "sampleTexts": "Sample texts",\n    "ttsEngine": "TTS Engine",'
assert target_i18n_en in content, "Anchor 2b (i18n en) not found!"
content = content.replace(target_i18n_en, replacement_i18n_en, 1)

target_i18n_ja = '    "sampleTexts": "サンプル例文",'
replacement_i18n_ja = '    "sampleTexts": "サンプル例文",\n    "ttsEngine": "音声合成 (TTS)",'
assert target_i18n_ja in content, "Anchor 2c (i18n ja) not found!"
content = content.replace(target_i18n_ja, replacement_i18n_ja, 1)
print("Anchor 2 (i18n additions) successfully applied.")

# Anchor 3: Filter chips in #view-dict
target_dict_chips = '        <div class="filter-chip dict-filter-chip" data-hsk="3" onclick="setDictFilter(\'3\')">HSK 3</div>'
replacement_dict_chips = '''        <div class="filter-chip dict-filter-chip" data-hsk="3" onclick="setDictFilter('3')">HSK 3</div>
        <div class="filter-chip dict-filter-chip" data-hsk="4" onclick="setDictFilter('4')">HSK 4</div>
        <div class="filter-chip dict-filter-chip" data-hsk="5" onclick="setDictFilter('5')">HSK 5</div>
        <div class="filter-chip dict-filter-chip" data-hsk="6" onclick="setDictFilter('6')">HSK 6</div>'''
assert target_dict_chips in content, "Anchor 3 (dict filter chips) not found!"
content = content.replace(target_dict_chips, replacement_dict_chips, 1)
print("Anchor 3 (dict filter chips) successfully applied.")

# Anchor 4: Filter chips in #view-saved
target_saved_chips = '        <div class="filter-chip" onclick="setSavedFilterHSK(\'3\')">HSK 3</div>'
replacement_saved_chips = '''        <div class="filter-chip" onclick="setSavedFilterHSK('3')">HSK 3</div>
        <div class="filter-chip" onclick="setSavedFilterHSK('4')">HSK 4</div>
        <div class="filter-chip" onclick="setSavedFilterHSK('5')">HSK 5</div>
        <div class="filter-chip" onclick="setSavedFilterHSK('6')">HSK 6</div>'''
assert target_saved_chips in content, "Anchor 4 (saved filter chips) not found!"
content = content.replace(target_saved_chips, replacement_saved_chips, 1)
print("Anchor 4 (saved filter chips) successfully applied.")

# Anchor 5: Settings HTML (TTS engine selector + dictionary sublabel)
target_settings_dict_label = '<div class="settings-sublabel">Bộ từ điển tích hợp sẵn 570 từ HSK 1-3 & 690+ âm Hán Việt</div>'
replacement_settings_dict_label = '<div class="settings-sublabel">Bộ từ điển tích hợp sẵn 1470+ từ HSK 1-6 & 690+ âm Hán Việt</div>'
assert target_settings_dict_label in content, "Anchor 5a (settings dict label) not found!"
content = content.replace(target_settings_dict_label, replacement_settings_dict_label, 1)

target_settings_voice = '''        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="testVoice">Kiểm tra giọng phát âm</div>'''

replacement_settings_voice = '''        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="ttsEngine">Công cụ phát âm (TTS)</div>
            <div class="settings-sublabel">Chọn nguồn phát âm giọng đọc tiếng Trung</div>
          </div>
          <div class="settings-control">
            <select id="tts-engine-select" onchange="state.ttsEngine=this.value; saveSettings()">
              <option value="google">Google Translate TTS (Chuẩn nhất)</option>
              <option value="dictcn">Dict.cn Audio (Dự phòng)</option>
              <option value="system">Web Speech API (Hệ thống)</option>
            </select>
          </div>
        </div>

        <div class="settings-row">
          <div>
            <div class="settings-label" data-i18n="testVoice">Kiểm tra giọng phát âm</div>'''

assert target_settings_voice in content, "Anchor 5b (settings voice row) not found!"
content = content.replace(target_settings_voice, replacement_settings_voice, 1)
print("Anchor 5 (Settings HTML) successfully applied.")

# Anchor 6: state object (ttsEngine property)
target_state = "  showMeaning: localStorage.getItem('cr_showMeaning') === 'true',\n  currentText: '',"
replacement_state = "  showMeaning: localStorage.getItem('cr_showMeaning') === 'true',\n  ttsEngine: localStorage.getItem('cr_ttsEngine') || 'google',\n  currentText: '',"
assert target_state in content, "Anchor 6 (state object) not found!"
content = content.replace(target_state, replacement_state, 1)
print("Anchor 6 (state ttsEngine) successfully applied.")

# Anchor 7: speakText replacement (3-Tier TTS Engine)
target_tts_module = '''// --- Module: Audio TTS ---
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
}'''

replacement_tts_module = '''// --- Module: Audio TTS (3-Tier Engine) ---
let currentAudio = null;

function speakViaWebSpeech(text) {
  try {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'zh-CN';
      utterance.rate = 0.85;
      const voices = window.speechSynthesis.getVoices();
      const zhVoice = voices.find(v => v.lang.startsWith('zh') || v.lang.includes('cmn'));
      if (zhVoice) utterance.voice = zhVoice;
      window.speechSynthesis.speak(utterance);
    }
  } catch (err) {
    console.error('All TTS failed', err);
  }
}

async function speakText(text) {
  if (!text) return;
  if (currentAudio) {
    try {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio.src = '';
    } catch (e) {}
    currentAudio = null;
  }
  if ('speechSynthesis' in window) {
    try {
      window.speechSynthesis.cancel();
    } catch (e) {}
  }

  // If user selected system, directly use Web Speech API
  if (state.ttsEngine === 'system') {
    speakViaWebSpeech(text);
    return;
  }

  // Tier 1: Google Translate TTS (Primary online engine)
  if (state.ttsEngine !== 'dictcn') {
    try {
      const url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=zh-CN&client=tw-ob&q=' + encodeURIComponent(text.slice(0, 200));
      const audio = new Audio(url);
      currentAudio = audio;
      await audio.play();
      return;
    } catch (e1) {
      console.warn('Google TTS failed, trying fallback', e1);
    }
  }

  // Tier 2: Dict.cn TTS fallback
  try {
    const url = 'https://audio.dict.cn/speak.mp3?v=3&s=' + encodeURIComponent(text.slice(0, 100));
    const audio = new Audio(url);
    currentAudio = audio;
    await audio.play();
    return;
  } catch (e2) {
    console.warn('Dict.cn TTS failed, trying Web Speech fallback', e2);
  }

  // Tier 3: Web Speech API fallback
  speakViaWebSpeech(text);
}'''

assert target_tts_module in content, "Anchor 7 (speakText module) not found!"
content = content.replace(target_tts_module, replacement_tts_module, 1)
print("Anchor 7 (speakText replacement) successfully applied.")

# Anchor 8: Settings JS (renderSettingsView + saveSettings + handleSettingChange)
target_render_settings = '''  const fontValText = document.getElementById('setting-font-val');
  if (fontSlider) fontSlider.value = state.fontSize;
  if (fontValText) fontValText.textContent = state.fontSize + 'px';
}'''

replacement_render_settings = '''  const fontValText = document.getElementById('setting-font-val');
  if (fontSlider) fontSlider.value = state.fontSize;
  if (fontValText) fontValText.textContent = state.fontSize + 'px';

  const ttsSelect = document.getElementById('tts-engine-select');
  if (ttsSelect) ttsSelect.value = state.ttsEngine || 'google';
}

function saveSettings() {
  if (state.ttsEngine) {
    localStorage.setItem('cr_ttsEngine', state.ttsEngine);
  }
}'''

assert target_render_settings in content, "Anchor 8a (renderSettingsView) not found!"
content = content.replace(target_render_settings, replacement_render_settings, 1)

target_handle_setting = '''    document.documentElement.style.setProperty('--reader-font-size', state.fontSize + 'px');
  }
}'''

replacement_handle_setting = '''    document.documentElement.style.setProperty('--reader-font-size', state.fontSize + 'px');
  } else if (key === 'ttsEngine') {
    state.ttsEngine = val;
    saveSettings();
  }
}'''

assert target_handle_setting in content, "Anchor 8b (handleSettingChange) not found!"
content = content.replace(target_handle_setting, replacement_handle_setting, 1)
print("Anchor 8 (Settings JS) successfully applied.")

# Save modified content
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully updated {html_path}!")
