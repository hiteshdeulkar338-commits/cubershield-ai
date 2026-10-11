"""
CyberShield AI - Cybersecurity Education & Awareness Routes
Provides educational modules, real-world case studies, interactive quizzes,
and a comprehensive cybersecurity glossary tailored for beginners and engineering students.
"""

from flask import Blueprint, request, jsonify

education_bp = Blueprint("education", __name__)

# Detailed list of educational topics
EDUCATION_TOPICS = [
    {
        "id": "phishing",
        "title": "Phishing Attacks",
        "icon": "mail-warning",
        "description": "Learn how attackers deceive victims into revealing credentials or installing malware via fraudulent communications.",
        "difficulty": "Beginner",
        "reading_time": "5 min",
        "definition": "Phishing is a social engineering attack where an attacker masquerades as a trusted entity (such as a bank, utility provider, or college portal) to deceive individuals into divulging sensitive information like usernames, passwords, or credit card numbers.",
        "example": "An employee receives an email appearing to come from 'IT-Helpdesk@company-support-desk.com' stating their password will expire in 2 hours. Clicking the link opens a cloned login form that captures their network credentials.",
        "warning_signs": [
            "Urgent deadlines demanding immediate action under threat of penalties or account closure.",
            "Sender email address looks slightly misspelled (e.g. support@paypa1.com instead of paypal.com).",
            "Generic greetings like 'Dear Valued Customer' instead of your registered name.",
            "Mismatched hyperlinks where the displayed text differs from the actual underlying URL.",
            "Unexpected attachments with extensions like .zip, .exe, or macro-enabled .docm."
        ],
        "prevention": [
            "Never click on links in unsolicited emails; navigate to the official portal manually.",
            "Always inspect the domain name in your browser's address bar before typing passwords.",
            "Enable Multi-Factor Authentication (MFA) so stolen passwords alone cannot grant access.",
            "Report phishing emails to your organization's IT security team or email provider."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "What is the primary objective of a phishing email?",
                "options": [
                    "To speed up your internet connection",
                    "To trick you into revealing sensitive credentials or downloading malware",
                    "To test your monitor display calibration",
                    "To update your computer's BIOS automatically"
                ],
                "correct_index": 1,
                "explanation": "Phishing relies on psychological manipulation to harvest login credentials, payment information, or infect systems."
            },
            {
                "id": "q2",
                "question": "Which of the following sender domains is most likely a phishing attempt impersonating State Bank of India?",
                "options": [
                    "support@onlinesbi.sbi",
                    "alerts@sbi.co.in",
                    "sbi-kyc-update@gmail.com",
                    "customercare@sbi.co.in"
                ],
                "correct_index": 2,
                "explanation": "Legitimate banking institutions never dispatch account compliance alerts from free public email providers like Gmail."
            },
            {
                "id": "q3",
                "question": "What is 'Spear Phishing'?",
                "options": [
                    "Phishing conducted strictly over satellite phones",
                    "A targeted phishing attack customized for a specific individual or organization",
                    "Spam emails sent randomly to millions of addresses",
                    "An attack that only targets computer hardware manufacturers"
                ],
                "correct_index": 1,
                "explanation": "Spear phishing uses tailored personal or corporate context to deceive high-value specific individuals."
            }
        ]
    },
    {
        "id": "password-security",
        "title": "Password Security",
        "icon": "key-round",
        "description": "Master passphrases, entropy, avoiding credential stuffing, and leveraging password managers.",
        "difficulty": "Beginner",
        "reading_time": "4 min",
        "definition": "Password security involves using strong, unique passphrases that resist automated guessing (brute force and dictionary attacks) combined with credential isolation across different services.",
        "example": "A user used 'Password123!' on both a minor gaming forum and their primary Google account. When the forum suffered a data leak, hackers used automated tools (credential stuffing) to take over their Google account.",
        "warning_signs": [
            "Using predictable patterns such as birthdays, pet names, or sequential digits (123456).",
            "Reusing the exact same password on more than one web application.",
            "Storing unencrypted passwords in plaintext text files or sticky notes on monitors.",
            "Receiving notification emails about login attempts from unrecognized geographic locations."
        ],
        "prevention": [
            "Use passphrases composed of 4+ random words (e.g. 'purple-elephant-guitar-bridge') for high entropy.",
            "Use a trusted open-source or audited password manager (like Bitwarden) to generate 16+ char random passwords.",
            "Never share passwords over chat, email, or telephone calls.",
            "Check haveibeenpwned.com periodically to audit if your accounts were involved in third-party data breaches."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Which password possesses the highest resistance to brute-force cracking?",
                "options": [
                    "Admin2024!",
                    "correct-horse-battery-staple",
                    "qwertyuiop",
                    "P@ssw0rd1"
                ],
                "correct_index": 1,
                "explanation": "Long passphrases have significantly higher mathematical entropy than short words with common character substitutions."
            },
            {
                "id": "q2",
                "question": "Why is password reuse across multiple sites dangerous?",
                "options": [
                    "It makes typing the password slower",
                    "A breach at one insecure website compromises all your other accounts",
                    "It causes browser tabs to crash",
                    "It consumes double the local disk space"
                ],
                "correct_index": 1,
                "explanation": "Attackers run automated credential stuffing attacks testing leaked username/password combos across popular platforms."
            },
            {
                "id": "q3",
                "question": "What is the primary benefit of using a password manager?",
                "options": [
                    "You only need to memorize one master passphrase while using unique complex passwords everywhere",
                    "It bypasses all website captchas automatically",
                    "It encrypts your physical monitor screen",
                    "It prevents your computer from overheating"
                ],
                "correct_index": 0,
                "explanation": "A password manager encrypts unique, complex passwords in a secure local or cloud vault secured by a single master key."
            }
        ]
    },
    {
        "id": "social-engineering",
        "title": "Social Engineering",
        "icon": "users",
        "description": "Understand psychological manipulation techniques used by threat actors to bypass technical defenses.",
        "difficulty": "Intermediate",
        "reading_time": "6 min",
        "definition": "Social engineering is the psychological manipulation of people into performing actions or divulging confidential information. It targets human cognitive biases—such as authority, trust, fear, and curiosity—rather than software vulnerabilities.",
        "example": "A caller claiming to be a senior executive calls the corporate finance desk demanding an urgent vendor payment before closing time, invoking authority and anxiety to bypass standard multi-signature approval rules.",
        "warning_signs": [
            "Requests to bypass standard organizational protocols or verification procedures.",
            "Aggressive insistence on speed, secrecy, or severe consequences if you hesitate.",
            "Unsolicited offers of help for problems you did not report.",
            "Flattery or excessive friendliness aimed at lowering your natural defense barriers."
        ],
        "prevention": [
            "Establish out-of-band verification procedures (confirming requests via a known secondary contact number).",
            "Slow down when someone pressures you to act quickly.",
            "Follow company and operational policies strictly without making informal exceptions.",
            "Always verify the caller's identity through official organizational directories."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "What human factor does social engineering exploit most commonly?",
                "options": [
                    "Processor clock frequency",
                    "Human trust, fear, authority, and urgency",
                    "Compiler optimizations",
                    "Network cable bandwidth"
                ],
                "correct_index": 1,
                "explanation": "Social engineering targets human psychology and cognitive shortcuts rather than hardware or software logic."
            },
            {
                "id": "q2",
                "question": "What is 'Pretexting' in the context of cyber attacks?",
                "options": [
                    "Sending text messages before making a phone call",
                    "Inventing an elaborate scenario or persona to manipulate the target into compliance",
                    "Converting text files into binary format",
                    "Writing code documentation before developing software"
                ],
                "correct_index": 1,
                "explanation": "Pretexting involves creating an invented scenario (the pretext) where the attacker pretends to be an auditor, technician, or law enforcement official."
            },
            {
                "id": "q3",
                "question": "What should you do if an unexpected caller demands urgent wire transfers while claiming to be your CEO?",
                "options": [
                    "Transfer the funds immediately to avoid being fired",
                    "Verify the request through a verified alternate communication channel before taking action",
                    "Post the details on your personal social media feed",
                    "Shut down your computer and disconnect the power cord"
                ],
                "correct_index": 1,
                "explanation": "Always authenticate unusual high-impact financial instructions out-of-band using known verified channels."
            }
        ]
    },
    {
        "id": "malware",
        "title": "Malware & Trojans",
        "icon": "bug",
        "description": "Examine viruses, worms, keyloggers, and trojan horses and how they establish persistence on target systems.",
        "difficulty": "Intermediate",
        "reading_time": "6 min",
        "definition": "Malware (malicious software) is any software intentionally designed to cause damage to a computer, server, client, or computer network, including exfiltrating confidential data or granting unauthorized remote access.",
        "example": "A student downloads a pirated 'cracked' version of video editing software from an untrusted forum. The installer secretly drops a background keylogger that logs every keystroke and sends passwords to an attacker's command-and-control server.",
        "warning_signs": [
            "Sudden CPU or RAM spikes, cooling fans running loudly while the computer is idle.",
            "Browser redirecting searches to unknown search engines or spam ad portals.",
            "Disabled antivirus or security software that cannot be restarted.",
            "New unrecognized desktop icons, startup applications, or browser toolbars."
        ],
        "prevention": [
            "Never download pirated software, cracked games, or questionable torrent payloads.",
            "Keep Windows Defender or reputable endpoint protection enabled and updated.",
            "Avoid enabling macros on Office documents received from unknown internet senders.",
            "Inspect running processes in Task Manager for suspicious unsigned binaries."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "What is the key difference between a computer virus and a computer worm?",
                "options": [
                    "Worms only infect mobile phones, while viruses only infect mainframes",
                    "A virus requires human execution or host file attachment, while a worm replicates autonomously across networks",
                    "Viruses are written in C, while worms are written in Python",
                    "Worms cannot cause any damage to data"
                ],
                "correct_index": 1,
                "explanation": "Worms are self-replicating programs that propagate autonomously over network vulnerabilities without needing user interaction."
            },
            {
                "id": "q2",
                "question": "What does a Trojan Horse program do?",
                "options": [
                    "It displays a picture of a wooden horse on your screen",
                    "It disguises itself as legitimate or desirable software while concealing malicious functionality",
                    "It protects your system against external intrusions",
                    "It speeds up network data compression"
                ],
                "correct_index": 1,
                "explanation": "Trojan horses masquerade as benign software (e.g. games, utilities) to trick users into executing them."
            },
            {
                "id": "q3",
                "question": "What is the primary function of a keylogger?",
                "options": [
                    "To generate cryptographic keys for encryption",
                    "To covertly capture and log keystrokes typed by the user",
                    "To fix sticky mechanical keyboard keys",
                    "To lock the keyboard when the screen turns off"
                ],
                "correct_index": 1,
                "explanation": "Keyloggers record keyboard input to capture passwords, credit card numbers, and private conversations."
            }
        ]
    },
    {
        "id": "ransomware",
        "title": "Ransomware Defense",
        "icon": "shield-alert",
        "description": "How cryptoviral extortion attacks work, their delivery vectors, and effective disaster recovery strategies.",
        "difficulty": "Intermediate",
        "reading_time": "6 min",
        "definition": "Ransomware is a category of malware that employs asymmetric cryptography to encrypt a victim's files and documents, demanding a ransom payment (often in cryptocurrency) in exchange for the decryption key.",
        "example": "A hospital's server is infected via an exposed Remote Desktop Protocol (RDP) port. Within hours, patient databases are encrypted with a .locked extension, displaying a ransom note demanding 5 Bitcoin.",
        "warning_signs": [
            "Files suddenly displaying strange unfamiliar file extensions (.locked, .crypt, .wnry).",
            "Text files or wallpaper images detailing payment instructions and countdown timers.",
            "Sudden loss of access to shared network drives and cloud sync storage.",
            "High disk write activity and rapid disappearance of file thumbnail previews."
        ],
        "prevention": [
            "Follow the 3-2-1 backup strategy: 3 copies of data, across 2 different media types, with 1 copy stored completely offline/air-gapped.",
            "Never expose RDP (Remote Desktop Protocol) directly to the public internet.",
            "Keep software and operating systems patched against known Remote Code Execution (RCE) flaws.",
            "Do not pay ransoms; payment does not guarantee decryption key delivery and funds cybercriminal organizations."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "What is the most effective safeguard for surviving a ransomware infection without paying ransom?",
                "options": [
                    "Paying half of the requested ransom immediately",
                    "Maintaining immutable, offline/air-gapped data backups",
                    "Restarting the computer repeatedly",
                    "Deleting your browser history"
                ],
                "correct_index": 1,
                "explanation": "Offline or immutable backups allow complete system restoration without succumbing to extortion demands."
            },
            {
                "id": "q2",
                "question": "What is 'Double Extortion' in modern ransomware operations?",
                "options": [
                    "Asking for payment in both Bitcoin and Ethereum simultaneously",
                    "Encrypting data AND threatening to leak confidential exfiltrated records publicly",
                    "Charging double fees for credit card processing",
                    "Infecting two computers in the same household"
                ],
                "correct_index": 1,
                "explanation": "In double extortion, threat actors exfiltrate sensitive files before encrypting them, threatening public release if the ransom is not paid."
            },
            {
                "id": "q3",
                "question": "Why do security agencies and law enforcement advise AGAINST paying ransomware demands?",
                "options": [
                    "Payment guarantees you will be targeted again and finances future criminal operations",
                    "Cryptocurrency payments cause system hardware damage",
                    "Ransom payments are illegal only in Antarctica",
                    "The decryptor keys never work under any circumstances"
                ],
                "correct_index": 0,
                "explanation": "Paying ransoms fuels cybercrime syndicates and marks the victim organization as a willing payer for future attacks."
            }
        ]
    },
    {
        "id": "identity-theft",
        "title": "Identity Theft & Privacy",
        "icon": "user-x",
        "description": "Techniques used to compromise personal identities, financial fraud, and preventative identity hygiene.",
        "difficulty": "Beginner",
        "reading_time": "5 min",
        "definition": "Identity theft occurs when someone unlawfully acquires and uses another individual's personal identification data—such as Social Security Number, PAN, Aadhaar, date of birth, or banking records—to commit fraud or obtain unauthorized credit.",
        "example": "A fraudster obtains a photocopy of an individual's PAN card and Aadhaar card discarded in the trash, submits a fraudulent SIM swap request at a telecom retail store, and intercepts banking OTPs to drain savings accounts.",
        "warning_signs": [
            "Receiving credit card statements or loan approval letters for accounts you never opened.",
            "Unexplained withdrawals or mysterious micro-debits on bank accounts.",
            "Your mobile SIM suddenly losing cellular network connectivity (possible SIM swap attack).",
            "Collection agency calls inquiring about debts you have never incurred."
        ],
        "prevention": [
            "Shred physical mail and utility bills containing personal data before disposal.",
            "Lock your Aadhaar biometrics using the official UIDAI portal or mAadhaar app when not in use.",
            "Never post boarding passes, passport pages, or tax forms on social media.",
            "Regularly monitor your credit reports (CIBIL, Experian) for unauthorized inquiries."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "What is a 'SIM Swap' attack?",
                "options": [
                    "Upgrading your SIM from 4G to 5G",
                    "Fraudulently transferring a victim's phone number to a criminal's SIM card to intercept SMS OTPs",
                    "Trading physical SIM cards with friends",
                    "Cleaning the golden contacts on your SIM card"
                ],
                "correct_index": 1,
                "explanation": "A SIM swap enables attackers to hijack phone numbers and intercept authentication codes and 2FA tokens."
            },
            {
                "id": "q2",
                "question": "What is the purpose of UIDAI's 'Masked Aadhaar' feature in India?",
                "options": [
                    "It conceals your photo completely",
                    "It masks the first 8 digits of your 12-digit Aadhaar number, revealing only the last 4 digits for enhanced privacy",
                    "It changes your name to an anonymous pseudonym",
                    "It makes the Aadhaar card valid only for online shopping"
                ],
                "correct_index": 1,
                "explanation": "Masked Aadhaar shields the primary 8 digits, mitigating risk if photocopies are mishandled by third-party vendors."
            },
            {
                "id": "q3",
                "question": "Which document should you NEVER share publicly on social media?",
                "options": [
                    "A picture of your college campus cafeteria",
                    "Your boarding pass barcode or identity documents",
                    "A review of a public park",
                    "A photograph of your bicycle"
                ],
                "correct_index": 1,
                "explanation": "Boarding pass barcodes and ID cards encode sensitive personal identification records easily decoded by scanners."
            }
        ]
    },
    {
        "id": "upi-fraud",
        "title": "UPI & Mobile Payment Fraud",
        "icon": "credit-card",
        "description": "Understanding UPI payment architecture, reverse QR scams, PIN deception, and Indian cybercrime mitigation.",
        "difficulty": "Beginner",
        "reading_time": "5 min",
        "definition": "UPI (Unified Payments Interface) fraud encompasses deceptive techniques where scammers exploit misunderstanding of UPI architecture—specifically the absolute rule that entering a UPI PIN is only required to send/debit money, never to receive money.",
        "example": "A seller on an online marketplace (OLX) is contacted by a buyer offering to pay an advance. The buyer sends a QR code claiming 'Scan this QR code and enter your PIN to receive Rs. 5,000'. The moment the seller inputs their PIN, Rs. 5,000 is deducted from their bank account.",
        "warning_signs": [
            "Anyone instructing you to enter your UPI PIN, MPIN, or password to 'claim', 'receive', or 'credit' money.",
            "Receiving 'Collect Request' notifications on Google Pay, PhonePe, or Paytm from unverified strangers.",
            "Calls claiming to be customer support asking you to install AnyDesk, TeamViewer, or QuickSupport.",
            "Offers of cashback or lottery rewards requiring an initial UPI transfer."
        ],
        "prevention": [
            "GOLDEN RULE: You NEVER enter your UPI PIN to receive money. Receiving funds requires zero action from your end.",
            "Never scan a QR code sent over WhatsApp or SMS to receive funds.",
            "Do not install remote screen-sharing tools under any circumstances.",
            "If defrauded, immediately dial the Indian National Cyber Crime Helpline at 1930 and freeze the transaction."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "When is entering your UPI PIN necessary?",
                "options": [
                    "When receiving cashback into your account",
                    "ONLY when sending/debiting money from your own bank account",
                    "When receiving payments from customers",
                    "When checking if your internet connection is active"
                ],
                "correct_index": 1,
                "explanation": "The UPI protocol only asks for a PIN when authorising a debit from your linked bank account."
            },
            {
                "id": "q2",
                "question": "What is the emergency helpline number in India to report online financial cyber fraud within the golden hour?",
                "options": [
                    "100",
                    "1930",
                    "108",
                    "911"
                ],
                "correct_index": 1,
                "explanation": "Helpline 1930 connects directly to the Indian Cyber Crime Coordination Centre (I4C) for quick transaction freezing."
            },
            {
                "id": "q3",
                "question": "A buyer on OLX sends you a QR code to receive payment. What will happen if you scan it and enter your PIN?",
                "options": [
                    "The payment will be instantly credited to your bank account",
                    "Your bank account will be DEBITED by that amount",
                    "The transaction will be rejected by NPCI automatically",
                    "You will receive double cashback"
                ],
                "correct_index": 1,
                "explanation": "Scanning a QR code and entering your PIN approves a transfer OUT of your account to the recipient."
            }
        ]
    },
    {
        "id": "public-wifi",
        "title": "Public Wi-Fi Risks",
        "icon": "wifi-off",
        "description": "Examine Evil Twin attacks, Man-in-the-Middle (MITM) snooping, packet sniffing, and secure tunnel defense.",
        "difficulty": "Intermediate",
        "reading_time": "5 min",
        "definition": "Public Wi-Fi risks refer to vulnerabilities inherent in unencrypted or shared wireless networks (airports, cafes, hotels) where malicious actors on the same local network can intercept traffic, inject payloads, or stage Evil Twin access points.",
        "example": "A traveler connects to an open Wi-Fi network named 'Airport_Free_WiFi_Official' created by an attacker using a Wi-Fi Pineapple router. The attacker inspects all unencrypted HTTP requests and spoofs DNS queries.",
        "warning_signs": [
            "Connecting to an open network that requires zero password or portal verification.",
            "Multiple Wi-Fi networks in the same location having nearly identical names.",
            "Browser displaying SSL/TLS certificate warning popups ('Your connection is not private').",
            "Device automatically connecting to open Wi-Fi networks without your permission."
        ],
        "prevention": [
            "Use a trusted Virtual Private Network (VPN) to encapsulate all network traffic inside an encrypted tunnel.",
            "Turn off 'Auto-connect to open Wi-Fi' in your smartphone and laptop Wi-Fi settings.",
            "Ensure websites utilize HTTPS before transmitting any credentials or credit card info.",
            "Use mobile cellular data tethering (hotspot) instead of public networks for banking activities."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "What is an 'Evil Twin' Wi-Fi attack?",
                "options": [
                    "A computer virus that infects two routers simultaneously",
                    "A fraudulent rogue Wi-Fi hotspot configured to mimic a legitimate network's SSID",
                    "Having two passwords for the same router",
                    "A router manufactured with defective antenna components"
                ],
                "correct_index": 1,
                "explanation": "An Evil Twin rogue AP broadcasts the same SSID as a legitimate hotspot to trick nearby devices into connecting through the attacker."
            },
            {
                "id": "q2",
                "question": "How does a Virtual Private Network (VPN) protect you on open Wi-Fi?",
                "options": [
                    "It charges your laptop battery faster",
                    "It encrypts your internet traffic end-to-end, preventing local network eavesdroppers from viewing data packets",
                    "It removes all spam emails from your inbox",
                    "It blocks physical cameras in the coffee shop"
                ],
                "correct_index": 1,
                "explanation": "VPNs create an encrypted cryptographic tunnel between your machine and the VPN endpoint, shielding traffic from local eavesdroppers."
            },
            {
                "id": "q3",
                "question": "If your browser warns that a website's SSL certificate is invalid while you are on cafe Wi-Fi, you should:",
                "options": [
                    "Click 'Proceed Anyway' because cafe connections are always fine",
                    "Disconnect immediately; an attacker may be conducting a Man-in-the-Middle (MITM) SSL interception",
                    "Turn your screen brightness to maximum",
                    "Clear your printer cache"
                ],
                "correct_index": 1,
                "explanation": "Certificate warnings on public Wi-Fi frequently signify SSL stripping or active Man-in-the-Middle certificate substitution."
            }
        ]
    },
    {
        "id": "two-factor-auth",
        "title": "Two-Factor Authentication",
        "icon": "shield-check",
        "description": "Explore the mechanisms of 2FA/MFA: SMS OTPs vs TOTP Authenticator apps vs FIDO2 hardware security keys.",
        "difficulty": "Beginner",
        "reading_time": "4 min",
        "definition": "Two-Factor Authentication (2FA) is a security process where a user provides two distinct authentication factors to verify identity, requiring something you know (password), something you have (phone/token), or something you are (biometrics).",
        "example": "An attacker obtains an engineer's GitHub password via a third-party breach. However, when attempting to sign in, GitHub prompts for a 6-digit TOTP code generated on the engineer's physical phone, completely blocking the attacker.",
        "warning_signs": [
            "Relying solely on passwords for critical email, financial, and code repository accounts.",
            "Receiving unexpected 2FA push notifications or SMS codes when you are not actively logging in.",
            "Using SMS-based OTP for high-value accounts when SIM swap attacks are prevalent.",
            "Storing recovery backup codes in plaintext in the same cloud drive as your passwords."
        ],
        "prevention": [
            "Enable 2FA across all essential online accounts starting with primary email and password manager.",
            "Prefer Time-based One-Time Password (TOTP) apps (Google Authenticator, Aegis, Ente Auth) over SMS.",
            "For highest security, use FIDO2/WebAuthn hardware keys (YubiKey) which are immune to phishing proxy attacks.",
            "Print recovery backup codes and store them in a secure physical location."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "Why is an app-based TOTP code (like Google Authenticator) more secure than an SMS OTP?",
                "options": [
                    "SMS OTPs are slower to arrive",
                    "SMS messages can be intercepted via SIM swapping and SS7 network vulnerabilities, whereas TOTP keys remain securely on the device",
                    "Authenticator apps do not require battery power",
                    "SMS codes can only be four digits long"
                ],
                "correct_index": 1,
                "explanation": "SMS relies on cellular telecommunications infrastructure vulnerable to SIM swaps, social engineering, and SS7 routing interception."
            },
            {
                "id": "q2",
                "question": "What are the three canonical authentication factors?",
                "options": [
                    "Length, Complexity, Expiration",
                    "Something you know, something you have, something you are",
                    "Username, Domain, Protocol",
                    "Public key, Private key, Symmetric key"
                ],
                "correct_index": 1,
                "explanation": "Multi-factor authentication requires combining knowledge (passwords), possession (token/phone), or inherence (fingerprint/biometrics)."
            },
            {
                "id": "q3",
                "question": "You receive an unsolicited 2FA code notification for your banking app while having lunch. What does this mean?",
                "options": [
                    "The bank is testing their SMS delivery servers",
                    "Someone knows your password and is actively attempting to authenticate as you",
                    "Your smartphone has run out of memory",
                    "Your phone number has been deleted from the database"
                ],
                "correct_index": 1,
                "explanation": "An unsolicited 2FA prompt indicates that an adversary has already entered your valid password and hit the second authentication barrier."
            }
        ]
    },
    {
        "id": "online-privacy",
        "title": "Online Privacy & Digital Footprint",
        "icon": "eye-off",
        "description": "Techniques to minimize digital footprints, manage ad trackers, browser fingerprinting, and application permissions.",
        "difficulty": "Intermediate",
        "reading_time": "5 min",
        "definition": "Online privacy involves your ability to control what information you share on the internet, who has access to your personal browsing telemetry, and how tracking algorithms create behavioural profiles from your digital footprint.",
        "example": "A user installs a flashlight app that requests permissions for Contacts, Microphone, Camera, and Precise Location. The app sells the user's location coordinates and address book data to programmatic advertising brokers.",
        "warning_signs": [
            "Apps demanding invasive permissions that have no relevance to their core functionality.",
            "Targeted ads appearing for items discussed in proximity to unvetted mobile apps.",
            "Public social media profiles displaying birthdays, hometowns, school names, and family relations.",
            "Reusing public usernames across every platform allowing easy cross-site profiling (OSINT)."
        ],
        "prevention": [
            "Audit application permissions in smartphone settings; revoke Camera, Microphone, and Location when unnecessary.",
            "Use privacy-focused browsers or extensions (like uBlock Origin) to neutralize cross-site trackers.",
            "Separate your personal email address from throwaway registrations using email aliasing tools.",
            "Regularly delete unused online accounts to reduce your attack surface."
        ],
        "quiz": [
            {
                "id": "q1",
                "question": "What is 'Browser Fingerprinting'?",
                "options": [
                    "Scanning physical fingerprints onto the glass screen of your phone",
                    "Collecting browser configuration details (screen resolution, fonts, GPU, extensions) to uniquely identify a user without cookies",
                    "Cleaning fingerprint smudges off your laptop monitor",
                    "Typing with only your thumb and index fingers"
                ],
                "correct_index": 1,
                "explanation": "Fingerprinting synthesizes dozens of client environment parameters to track devices across websites even when cookies are blocked."
            },
            {
                "id": "q2",
                "question": "Why should you regularly review application permissions on your smartphone?",
                "options": [
                    "To free up space on your micro SD card",
                    "To prevent rogue apps from harvesting contacts, location, microphone audio, and camera access without need",
                    "To make the phone's speaker volume louder",
                    "To change the color of app icons"
                ],
                "correct_index": 1,
                "explanation": "Restricting app permissions enforces the Principle of Least Privilege, preventing unauthorized data exfiltration."
            },
            {
                "id": "q3",
                "question": "What is OSINT (Open Source Intelligence)?",
                "options": [
                    "Operating System Internal Network Table",
                    "Information gathered from publicly available sources (social media, public records, forums) used in research or targeting",
                    "Open Source software development for artificial intelligence",
                    "A protocol for encrypting optical storage disks"
                ],
                "correct_index": 1,
                "explanation": "OSINT involves collecting and correlating publicly available data to build detailed intelligence profiles on targets."
            }
        ]
    }
]

