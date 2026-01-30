"""Compact Post Fetcher with duplicate prevention"""
import logging
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Post:
    """Post data"""
    message_id: int
    source: str
    text: str
    date: datetime
    sender_id: Optional[int] = None
    media_present: bool = False


class PostFetcher:
    """Fetch posts with duplicate prevention via timestamp tracking"""

    def __init__(self, client_manager, config):
        self.logger = logging.getLogger(__name__)
        self.client = client_manager
        self.config = config
        self.posts: List[Post] = []
        self.fetch_log = Path(__file__).parent / "fetch_log.json"
        
        self.minutes_to_fetch = self.config.get_fetching_config().get("minutes_to_fetch", 360)
        self.last_fetch = self._load_last_fetch()

    def _load_last_fetch(self) -> datetime:
        if self.fetch_log.exists():
            try:
                data = json.loads(self.fetch_log.read_text())
                dt = datetime.fromisoformat(data["last_fetch"])

                # ✅ force UTC if naive
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)

                return dt
            except Exception:
                return datetime.now(timezone.utc) - timedelta(minutes=self.minutes_to_fetch)

        return datetime.now(timezone.utc) - timedelta(minutes=self.minutes_to_fetch)

    def _save_fetch_time(self):
        """Save fetch timestamp"""
        try:
            now = datetime.now(timezone.utc)
            self.logger.info(f"Current local time: {now.isoformat()}")
            self.fetch_log.write_text(json.dumps({
                "last_fetch": now.isoformat()
            }))
            self.logger.info(f"Updated fetch_log at {now.isoformat()}")
        except Exception as e:
            self.logger.error(f"Failed to save fetch_log: {e}")

    async def fetch_all(self) -> List[Post]:
        """Fetch from all sources since last fetch"""
        self.posts = []
        config = self.config.get_fetching_config()
        minutes = config.get("minutes_to_fetch", 30)
        limit = config.get("messages_per_fetch", 10)
        
        since = self.last_fetch

        for source in self.config.get_sources():
            try:
                client = self.client.get_client()
                messages = []
                async for msg in client.iter_messages(
                    source["username"],
                    limit=limit,
                    offset_date=since,
                    reverse=True
                ):
                    if msg.text:
                        self.posts.append(Post(
                            message_id=msg.id,
                            source=source["name"],
                            text=msg.text,
                            date=msg.date,
                            sender_id=msg.sender_id,
                            media_present=msg.media is not None
                        ))
                        messages.append(msg)
                        
                
                self.logger.info(f"Fetched {len(messages)} from {source['name']}")
            except Exception as e:
                self.logger.error(f"Fetch error from {source['username']}: {e}")
        
        self._save_fetch_time()
        self.logger.info(f"Total posts: {len(self.posts)}")
        return self.posts


