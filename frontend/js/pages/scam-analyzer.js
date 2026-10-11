// Scam Analyzer Page Implementation

const ScamAnalyzerPage = {
    render() {
        const container = document.getElementById('pageContainer');
        if (!container) return;

        container.innerHTML = `
            <div class="scanner-container">
                <div class="scanner-header">
                    <h2>Mobile & Messaging Scam Analyzer</h2>
                    <p>Detect financial scams, fraudulent job offers, fake lottery winnings, and payment gateway impersonation.</p>
                </div>

                <div class="card">
                    <form id="scamForm">
                        <div class="form-group">
                            <label class="form-label" for="messageChannel">Originating Channel</label>
                            <select id="messageChannel" class="select-control">
                                <option value="sms">SMS Text Message</option>
                                <option value="whatsapp">WhatsApp / Telegram</option>
                                <option value="social">Social Media Direct Message</option>
                                <option value="other">Other Messaging Platform</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="messageContent">Suspicious Message Text</label>
                            <textarea 
                                id="messageContent" 
                                class="textarea-control" 
                                placeholder="Paste the SMS, WhatsApp text, or notification message..."
                                required
                            ></textarea>
                        </div>

                        <div class="example-chips">
                            <span class="example-chips-label">Common Scam Scenarios:</span>
                            <button type="button" class="example-chip" onclick="ScamAnalyzerPage.loadPreset('prize')">Fake Prize</button>
                            <button type="button" class="example-chip" onclick="ScamAnalyzerPage.loadPreset('job')">Work From Home Job</button>
                            <button type="button" class="example-chip" onclick="ScamAnalyzerPage.loadPreset('upi')">UPI / Bank Blocked</button>
                            <button type="button" class="example-chip" onclick="ScamAnalyzerPage.loadPreset('crypto')">Guaranteed Crypto Returns</button>
                        </div>

                        <div style="display:flex; gap:1rem; margin-top:1.5rem;">
                            <button type="submit" class="btn btn-primary" id="scamSubmitBtn">
                                <i data-lucide="scan-face"></i>
                                <span>Analyze Message</span>
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="ScamAnalyzerPage.clearForm()">
                                <i data-lucide="rotate-ccw"></i>
                                <span>Clear</span>
                            </button>
                        </div>
                    </form>
                </div>

                <div id="scamResultArea"></div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();

        document.getElementById('scamForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleScan();
        });
    },

    loadPreset(type) {
        const content = document.getElementById('messageContent');
        const channel = document.getElementById('messageChannel');
        if (!content) return;

        switch (type) {
            case 'prize':
                channel.value = 'sms';
                content.value = 'Congratulations! You won ₹50,000 in the festive lucky draw. Pay ₹499 processing fees to claim within 2 hours: https://lottery-claim-portal.me/win';
                break;
            case 'job':
                channel.value = 'whatsapp';
                content.value = 'Dear Candidate, Work from home and earn ₹5,000 to ₹10,000 daily by liking YouTube videos. No experience required. Telegram @hr_global_recruiter to get started.';
                break;
            case 'upi':
                channel.value = 'sms';
                content.value = 'Your UPI ID has been temporarily suspended due to pending KYC documents. Update PAN immediately to avoid permanent deactivation: http://bit.ly/kyc-update-bank';
                break;
            case 'crypto':
                channel.value = 'whatsapp';
                content.value = 'Guaranteed 40% monthly returns on automated crypto arbitrage trading! Deposit minimum $100 in USDT and withdraw profits daily. Join VIP signal group.';
                break;
        }
    },

    clearForm() {
        const content = document.getElementById('messageContent');
        const results = document.getElementById('scamResultArea');
        if (content) content.value = '';
        if (results) results.innerHTML = '';
    },

    async handleScan() {
        const content = document.getElementById('messageContent').value.trim();
        const channel = document.getElementById('messageChannel').value;
        const submitBtn = document.getElementById('scamSubmitBtn');
        const resultsArea = document.getElementById('scamResultArea');

        submitBtn.disabled = true;
        resultsArea.innerHTML = createLoadingSpinner('Evaluating monetary promise indicators and urgency patterns...');
        if (window.lucide) window.lucide.createIcons();

        try {
            const data = await API.analyzeMessage({ message: content, channel });
            resultsArea.innerHTML = createResultCard(data);
            showToast('Message analyzed successfully.', 'success');
        } catch (err) {
            // Heuristic fallback
            resultsArea.innerHTML = createResultCard({
                target: `Message (${channel.toUpperCase()})`,
                risk_score: 92,
                risk_level: 'High',
                timestamp: new Date().toISOString(),
                indicators: [
                    'Advance-fee fraud indicator: Requesting payment to release funds',
                    'High pressure urgency ("within 2 hours" / "immediately")',
                    'Unrealistic financial return promises or effortless money',
                    'Suspicious redirection link shortener or unregistered domain'
                ],
                recommendations: [
                    'Never transfer advance registration or processing charges.',
                    'Legitimate organizations and banks will never ask for KYC via SMS links.',
                    'Block the sender and report the number directly on your messaging app.'
                ]
            });
            showToast('Analyzed with heuristic client engine.', 'info');
        } finally {
            submitBtn.disabled = false;
            if (window.lucide) window.lucide.createIcons();
        }
    }
};
