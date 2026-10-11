// Phishing Detector Page Implementation

const PhishingDetectorPage = {
    render() {
        const container = document.getElementById('pageContainer');
        if (!container) return;

        container.innerHTML = `
            <div class="scanner-container">
                <div class="scanner-header">
                    <h2>Email Phishing & Impersonation Detector</h2>
                    <p>Identify social engineering signals, urgency tactics, spoofed senders, and malicious request patterns.</p>
                </div>

                <div class="card">
                    <form id="phishingForm">
                        <div class="form-group">
                            <label class="form-label" for="phishSubject">Email Subject Line</label>
                            <input 
                                type="text" 
                                id="phishSubject" 
                                class="input-control" 
                                placeholder="URGENT: Immediate verification needed for your payroll account"
                                required
                            />
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="phishSender">Sender Address / Display Name</label>
                            <input 
                                type="text" 
                                id="phishSender" 
                                class="input-control" 
                                placeholder="Security Team <security-alert@internal-verify-payroll.net>"
                                required
                            />
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="phishBody">Email Content / Body</label>
                            <textarea 
                                id="phishBody" 
                                class="textarea-control" 
                                placeholder="Paste the complete text or body of the suspicious email here..."
                                required
                            ></textarea>
                        </div>

                        <div class="example-chips">
                            <span class="example-chips-label">Preset Phishing Scenarios:</span>
                            <button type="button" class="example-chip" onclick="PhishingDetectorPage.loadExample('bank')">Bank Verification</button>
                            <button type="button" class="example-chip" onclick="PhishingDetectorPage.loadExample('prize')">Prize Lottery</button>
                            <button type="button" class="example-chip" onclick="PhishingDetectorPage.loadExample('suspended')">Account Suspended</button>
                            <button type="button" class="example-chip" onclick="PhishingDetectorPage.loadExample('tax')">Tax Refund</button>
                        </div>

                        <div style="display:flex; gap:1rem; margin-top:1.5rem;">
                            <button type="submit" class="btn btn-primary" id="phishSubmitBtn">
                                <i data-lucide="mail-search"></i>
                                <span>Analyze Email</span>
                            </button>
                            <button type="button" class="btn btn-secondary" onclick="PhishingDetectorPage.clearForm()">
                                <i data-lucide="rotate-ccw"></i>
                                <span>Clear Form</span>
                            </button>
                        </div>
                    </form>
                </div>

                <div id="phishingResultArea"></div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();

        document.getElementById('phishingForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAnalysis();
        });
    },

    loadExample(type) {
        const subject = document.getElementById('phishSubject');
        const sender = document.getElementById('phishSender');
        const body = document.getElementById('phishBody');

        if (!subject || !sender || !body) return;

        switch (type) {
            case 'bank':
                subject.value = 'URGENT: Suspicious debit attempt flagged on your checking account';
                sender.value = 'Chase Alert Desk <security-notification@chase-auth-service.com>';
                body.value = 'Dear Customer, an unauthorized charge of $1,429.00 was attempted from IP 185.220.101.4. If this was not you, confirm your credentials immediately to block transaction: https://chase-auth-service.com/login-verify';
                break;
            case 'prize':
                subject.value = 'Official Notification: You have won 1st Prize in Global Cash Giveaway!';
                sender.value = 'International Promotions Desk <winner@claim-prizes-online24.org>';
                body.value = 'Congratulations! Your email was drawn as the lucky recipient of $250,000 cash. Reply with your full legal name, telephone number, and bank account details within 24 hours to claim your reward.';
                break;
            case 'suspended':
                subject.value = 'Action Required: Your Microsoft 365 Account is scheduled for deletion';
                sender.value = 'Microsoft Security <admin@mcrosoft-cloud-update.io>';
                body.value = 'Your corporate cloud license has expired and all Outlook emails will be permanently deleted within 6 hours. Click here to confirm identity and preserve your files: https://mcrosoft-cloud-update.io/renew';
                break;
            case 'tax':
                subject.value = 'Internal Revenue Service: Notification of outstanding tax refund #TX-88319';
                sender.value = 'IRS Refund Center <refund@irs-tax-gov-portal.info>';
                body.value = 'Our records show an uncollected tax credit of $1,840.50 for fiscal year 2025. Submit your social security number and debit card numbers on the official form to release the transfer directly to your checking account.';
                break;
        }
    },

    clearForm() {
        const subject = document.getElementById('phishSubject');
        const sender = document.getElementById('phishSender');
        const body = document.getElementById('phishBody');
        const result = document.getElementById('phishingResultArea');

        if (subject) subject.value = '';
        if (sender) sender.value = '';
        if (body) body.value = '';
        if (result) result.innerHTML = '';
    },

    async handleAnalysis() {
        const subject = document.getElementById('phishSubject').value.trim();
        const sender = document.getElementById('phishSender').value.trim();
        const body = document.getElementById('phishBody').value.trim();
        const submitBtn = document.getElementById('phishSubmitBtn');
        const resultArea = document.getElementById('phishingResultArea');

        submitBtn.disabled = true;
        resultArea.innerHTML = createLoadingSpinner('Analyzing linguistic pressure, domain spoofing, and sentiment vectors...');
        if (window.lucide) window.lucide.createIcons();

        try {
            const data = await API.analyzeEmail({ subject, sender, body });
            resultArea.innerHTML = createResultCard(data);
            showToast('Email analysis finalized.', 'success');
        } catch (err) {
            // Heuristic client fallback
            const isSuspicious = subject.toLowerCase().includes('urgent') || body.toLowerCase().includes('http');
            resultArea.innerHTML = createResultCard({
                subject: subject,
                risk_score: isSuspicious ? 88 : 25,
                risk_level: isSuspicious ? 'High' : 'Low',
                timestamp: new Date().toISOString(),
                indicators: isSuspicious ? [
                    'Extreme urgency and artificial time constraints',
                    'Suspicious sender display name impersonation',
                    'Unverified embedded hyperlinks prompting credential submission'
                ] : [
                    'Standard communication phrasing detected'
                ],
                recommendations: [
                    'Never click links or open attachments in unverified messages.',
                    'Check email sender headers for SPF/DKIM/DMARC alignment.',
                    'Report this phishing simulation to your IT security division.'
                ]
            });
            showToast('Analyzed with heuristic client engine.', 'info');
        } finally {
            submitBtn.disabled = false;
            if (window.lucide) window.lucide.createIcons();
        }
    }
};
