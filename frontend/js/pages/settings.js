// Settings Page Implementation

const SettingsPage = {
    render() {
        const container = document.getElementById('pageContainer');
        if (!container) return;

        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const animationsEnabled = localStorage.getItem('cybershield_animations') !== 'disabled';

        container.innerHTML = `
            <div style="max-width: 800px; margin: 0 auto; display:flex; flex-direction:column; gap:1.5rem;">
                <div class="scanner-header">
                    <h2>Application Settings & Preferences</h2>
                    <p>Configure interface themes, privacy preferences, performance options, and system metadata.</p>
                </div>

                <!-- Appearance Section -->
                <div class="card">
                    <h3 class="card-title" style="margin-bottom:1rem;">
                        <i data-lucide="palette" style="color:var(--accent-cyan); width:20px;"></i>
                        Interface & Theme
                    </h3>
                    <div class="settings-section">
                        <div class="settings-row">
                            <div class="settings-info">
                                <span class="settings-title">Color Theme Mode</span>
                                <span class="settings-desc">Switch between Cyberpunk Dark and Clean Light visual themes</span>
                            </div>
                            <button type="button" class="btn btn-secondary btn-sm" id="themeSwitchBtn" onclick="SettingsPage.toggleTheme()">
                                <i data-lucide="${currentTheme === 'dark' ? 'sun' : 'moon'}"></i>
                                <span>${currentTheme === 'dark' ? 'Switch to Light' : 'Switch to Dark'}</span>
                            </button>
                        </div>

                        <div class="settings-row">
                            <div class="settings-info">
                                <span class="settings-title">Smooth UI Animations</span>
                                <span class="settings-desc">Enable subtle ambient transitions and counters</span>
                            </div>
                            <button type="button" class="btn btn-secondary btn-sm" id="animSwitchBtn" onclick="SettingsPage.toggleAnimations()">
                                <i data-lucide="${animationsEnabled ? 'check-circle' : 'circle'}"></i>
                                <span>${animationsEnabled ? 'Enabled' : 'Disabled'}</span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Privacy & Local Data -->
                <div class="card">
                    <h3 class="card-title" style="margin-bottom:1rem;">
                        <i data-lucide="shield" style="color:var(--accent-green); width:20px;"></i>
                        Privacy & Local Data Management
                    </h3>
                    <div class="settings-section">
                        <div class="settings-row">
                            <div class="settings-info">
                                <span class="settings-title">Client-Side Quarantine & Cache</span>
                                <span class="settings-desc">Clear local education quiz progress and browser preferences</span>
                            </div>
                            <button type="button" class="btn btn-secondary btn-sm" onclick="SettingsPage.clearLocalData()">
                                <i data-lucide="trash"></i>
                                <span>Reset Local Storage</span>
                            </button>
                        </div>

                        <div class="settings-row">
                            <div class="settings-info">
                                <span class="settings-title">Heuristic Telemetry</span>
                                <span class="settings-desc">Zero telemetry: All passwords and secrets remain exclusively on your device</span>
                            </div>
                            <span class="badge badge-safe">Enforced</span>
                        </div>
                    </div>
                </div>

                <!-- Language / Localization -->
                <div class="card">
                    <h3 class="card-title" style="margin-bottom:1rem;">
                        <i data-lucide="globe" style="color:var(--accent-purple); width:20px;"></i>
                        Language & Locale
                    </h3>
                    <div class="settings-section">
                        <div class="settings-row">
                            <div class="settings-info">
                                <span class="settings-title">System Language</span>
                                <span class="settings-desc">Choose application UI language</span>
                            </div>
                            <select class="select-control" style="width:160px; padding:0.4rem 0.75rem; font-size:0.85rem;" disabled>
                                <option value="en" selected>English (US)</option>
                                <option value="es">Español (Coming)</option>
                                <option value="hi">Hindi (Coming)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- About System -->
                <div class="card" style="background: rgba(255,255,255,0.02);">
                    <h3 class="card-title" style="margin-bottom:1rem;">
                        <i data-lucide="info" style="color:var(--accent-yellow); width:20px;"></i>
                        About CyberShield AI
                    </h3>
                    <div style="font-size:0.85rem; color:var(--text-secondary); line-height:1.7;">
                        <p><strong>Version:</strong> v2.4.0-Production (Enterprise Heuristic Engine)</p>
                        <p><strong>Architecture:</strong> Python Flask Backend + Modern SPA Vanilla Frontend</p>
                        <p><strong>Disclaimer:</strong> CyberShield AI provides multi-vector heuristic risk scoring and educational awareness. Heuristic scanning does not guarantee 100% threat detection. Always exercise proactive digital caution.</p>
                    </div>
                </div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();
    },

    toggleTheme() {
        const root = document.documentElement;
        const current = root.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        localStorage.setItem('cybershield_theme', next);

        const btn = document.getElementById('themeSwitchBtn');
        const themeNavIcon = document.getElementById('themeToggle');
        if (btn) {
            btn.innerHTML = `<i data-lucide="${next === 'dark' ? 'sun' : 'moon'}"></i><span>${next === 'dark' ? 'Switch to Light' : 'Switch to Dark'}</span>`;
        }
        if (themeNavIcon) {
            themeNavIcon.innerHTML = `<i data-lucide="${next === 'dark' ? 'moon' : 'sun'}"></i>`;
        }
        if (window.lucide) window.lucide.createIcons();
        showToast(`Theme switched to ${next} mode.`, 'info');
    },

    toggleAnimations() {
        const current = localStorage.getItem('cybershield_animations') !== 'disabled';
        const next = !current;
        localStorage.setItem('cybershield_animations', next ? 'enabled' : 'disabled');
        
        const btn = document.getElementById('animSwitchBtn');
        if (btn) {
            btn.innerHTML = `<i data-lucide="${next ? 'check-circle' : 'circle'}"></i><span>${next ? 'Enabled' : 'Disabled'}</span>`;
            if (window.lucide) window.lucide.createIcons({ root: btn });
        }
        showToast(`Animations ${next ? 'enabled' : 'disabled'}.`, 'info');
    },

    clearLocalData() {
        if (confirm('Clear local progress cache?')) {
            localStorage.removeItem('cybershield_completed_topics');
            showToast('Local browser storage cleared.', 'success');
        }
    }
};
