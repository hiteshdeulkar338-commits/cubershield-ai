// Client-Side Hash Router

const Router = {
    routes: {},
    currentPage: null,

    register(path, handler) {
        this.routes[path] = handler;
    },

    init() {
        window.addEventListener('hashchange', () => this.handleRouting());
        this.handleRouting();
    },

    handleRouting() {
        const hash = window.location.hash.slice(1) || 'dashboard';
        const [routePath, queryString] = hash.split('?');
        const handler = this.routes[routePath] || this.routes['dashboard'];

        if (handler) {
            this.currentPage = routePath;
            this.updateNavigation(routePath);
            this.updateBreadcrumb(routePath);
            
            const params = new URLSearchParams(queryString || '');
            const container = document.getElementById('pageContainer');
            if (container) {
                container.innerHTML = '';
                container.classList.remove('animate-in');
                void container.offsetWidth; // Trigger reflow
                container.classList.add('animate-in');
            }

            handler(params);

            // Close mobile sidebar on route switch
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebarOverlay');
            if (sidebar && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                if (overlay) overlay.classList.remove('active');
            }

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    },

    updateNavigation(route) {
        document.querySelectorAll('.sidebar-nav .nav-item').forEach(item => {
            const page = item.getAttribute('data-page');
            if (page === route) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    },

    updateBreadcrumb(route) {
        const breadcrumb = document.getElementById('breadcrumb');
        if (!breadcrumb) return;

        const titles = {
            'dashboard': 'Dashboard',
            'url-scanner': 'URL Scanner',
            'phishing-detector': 'Phishing Detector',
            'scam-analyzer': 'Scam Analyzer',
            'password-security': 'Password Security',
            'security-score': 'Security Score',
            'education': 'Security Education',
            'scan-history': 'Scan History',
            'settings': 'Settings'
        };

        const pageTitle = titles[route] || 'Overview';
        breadcrumb.innerHTML = `<span>${sanitizeHTML(pageTitle)}</span>`;
        document.title = `${pageTitle} — CyberShield AI`;
    },

    navigate(path) {
        window.location.hash = path;
    }
};
