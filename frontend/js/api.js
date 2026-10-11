// CyberShield AI API Client

const API = {
    baseUrl: '/api',

    async request(endpoint, options = {}) {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 30000);

        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                ...options,
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            clearTimeout(timeout);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Request failed' }));
                throw new Error(errorData.error || errorData.message || `HTTP error ${response.status}`);
            }
            return await response.json();
        } catch (err) {
            clearTimeout(timeout);
            if (err.name === 'AbortError') {
                throw new Error('Request timed out. Please try again.');
            }
            throw err;
        }
    },

    // HTTP method shortcuts
    get(endpoint) {
        return this.request(endpoint);
    },

    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    },

    // Threat Scanner Endpoints
    healthCheck() {
        return this.get('/health');
    },

    scanUrl(url) {
        return this.post('/scan-url', { url });
    },

    analyzeEmail(data) {
        return this.post('/analyze-email', data);
    },

    analyzeMessage(data) {
        return this.post('/analyze-message', data);
    },

    calculateSecurityScore(answers) {
        return this.post('/security-score', { answers });
    },

    // History Endpoints
    getHistory(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.get(`/history${query ? '?' + query : ''}`);
    },

    getDashboardStats() {
        return this.get('/dashboard-stats');
    },

    deleteHistoryItem(id) {
        return this.delete(`/history/${id}`);
    },

    clearHistory() {
        return this.delete('/history');
    },

    // Education & Knowledge Endpoints
    getEducationTopics() {
        return this.get('/education/topics');
    },

    getTopicDetail(id) {
        return this.get(`/education/topics/${id}`);
    },

    getGlossary() {
        return this.get('/glossary');
    }
};
