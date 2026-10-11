// Utility Functions

/**
 * Sanitize strings to prevent XSS injection in innerHTML
 */
function sanitizeHTML(str) {
    if (str === null || str === undefined) return '';
    const temp = document.createElement('div');
    temp.textContent = String(str);
    return temp.innerHTML;
}

/**
 * Format timestamp into readable string
 */
function formatDate(dateInput) {
    if (!dateInput) return 'N/A';
    const date = new Date(dateInput);
    if (isNaN(date.getTime())) return String(dateInput);
    return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

/**
 * Debounce utility
 */
function debounce(fn, delay = 250) {
    let timeoutId;
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn(...args), delay);
    };
}

/**
 * Generate random identifier
 */
function generateId() {
    return 'id-' + Math.random().toString(36).substring(2, 9) + Date.now().toString(36);
}

/**
 * Map risk level to semantic color code
 */
function getRiskColor(level) {
    const l = (level || '').toLowerCase();
    switch (l) {
        case 'safe':
            return 'var(--risk-safe)';
        case 'low':
            return 'var(--risk-low)';
        case 'medium':
            return 'var(--risk-medium)';
        case 'high':
            return 'var(--risk-high)';
        case 'critical':
            return 'var(--risk-critical)';
        default:
            return 'var(--accent-blue)';
    }
}

/**
 * Convert numeric threat score (0-100) to risk level string
 */
function getRiskLabel(score) {
    const s = Number(score) || 0;
    if (s < 20) return 'Safe';
    if (s < 50) return 'Low';
    if (s < 75) return 'Medium';
    return 'High';
}

/**
 * Show animated toast notification
 */
function showToast(message, type = 'info', title = null) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let iconName = 'info';
    if (type === 'success') iconName = 'check-circle';
    if (type === 'error') iconName = 'alert-triangle';
    if (type === 'warning') iconName = 'alert-circle';

    const defaultTitle = type.charAt(0).toUpperCase() + type.slice(1);
    const toastTitle = title || defaultTitle;

    toast.innerHTML = `
        <i data-lucide="${iconName}"></i>
        <div class="toast-content">
            <div class="toast-title">${sanitizeHTML(toastTitle)}</div>
            <div class="toast-message">${sanitizeHTML(message)}</div>
        </div>
    `;

    container.appendChild(toast);
    if (window.lucide) {
        window.lucide.createIcons({ root: toast });
    }

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(() => toast.remove(), 250);
    }, 4000);
}

/**
 * DOM Helper to create elements with attributes and children
 */
function createElement(tag, attrs = {}, children = []) {
    const el = document.createElement(tag);
    for (const [key, val] of Object.entries(attrs)) {
        if (key === 'className') {
            el.className = val;
        } else if (key === 'dataset') {
            for (const [dKey, dVal] of Object.entries(val)) {
                el.dataset[dKey] = dVal;
            }
        } else if (key.startsWith('on') && typeof val === 'function') {
            el.addEventListener(key.substring(2).toLowerCase(), val);
        } else {
            el.setAttribute(key, val);
        }
    }

    children.forEach(child => {
        if (typeof child === 'string' || typeof child === 'number') {
            el.appendChild(document.createTextNode(child));
        } else if (child instanceof Node) {
            el.appendChild(child);
        }
    });

    return el;
}

/**
 * Animate numeric counter on an element
 */
function animateNumber(element, target, duration = 800) {
    if (!element) return;
    const start = 0;
    const end = parseInt(target, 10) || 0;
    const startTime = performance.now();

    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeOutQuad = 1 - (1 - progress) * (1 - progress);
        const current = Math.floor(start + (end - start) * easeOutQuad);
        element.textContent = current.toLocaleString();
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = end.toLocaleString();
        }
    }

    requestAnimationFrame(update);
}

/**
 * Validate URL string
 */
function isValidUrl(str) {
    if (!str || typeof str !== 'string') return false;
    try {
        const url = new URL(str.startsWith('http://') || str.startsWith('https://') ? str : `https://${str}`);
        return Boolean(url.hostname && url.hostname.includes('.'));
    } catch (_) {
        return false;
    }
}

/**
 * Truncate text with ellipsis
 */
function truncate(str, len = 50) {
    if (!str) return '';
    return str.length > len ? str.substring(0, len) + '...' : str;
}

/**
 * Escape text for safe inline display
 */
function escapeForDisplay(str) {
    return sanitizeHTML(str);
}
