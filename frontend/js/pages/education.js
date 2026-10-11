// Education, Interactive Quizzes, and Knowledge Base

const EducationPage = {
    topics: [
        {
            id: 'phishing',
            title: 'Phishing & Spear Phishing',
            category: 'Social Engineering',
            icon: 'mail-warning',
            summary: 'Deceptive messages engineered to hijack login credentials and corporate access.',
            definition: 'Phishing is a social engineering attack where malicious actors impersonate trusted organizations (banks, employers, cloud providers) to manipulate users into disclosing sensitive credentials or installing malware.',
            example: 'An employee receives an email appearing to come from the HR director asking them to review updated bonus benefits via a fake Office 365 login portal.',
            warningSigns: [
                'Generic greetings or slightly altered corporate email domains (e.g., @micros0ft.com)',
                'Urgent calls to action threatening immediate account termination',
                'Hyperlinks pointing to mismatched or unfamiliar hostnames'
            ],
            preventionTips: [
                'Inspect the complete sender email header, not just the display name',
                'Hover over links to preview destination URLs prior to clicking',
                'Enforce FIDO2 hardware keys or authenticator apps rather than SMS OTPs'
            ],
            quiz: [
                {
                    question: 'What is the most secure defense against credential harvesting phishing pages?',
                    options: ['Using longer passwords', 'FIDO2 / WebAuthn Hardware Keys', 'Changing password every 15 days', 'Using Incognito mode'],
                    answer: 1
                },
                {
                    question: 'Which of the following sender addresses is likely fraudulent for PayPal?',
                    options: ['service@paypal.com', 'support@paypal-security-update24.org', 'billing@paypal.co.uk', 'noreply@mail.paypal.com'],
                    answer: 1
                },
                {
                    question: 'Spear phishing differs from standard phishing because:',
                    options: ['It uses automated bots only', 'It specifically targets an individual or organization using tailored reconnaissance', 'It only happens over phone calls', 'It cannot contain links'],
                    answer: 1
                }
            ]
        },
        {
            id: 'ransomware',
            title: 'Ransomware & Malware Defense',
            category: 'Malware Threats',
            icon: 'shield-alert',
            summary: 'Extortion tactics using military-grade encryption against victim files.',
            definition: 'Ransomware is malicious software designed to lock or encrypt a victim’s computer systems and databases until an extortion payment is transferred to cybercriminals.',
            example: 'WannaCry ransomware exploited a Windows SMB vulnerability (EternalBlue) to propagate through enterprise networks and lock healthcare systems worldwide.',
            warningSigns: [
                'Unexpected high CPU or disk write operations while idle',
                'File extensions randomly changing to unfamiliar suffixes (e.g., .locked, .crypt)',
                'Desktop wallpaper replaced with extortion payment instructions'
            ],
            preventionTips: [
                'Implement the 3-2-1 backup strategy (3 copies, 2 different media, 1 immutable offsite)',
                'Disable unauthenticated network services like RDP and legacy SMBv1 on public interfaces',
                'Apply critical security updates promptly across all endpoints'
            ],
            quiz: [
                {
                    question: 'What is the 3-2-1 backup rule?',
                    options: ['3 passwords, 2 emails, 1 computer', '3 copies of data, across 2 different storage media, with 1 stored offsite', 'Backing up every 3 weeks, 2 times, 1 day', '3 cloud accounts, 2 drives, 1 USB'],
                    answer: 1
                },
                {
                    question: 'If infected by ransomware, what is the FIRST recommended immediate step?',
                    options: ['Pay the cryptocurrency ransom immediately', 'Isolate the machine from the local network and Wi-Fi', 'Reboot the system repeatedly', 'Open all encrypted documents'],
                    answer: 1
                }
            ]
        },
        {
            id: 'social-eng',
            title: 'Social Engineering & Smishing',
            category: 'Human Exploits',
            icon: 'message-square-warning',
            summary: 'Psychological manipulation via SMS, voice calls, and urgent impersonations.',
            definition: 'Social engineering exploits psychological vulnerabilities (curiosity, fear, greed, authority) to convince people into circumventing security procedures.',
            example: 'A victim receives a call from a fraudster pretending to be their bank fraud division, requesting the one-time code to cancel a non-existent charge.',
            warningSigns: [
                'Caller demands immediate verification of a 6-digit OTP code',
                'High emotional stimulation: "You will be arrested" or "You have won $100,000"',
                'Unsolicited offers to assist with technical computer problems'
            ],
            preventionTips: [
                'Never recite or share One-Time Passwords (OTPs) with any incoming caller',
                'Hang up and dial the bank back directly through their verified official number',
                'Treat any request demanding immediate secrecy with extreme skepticism'
            ],
            quiz: [
                {
                    question: 'Will legitimate banks ever ask you to read back your SMS OTP over the phone?',
                    options: ['Yes, during fraud disputes', 'No, never under any circumstance', 'Only during business hours', 'Yes, if you forgot your PIN'],
                    answer: 1
                }
            ]
        },
        {
            id: 'passwords-mfa',
            title: 'Credential Security & Modern MFA',
            category: 'Authentication',
            icon: 'key-round',
            summary: 'Building impenetrable defense using password managers and cryptographic authentication.',
            definition: 'Credential hygiene involves generating high-entropy, unique passphrases across every single account, shielded by multi-factor authentication barriers.',
            example: 'A user creates a unique 20-character randomized password for their email, stored in a password manager and secured with a YubiKey.',
            warningSigns: [
                'Using variations of family names, pet names, or sequential digits',
                'Reusing the exact same password for email, banking, and gaming platforms',
                'Relying solely on SMS OTPs vulnerable to SIM swapping'
            ],
            preventionTips: [
                'Transition to passkeys (FIDO2) wherever platforms support it',
                'Store all unique credentials in a zero-knowledge password vault',
                'Monitor haveibeenpwned.com to detect compromised credentials proactively'
            ],
            quiz: [
                {
                    question: 'Why is credential reuse across websites dangerous?',
                    options: ['It uses more RAM', 'A breach on one low-security website allows attackers to access your primary accounts via credential stuffing', 'Websites block shared passwords automatically', 'It makes passwords expire faster'],
                    answer: 1
                }
            ]
        }
    ],

    currentTopic: null,

    render() {
        const container = document.getElementById('pageContainer');
        if (!container) return;

        const completedCount = this.getCompletedTopics().length;
        const total = this.topics.length;
        const progressPercent = Math.round((completedCount / total) * 100);

        container.innerHTML = `
            <div style="display:flex; flex-direction:column; gap:1.5rem;">
                <div class="scanner-header">
                    <h2>Cybersecurity Academy & Knowledge Center</h2>
                    <p>Master defensive cybersecurity practices through practical threat breakdowns and interactive quizzes.</p>
                </div>

                <!-- Progress Header Card -->
                <div class="card" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem;">
                    <div>
                        <h4 style="margin-bottom:0.25rem;">Your Learning Progress</h4>
                        <span style="font-size:0.85rem; color:var(--text-muted);">${completedCount} of ${total} Modules Mastered</span>
                    </div>
                    <div style="width:260px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:0.35rem; font-weight:600;">
                            <span>Completion</span>
                            <span style="color:var(--accent-cyan);">${progressPercent}%</span>
                        </div>
                        <div class="progress-bar-container">
                            <div class="progress-bar-fill" style="width: ${progressPercent}%;"></div>
                        </div>
                    </div>
                </div>

                <div id="educationMainView">
                    <!-- Topics Grid -->
                    <div class="topics-grid">
                        ${this.topics.map(t => {
                            const isDone = this.isTopicCompleted(t.id);
                            return `
                                <div class="topic-card" onclick="EducationPage.openTopic('${t.id}')">
                                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                        <div class="topic-card-icon">
                                            <i data-lucide="${t.icon}"></i>
                                        </div>
                                        ${isDone ? '<span class="badge badge-safe"><i data-lucide="check"></i> Completed</span>' : `<span class="badge badge-low">${sanitizeHTML(t.category)}</span>`}
                                    </div>
                                    <h3 style="font-size:1.1rem; margin-top:0.5rem;">${sanitizeHTML(t.title)}</h3>
                                    <p style="font-size:0.85rem; color:var(--text-secondary); margin:0;">${sanitizeHTML(t.summary)}</p>
                                    <div style="margin-top:auto; padding-top:0.75rem; display:flex; align-items:center; gap:0.4rem; color:var(--accent-cyan); font-size:0.85rem; font-weight:600;">
                                        <span>Start Module</span>
                                        <i data-lucide="chevron-right" style="width:16px;"></i>
                                    </div>
                                </div>
                            `;
                        }).join('')}
                    </div>

                    <!-- Glossary Section -->
                    <div class="card" style="margin-top: 2rem;">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i data-lucide="book-open" style="color:var(--accent-cyan); width:20px;"></i>
                                Cybersecurity Glossary & Quick Reference
                            </h3>
                        </div>
                        <div class="form-group">
                            <input 
                                type="text" 
                                id="glossarySearchInput" 
                                class="input-control" 
                                placeholder="Search security definitions (e.g., Zero-Day, MFA, Phishing, Ransomware)..." 
                                oninput="EducationPage.filterGlossary(this.value)"
                            />
                        </div>
                        <div id="glossaryList" style="display:grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap:1rem; margin-top:1rem;">
                            ${this.renderGlossaryItems()}
                        </div>
                    </div>
                </div>

                <div id="educationDetailView" style="display:none;"></div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons();
    },

    glossaryTerms: [
        { term: 'Zero-Day (0-Day)', desc: 'A software security vulnerability that is unpatched and unknown to the vendor, leaving users exposed to exploit.' },
        { term: 'MFA / 2FA', desc: 'Multi-Factor Authentication requiring 2 or more distinct verification factors to authorize an account login.' },
        { term: 'Passkeys', desc: 'Cryptographic credentials based on FIDO standards that eliminate traditional passwords using asymmetric public-key cryptography.' },
        { term: 'DDoS Attack', desc: 'Distributed Denial of Service attack flooding target servers with coordinated bot traffic to crash public accessibility.' },
        { term: 'Homograph Attack', desc: 'Registering deceptive domains with identical-looking Cyrillic or Unicode characters to fool unsuspecting users.' },
        { term: 'Brute Force', desc: 'An automated trial-and-error method used by hackers to guess combinations of passcodes or cryptographic keys.' }
    ],

    renderGlossaryItems(filter = '') {
        const query = filter.toLowerCase().trim();
        const filtered = this.glossaryTerms.filter(g => g.term.toLowerCase().includes(query) || g.desc.toLowerCase().includes(query));

        if (filtered.length === 0) {
            return '<p style="color:var(--text-muted); font-size:0.85rem;">No matching cybersecurity definitions found.</p>';
        }

        return filtered.map(item => `
            <div style="padding:1rem; border-radius:var(--radius-md); background:rgba(255,255,255,0.02); border:1px solid var(--border-color);">
                <strong style="color:var(--accent-cyan); font-size:0.95rem; display:block; margin-bottom:0.25rem;">${sanitizeHTML(item.term)}</strong>
                <p style="font-size:0.8rem; color:var(--text-secondary); margin:0;">${sanitizeHTML(item.desc)}</p>
            </div>
        `).join('');
    },

    filterGlossary(query) {
        const list = document.getElementById('glossaryList');
        if (list) list.innerHTML = this.renderGlossaryItems(query);
    },

    openTopic(topicId) {
        const topic = this.topics.find(t => t.id === topicId);
        if (!topic) return;

        this.currentTopic = topic;
        const mainView = document.getElementById('educationMainView');
        const detailView = document.getElementById('educationDetailView');

        mainView.style.display = 'none';
        detailView.style.display = 'block';

        detailView.innerHTML = `
            <div class="topic-detail-view">
                <button type="button" class="btn btn-secondary btn-sm" onclick="EducationPage.closeTopic()" style="align-self:flex-start;">
                    <i data-lucide="arrow-left"></i>
                    <span>Back to Topics</span>
                </button>

                <div class="card">
                    <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:1rem;">
                        <div class="topic-card-icon"><i data-lucide="${topic.icon}"></i></div>
                        <div>
                            <h2 style="margin:0;">${sanitizeHTML(topic.title)}</h2>
                            <span class="badge badge-low" style="margin-top:0.25rem;">${sanitizeHTML(topic.category)}</span>
                        </div>
                    </div>

                    <div style="margin-bottom:1.5rem;">
                        <h4 style="color:var(--accent-cyan); margin-bottom:0.4rem;">Overview & Definition</h4>
                        <p>${sanitizeHTML(topic.definition)}</p>
                    </div>

                    <div style="margin-bottom:1.5rem; background:rgba(255,255,255,0.02); padding:1rem; border-radius:var(--radius-md); border-left:3px solid var(--accent-purple);">
                        <h4 style="color:var(--accent-purple); margin-bottom:0.4rem;">Real-World Case Example</h4>
                        <p style="font-style:italic; margin:0;">"${sanitizeHTML(topic.example)}"</p>
                    </div>

                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.25rem; margin-bottom:1.5rem;">
                        <div>
                            <h4 style="color:var(--accent-red); margin-bottom:0.75rem; display:flex; align-items:center; gap:0.4rem;">
                                <i data-lucide="alert-triangle"></i> Warning Signs
                            </h4>
                            <div class="indicator-list">
                                ${topic.warningSigns.map(w => createIndicatorItem(w)).join('')}
                            </div>
                        </div>

                        <div>
                            <h4 style="color:var(--accent-green); margin-bottom:0.75rem; display:flex; align-items:center; gap:0.4rem;">
                                <i data-lucide="shield-check"></i> Actionable Prevention Tips
                            </h4>
                            <div class="recommendation-list">
                                ${topic.preventionTips.map(p => createRecommendationItem(p)).join('')}
                            </div>
                        </div>
                    </div>

                    <!-- Interactive Quiz -->
                    <div style="margin-top:2rem; padding-top:1.5rem; border-top:1px solid var(--border-color);">
                        <h3 style="margin-bottom:1rem; display:flex; align-items:center; gap:0.5rem;">
                            <i data-lucide="help-circle" style="color:var(--accent-yellow);"></i>
                            Knowledge Verification Quiz
                        </h3>
                        <div id="topicQuizContainer">
                            ${topic.quiz.map((q, qIndex) => `
                                <div style="margin-bottom:1.5rem;">
                                    <div style="font-weight:600; margin-bottom:0.5rem; font-size:0.95rem;">
                                        Q${qIndex + 1}: ${sanitizeHTML(q.question)}
                                    </div>
                                    <div>
                                        ${q.options.map((opt, optIndex) => `
                                            <button 
                                                type="button" 
                                                class="quiz-option-choice" 
                                                id="q-${qIndex}-opt-${optIndex}"
                                                onclick="EducationPage.answerQuiz('${topic.id}', ${qIndex}, ${optIndex}, ${q.answer})"
                                            >
                                                ${sanitizeHTML(opt)}
                                            </button>
                                        `).join('')}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;

        if (window.lucide) window.lucide.createIcons({ root: detailView });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    answerQuiz(topicId, questionIndex, selectedOption, correctOption) {
        const btn = document.getElementById(`q-${questionIndex}-opt-${selectedOption}`);
        if (!btn) return;

        // Disable options for this question
        const topic = this.topics.find(t => t.id === topicId);
        topic.quiz[questionIndex].options.forEach((_, idx) => {
            const b = document.getElementById(`q-${questionIndex}-opt-${idx}`);
            if (b) b.disabled = true;
        });

        if (selectedOption === correctOption) {
            btn.classList.add('correct');
            showToast('Correct answer! Excellent discernment.', 'success');
            this.markTopicCompleted(topicId);
        } else {
            btn.classList.add('wrong');
            const correctBtn = document.getElementById(`q-${questionIndex}-opt-${correctOption}`);
            if (correctBtn) correctBtn.classList.add('correct');
            showToast('Incorrect answer. Review the prevention tips above.', 'warning');
        }
    },

    closeTopic() {
        this.render();
    },

    getCompletedTopics() {
        try {
            return JSON.parse(localStorage.getItem('cybershield_completed_topics') || '[]');
        } catch (_) {
            return [];
        }
    },

    isTopicCompleted(id) {
        return this.getCompletedTopics().includes(id);
    },

    markTopicCompleted(id) {
        const completed = this.getCompletedTopics();
        if (!completed.includes(id)) {
            completed.push(id);
            localStorage.setItem('cybershield_completed_topics', JSON.stringify(completed));
        }
    }
};
