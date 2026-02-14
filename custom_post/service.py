
import logging
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from .core import CustomPostContactsService



class CustomPostService:
    """Main service for DM-based channel promotion"""
    
    def __init__(self,distributor):
        self.logger = logging.getLogger(__name__)
        self.distributor = distributor
        self.contact_distributer=CustomPostContactsService(self.distributor)
    
    async def run(self):
        """Main execution loop"""
        self.logger.info("Starting Custom Post For Contacts Upload Service")

        await self.contact_distributer.send_hr_contacts()
        await self.contact_distributer.send_promotional_post()
        self.logger.info("Custom Post For Contacts Upload Service completed")
    