# Comprehensive Cybersecurity Glossary (32 terms)
GLOSSARY_TERMS = [
    {"term": "2FA (Two-Factor Authentication)", "category": "Authentication", "definition": "A security procedure requiring two distinct forms of identification before granting access.", "example": "Typing a password and then entering a 6-digit code from an authenticator app."},
    {"term": "Air-Gapped System", "category": "Network Security", "definition": "A computer or network completely isolated from the internet and all unsecured networks.", "example": "Industrial control systems managing nuclear facilities are typically air-gapped."},
    {"term": "Antivirus", "category": "Endpoint Defense", "definition": "Software designed to detect, isolate, and remove computer viruses and other malicious software.", "example": "Windows Defender continuously monitoring disk writes for known signatures."},
    {"term": "API Key", "category": "Application Security", "definition": "A unique code passed by an application to verify the caller's identity when calling an API.", "example": "Never commit OpenAI or Stripe API keys to public GitHub repositories."},
    {"term": "Asymmetric Encryption", "category": "Cryptography", "definition": "Cryptographic system using a pair of mathematically linked keys: a public key for encryption and a private key for decryption.", "example": "RSA, ECC, and HTTPS/TLS handshakes."},
    {"term": "Botnet", "category": "Threats", "definition": "A network of compromised computers or IoT devices controlled collectively by an attacker.", "example": "The Mirai botnet orchestrated massive distributed denial of service attacks using hacked webcams."},
    {"term": "Brute Force Attack", "category": "Attacks", "definition": "A trial-and-error method used by automated software to guess passwords or cryptographic keys by checking every possible combination.", "example": "Trying all 8-character numeric combinations from 00000000 to 99999999."},
    {"term": "Buffer Overflow", "category": "Vulnerabilities", "definition": "A vulnerability occurring when a program writes more data to a buffer than it was allocated, overwriting adjacent memory.", "example": "Improper use of strcpy() in C leading to remote code execution."},
    {"term": "Cross-Site Scripting (XSS)", "category": "Web Security", "definition": "An injection attack where malicious scripts are injected into trusted web applications viewed by other users.", "example": "Injecting `<script>stealCookie()</script>` into a vulnerable comment forum."},
    {"term": "Credential Stuffing", "category": "Attacks", "definition": "Automated injection of breached username/password pairs into website login forms to gain unauthorized access.", "example": "Testing credentials dumped from one breach against streaming platforms and banking portals."},
    {"term": "CSRF (Cross-Site Request Forgery)", "category": "Web Security", "definition": "An attack forcing an authenticated end user to execute unwanted actions on a web application.", "example": "A malicious site submitting a fund transfer form on a bank tab where the victim is already logged in."},
    {"term": "DDoS (Distributed Denial of Service)", "category": "Network Security", "definition": "An attempt to overwhelm a targeted server or network with excessive internet traffic from multiple distributed machines.", "example": "Flooding an e-commerce website with 500 Gbps of traffic during a holiday sale."},
    {"term": "End-to-End Encryption (E2EE)", "category": "Cryptography", "definition": "Communication architecture where only the communicating users can read messages; even the service provider cannot decrypt them.", "example": "Signal and WhatsApp using the Signal Protocol for private messaging."},
    {"term": "Firewall", "category": "Network Security", "definition": "A network security device that monitors and filters incoming and outgoing network traffic based on predetermined rules.", "example": "Blocking all inbound traffic on port 22 (SSH) except from a known administrative IP."},
    {"term": "Hashing", "category": "Cryptography", "definition": "One-way mathematical transformation of arbitrary data into a fixed-length string of characters.", "example": "Storing user passwords as bcrypt hashes rather than cleartext."},
    {"term": "Homograph Attack", "category": "Phishing", "definition": "A deception attack where an attacker registers domains using lookalike characters from different alphabets (IDN).", "example": "Using Cyrillic 'а' to create a deceptive spoof of 'apple.com'."
    },
    {"term": "IP Address Spoofing", "category": "Network Security", "definition": "Creation of Internet Protocol packets with a false source IP address to conceal identity or impersonate another system.", "example": "Sending forged UDP packets to NTP servers during amplification DDoS attacks."},
    {"term": "Keylogger", "category": "Malware", "definition": "Surveillance software or hardware that covertly records every keystroke typed by an operator.", "example": "Stealing bank credentials as the victim types them on their physical keyboard."},
    {"term": "Man-in-the-Middle (MITM)", "category": "Attacks", "definition": "An attack where the perpetrator secretly relays and possibly alters communications between two parties who believe they are directly communicating.", "example": "An attacker intercepting HTTP traffic on an open cafe Wi-Fi network."},
    {"term": "MFA (Multi-Factor Authentication)", "category": "Authentication", "definition": "An authentication method that requires two or more verification factors to gain access to an application or resource.", "example": "Requiring a password, an authenticator app token, and a fingerprint."},
    {"term": "Phishing", "category": "Social Engineering", "definition": "Fraudulent communication masquerading as a reputable source to trick victims into revealing sensitive data.", "example": "A fake email urging you to verify your banking credentials on a cloned page."},
    {"term": "Ransomware", "category": "Malware", "definition": "Malicious software that encrypts computer files and demands payment in exchange for the decryption key.", "example": "WannaCry encrypting thousands of Windows systems worldwide."},
    {"term": "Salting", "category": "Cryptography", "definition": "Adding unique random data to passwords before hashing to defend against rainbow table attacks.", "example": "Appending a unique 16-byte random string to each user's password prior to computing bcrypt hash."},
    {"term": "Smishing (SMS Phishing)", "category": "Social Engineering", "definition": "A variant of phishing conducted through Short Message Service (SMS) text messages.", "example": "A text message stating your electricity will be disconnected tonight unless you click a link."},
    {"term": "SQL Injection (SQLi)", "category": "Application Security", "definition": "A code injection technique where malicious SQL statements are inserted into entry fields for execution.", "example": "Entering `' OR '1'='1` into a login field to bypass authentication checks."},
    {"term": "SSL / TLS", "category": "Cryptography", "definition": "Cryptographic protocols providing end-to-end communications security and data privacy over computer networks.", "example": "The padlock icon in web browsers ensuring HTTPS encryption."},
    {"term": "Trojan Horse", "category": "Malware", "definition": "Malicious code disguised as legitimate software to deceive users into installing it.", "example": "A downloadable game that secretly runs a cryptocurrency miner in the background."},
    {"term": "UPI (Unified Payments Interface)", "category": "Payments", "definition": "An instant real-time payment system developed by NPCI facilitating inter-bank peer-to-peer and merchant transactions.", "example": "Transferring funds via Google Pay, PhonePe, or Paytm using a Virtual Payment Address (VPA)."},
    {"term": "Vishing (Voice Phishing)", "category": "Social Engineering", "definition": "The fraudulent practice of conducting phone calls to trick victims into revealing personal or financial information.", "example": "A scammer calling pretending to be a bank manager needing your card CVV."},
    {"term": "VPN (Virtual Private Network)", "category": "Network Security", "definition": "A service that encrypts internet traffic and disguises online identity by routing connections through remote proxy servers.", "example": "Encrypting browser traffic while connected to an untrusted hotel Wi-Fi."},
    {"term": "Zero-Day Vulnerability", "category": "Threats", "definition": "A software security flaw unknown to the software developer, leaving zero days to fix before exploits can occur.", "example": "A flaw in an operating system exploited in the wild before any security patch exists."},
    {"term": "Zombie Computer", "category": "Threats", "definition": "An internet-connected computer compromised by a hacker via malware that can be directed remotely to perform malicious tasks.", "example": "An infected home PC sending spam emails as part of a global botnet."}
]


