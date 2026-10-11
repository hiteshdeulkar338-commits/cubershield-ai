"""
CyberShield AI - Email Phishing & Threat Analyzer
Evaluates email metadata, headers/sender patterns, and content semantics for social engineering,
credential harvesting, financial fraud, and impersonation indicators.
"""

import re
from urllib.parse import urlparse


class EmailAnalyzer:
    """
    Heuristic analyzer for detecting email phishing, spoofing, and advance fee scams.
    """

    # Urgency & coercion triggers
    URGENCY_PATTERNS = [
        r"\burgent(ly)?\b",
        r"\bimmediate(ly)?\b",
        r"\baccount\s+(suspended|locked|blocked|disabled|frozen)\b",
        r"\bverify\s+(now|immediately|your\s+account)\b",
        r"\baction\s+required\b",
        r"\bwithin\s+(24|48|12)\s+hours\b",
        r"\bfinal\s+(warning|notice)\b",
        r"\bdeadline\s+approaching\b",
        r"\bunauthorized\s+activity\b",
        r"\bsecurity\s+alert\b",
        r"\bcompromised\b"
    ]

    # Financial bait & lottery scams
    FINANCIAL_BAIT_PATTERNS = [
        r"\b(won|winner|winning)\b",
        r"\b(lottery|prize|jackpot|reward)\b",
        r"\binheritance\b",
        r"\bmillion\s+(dollars|pounds|euros|rupees)\b",
        r"\b(claim|collect)\s+your\s+(cash|money|prize|fund|refund)\b",
        r"\bwire\s+transfer\b",
        r"\btax\s+refund\b",
        r"\bcompensation\s+fund\b",
        r"\bbeneficiary\b",
        r"\bcrore(s)?\b",
        r"\blakh(s)?\b"
    ]

    # Credential harvesting patterns
    CREDENTIAL_PATTERNS = [
        r"\b(password|passwd|pwd)\b",
        r"\b(otp|one[\s-]time[\s-]password|verification\s+code)\b",
        r"\b(credit\s+card|debit\s+card|cvv|pin\s+number)\b",
        r"\b(ssn|social\s+security\s+number)\b",
        r"\bbank\s+account\s+(number|details)\b",
        r"\bconfirm\s+your\s+identity\b",
        r"\bupdate\s+billing\b",
        r"\blogin\s+credentials\b",
        r"\benter\s+your\s+credentials\b"
    ]

    # Extortion & threat rhetoric
    THREAT_PATTERNS = [
        r"\blegal\s+(action|proceedings)\b",
        r"\barrest(ed)?\b",
        r"\bcourt\s+(order|summons)\b",
        r"\bpolice\b",
        r"\blaw\s+enforcement\b",
        r"\btermination\b",
        r"\bblacklisted\b",
        r"\bpenalty\b",
        r"\brecorded\s+you\b",
        r"\bwebcam\b"
    ]

    # Suspicious attachment warnings
    ATTACHMENT_PATTERNS = [
        r"\.(exe|vbs|scr|iso|bat|cmd|pif|jar|js|ps1|docm|xlsm)\b",
        r"\bopen\s+(the\s+)?attached\b",
        r"\bview\s+attachment\b",
        r"\bdownload\s+(the\s+)?invoice\b",
        r"\bsee\s+attached\s+(receipt|document|file|bill)\b"
    ]

    # Public free webmail domains
    FREE_MAIL_PROVIDERS = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
        "aol.com", "protonmail.com", "zoho.com", "mail.com", "yandex.com"
    }

    # High-profile institutional organizations commonly faked
    IMPERSONATION_TARGETS = [
        {"name": "Internal Revenue Service (IRS)", "regex": r"\b(irs|internal\s+revenue\s+service)\b"},
        {"name": "Income Tax Department", "regex": r"\b(income\s+tax\s+department|it\s+department|cbic)\b"},
        {"name": "Reserve Bank of India (RBI)", "regex": r"\b(rbi|reserve\s+bank\s+of\s+india)\b"},
        {"name": "State Bank of India (SBI)", "regex": r"\b(sbi|state\s+bank\s+of\s+india)\b"},
        {"name": "PayPal", "regex": r"\bpaypal\b"},
        {"name": "Microsoft Support", "regex": r"\bmicrosoft\s+(support|security|team)\b"},
        {"name": "Apple Support", "regex": r"\bapple\s+(support|security|id)\b"},
        {"name": "Amazon Security", "regex": r"\bamazon\s+(order|customer\s+service|account)\b"},
        {"name": "Netflix Billing", "regex": r"\bnetflix\b"},
        {"name": "Google Account Team", "regex": r"\bgoogle\s+(security|account|workspace)\b"},
    ]

    def analyze(self, subject: str, sender: str, body: str) -> dict:
        """
        Execute comprehensive heuristic analysis on an email message.

        :param subject: Email subject line
        :param sender: Sender email address or name
        :param body: Full body text of the email
        :return: Assessment containing score, categorized indicators, and security tips
        """
        subject = subject.strip()
        sender = sender.strip().lower()
        body = body.strip()
        full_content = f"{subject}\n{body}".lower()

        indicators = []

        # 1. Check Sender Domain Discrepancy & Freemail Impersonation
        sender_email_match = re.search(r"[\w\.-]+@([\w\.-]+)", sender)
        sender_domain = sender_email_match.group(1).lower() if sender_email_match else ""

        # Test if email claims to be a corporate institution but uses free webmail
        for target in self.IMPERSONATION_TARGETS:
            if re.search(target["regex"], full_content, re.IGNORECASE):
                if sender_domain in self.FREE_MAIL_PROVIDERS:
                    indicators.append({
                        "name": f"Freemail Domain Impersonating {target['name']}",
                        "description": f"Sender claims to represent '{target['name']}' but sends from a public '{sender_domain}' address.",
                        "severity": "high",
                        "points": 40
                    })
                    break

        # 2. Check Urgency / Panic Induction
        urgency_hits = [p for p in self.URGENCY_PATTERNS if re.search(p, full_content)]
        if urgency_hits:
            indicators.append({
                "name": "Artificial Urgency & Pressure Tactics",
                "description": f"Language designed to induce panic and prompt hasty action detected ({len(urgency_hits)} matches).",
                "severity": "high" if len(urgency_hits) >= 2 else "medium",
                "points": min(30, len(urgency_hits) * 15)
            })

        # 3. Check Financial Bait / Advance-Fee Fraud
        financial_hits = [p for p in self.FINANCIAL_BAIT_PATTERNS if re.search(p, full_content)]
        if financial_hits:
            indicators.append({
                "name": "Financial Bait or Prize Lure",
                "description": f"Unrealistic monetary promises or unclaimed rewards referenced ({len(financial_hits)} triggers).",
                "severity": "high",
                "points": min(35, len(financial_hits) * 18)
            })

        # 4. Check Direct Credential / Personal Information Inquiries
        credential_hits = [p for p in self.CREDENTIAL_PATTERNS if re.search(p, full_content)]
        if credential_hits:
            indicators.append({
                "name": "Sensitive Credential Solicitation",
                "description": "Email solicits passwords, PINs, OTP codes, or financial account credentials.",
                "severity": "high",
                "points": 40
            })

        # 5. Check Threat & Coercion Rhetoric
        threat_hits = [p for p in self.THREAT_PATTERNS if re.search(p, full_content)]
        if threat_hits:
            indicators.append({
                "name": "Intimidation & Legal Threat Language",
                "description": "Email utilizes coercive legal threats, arrest warnings, or blackmail extortion techniques.",
                "severity": "high",
                "points": 35
            })

        # 6. Check for Embedded Links & Suspicious Link Patterns
        links = re.findall(r"https?://[^\s<>\"']+|www\.[^\s<>\"']+", body)
        if links:
            has_ip_link = any(re.search(r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", l) for l in links)
            if has_ip_link:
                indicators.append({
                    "name": "Direct IP Address Link in Body",
                    "description": "Body embeds hyperlinks pointing to raw numeric IP addresses rather than verified domain names.",
                    "severity": "high",
                    "points": 30
                })
            elif len(links) > 3:
                indicators.append({
                    "name": "Multiple External Hyperlinks",
                    "description": f"Email contains {len(links)} external links, often used in spam campaigns to distribute landing pages.",
                    "severity": "medium",
                    "points": 15
                })

        # 7. Check for Dangerous Attachment Extensions or Injunctions
        attachment_hits = [p for p in self.ATTACHMENT_PATTERNS if re.search(p, full_content)]
        if attachment_hits:
            indicators.append({
                "name": "Executable Attachment or Coercive Download Prompt",
                "description": "References dangerous file attachments (.exe, .vbs, .docm) or urges the user to download an unverified file.",
                "severity": "high",
                "points": 35
            })

        # 8. Check for Generic Greetings
        generic_greetings = [
            r"\bdear\s+customer\b", r"\bdear\s+user\b", r"\bdear\s+client\b",
            r"\bdear\s+beneficiary\b", r"\bdear\s+beloved\b", r"\battention\s+user\b"
        ]
        if any(re.search(g, full_content) for g in generic_greetings):
            indicators.append({
                "name": "Generic Salutation",
                "description": "Email uses an impersonal greeting like 'Dear Customer'. Legitimate banks usually address customers by registered name.",
                "severity": "low",
                "points": 10
            })

        # Calculate final aggregated risk score
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

        # Generate action-oriented recommendations
        recommendations = self._generate_recommendations(risk_level, indicators)

        return {
            "sender": sender,
            "subject": subject,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "indicators": indicators,
            "recommendations": recommendations,
            "disclaimer": "This analysis is based on static text heuristics, known phishing phrases, and sender patterns. Never share passwords or OTPs over email."
        }

    def _generate_recommendations(self, risk_level: str, indicators: list) -> list:
        recs = []
        if risk_level == "high":
            recs.append("DO NOT click any links, open attachments, or reply to this sender.")
            recs.append("No reputable bank or service provider asks for OTPs, CVVs, or passwords via email.")
            recs.append("Mark this message as Phishing/Spam in your email client and delete it.")
        elif risk_level == "medium":
            recs.append("Verify the sender's full email address and domain closely for slight misspellings (typosquatting).")
            recs.append("If this message claims an issue with your account, log into the official app or website directly.")
            recs.append("Avoid opening attached invoices or archives until verified with the purported sender through a separate channel.")
        elif risk_level == "low":
            recs.append("A few low-risk flags were observed. Review the message details carefully before responding.")
            recs.append("Check whether you were expecting this correspondence.")
        else:
            recs.append("No prominent social engineering or phishing patterns detected.")
            recs.append("Always exercise general caution with unsolicited attachments.")

        return recs
