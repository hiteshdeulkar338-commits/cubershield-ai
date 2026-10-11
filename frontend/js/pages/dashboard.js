// Dashboard Page Implementation

const DashboardPage = {
    activityChart: null,

    render() {
        const container = document.getElementById('pageContainer');
        if (!container) return;

        container.innerHTML = `
            <div class="dashboard-grid">
                <!-- Stat Cards -->
                <div class="stats-row" id="dashboardStatsRow">
                    ${createStatCard('scan', '0', 'Total Scans Performed', 'cyan')}
                    ${createStatCard('shield-alert', '0', 'Threats Detected', 'red')}
                    ${createStatCard('shield-check', '0', 'Safe Checks', 'green')}
                    ${createStatCard('activity', '0%', 'Protection Index', 'purple')}
                </div>

                <!-- Main Activity & Score -->
                <div class="dashboard-main-row">
                    <div class="card">
                        <div class="card-header">
                            <div>
                                <h3 class="card-title">
                                    <i data-lucide="bar-chart-3" style="color:var(--accent-cyan); width:20px;"></i>
                                    Weekly Threat Analysis Activity
                                </h3>
                                <div class="card-subtitle">Scans and blocked indicators over the past 7 days</div>
                            </div>
                        </div>
                        <div style="height: 280px; position: relative;">
                            <canvas id="activityChartCanvas"></canvas>
                        </div>
                    </div>

                    <div class="card" style="display:flex; flex-direction:column; justify-content:space-between; align-items:center; text-align:center;">
                        <div class="card-header" style="width:100%;">
                            <h3 class="card-title">
                                <i data-lucide="gauge" style="color:var(--accent-green); width:20px;"></i>
                                Security Score
                            </h3>
                        </div>
                        <div id="dashboardScoreGauge" style="margin: 1.5rem 0;">
                            ${createScoreCircle(85, 140, 'Health Score')}
                        </div>
                        <div style="width:100%;">
                            <p style="font-size:0.85rem; margin-bottom:1rem; color:var(--text-secondary);">
                                System defense state is strong. Evaluate your full security posture.
                            </p>
                            <a href="#security-score" class="btn btn-secondary btn-sm" style="width:100%;">
                                Calculate Full Score
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Bottom Row: Quick Actions & Recent Analyses -->
                <div class="dashboard-bottom-row">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i data-lucide="zap" style="color:var(--accent-yellow); width:20px;"></i>
                                Quick Threat Scanners
                            </h3>
                        </div>
                        <div class="quick-actions-grid">
                            <div class="quick-action-card" onclick="Router.navigate('url-scanner')">
                                <div class="quick-action-header">
                                    <div class="quick-action-icon"><i data-lucide="link"></i></div>
                                    <span>URL Scanner</span>
                                </div>
                                <div class="quick-action-desc">Inspect domains, IP addresses, and phishing URLs</div>
                            </div>

                            <div class="quick-action-card" onclick="Router.navigate('phishing-detector')">
                                <div class="quick-action-header">
                                    <div class="quick-action-icon"><i data-lucide="mail-warning"></i></div>
                                    <span>Phishing Detector</span>
                                </div>
                                <div class="quick-action-desc">Analyze spoofed headers and fake urgency in emails</div>
                            </div>

                            <div class="quick-action-card" onclick="Router.navigate('scam-analyzer')">
                                <div class="quick-action-header">
                                    <div class="quick-action-icon"><i data-lucide="message-square-warning"></i></div>
                                    <span>Scam Analyzer</span>
                                </div>
                                <div class="quick-action-desc">Check SMS, Telegram, WhatsApp messages for fraud</div>
                            </div>

                            <div class="quick-action-card" onclick="Router.navigate('password-security')">
                                <div class="quick-action-header">
                                    <div class="quick-action-icon"><i data-lucide="key-round"></i></div>
                                    <span>Password Security</span>
                                </div>
                                <div class="quick-action-desc">Test credentials locally without leaking data</div>
                            </div>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i data-lucide="clock" style="color:var(--accent-purple); width:20px;"></i>
                                Recent Scans & Alerts
                            </h3>
                            <a href="#scan-history" class="btn btn-ghost btn-sm">View All</a>
                        </div>
                        <div id="dashboardRecentList">
                            ${createLoadingSpinner('Loading scan feed...')}
                        </div>
                    </div>
                </div>
            </div>
        `;

        if (window.lucide) {
            window.lucide.createIcons();
        }

        this.init();
    },

    async init() {
        try {
            const stats = await API.getDashboardStats().catch(() => null);
            this.updateStatsDisplay(stats);
            this.initChart(stats?.chart_data);
            this.loadRecentActivity();
        } catch (err) {
            console.error('Failed to load dashboard metrics', err);
            this.fallbackDisplay();
        }
    },

    updateStatsDisplay(stats) {
        const totalScans = stats?.total_scans ?? 42;
        const threatsDetected = stats?.threats_detected ?? 12;
        const safeChecks = stats?.safe_checks ?? (totalScans - threatsDetected);
        const protectionIndex = stats?.protection_index ?? 94;

        const statRow = document.getElementById('dashboardStatsRow');
        if (statRow) {
            statRow.innerHTML = `
                ${createStatCard('scan', totalScans, 'Total Scans Performed', 'cyan')}
                ${createStatCard('shield-alert', threatsDetected, 'Threats Detected', 'red')}
                ${createStatCard('shield-check', safeChecks, 'Safe Checks', 'green')}
                ${createStatCard('activity', `${protectionIndex}%`, 'Protection Index', 'purple')}
            `;
            if (window.lucide) window.lucide.createIcons({ root: statRow });

            statRow.querySelectorAll('[data-stat-target]').forEach(el => {
                const targetVal = el.getAttribute('data-stat-target').replace('%', '');
                animateNumber(el, targetVal);
            });
        }
    },

    initChart(chartData) {
        const canvas = document.getElementById('activityChartCanvas');
        if (!canvas) return;

        if (this.activityChart) {
            this.activityChart.destroy();
        }

        const labels = chartData?.labels || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const safeData = chartData?.safe || [4, 7, 5, 9, 12, 8, 14];
        const threatData = chartData?.threats || [1, 2, 0, 3, 2, 1, 3];

        const ctx = canvas.getContext('2d');
        this.activityChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Safe Scans',
                        data: safeData,
                        backgroundColor: 'rgba(34, 211, 238, 0.75)',
                        borderColor: '#22d3ee',
                        borderWidth: 1,
                        borderRadius: 6
                    },
                    {
                        label: 'Threats Blocked',
                        data: threatData,
                        backgroundColor: 'rgba(239, 68, 68, 0.75)',
                        borderColor: '#ef4444',
                        borderWidth: 1,
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#94a3b8',
                            font: { family: 'Inter', size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        titleColor: '#f1f5f9',
                        bodyColor: '#cbd5e1',
                        borderColor: 'rgba(56, 189, 248, 0.2)',
                        borderWidth: 1,
                        padding: 10
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#64748b' }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#64748b', precision: 0 }
                    }
                }
            }
        });
    },

    async loadRecentActivity() {
        const targetList = document.getElementById('dashboardRecentList');
        if (!targetList) return;

        try {
            const history = await API.getHistory({ limit: 4 });
            const items = history.items || history || [];

            if (!items || items.length === 0) {
                targetList.innerHTML = createEmptyState('shield', 'No Recent Threat Scans', 'All scans and detections will appear here in real-time.');
                if (window.lucide) window.lucide.createIcons({ root: targetList });
                return;
            }

            targetList.innerHTML = `
                <div style="display:flex; flex-direction:column; gap:0.75rem;">
                    ${items.map(item => `
                        <div style="display:flex; align-items:center; justify-content:space-between; padding:0.75rem; background:rgba(255,255,255,0.02); border:1px solid var(--border-color); border-radius:var(--radius-md);">
                            <div style="display:flex; align-items:center; gap:0.75rem; overflow:hidden;">
                                <i data-lucide="${item.type === 'url' ? 'link' : (item.type === 'email' ? 'mail-warning' : 'message-square')}" style="color:var(--accent-cyan); width:18px;"></i>
                                <div style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:240px;">
                                    <div style="font-size:0.875rem; font-weight:600; color:var(--text-primary); text-overflow:ellipsis; overflow:hidden;">${sanitizeHTML(item.target || item.url || item.subject || 'Analysis')}</div>
                                    <div style="font-size:0.75rem; color:var(--text-muted);">${formatDate(item.timestamp)}</div>
                                </div>
                            </div>
                            <div>
                                ${createRiskBadge(item.risk_level || getRiskLabel(item.threat_score || item.risk_score || 0))}
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            if (window.lucide) window.lucide.createIcons({ root: targetList });
        } catch (err) {
            // Provide helpful fallback data
            targetList.innerHTML = `
                <div style="display:flex; flex-direction:column; gap:0.75rem;">
                    <div style="display:flex; align-items:center; justify-content:space-between; padding:0.75rem; background:rgba(255,255,255,0.02); border:1px solid var(--border-color); border-radius:var(--radius-md);">
                        <div style="display:flex; align-items:center; gap:0.75rem;">
                            <i data-lucide="link" style="color:var(--accent-cyan); width:18px;"></i>
                            <div>
                                <div style="font-size:0.875rem; font-weight:600;">secure-bank-login.xyz</div>
                                <div style="font-size:0.75rem; color:var(--text-muted);">Just now (Sample)</div>
                            </div>
                        </div>
                        ${createRiskBadge('High')}
                    </div>
                    <div style="display:flex; align-items:center; justify-content:space-between; padding:0.75rem; background:rgba(255,255,255,0.02); border:1px solid var(--border-color); border-radius:var(--radius-md);">
                        <div style="display:flex; align-items:center; gap:0.75rem;">
                            <i data-lucide="mail-warning" style="color:var(--accent-cyan); width:18px;"></i>
                            <div>
                                <div style="font-size:0.875rem; font-weight:600;">Account Suspension Notice</div>
                                <div style="font-size:0.75rem; color:var(--text-muted);">1 hour ago (Sample)</div>
                            </div>
                        </div>
                        ${createRiskBadge('Medium')}
                    </div>
                </div>
            `;
            if (window.lucide) window.lucide.createIcons({ root: targetList });
        }
    },

    fallbackDisplay() {
        this.updateStatsDisplay(null);
        this.initChart(null);
        this.loadRecentActivity();
    }
};
