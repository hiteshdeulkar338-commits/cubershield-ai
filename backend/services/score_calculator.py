"""
CyberShield AI - Personal Security Posture Calculator
Evaluates personal cybersecurity habits across authentication, device security,
network hygiene, and fraud awareness to generate a structured security score and action plan.
"""

from typing import Dict, Any, List


class SecurityScoreCalculator:
    """
    Transparent rule-based calculator for personal digital hygiene assessments.
    Produces category breakdown, observed strengths, weaknesses, and a concrete action plan.
    """

    CATEGORIES = {
        "authentication": {
            "name": "Authentication & Credentials",
            "weight": 0.35,
            "questions": {
                "mfa_enabled": {
                    "label": "Multi-Factor Authentication (MFA/2FA)",
                    "weight": 40,
                    "good": True,
                    "strength": "You enforce Multi-Factor Authentication (MFA) on critical accounts, drastically reducing credential stuffing risks.",
                    "improvement": "Enable MFA/2FA on all important accounts (email, banking, social media). Prefer authenticator apps over SMS.",
                    "action": "Download an authenticator app (e.g., Google Authenticator, Aegis) and enable 2FA on primary email and banking portals."
                },
                "unique_passwords": {
                    "label": "Unique Passwords per Account",
                    "weight": 35,
                    "good": True,
                    "strength": "You avoid reusing passwords across multiple online accounts, preventing breach cascading.",
                    "improvement": "Stop reusing passwords across services; a breach at one site exposes all accounts with matching credentials.",
                    "action": "Audit accounts and change passwords for reused services starting with your primary email."
                },
                "uses_password_manager": {
                    "label": "Password Manager Adoption",
                    "weight": 25,
                    "good": True,
                    "strength": "You utilize a password manager to store and generate complex, high-entropy passphrases.",
                    "improvement": "Adopt a reputable password manager (e.g. Bitwarden, 1Password) rather than relying on memory or browser auto-save.",
                    "action": "Install an open-source or audited password manager like Bitwarden to manage complex passwords."
                }
            }
        },
        "device_hygiene": {
            "name": "Device & System Hygiene",
            "weight": 0.25,
            "questions": {
                "automatic_updates": {
                    "label": "Automatic Software & OS Updates",
                    "weight": 50,
                    "good": True,
                    "strength": "You keep operating systems and applications up to date with the latest security patches.",
                    "improvement": "Enable automatic updates on your OS and mobile devices to patch known vulnerabilities promptly.",
                    "action": "Turn on automatic updates in Windows Update / macOS Settings and mobile app stores."
                },
                "screen_lock_enabled": {
                    "label": "Device Lock Screen (PIN / Biometrics)",
                    "weight": 50,
                    "good": True,
                    "strength": "All devices are secured with biometric or strong PIN screen locks, protecting against physical theft.",
                    "improvement": "Set a screen lock with a strong PIN (at least 6 digits) or biometric authentication on all devices.",
                    "action": "Ensure phone and laptop automatically lock within 2 minutes of inactivity."
                }
            }
        },
        "data_protection": {
            "name": "Data Protection & Backups",
            "weight": 0.20,
            "questions": {
                "regular_backups": {
                    "label": "Regular Data Backups (3-2-1 Rule)",
                    "weight": 60,
                    "good": True,
                    "strength": "You maintain regular offline or cloud backups, safeguarding against ransomware and hardware failures.",
                    "improvement": "Implement regular data backups for vital documents, photos, and records.",
                    "action": "Set up an encrypted cloud backup or weekly backup routine to an external hard drive."
                },
                "document_privacy": {
                    "label": "Careful Handling of Physical/Digital IDs",
                    "weight": 40,
                    "good": True,
                    "strength": "You safely store and redact identification documents (Aadhaar, PAN, SSN) before sharing.",
                    "improvement": "Avoid sharing unredacted photocopies of identity proofs (like Aadhaar, PAN) via insecure channels.",
                    "action": "Use masked Aadhaar where possible and write the specific purpose on document copies."
                }
            }
        },
        "network_awareness": {
            "name": "Network Safety & Fraud Awareness",
            "weight": 0.20,
            "questions": {
                "public_wifi_vpn": {
                    "label": "Secure Public Wi-Fi Usage",
                    "weight": 50,
                    "good": True,
                    "strength": "You avoid accessing sensitive services on open public Wi-Fi or properly utilize a trusted VPN.",
                    "improvement": "Avoid conducting online banking or entering credentials while connected to unencrypted public Wi-Fi.",
                    "action": "Use mobile cellular data or a trusted VPN when connecting outside your home network."
                },
                "phishing_vigilance": {
                    "label": "Phishing & Link Verification Discipline",
                    "weight": 50,
                    "good": True,
                    "strength": "You systematically inspect URLs and sender addresses before clicking links in messages.",
                    "improvement": "Develop a reflex to verify links manually and never share OTPs or enter UPI PINs to receive money.",
                    "action": "Bookmark official banking and government portals and always access them via saved bookmarks."
                }
            }
        }
    }

    def calculate(self, answers: Dict[str, Any]) -> dict:
        """
        Compute overall security posture score and breakdown by evaluating answers.

        :param answers: Key-value dictionary of user responses (booleans)
        :return: Comprehensive score summary, categories, strengths, improvements, and action plan
        """
        overall_score = 0.0
        categories_result = []
        strengths = []
        improvements = []
        action_plan = []

        # Map alternate key names if user submitted common variants
        normalized_answers = self._normalize_answers(answers)

        for cat_key, cat_data in self.CATEGORIES.items():
            cat_name = cat_data["name"]
            cat_weight = cat_data["weight"]
            cat_questions = cat_data["questions"]

            earned_points = 0.0
            total_possible = 0.0

            for q_key, q_data in cat_questions.items():
                q_weight = q_data["weight"]
                total_possible += q_weight

                val = bool(normalized_answers.get(q_key, False))
                expected = q_data["good"]

                if val == expected:
                    earned_points += q_weight
                    strengths.append(q_data["strength"])
                else:
                    improvements.append(q_data["improvement"])
                    action_plan.append({
                        "priority": "High" if cat_key in ("authentication", "device_hygiene") else "Medium",
                        "category": cat_name,
                        "recommendation": q_data["action"]
                    })

            cat_score = round((earned_points / total_possible) * 100) if total_possible > 0 else 0
            overall_score += (cat_score * cat_weight)

            categories_result.append({
                "id": cat_key,
                "name": cat_name,
                "score": cat_score,
                "weight_percent": int(cat_weight * 100)
            })

        final_score = int(round(overall_score))
        final_score = max(0, min(100, final_score))

        # Overall rating label
        if final_score >= 85:
            rating = "Excellent"
        elif final_score >= 70:
            rating = "Good"
        elif final_score >= 50:
            rating = "Moderate"
        else:
            rating = "Vulnerable"

        # Sort action plan by priority
        action_plan.sort(key=lambda x: 0 if x["priority"] == "High" else 1)

        return {
            "overall": final_score,
            "rating": rating,
            "categories": categories_result,
            "strengths": strengths,
            "improvements": improvements,
            "action_plan": action_plan,
            "disclaimer": "This is an educational self-assessment based on standard cybersecurity hygiene guidelines. It does not replace enterprise vulnerability assessments."
        }

    def _normalize_answers(self, answers: Dict[str, Any]) -> Dict[str, bool]:
        """Convert varied question key names into standard canonical keys."""
        norm = {}
        for k, v in answers.items():
            val = bool(v)
            key = k.lower().strip()

            if key in ("mfa", "2fa", "two_factor", "mfa_enabled"):
                norm["mfa_enabled"] = val
            elif key in ("unique_passwords", "password_reuse"):
                # If question asked "password_reuse: true", that means bad practice, invert
                norm["unique_passwords"] = (not val) if "reuse" in key else val
            elif key in ("password_manager", "uses_password_manager", "pw_manager"):
                norm["uses_password_manager"] = val
            elif key in ("software_updates", "automatic_updates", "auto_update"):
                norm["automatic_updates"] = val
            elif key in ("lock_screen", "screen_lock_enabled", "screen_lock"):
                norm["screen_lock_enabled"] = val
            elif key in ("backup_regularly", "regular_backups", "backup"):
                norm["regular_backups"] = val
            elif key in ("document_privacy", "shred_documents", "safe_documents"):
                norm["document_privacy"] = val
            elif key in ("public_wifi_vpn", "vpn_usage", "safe_wifi"):
                norm["public_wifi_vpn"] = val
            elif key in ("phishing_awareness", "phishing_vigilance", "link_check"):
                norm["phishing_vigilance"] = val
            else:
                norm[key] = val
        return norm