@education_bp.route("/education/topics", methods=["GET"])
def get_topics_list():
    """
    GET /api/education/topics
    Returns a summary catalog of all cybersecurity educational topics.
    """
    topics_summary = [
        {
            "id": t["id"],
            "title": t["title"],
            "icon": t["icon"],
            "description": t["description"],
            "difficulty": t["difficulty"],
            "reading_time": t["reading_time"]
        }
        for t in EDUCATION_TOPICS
    ]
    return jsonify({
        "success": True,
        "topics": topics_summary
    }), 200


@education_bp.route("/education/topics/<topic_id>", methods=["GET"])
def get_topic_detail(topic_id: str):
    """
    GET /api/education/topics/<topic_id>
    Returns the comprehensive curriculum, examples, prevention steps, and quiz for a specific topic.
    """
    clean_id = topic_id.strip().lower()
    matched = next((t for t in EDUCATION_TOPICS if t["id"] == clean_id), None)

    if not matched:
        return jsonify({
            "success": False,
            "error": f"Topic '{topic_id}' not found"
        }), 404

    return jsonify({
        "success": True,
        "topic": matched
    }), 200


@education_bp.route("/glossary", methods=["GET"])
def get_glossary():
    """
    GET /api/glossary
    Returns cybersecurity glossary terms with optional search query ('q') or category filter.
    """
    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip().lower()

    filtered = GLOSSARY_TERMS

    if category and category != "all":
        filtered = [item for item in filtered if item["category"].lower() == category]

    if query:
        filtered = [
            item for item in filtered
            if query in item["term"].lower() or query in item["definition"].lower() or query in item["category"].lower()
        ]

    # Unique categories for filtering UI
    categories = sorted(list({item["category"] for item in GLOSSARY_TERMS}))

    return jsonify({
        "success": True,
        "total": len(filtered),
        "categories": categories,
        "terms": filtered
    }), 200
