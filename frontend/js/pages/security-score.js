// Security Score Assessment Questionnaire & Hygiene Calculation

const SecurityScorePage = {
    questions: [
        { id: 'q1', text: 'Do you use Multi-Factor Authentication (MFA/2FA) on all critical accounts?', weight: 15 },
        { id: 'q2', text: 'Do you avoid reusing passwords across multiple online websites?', weight: 15 },
        { id: 'q3', text: 'Are your operating system, browser, and security patches automatically updated?', weight: 10 },
        { id: 'q4', text: 'Do you store your credentials inside a dedicated Password Manager?', weight: 10 },
        { id: 'q5', text: 'Do you verify domain links and sender addresses before clicking or opening attachments?', weight: 10 },
        { id: 'q6', text: 'Do you maintain regular encrypted backups of essential personal and work files?', weight: 10 },
        { id: 'q7', text: 'Is your home Wi-Fi secured with WPA2/WPA3 and a custom non-default password?', weight: 10 },
        { id: 'q8', text: 'Do you regularly review app permissions on your mobile devices?', weight: 5 },
        { id: 'q9', text: 'Do you avoid logging into sensitive banking portals on unsecured public Wi-Fi without a VPN?', weight: 10 },
        { id: 'q10', text: 'Do you check for HTTPS encryption (padlock) before entering payment details?', weight: 5 }
    ],

    answers: {},

    render() {
        const container = document.getElementById('pageContainer');
        if (!container) return;

        this.answers = {};

        container.innerHTML = `
            <div class="quiz-container">
                <div class="scanner-header">
                    <h2>Personal Cybersecurity Posture Assessment</h2>
                    <p>Answer 10 foundational cybersecurity questions to calculate your defensive score and customized protection plan.</p>
                </div>

                <div id="scoreFormContainer">
                    <form id="securityScoreForm">
                        <div style="display:flex; flex-direction:column; gap:1rem;">
                            ${this.questions.map((q, idx) => `
                                <div class="question-card" id="card-${q.id}">
                                    <div class="question-title">
                                        <span class="question-num">#${idx + 1}</span>
                                        <span>${q.text}</span>
                                    </div>
                                    <div class="option-group">
                                        <button type="button" class="option-btn" data-qid="${q.id}" data-val="yes" onclick="SecurityScorePage.selectOption('${q.id}', 'yes', this)">
                                            Yes, Always
                                        </button>
                                        <button type="button" class="option-btn" data-qid="${q.id}" data-val="sometimes" onclick="SecurityScorePage.selectOption('${q.id}', 'sometimes', this)">
                                            Sometimes / Unsure
                                        </button>
                                        <button type="button" class="option-btn" data-qid="${q.id}" data-val="no" onclick="SecurityScorePage.selectOption('${q.id}', 'no', this)">
                                            No, Rarely
                                        </button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>

                        <div style="display:flex; justify-content:center; margin-top:2rem;">
                            <button type="submit" class="btn btn-primary btn-lg" id="submitScoreBtn">
                                <i data-lucide="calculator"></i>
                                <span>Calculate Security Posture</span>
                            </button>
                        </div>
                    </form>
                </div>

                <div id="scoreResultsArea" style="display:none;"></div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();

        document.getElementById('securityScoreForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.calculateScore();
        });
    },

    selectOption(qid, value, btnElement) {
        this.answers[qid] = value;
        const parent = document.getElementById(`card-${qid}`);
        if (!parent) return;

        parent.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
        btnElement.classList.add('selected');
    },

    async calculateScore() {
        const answeredCount = Object.keys(this.answers).length;
        if (answeredCount < this.questions.length) {
            showToast(`Please answer all 10 questions (${answeredCount}/10 completed).`, 'warning');
            return;
        }

        const submitBtn = document.getElementById('submitScoreBtn');
        const formContainer = document.getElementById('scoreFormContainer');
        const resultsArea = document.getElementById('scoreResultsArea');

        submitBtn.disabled = true;

        try {
            const result = await API.calculateSecurityScore(this.answers).catch(() => null);
            this.displayScoreResult(result || this.computeLocalScore());
        } catch (err) {
            this.displayScoreResult(this.computeLocalScore());
        } finally {
            submitBtn.disabled = false;
        }
    },

    computeLocalScore() {
        let rawScore = 0;
        const strengths = [];
        const improvements = [];

        this.questions.forEach(q => {
            const ans = this.answers[q.id];
            if (ans === 'yes') {
                rawScore += q.weight;
                strengths.push(q.text.replace('Do you ', '').replace('Is your ', ''));
            } else if (ans === 'sometimes') {
                rawScore += Math.floor(q.weight * 0.5);
                improvements.push(`Inconsistent: ${q.text}`);
            } else {
                improvements.push(`High Priority: ${q.text}`);
            }
        });

        return {
            overall_score: Math.min(Math.max(rawScore, 0), 100),
            strengths: strengths.slice(0, 4),
            improvements: improvements.slice(0, 4)
        };
    },

    displayScoreResult(data) {
        const formContainer = document.getElementById('scoreFormContainer');
        const resultsArea = document.getElementById('scoreResultsArea');
        if (!resultsArea) return;

        const score = data.overall_score ?? 80;
        let rating = 'Robust Security Posture';
        let ratingColor = 'var(--accent-green)';

        if (score < 50) {
            rating = 'Vulnerable Posture — High Risk';
            ratingColor = 'var(--accent-red)';
        } else if (score < 75) {
            rating = 'Moderate Posture — Needs Attention';
            ratingColor = 'var(--accent-yellow)';
        }

        formContainer.style.display = 'none';
        resultsArea.style.display = 'block';

        resultsArea.innerHTML = `
            <div class="card" style="text-align:center; padding: 2.5rem 1.5rem;">
                <div style="margin-bottom:1.5rem;">
                    ${createScoreCircle(score, 150, 'Security Index')}
                </div>
                <h3 style="color:${ratingColor}; margin-bottom:0.5rem;">${rating}</h3>
                <p style="max-width:550px; margin:0 auto 1.5rem auto; font-size:0.9rem;">
                    Your rating reflects foundational cyber preparedness across credential safety, endpoint updates, network security, and phishing resistance.
                </p>

                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.5rem; text-align:left; margin: 2rem 0;">
                    <div>
                        <h4 style="color:var(--accent-green); margin-bottom:0.75rem; display:flex; align-items:center; gap:0.5rem;">
                            <i data-lucide="check-circle-2"></i> Strong Defense Habits
                        </h4>
                        <div class="recommendation-list">
                            ${(data.strengths || ['Good awareness of baseline security']).map(s => `
                                <div class="recommendation-item">
                                    <i data-lucide="shield-check"></i>
                                    <div>${sanitizeHTML(s)}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <div>
                        <h4 style="color:var(--accent-red); margin-bottom:0.75rem; display:flex; align-items:center; gap:0.5rem;">
                            <i data-lucide="alert-triangle"></i> Vulnerabilities To Fix
                        </h4>
                        <div class="indicator-list">
                            ${(data.improvements || ['Ensure all passwords are unique and store backups']).map(imp => `
                                <div class="indicator-item">
                                    <i data-lucide="arrow-up-circle"></i>
                                    <div>${sanitizeHTML(imp)}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <div style="display:flex; justify-content:center; gap:1rem; margin-top:1.5rem;">
                    <button type="button" class="btn btn-secondary" onclick="SecurityScorePage.retake()">
                        <i data-lucide="rotate-ccw"></i>
                        <span>Retake Assessment</span>
                    </button>
                    <a href="#education" class="btn btn-primary">
                        <i data-lucide="graduation-cap"></i>
                        <span>Explore Security Guides</span>
                    </a>
                </div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons({ root: resultsArea });
    },

    retake() {
        this.render();
    }
};
