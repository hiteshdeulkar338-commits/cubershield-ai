// CyberShield AI Application Bootstrap

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Theme from LocalStorage
    const savedTheme = localStorage.getItem('cybershield_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeNavBtn = document.getElementById('themeToggle');
    if (themeNavBtn) {
        themeNavBtn.innerHTML = `<i data-lucide="${savedTheme === 'dark' ? 'moon' : 'sun'}"></i>`;
        themeNavBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme') || 'dark';
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('cybershield_theme', next);
            themeNavBtn.innerHTML = `<i data-lucide="${next === 'dark' ? 'moon' : 'sun'}"></i>`;
            if (window.lucide) window.lucide.createIcons({ root: themeNavBtn });
            showToast(`Theme switched to ${next} mode.`, 'info');
        });
    }

    // 2. Setup Mobile Navigation Sidebar Toggle
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (menuToggle && sidebar && overlay) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('active');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }

    // 3. Notification Button interaction
    const notifBtn = document.getElementById('notificationsBtn');
    if (notifBtn) {
        notifBtn.addEventListener('click', () => {
            showToast('All real-time heuristic monitoring shields are currently operational.', 'info', 'System Notice');
        });
    }

    // 4. Register Routes
    Router.register('dashboard', () => DashboardPage.render());
    Router.register('url-scanner', () => UrlScannerPage.render());
    Router.register('phishing-detector', () => PhishingDetectorPage.render());
    Router.register('scam-analyzer', () => ScamAnalyzerPage.render());
    Router.register('password-security', () => PasswordSecurityPage.render());
    Router.register('security-score', () => SecurityScorePage.render());
    Router.register('education', () => EducationPage.render());
    Router.register('scan-history', () => ScanHistoryPage.render());
    Router.register('settings', () => SettingsPage.render());

    // 5. Initialize Router
    Router.init();

    // 6. Global Icon Initialization
    if (window.lucide) {
        window.lucide.createIcons();
    }

    // 7. Silent API Health Check
    API.healthCheck().then(() => {
        const dot = document.querySelector('.system-status .status-dot');
        if (dot) {
            dot.className = 'status-dot online';
        }
    }).catch(() => {
        // Fallback gracefully without breaking UI
        console.warn('Backend API endpoint offline. Running in client heuristic mode.');
    });
});
