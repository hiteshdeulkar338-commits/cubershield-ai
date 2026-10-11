// Reusable UI Components

/**
 * Creates SVG circular score gauge
 */
function createScoreCircle(score = 0, size = 120, label = 'Threat Score') {
    const strokeWidth = 8;
    const radius = (size - strokeWidth * 2) / 2;
    const circumference = 2 * Math.PI * radius;
    const clampedScore = Math.min(Math.max(Number(score) || 0, 0), 100);
    const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

    let strokeColor = 'var(--risk-safe)';
    if (clampedScore >= 75) strokeColor = 'var(--risk-high)';
    else if (clampedScore >= 50) strokeColor = 'var(--risk-medium)';
    else if (clampedScore >= 20) strokeColor = 'var(--risk-low)';

    return `
        <div class="score-circle-wrap" style="width: ${size}px; height: ${size}px;">
            <svg class="score-circle-svg" width="${size}" height="${size}">
                <circle class="score-circle-bg" cx="${size/2}" cy="${size/2}" r="${radius}" stroke-width="${strokeWidth}" fill="transparent"></circle>
                <circle class="score-circle-progress" cx="${size/2}" cy="${size/2}" r="${radius}" stroke-width="${strokeWidth}"
                    stroke="${strokeColor}" fill="transparent"
                    stroke-dasharray="${circumference}" stroke-dashoffset="${strokeDashoffset}"></circle>
            </svg>
            <div class="score-circle-text">
                <span class="score-circle-number">${clampedScore}</span>
                <span class="score-circle-label">${sanitizeHTML(label)}</span>
            </div>
        </div>
    `;
}

/**
 * Creates risk badge component
 */
function createRiskBadge(level = 'Safe') {
    const l = (level || 'safe').toLowerCase();
    let badgeClass = 'badge-safe';
    let icon = 'shield-check';

    if (l.includes('critical') || l.includes('high')) {
        badgeClass = 'badge-high';
        icon = 'alert-triangle';
    } else if (l.includes('medium')) {
        badgeClass = 'badge-medium';
        icon = 'alert-circle';
    } else if (l.includes('low')) {
        badgeClass = 'badge-low';
        icon = 'info';
    }

    return `
        <span class="badge ${badgeClass}">
            <i data-lucide="${icon}"></i>
            <span>${sanitizeHTML(level)}</span>
        </span>
    `;
}

/**
 * Creates linear horizontal risk meter
 */
function createRiskMeter(score = 0) {
    const clamped = Math.min(Math.max(Number(score) || 0, 0), 100);
    let color = 'var(--risk-safe)';
    if (clamped >= 75) color = 'var(--risk-high)';
    else if (clamped >= 50) color = 'var(--risk-medium)';
    else if (clamped >= 20) color = 'var(--risk-low)';

    return `
        <div class="risk-meter">
            <div class="risk-meter-header">
                <span>Threat Level</span>
                <span style="color: ${color}; font-weight: 700;">${clamped}/100</span>
            </div>
            <div class="risk-meter-bar">
                <div class="risk-meter-fill" style="width: ${clamped}%; background-color: ${color};"></div>
            </div>
        </div>
    `;
}

/**
 * Creates dashboard stat card
 */
function createStatCard(icon, value, label, color = 'cyan') {
    return `
        <div class="stat-card">
            <div class="stat-icon ${color}">
                <i data-lucide="${icon}"></i>
            </div>
            <div class="stat-content">
                <span class="stat-value" data-stat-target="${value}">${value}</span>
                <span class="stat-label">${sanitizeHTML(label)}</span>
            </div>
        </div>
    `;
}

/**
 * Creates loading spinner wrapper
 */
function createLoadingSpinner(text = 'Analyzing security heuristics...') {
    return `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>${sanitizeHTML(text)}</p>
        </div>
    `;
}

/**
 * Creates empty state display
 */
function createEmptyState(icon = 'inbox', title = 'No Data Available', description = 'There are no records to display at this moment.') {
    return `
        <div class="empty-state">
            <div class="empty-state-icon">
                <i data-lucide="${icon}"></i>
            </div>
            <h4 class="empty-state-title">${sanitizeHTML(title)}</h4>
            <p class="empty-state-desc">${sanitizeHTML(description)}</p>
        </div>
    `;
}

/**
 * Creates analysis result card
 */
function createResultCard(analysis = {}) {
    const score = analysis.risk_score ?? analysis.threat_score ?? analysis.score ?? 0;
    const level = analysis.risk_level ?? getRiskLabel(score);
    const target = analysis.url || analysis.target || analysis.subject || 'Scanned Input';
    const indicators = analysis.indicators || analysis.threat_indicators || [];
    const recommendations = analysis.recommendations || [];

    return `
        <div class="results-card">
            <div class="results-hero">
                <div class="results-hero-left">
                    <div style="display:flex; align-items:center; gap:0.75rem;">
                        <h3 style="margin:0;">Analysis Result</h3>
                        ${createRiskBadge(level)}
                    </div>
                    <span class="target-analyzed">${sanitizeHTML(target)}</span>
                    <p style="margin:0; font-size:0.85rem; color:var(--text-muted);">
                        Scanned on ${formatDate(analysis.timestamp || new Date())}
                    </p>
                </div>
                <div>
                    ${createScoreCircle(score, 100, 'Risk Score')}
                </div>
            </div>

            ${createRiskMeter(score)}

            <div>
                <h4 style="margin-bottom: 0.75rem; display:flex; align-items:center; gap:0.5rem;">
                    <i data-lucide="alert-octagon" style="color:var(--accent-red); width:18px;"></i>
                    Detected Threat Indicators (${indicators.length})
                </h4>
                ${indicators.length > 0 
                    ? `<div class="indicator-list">${indicators.map(ind => createIndicatorItem(ind)).join('')}</div>`
                    : '<p style="font-size:0.85rem; color:var(--text-muted); padding:0.5rem 0;">No obvious malicious indicators detected in this scan.</p>'
                }
            </div>

            <div>
                <h4 style="margin-bottom: 0.75rem; display:flex; align-items:center; gap:0.5rem;">
                    <i data-lucide="shield" style="color:var(--accent-cyan); width:18px;"></i>
                    Actionable Recommendations
                </h4>
                <div class="recommendation-list">
                    ${recommendations.length > 0
                        ? recommendations.map(rec => createRecommendationItem(rec)).join('')
                        : createRecommendationItem('Exercise standard cyber hygiene before interacting with unknown sources.')
                    }
                </div>
            </div>
        </div>
    `;
}

function createIndicatorItem(indicator) {
    const text = typeof indicator === 'object' ? (indicator.description || indicator.name || JSON.stringify(indicator)) : indicator;
    return `
        <div class="indicator-item">
            <i data-lucide="alert-triangle"></i>
            <div>${sanitizeHTML(text)}</div>
        </div>
    `;
}

function createRecommendationItem(text) {
    return `
        <div class="recommendation-item">
            <i data-lucide="check-circle-2"></i>
            <div>${sanitizeHTML(text)}</div>
        </div>
    `;
}
