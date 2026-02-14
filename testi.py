import sys
sys.stdout.reconfigure(encoding='utf-8')

# https://script.google.com/macros/s/AKfycbwmU2M8Ez9a1IXBfW9yhOsQsW8eT4JNaXoYyQs2KUYPPA6QhCxLIR5YEpoikxTMPUlH/exec
post="""🚨 Only 4 hours left ‼️

DecodeX Hiring Hackathon 2026:

Graduation Year: 2026 / 2027

Perks: Pre placement opportunities for Software Development Internships

Register Link: https://apna.co/contests/nl-dalmia-synapse-decodex-2026?utm_source=external&utm_medium=external&utm_campaign=groimon1&utm_id=groimon&user_auth=phone_number

Telegram: https://telegram.me/OFF_CAMPUS_JOBS_AND_INTERNSHIPS"""

import re

def handle_source_5(text: str) -> str:
        if not text:
            return ""

        # ❌ Remove entire post if PlacementLelo links exist (apply/register/hackathons)
        if re.search(
            r"^.*telegram\.me.*$",
            text,
            flags=re.IGNORECASE
        ):
            return ""

        # ❌ Remove entire post if resume builder / resume promo exists
        if re.search(
            r"resume\s*(builder|enhancer)|resume\s*tool|resume\s*link|bit\.ly/\S+",
            text,
            flags=re.IGNORECASE
        ):
            return ""

        cleaned = text

        # ❌ Remove Telegram links only (keep post otherwise)
        cleaned = re.sub(
            r"Telegram\s*:\s*https?://(t\.me|telegram\.me)/\S+",
            "",
            cleaned,
            flags=re.IGNORECASE
        )

        # ❌ Remove WhatsApp links always
        cleaned = re.sub(
            r"https?://(www\.)?whatsapp\.com/\S+",
            "",
            cleaned,
            flags=re.IGNORECASE
        )

        # Normalize spacing
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

        return cleaned

print(handle_source_5(post))