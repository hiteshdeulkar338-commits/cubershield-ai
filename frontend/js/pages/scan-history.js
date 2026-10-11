// Scan History Page Implementation

const ScanHistoryPage = {
    historyItems: [],
    filterType: 'all',
    sortOrder: 'desc',

    render() {
        const container = document.getElementById('pageContainer');
        if (!container) return;

        container.innerHTML = `
            <div style="display:flex; flex-direction:column; gap:1.5rem;">
                <div class="scanner-header">
                    <h2>Threat Intelligence & Scan Audit Log</h2>
                    <p>Review past heuristic scans, detected indicators, risk scores, and security reports.</p>
                </div>

                <!-- Controls Bar -->
                <div class="card" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; padding:1rem 1.5rem;">
                    <div style="display:flex; align-items:center; gap:0.75rem; flex-wrap:wrap;">
                        <span style="font-size:0.85rem; font-weight:600; color:var(--text-muted);">Filter Type:</span>
                        <div class="example-chips" style="margin:0;">
                            <button type="button" class="example-chip active" id="filter-all" onclick="ScanHistoryPage.setFilter('all')">All Scans</button>
                            <button type="button" class="example-chip" id="filter-url" onclick="ScanHistoryPage.setFilter('url')">URLs</button>
                            <button type="button" class="example-chip" id="filter-email" onclick="ScanHistoryPage.setFilter('email')">Emails</button>
                            <button type="button" class="example-chip" id="filter-message" onclick="ScanHistoryPage.setFilter('message')">Messages</button>
                        </div>
                    </div>

                    <div style="display:flex; align-items:center; gap:1rem;">
                        <select id="sortSelect" class="select-control" style="width:160px; padding:0.4rem 0.75rem; font-size:0.8rem;" onchange="ScanHistoryPage.setSort(this.value)">
                            <option value="desc">Newest First</option>
                            <option value="asc">Oldest First</option>
                        </select>
                        <button type="button" class="btn btn-danger btn-sm" onclick="ScanHistoryPage.confirmClearHistory()">
                            <i data-lucide="trash-2"></i>
                            <span>Clear All</span>
                        </button>
                    </div>
                </div>

                <!-- History Table View -->
                <div class="card" style="padding:0; overflow:hidden;" id="historyContentWrapper">
                    ${createLoadingSpinner('Loading scan history audit...')}
                </div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();

        this.loadHistory();
    },

    async loadHistory() {
        try {
            const data = await API.getHistory().catch(() => null);
            this.historyItems = data?.items || data || this.getDemoHistory();
            this.renderList();
        } catch (err) {
            this.historyItems = this.getDemoHistory();
            this.renderList();
        }
    },

    getDemoHistory() {
        return [
            { id: 'scan-1', type: 'url', target: 'https://paypal-verify-alert.xyz/auth', risk_level: 'High', threat_score: 86, timestamp: new Date(Date.now() - 3600000).toISOString() },
            { id: 'scan-2', type: 'email', target: 'Urgent Payroll Invoice #39281', risk_level: 'Medium', threat_score: 62, timestamp: new Date(Date.now() - 7200000).toISOString() },
            { id: 'scan-3', type: 'message', target: 'Won ₹50,000 lottery draw claim', risk_level: 'High', threat_score: 95, timestamp: new Date(Date.now() - 86400000).toISOString() },
            { id: 'scan-4', type: 'url', target: 'https://github.com', risk_level: 'Safe', threat_score: 5, timestamp: new Date(Date.now() - 172800000).toISOString() }
        ];
    },

    setFilter(type) {
        this.filterType = type;
        document.querySelectorAll('.example-chips .example-chip').forEach(c => c.classList.remove('active'));
        const btn = document.getElementById(`filter-${type}`);
        if (btn) btn.classList.add('active');
        this.renderList();
    },

    setSort(order) {
        this.sortOrder = order;
        this.renderList();
    },

    renderList() {
        const wrapper = document.getElementById('historyContentWrapper');
        if (!wrapper) return;

        let filtered = [...this.historyItems];
        if (this.filterType !== 'all') {
            filtered = filtered.filter(item => (item.type || '').toLowerCase() === this.filterType);
        }

        filtered.sort((a, b) => {
            const dateA = new Date(a.timestamp || 0).getTime();
            const dateB = new Date(b.timestamp || 0).getTime();
            return this.sortOrder === 'asc' ? dateA - dateB : dateB - dateA;
        });

        if (filtered.length === 0) {
            wrapper.innerHTML = createEmptyState('archive', 'No Scans in Log', 'No matching scans found for the chosen criteria.');
            if (window.lucide) window.lucide.createIcons({ root: wrapper });
            return;
        }

        wrapper.innerHTML = `
            <div class="history-table-container">
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Target / Subject</th>
                            <th>Risk Assessment</th>
                            <th>Score</th>
                            <th>Timestamp</th>
                            <th style="text-align:right;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${filtered.map(item => `
                            <tr>
                                <td>
                                    <div style="display:flex; align-items:center; gap:0.5rem; text-transform:uppercase; font-size:0.75rem; font-weight:700; color:var(--accent-cyan);">
                                        <i data-lucide="${this.getTypeIcon(item.type)}" style="width:16px;"></i>
                                        <span>${sanitizeHTML(item.type || 'scan')}</span>
                                    </div>
                                </td>
                                <td>
                                    <div style="font-weight:600; color:var(--text-primary); max-width:320px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                                        ${sanitizeHTML(item.target || item.url || item.subject || 'Analysis Record')}
                                    </div>
                                </td>
                                <td>
                                    ${createRiskBadge(item.risk_level || getRiskLabel(item.threat_score || item.risk_score || 0))}
                                </td>
                                <td>
                                    <span style="font-weight:700; font-family:var(--font-mono); color:var(--text-primary);">
                                        ${item.threat_score ?? item.risk_score ?? 0}/100
                                    </span>
                                </td>
                                <td>
                                    <span style="font-size:0.8rem; color:var(--text-muted);">${formatDate(item.timestamp)}</span>
                                </td>
                                <td style="text-align:right;">
                                    <button 
                                        type="button" 
                                        class="btn btn-ghost btn-sm" 
                                        style="color:var(--accent-red);" 
                                        onclick="ScanHistoryPage.deleteItem('${item.id}')"
                                        title="Delete Log"
                                    >
                                        <i data-lucide="trash"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons({ root: wrapper });
    },

    getTypeIcon(type = '') {
        const t = type.toLowerCase();
        if (t === 'url') return 'link';
        if (t === 'email') return 'mail-warning';
        if (t === 'message') return 'message-square';
        return 'shield';
    },

    async deleteItem(id) {
        try {
            await API.deleteHistoryItem(id).catch(() => null);
        } catch (_) {}

        this.historyItems = this.historyItems.filter(i => String(i.id) !== String(id));
        this.renderList();
        showToast('Scan log entry removed.', 'info');
    },

    async confirmClearHistory() {
        if (!confirm('Are you sure you want to permanently delete all scan records?')) {
            return;
        }

        try {
            await API.clearHistory().catch(() => null);
        } catch (_) {}

        this.historyItems = [];
        this.renderList();
        showToast('All scan history logs have been cleared.', 'success');
    }
};
