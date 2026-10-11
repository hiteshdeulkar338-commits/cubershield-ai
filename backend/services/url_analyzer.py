"""
CyberShield AI - Heuristic URL Security Analyzer
Evaluates URLs for phishing, brand spoofing, obfuscation, and credential harvesting
without actively requesting or connecting to the destination server.
"""

import re
import ipaddress
from urllib.parse import urlparse, unquote


class UrlAnalyzer:
    """
    Pure-Python static heuristic analyzer for evaluating URL safety.
    Never establishes an outbound network connection to the target URL.
    """

    # High-value brands commonly targeted in phishing attacks
    COMMON_TARGET_BRANDS = [
        "google", "gmail", "paypal", "amazon", "apple", "microsoft", "office365",
        "facebook", "instagram", "whatsapp", "netflix", "twitter", "linkedin",
        "chase", "wellsfargo", "bankofamerica", "citibank", "sbi", "hdfc",
        "icicibank", "paytm", "phonepe", "axisbank", "punjabnationalbank",
        "irctc", "binance", "coinbase", "metamask", "dropbox", "github"
    ]

    # Suspicious or high-abuse Top Level Domains (TLDs) frequently seen in spam/phishing
    SUSPICIOUS_TLDS = {
        "tk", "ml", "ga", "cf", "gq", "top", "xyz", "buzz", "click", "club",
        "work", "loan", "fit", "surf", "monster", "rest", "cam", "country",
        "kim", "racing", "science", "party", "accountant", "date", "faith"
    }

    # Known URL shortener domains that obscure destinations
    URL_SHORTENERS = {
        "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
        "buff.ly", "adf.ly", "bit.do", "rebrand.ly", "cutt.ly", "shorturl.at"
    }

    # Common phishing keywords in paths or subdomains
    PHISHING_KEYWORDS = [
        "login", "signin", "verify", "verification", "secure", "security",
        "update", "account", "banking", "authenticate", "confirm", "recovery",
        "wallet", "password", "credential", "suspend", "kyc", "unblock"
    ]

    def analyze(self, url: str) -> dict:
        """
        Analyze the given URL string against security heuristic rules.

        :param url: The raw URL string provided by the user
        :return: Structured analysis result with score, indicators, and recommendations
        """
        raw_url = url.strip()
        indicators = []
        risk_score = 0

        # 1. Scheme checks (Dangerous protocol handling)
        lower_url = raw_url.lower()
        if lower_url.startswith("javascript:"):
            indicators.append({
                "name": "JavaScript Pseudo-Protocol",
                "description": "URL uses 'javascript:' which can execute arbitrary script in browsers (XSS vector).",
                "severity": "high",
                "points": 50
            })
        elif lower_url.startswith("data:"):
            indicators.append({
                "name": "Data URI Scheme",
                "description": "URL uses 'data:' scheme to embed inline documents, frequently used in phishing redirects.",
                "severity": "high",
                "points": 45
            })

        # Prepend http:// for parsing if scheme is missing
        parse_target = raw_url
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", raw_url):
            parse_target = "http://" + raw_url

        try:
            parsed = urlparse(parse_target)
            hostname = parsed.hostname or ""
            port = parsed.port
            path = parsed.path or ""
            query = parsed.query or ""
        except Exception:
            hostname = ""
            port = None
            path = ""
            query = ""

        # 2. Check for @ symbol in URL (credentials in authority)
        if "@" in raw_url:
            indicators.append({
                "name": "Userinfo Credentials / Redirection Trick (@)",
                "description": "Contains '@' symbol. Browsers may ignore text before '@', misleading users about the real host.",
                "severity": "high",
                "points": 35
            })

        # 3. Check for raw IP address in host
        is_ip_host = False
        if hostname:
            try:
                ipaddress.ip_address(hostname)
                is_ip_host = True
                indicators.append({
                    "name": "IP Address Used as Hostname",
                    "description": f"URL connects directly to IP '{hostname}' instead of a verified domain name.",
                    "severity": "high",
                    "points": 30
                })
            except ValueError:
                is_ip_host = False

        # 4. Check for Punycode / Homograph attack (IDN spoofing)
        if "xn--" in hostname.lower():
            indicators.append({
                "name": "Internationalized Domain Name (Punycode)",
                "description": "Domain contains 'xn--', often used in homograph attacks to mimic familiar characters using Cyrillic/Greek alphabets.",
                "severity": "high",
                "points": 30
            })

        # 5. Non-standard port checks
        if port and port not in (80, 443, 8080):
            indicators.append({
                "name": "Non-Standard Port Number",
                "description": f"Connecting over unusual port {port}. Legitimate web services normally operate on standard ports (80/443).",
                "severity": "medium",
                "points": 20
            })

        # 6. Suspicious TLD check
        host_parts = hostname.lower().split(".")
        if len(host_parts) >= 2 and not is_ip_host:
            tld = host_parts[-1]
            if tld in self.SUSPICIOUS_TLDS:
                indicators.append({
                    "name": "High-Risk Top Level Domain (TLD)",
                    "description": f"Domain ends in '.{tld}', which is statistically associated with high volumes of malicious campaigns.",
                    "severity": "medium",
                    "points": 25
                })

        # 7. Excessive subdomains check (> 3 levels)
        if len(host_parts) > 4 and not is_ip_host:
            indicators.append({
                "name": "Excessive Subdomains",
                "description": f"Host contains {len(host_parts)-2} subdomains, a pattern used to evade brand filters.",
                "severity": "medium",
                "points": 15
            })

        # 8. Known URL shortener check
        if hostname.lower() in self.URL_SHORTENERS:
            indicators.append({
                "name": "URL Shortener Service",
                "description": f"URL uses shortening service '{hostname}', hiding the true destination and landing page.",
                "severity": "medium",
                "points": 20
            })

        # 9. Brand Impersonation check
        # Looks for trusted brand names in subdomains or path while the registered domain is not the brand
        registered_domain = ".".join(host_parts[-2:]) if len(host_parts) >= 2 else hostname
        matched_brand = None
        for brand in self.COMMON_TARGET_BRANDS:
            if brand in lower_url:
                # If the brand appears anywhere in the URL but the apex domain is not the brand's domain
                if brand not in registered_domain:
                    matched_brand = brand
                    break
                elif f"-{brand}" in registered_domain or f"{brand}-" in registered_domain:
                    matched_brand = brand
                    break

        if matched_brand:
            indicators.append({
                "name": "Potential Brand Impersonation",
                "description": f"Reference to '{matched_brand}' detected in URL, but domain '{registered_domain}' is not the official brand property.",
                "severity": "high",
                "points": 35
            })

        # 10. URL Length checks
        if len(raw_url) > 120:
            indicators.append({
                "name": "Excessive URL Length",
                "description": f"URL is unusually long ({len(raw_url)} chars). Attackers often bloat URLs to hide payloads from address bars.",
                "severity": "medium",
                "points": 15
            })
        elif len(raw_url) > 75:
            indicators.append({
                "name": "Elevated URL Length",
                "description": f"URL length is {len(raw_url)} characters, which is longer than typical landing links.",
                "severity": "low",
                "points": 10
            })

        # 11. Suspicious URL encoding and Hex representations
        hex_encoded_count = len(re.findall(r"%[0-9a-fA-F]{2}", raw_url))
        if "%00" in raw_url:
            indicators.append({
                "name": "Null Byte Injection Character",
                "description": "URL contains encoded null byte (%00), frequently used in bypass or evasion exploits.",
                "severity": "high",
                "points": 30
            })
        elif hex_encoded_count > 4:
            indicators.append({
                "name": "Excessive Percent-Encoding",
                "description": f"URL has {hex_encoded_count} encoded character sequences, potentially obfuscating target words.",
                "severity": "medium",
                "points": 15
            })

        # 12. Phishing keywords in path or query
        detected_phish_words = []
        combined_path_query = (path + " " + query).lower()
        for kw in self.PHISHING_KEYWORDS:
            if re.search(r"\b" + re.escape(kw) + r"\b", combined_path_query):
                detected_phish_words.append(kw)

        if detected_phish_words:
            indicators.append({
                "name": "Suspicious Authentication / Security Keywords",
                "description": f"URL path/parameters contain security trigger terms: {', '.join(detected_phish_words[:4])}.",
                "severity": "medium",
                "points": min(25, len(detected_phish_words) * 10)
            })

        # 13. Insecure HTTP check if scheme was explicitly provided
        if raw_url.lower().startswith("http://"):
            indicators.append({
                "name": "Unencrypted HTTP Protocol",
                "description": "Link uses plain HTTP without TLS/SSL encryption. Data transmitted can be intercepted or altered.",
                "severity": "low",
                "points": 10
            })

        # Aggregate risk score (cap at 100)
        total_points = sum(item.pop("points", 0) for item in indicators)
        risk_score = min(100, max(0, total_points))

        # Determine risk level category
        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        elif risk_score >= 20:
            risk_level = "low"
        else:
            risk_level = "safe"

        # Generate contextual recommendations
        recommendations = self._generate_recommendations(risk_level, indicators, hostname)

        return {
            "url": raw_url,
            "hostname": hostname or "unknown",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "indicators": indicators,
            "recommendations": recommendations,
            "disclaimer": "This analysis is based on URL pattern heuristics and known threat indicators. It does not actively visit or connect to the destination server."
        }

    def _generate_recommendations(self, risk_level: str, indicators: list, hostname: str) -> list:
        """Helper to generate clear, actionable user recommendations."""
        recs = []
        if risk_level == "high":
            recs.append("Do NOT click this link or submit any passwords, phone numbers, or OTPs.")
            recs.append("Delete the message or email containing this link immediately.")
            recs.append(f"If you need to access {hostname or 'this service'}, navigate manually via official bookmarks or a search engine.")
        elif risk_level == "medium":
            recs.append("Exercise caution. Verify the domain carefully before entering credentials.")
            recs.append("Inspect whether the site employs a valid HTTPS certificate once loaded.")
            recs.append("Be wary if this link arrived from an unsolicited SMS, WhatsApp, or email.")
        elif risk_level == "low":
            recs.append("Minor anomalies detected. Check that the domain matches what you expected.")
            recs.append("Always verify the address bar before entering payment or personal data.")
        else:
            recs.append("No obvious heuristic threats detected in the URL structure.")
            recs.append("Remain vigilant: new or legitimate compromised domains can still host malicious forms.")

        return recs
