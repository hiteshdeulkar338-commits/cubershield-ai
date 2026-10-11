// Password Security & Strength Evaluator (100% Client-Side Evaluation)

const PasswordSecurityPage = {
    render() {
        const container = document.getElementById('pageContainer');
        if (!container) return;

        container.innerHTML = `
            <div class="password-checker-container">
                <div class="scanner-header">
                    <h2>Client-Side Password Security Meter</h2>
                    <p>Evaluate credential resilience, entropy, and dictionary vulnerability in your browser.</p>
                </div>

                <div class="card" style="border-left: 4px solid var(--accent-cyan);">
                    <div style="display:flex; align-items:center; gap:0.75rem;">
                        <i data-lucide="lock" style="color:var(--accent-cyan); width:24px;"></i>
                        <div>
                            <strong style="color:var(--text-primary); font-size:0.95rem;">Zero Knowledge Guarantee</strong>
                            <p style="margin:0; font-size:0.8rem; color:var(--text-muted);">
                                Your password NEVER leaves your device. All entropy calculations and checks occur entirely in client JavaScript.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="form-group">
                        <label class="form-label" for="passwordInput">Test Password</label>
                        <div class="password-input-wrap">
                            <input 
                                type="password" 
                                id="passwordInput" 
                                class="input-control" 
                                placeholder="Enter a password to test..." 
                                autocomplete="off"
                                spellcheck="false"
                            />
                            <button type="button" class="password-toggle-btn" id="passwordToggleBtn" aria-label="Toggle password visibility">
                                <i data-lucide="eye"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Strength Meter -->
                    <div style="margin-top: 1rem;">
                        <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:600;">
                            <span>Strength Rating</span>
                            <span id="strengthLabel" style="color: var(--text-muted);">Enter password</span>
                        </div>
                        <div class="strength-meter-bar">
                            <div class="strength-fill" id="strengthBarFill"></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:var(--text-muted); margin-top:0.25rem;">
                            <span>Estimated Brute Force Time:</span>
                            <span id="crackTimeEstimate" style="font-weight:600; color:var(--text-primary);">0 seconds</span>
                        </div>
                    </div>

                    <!-- Criteria Checklist -->
                    <div class="checklist-grid" id="criteriaChecklist">
                        <div class="checklist-item" id="crit-len8">
                            <i data-lucide="circle"></i>
                            <span>At least 8 characters</span>
                        </div>
                        <div class="checklist-item" id="crit-len12">
                            <i data-lucide="circle"></i>
                            <span>12+ characters (Recommended)</span>
                        </div>
                        <div class="checklist-item" id="crit-upper">
                            <i data-lucide="circle"></i>
                            <span>Uppercase letters (A-Z)</span>
                        </div>
                        <div class="checklist-item" id="crit-lower">
                            <i data-lucide="circle"></i>
                            <span>Lowercase letters (a-z)</span>
                        </div>
                        <div class="checklist-item" id="crit-num">
                            <i data-lucide="circle"></i>
                            <span>Numbers (0-9)</span>
                        </div>
                        <div class="checklist-item" id="crit-special">
                            <i data-lucide="circle"></i>
                            <span>Special symbols (!@#$%^&*)</span>
                        </div>
                        <div class="checklist-item" id="crit-patterns">
                            <i data-lucide="circle"></i>
                            <span>No common patterns (qwerty, 12345)</span>
                        </div>
                        <div class="checklist-item" id="crit-repeat">
                            <i data-lucide="circle"></i>
                            <span>No consecutive repeats (aaa, 111)</span>
                        </div>
                    </div>

                    <!-- Suggestions -->
                    <div id="suggestionsBox" style="margin-top: 1.5rem; display:none;">
                        <h4 style="font-size:0.9rem; margin-bottom:0.5rem; color:var(--accent-yellow); display:flex; align-items:center; gap:0.4rem;">
                            <i data-lucide="lightbulb" style="width:16px;"></i>
                            Recommendations to Strengthen
                        </h4>
                        <div id="suggestionsList" class="recommendation-list"></div>
                    </div>
                </div>

                <div class="card" style="background: rgba(255, 255, 255, 0.02);">
                    <h4 style="display:flex; align-items:center; gap:0.5rem; font-size:0.95rem; margin-bottom:0.5rem;">
                        <i data-lucide="shield-check" style="color:var(--accent-green); width:18px;"></i>
                        Password Manager Recommendation
                    </h4>
                    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">
                        Human memory is prone to patterns. We strongly recommend using open-source or audited password managers like <strong>Bitwarden</strong>, <strong>1Password</strong>, or <strong>KeePassXC</strong> combined with Multi-Factor Authentication (MFA).
                    </p>
                </div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();

        this.initEvents();
    },

    initEvents() {
        const input = document.getElementById('passwordInput');
        const toggleBtn = document.getElementById('passwordToggleBtn');

        if (toggleBtn && input) {
            toggleBtn.addEventListener('click', () => {
                const isPassword = input.getAttribute('type') === 'password';
                input.setAttribute('type', isPassword ? 'text' : 'password');
                toggleBtn.innerHTML = `<i data-lucide="${isPassword ? 'eye-off' : 'eye'}"></i>`;
                if (window.lucide) window.lucide.createIcons({ root: toggleBtn });
            });
        }

        if (input) {
            input.addEventListener('input', (e) => {
                this.evaluatePassword(e.target.value);
            });
        }
    },

    evaluatePassword(password) {
        const len = password.length;
        const hasUpper = /[A-Z]/.test(password);
        const hasLower = /[a-z]/.test(password);
        const hasNum = /[0-9]/.test(password);
        const hasSpecial = /[^A-Za-z0-9]/.test(password);

        // Pattern checking
        const commonSequences = ['password', '123456', 'qwerty', 'admin', 'welcome', 'letmein', '111111', 'abc123'];
        const lowerPass = password.toLowerCase();
        const hasCommonPattern = commonSequences.some(seq => lowerPass.includes(seq));
        const hasRepeats = /(.)\1{2,}/.test(password);

        // Criteria checklist updates
        this.updateCriteria('crit-len8', len >= 8);
        this.updateCriteria('crit-len12', len >= 12);
        this.updateCriteria('crit-upper', hasUpper);
        this.updateCriteria('crit-lower', hasLower);
        this.updateCriteria('crit-num', hasNum);
        this.updateCriteria('crit-special', hasSpecial);
        this.updateCriteria('crit-patterns', len > 0 && !hasCommonPattern);
        this.updateCriteria('crit-repeat', len > 0 && !hasRepeats);

        if (!password) {
            document.getElementById('strengthBarFill').style.width = '0%';
            document.getElementById('strengthLabel').textContent = 'Enter password';
            document.getElementById('strengthLabel').style.color = 'var(--text-muted)';
            document.getElementById('crackTimeEstimate').textContent = '0 seconds';
            document.getElementById('suggestionsBox').style.display = 'none';
            return;
        }

        // Calculate entropy
        let poolSize = 0;
        if (hasLower) poolSize += 26;
        if (hasUpper) poolSize += 26;
        if (hasNum) poolSize += 10;
        if (hasSpecial) poolSize += 32;

        const entropy = len * (poolSize > 0 ? Math.log2(poolSize) : 0);
        let score = 0;

        if (len >= 8) score += 20;
        if (len >= 12) score += 25;
        if (len >= 16) score += 15;
        if (hasUpper) score += 10;
        if (hasLower) score += 10;
        if (hasNum) score += 10;
        if (hasSpecial) score += 15;
        if (hasCommonPattern) score = Math.max(score - 40, 10);
        if (hasRepeats) score = Math.max(score - 20, 10);

        score = Math.min(Math.max(score, 5), 100);

        // Label and fill
        const bar = document.getElementById('strengthBarFill');
        const label = document.getElementById('strengthLabel');
        bar.style.width = `${score}%`;

        let labelText = 'Very Weak';
        let color = 'var(--risk-high)';

        if (score > 80) {
            labelText = 'Very Strong';
            color = 'var(--risk-safe)';
        } else if (score > 60) {
            labelText = 'Strong';
            color = 'var(--risk-low)';
        } else if (score > 40) {
            labelText = 'Moderate';
            color = 'var(--risk-medium)';
        }

        bar.style.backgroundColor = color;
        label.textContent = labelText;
        label.style.color = color;

        // Crack time calculation (10 billion guesses/sec assumed for modern offline rigs)
        const guesses = Math.pow(poolSize || 1, len);
        const seconds = guesses / 1e10;
        document.getElementById('crackTimeEstimate').textContent = this.formatTime(seconds);

        // Suggestions
        const suggestions = [];
        if (len < 12) suggestions.push('Increase length to 12 or more characters (passphrases work best).');
        if (!hasSpecial) suggestions.push('Include special symbols like #, $, %, or !.');
        if (!hasUpper || !hasLower) suggestions.push('Mix both UPPERCASE and lowercase letters.');
        if (hasCommonPattern) suggestions.push('Avoid obvious dictionary words or sequential characters.');

        const suggestionsBox = document.getElementById('suggestionsBox');
        const suggestionsList = document.getElementById('suggestionsList');

        if (suggestions.length > 0 && score < 85) {
            suggestionsBox.style.display = 'block';
            suggestionsList.innerHTML = suggestions.map(s => createRecommendationItem(s)).join('');
            if (window.lucide) window.lucide.createIcons({ root: suggestionsList });
        } else {
            suggestionsBox.style.display = 'none';
        }
    },

    updateCriteria(id, valid) {
        const el = document.getElementById(id);
        if (!el) return;
        if (valid) {
            el.classList.add('valid');
            el.querySelector('i, svg').outerHTML = '<i data-lucide="check-circle" style="color:var(--accent-green); width:16px;"></i>';
        } else {
            el.classList.remove('valid');
            el.querySelector('i, svg').outerHTML = '<i data-lucide="circle" style="color:var(--text-muted); width:16px;"></i>';
        }
        if (window.lucide) window.lucide.createIcons({ root: el });
    },

    formatTime(seconds) {
        if (seconds < 1) return 'Instant';
        if (seconds < 60) return `${Math.round(seconds)} seconds`;
        if (seconds < 3600) return `${Math.round(seconds / 60)} minutes`;
        if (seconds < 86400) return `${Math.round(seconds / 3600)} hours`;
        if (seconds < 31536000) return `${Math.round(seconds / 86400)} days`;
        if (seconds < 3153600000) return `${Math.round(seconds / 31536000)} years`;
        return 'Centuries+';
    }
};
