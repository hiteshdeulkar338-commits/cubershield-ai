"""
CyberShield AI - SMS & Instant Message Threat Analyzer
Evaluates mobile messages (SMS, WhatsApp, Telegram) for smishing, advance fee fraud,
fake job offers, high-yield investment schemes, and KYC/UPI impersonation scams
with specialized coverage for the Indian cyber-fraud ecosystem.
"""

import re


class MessageAnalyzer:
    """
    Heuristic analyzer detecting fraudulent SMS and messaging patterns.
    Covers global threats alongside Indian fraud vectors (UPI scams, APK malwares, KYC alerts).
    """

    # 1. High-Yield Investment & Ponzi Schemes
    INVESTMENT_SCAM_PATTERNS = [
        (r"\b(guaranteed\s+(return|profit|income)|100%\s+profit)\b", "Guaranteed Profit Claim", "Promises risk-free high financial returns.", 35),
        (r"\b(double\s+your\s+money|2x\s+in\s+\d+\s+days)\b", "Money Doubling Scheme", "Classic Ponzi indicator claiming unrealistic financial multiplication.", 40),
        (r"\b(forex\s+trading|crypto\s+(mining|signals|pump)|binary\s+options)\b", "High-Risk Speculative Trading Lure", "Pushes unregulated foreign exchange or crypto investment schemes.", 25),
        (r"\b(vip\s+stock\s+tips|insider\s+trading\s+group|stock\s+market\s+calls)\b", "Unregistered Financial Advice Group", "Invites users into illicit stock advisory chat channels.", 25),
    ]

    # 2. Fake Job & Task Scams (e.g. YouTube like scam, Work from Home)
    FAKE_JOB_PATTERNS = [
        (r"\b(work\s+from\s+home|part[\s-]time\s+job|earn\s+from\s+home)\b", "Unsolicited Job Offer", "Unsolicited recruitment offer frequently linked to advance task fraud.", 25),
        (r"\b(earn\s+(rs\.?|inr|\$)?\s*\d{3,5}\s*(per|a|every)?\s*(day|daily|hour))\b", "Unrealistic Daily Compensation", "Advertises suspiciously high daily earnings for minimal effort.", 35),
        (r"\b(like\s+(youtube\s+videos|reviews)|rate\s+google\s+maps|subscribe\s+channels)\b", "Task-Based Review Fraud", "Classic scam format where victims perform micro-tasks then are forced to pay fees to withdraw funds.", 40),
        (r"\b(no\s+experience\s+needed|no\s+skills\s+required|anyone\s+can\s+join)\b", "No Qualifications Lure", "Lowers barrier to entry to maximize target reach.", 20),
    ]

    # 3. Urgency, Utility Cutoff & Pressure Tactics
    URGENCY_PATTERNS = [
        (r"\b(electricity\s+(power\s+)?(bill\s+)?will\s+be\s+(cut\s+off|disconnected|suspended))\b", "Electricity Bill / Power Cutoff Scam", "Pretends power will be disconnected due to unpaid bill to incite instant panic.", 40),
        (r"\b(sim\s+(card\s+)?(blocked|deactivated|suspended))\b", "SIM Card Deactivation Threat", "Falsely threatens mobile disconnection to force immediate compliance.", 35),
        (r"\b(immediate(ly)?|urgent(ly)?|within\s+\d+\s+hours?|last\s+chance|expiring\s+today)\b", "High Pressure Urgency", "Urges quick response to prevent victim from verifying claims.", 25),
        (r"\b(account\s+will\s+be\s+(locked|closed|suspended))\b", "Account Suspension Threat", "Threatens immediate service forfeiture.", 25),
    ]

    # 4. KYC, Aadhaar & PAN Card Phishing (India Specific)
    KYC_PATTERNS = [
        (r"\b(ekyc|kyc)\s+(expired|pending|suspended|update|mandatory)\b", "Urgent KYC Verification Bait", "Phishes personal IDs claiming banking or wallet KYC has lapsed.", 40),
        (r"\b(pan\s+card\s+(not\s+linked|blocked|update)|link\s+pan\s+with\s+aadhaar)\b", "PAN/Aadhaar Linking Phishing", "Exploits regulatory PAN-Aadhaar compliance deadlines.", 35),
        (r"\b(sbi\s+yono|yono\s+account|pnb\s+one|bob\s+world)\b", "Banking App Impersonation", "Targets major Indian banking portal credentials.", 35),
    ]

    # 5. Lottery, KBC & Unrealistic Rewards
    REWARD_PATTERNS = [
        (r"\b(kbc\s+(lottery|winner|crorepati)|kaun\s+banega\s+crorepati)\b", "KBC Lottery Scam", "Infamous fraud falsely claiming the recipient won the KBC television lottery.", 45),
        (r"\b(won\s+(rs\.?|inr|\$)?\s*\d+\s*(lakh|crore|million))\b", "High-Sum Lottery Announcement", "Claims recipient won huge sums from contests never entered.", 45),
        (r"\b(lucky\s+draw|selected\s+as\s+lucky\s+winner|congratulations\s+you\s+won)\b", "Unsolicited Prize Notification", "Lures targets into paying release or processing fees.", 30),
        (r"\b(amazon|flipkart)\s+(gift\s+card|free\s+voucher|spin\s+and\s+win)\b", "E-Commerce Gift Voucher Bait", "Impersonates top shopping platforms with fake reward claims.", 25),
    ]

    # 6. Payment, UPI & Advance Fee Indicators
    PAYMENT_PATTERNS = [
        (r"\b(scan\s+qr\s+code\s+to\s+receive|enter\s+pin\s+to\s+receive\s+money)\b", "Reverse UPI Payment / PIN Scam", "Critical fraud: Entering UPI PIN ALWAYS DEBITS money, never receives money.", 50),
        (r"\b(pay\s+(processing|registration|delivery|customs|clearance)\s+fee)\b", "Advance Fee Fraud", "Demands upfront payment before promised funds or items can be released.", 40),
        (r"\b(send\s+(money|upi)\s+to\s+receive\s+cashback)\b", "Cashback Upfront Scam", "Demands outgoing payment under the guise of an incoming cashback reward.", 40),
        (r"\b(telegram\s+admin|join\s+telegram\s+channel|contact\s+on\s+whatsapp\s+at)\b", "Redirection to Encrypted Channels", "Steers victims into private Telegram or WhatsApp groups where fraud is executed.", 25),
    ]

    # 7. Credential / Remote Access / Malicious APK Installation
    MALWARE_REMOTE_ACCESS_PATTERNS = [
        (r"\b(install|download)\s+.*\.apk\b", "Untrusted Android APK Sideloading", "Prompts installing raw .apk file, common vector for SMS-stealing and banking trojans.", 45),
        (r"\b(anydesk|teamviewer|quicksupport|rustdesk)\b", "Remote Screen Sharing App Request", "Tricks users into installing screen sharing tools allowing complete remote phone control.", 45),
        (r"\b(share\s+(the\s+)?otp|forward\s+(this\s+)?sms|send\s+otp)\b", "OTP Interception Solicitation", "Attempts to persuade the user to share private two-factor authentication codes.", 45),
    ]

    # 8. Fake Delivery / Courier Scams
    DELIVERY_PATTERNS = [
        (r"\b(india\s+post|bluedart|delhivery|dtdc)\s+.*(package|parcel|address\s+incomplete|delivery\s+failed)\b", "Fake Parcel Delivery Notice", "Claims delivery failed to trick user into paying a small redelivery fee or submitting card details.", 35),
        (r"\b(customs\s+(clearance|duty|held\s+parcel))\b", "Customs Impersonation Extortion", "Falsely claims an international package is detained at customs.", 35),
    ]

    def analyze(self, message: str, msg_type: str = "sms") -> dict:
        """
        Scan a text message against known social engineering and financial fraud patterns.

        :param message: Raw text message content
        :param msg_type: Channel type ('sms', 'whatsapp', 'telegram', 'other')
        :return: Analysis results with risk score, categorized indicators, and safety guidelines
        """
        msg = message.strip()
        lower_msg = msg.lower()
        indicators = []

        all_pattern_groups = [
            self.INVESTMENT_SCAM_PATTERNS,
            self.FAKE_JOB_PATTERNS,
            self.URGENCY_PATTERNS,
            self.KYC_PATTERNS,
            self.REWARD_PATTERNS,
            self.PAYMENT_PATTERNS,
            self.MALWARE_REMOTE_ACCESS_PATTERNS,
            self.DELIVERY_PATTERNS
        ]

        # Scan each rule group
        for group in all_pattern_groups:
            for regex_str, name, description, points in group:
                if re.search(regex_str, lower_msg):
                    indicators.append({
                        "name": name,
                        "description": description,
                        "severity": "high" if points >= 35 else "medium",
                        "points": points
                    })

        # Check for suspicious shortened or masked links inside the message
        url_matches = re.findall(r"https?://[^\s]+|bit\.ly/[^\s]+|tinyurl\.com/[^\s]+|t\.me/[^\s]+", lower_msg)
        if url_matches:
            indicators.append({
                "name": "Embedded Link in Mobile Message",
                "description": f"Contains embedded link ({url_matches[0][:30]}...). Phishers use mobile links because full URLs are truncated on phone screens.",
                "severity": "medium",
                "points": 20
            })

        # Calculate total score
        total_points = sum(item.pop("points", 0) for item in indicators)
        risk_score = min(100, max(0, total_points))

        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        elif risk_score >= 20:
            risk_level = "low"
        else:
            risk_level = "safe"

        recommendations = self._generate_recommendations(risk_level, indicators)

        return {
            "type": msg_type,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "indicators": indicators,
            "recommendations": recommendations,
            "disclaimer": "This analysis identifies patterns common in SMS phishing (smishing), UPI fraud, and cyber scams. CyberShield AI does not communicate with any telecom operator or external service."
        }

    def _generate_recommendations(self, risk_level: str, indicators: list) -> list:
        recs = []
        if risk_level == "high":
            recs.append("CRITICAL: NEVER enter your UPI PIN to receive money. UPI PIN is ONLY needed for paying.")
            recs.append("NEVER share OTPs or install remote assistance apps (AnyDesk, TeamViewer) at anyone's request.")
            recs.append("Block and report this number immediately inside WhatsApp/SMS.")
            recs.append("In India, report cyber fraud promptly at https://cybercrime.gov.in or call helpline 1930.")
        elif risk_level == "medium":
            recs.append("Be highly skeptical. Do not click links or call numbers provided directly in the text.")
            recs.append("If this concerns banking or utilities, contact the official company helpline found on their website or your utility bill.")
            recs.append("Do not send money or register for unknown task groups.")
        elif risk_level == "low":
            recs.append("Exercise standard vigilance. Verify the sender identity.")
            recs.append("Check if the sender is using an official SMS header (e.g. VK-HDFCBK) vs an unknown 10-digit mobile number.")
        else:
            recs.append("No common scam keywords or red flags recognized.")
            recs.append("Remember: authentic organizations will never ask for your passwords, OTP, or remote screen access.")

        return recs
