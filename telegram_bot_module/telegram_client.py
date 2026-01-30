import logging
from pathlib import Path
from typing import Optional
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


class TelegramClientManager:

    def __init__(self, api_id: int, api_hash: str, session_name: str):

        self.logger = logging.getLogger(__name__)
        self.api_id = api_id
        self.api_hash = api_hash
        
        module_dir = Path(__file__).parent
        self.session_path = str(module_dir / session_name)
        self.client: Optional[TelegramClient] = None

    async def initialize(self) -> bool:

        try:
            self.client = TelegramClient(self.session_path, self.api_id, self.api_hash)
            await self.client.connect()
            
            if not await self.client.is_user_authorized():
                self.logger.info("Authorization required - session expired or invalid")
                await self._authorize()
            else:
                self.logger.info("Using existing session")
            
            self.logger.info("Telegram client connected successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Telegram client: {e}")
            # Try to re-authorize if session is corrupted
            if "AuthKeyUnregistered" in str(e) or "SessionPasswordNeeded" in str(e):
                self.logger.info("Session corrupted, attempting re-authorization...")
                try:
                    await self._authorize()
                    return True
                except Exception as auth_error:
                    self.logger.error(f"Re-authorization failed: {auth_error}")
            return False

    async def _authorize(self):
        """Handle Telegram authentication with user input"""
        try:
            phone = input("Enter your phone number: ")
            await self.client.send_code_request(phone)
           

            code = input("Enter the code you received: ")
            
            try:
                # Try to sign in with code
                await self.client.sign_in(phone, code)
            except SessionPasswordNeededError:
                # If 2FA is enabled, ask for password
                password = input("2FA password required. Enter your password: ")
                await self.client.sign_in(password=password)
            
            self.logger.info("Authorization successful")
        except Exception as e:
            self.logger.error(f"Authorization failed: {e}")
            raise

    async def disconnect(self):
        """Disconnect Telegram client"""
        if self.client:
            try:
                await self.client.disconnect()
                self.logger.info("Telegram client disconnected")
            except Exception as e:
                self.logger.error(f"Error disconnecting client: {e}")

    def get_client(self) -> Optional[TelegramClient]:
        """Get active Telegram client"""
        return self.client

