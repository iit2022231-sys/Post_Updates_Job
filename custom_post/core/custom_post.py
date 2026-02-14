from anyio import Path
import logging
import pandas as pd
from datetime import datetime
import logging
from telegram_bot_module.post_fetcher import Post

# @dataclass
# class Post:
#     """Post data"""
#     message_id: int
#     source: str
#     text: str
#     date: datetime
#     sender_id: Optional[int] = None
#     media_present: bool = False

class CustomPostContactsService:
    def __init__(self, distributor):
        self.distributor = distributor
        self.logger = logging.getLogger(__name__)
        self.path_1= Path(__file__).parent.parent.parent / "assets" / "company_phone_no.xlsx"
        self.path_2= Path(__file__).parent.parent.parent / "assets" / "hr_details.xlsx"
        self.path_3= Path(__file__).parent.parent.parent / "assets" / "hr_emails_5000.xlsx"
         # Placeholder, will be set later

    def format_contacts_1(self, df: pd.DataFrame) -> str:
        lines = ["📌 *HR / Recruiter Contacts*\n"]

        for _, row in df.iterrows():
            lines.append(
                f"🏢 *{row['Company']}*\n"
                f"👤 {row['POC Name']} ({row['Designation']})\n"
                f"📞 `{row['Phone Number']}`\n"
                f"📧 {str(row['Email Address']).strip('<>')}\n"
            )

        lines.append("⚠️ _Use responsibly. Avoid spamming._")
        return "\n".join(lines)

    def format_contacts_2(self, df: pd.DataFrame) -> str:
        cols = [
            "First Name",
            "Last Name",
            "Job Title",
            "Email Address",
            "Company",
            "Website",
            "Company Industry",
            "Company Size",
            "Linkedin URL",
        ]

        df = df[cols]

        lines = ["📌 *Senior HR / Talent Acquisition Contacts*\n"]

        for _, row in df.iterrows():
            lines.append(
                f"🏢 *{row['Company']}*\n"
                f"👤 {row['First Name']} {row['Last Name']} — {row['Job Title']}\n"
                f"📧 {row['Email Address']}\n"
                f"🌐 {row['Website']}\n"
                f"🏭 {row['Company Industry']} | 👥 {row['Company Size']}\n"
                f"🔗 {row['Linkedin URL']}\n"
            )

        lines.append("⚠️ _Reach out professionally. Personalize your message._")
        return "\n".join(lines)

    
    def format_contacts_3(self, df: pd.DataFrame) -> str:
        lines = ["📌 *HR Email Contacts*\n"]

        for _, row in df.iterrows():
            lines.append(
                f"🏢 *{row['company']}*\n"
                f"👤 {row['name']}\n"
                f"📧 {row['email']}\n"
            )

        lines.append("⚠️ _Send concise & relevant job applications only._")
        return "\n".join(lines)
    


    async def send_hr_contacts(self):
        self.logger.info("Sending HR contacts...")

        formatters = [
            (pd.read_excel(self.path_1).sample(3), "16:00", "23:59", self.format_contacts_1),
            (pd.read_excel(self.path_2).sample(3), "08:00", "16:00", self.format_contacts_2),
            (pd.read_excel(self.path_3).sample(3), "00:00", "08:00", self.format_contacts_3),
        ]

        now = datetime.now().time()

        for df, start, end, formatter in formatters:
            if datetime.strptime(start, "%H:%M").time() <= now <= datetime.strptime(end, "%H:%M").time():
                post = Post(
                    message_id=0,
                    source="custom_post_contacts",
                    text=formatter(df),
                    date=datetime.now()
                )
                await self.distributor.send_posts([post])
                break


        


