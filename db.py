# ------------------------------------------------
# File Name: MyselfNeon/db.py
# Description: Database with IST Support & 7-Day History
# ------------------------------------------------

import motor.motor_asyncio
import logging
from config import DB_NAME, DB_URI
import datetime 

logger = logging.getLogger(__name__)

# --- DEFINE IST TIMEZONE (UTC + 5:30) ---
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

class Database:
    def __init__(self):
        if not DB_URI:
            logger.error("❌ DB_URI is missing in config.py! Bot will not save data.")
            self.client = None
            return

        self.client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
        self.db = self.client[DB_NAME]
        
        # Collections
        self.states = self.db.states     # Status State (Online/Offline)
        self.targets = self.db.targets   # Monitoring Targets
        self.auth = self.db.auth         # Authorized Admins
        self.activity = self.db.activity # Activity Logs

    # --- 1. Tracking State ---
    async def get_state(self, key):
        if not self.client: return None
        data = await self.states.find_one({'_id': key})
        return data['value'] if data else None

    async def set_state(self, key, value):
        if not self.client: return
        await self.states.update_one({'_id': key}, {'$set': {'value': value}}, upsert=True)

    # --- 2. Target Management ---
    async def add_target(self, type, name, url, selector=None):
        if not self.client: return
        data = {'type': type, 'url': url, 'selector': selector}
        await self.targets.update_one({'_id': name}, {'$set': data}, upsert=True)

    async def remove_target(self, name):
        if not self.client: return False
        res = await self.targets.delete_one({'_id': name})
        return res.deleted_count > 0

    async def get_targets(self, type):
        if not self.client: return []
        return await self.targets.find({'type': type}).to_list(length=None)

    # --- 3. Auth Management ---
    async def add_auth_user(self, uid):
        if not self.client: return
        await self.auth.update_one({'_id': int(uid)}, {'$set': {'active': True}}, upsert=True)

    async def remove_auth_user(self, uid):
        if not self.client: return
        await self.auth.delete_one({'_id': int(uid)})

    async def get_all_auth_users(self):
        if not self.client: return []
        users = await self.auth.find({}).to_list(length=None)
        return [u['_id'] for u in users]

    async def is_user_authorized(self, uid):
        if not self.client: return False
        return bool(await self.auth.find_one({'_id': int(uid)}))

    # --- 4. Activity & Time Management (IST + 7-Day Limit) ---
    async def log_activity(self, name):
        """
        Logs current IST time if online.
        Removes entries older than 7 days.
        """
        if not self.client: return
        
        # Get Current Time in IST
        now_ist = datetime.datetime.now(IST)
        
        # Calculate the cutoff date (Current Time - 7 Days)
        cutoff = now_ist - datetime.timedelta(days=7)

        # 1. Add the new timestamp
        await self.activity.update_one(
            {'_id': name},
            {'$push': {'log': now_ist}},
            upsert=True
        )
        
        # 2. Cleanup: Remove any logs older than the cutoff
        await self.activity.update_one(
            {'_id': name},
            {'$pull': {'log': {'$lt': cutoff}}}
        )

    async def get_activity_data(self, name):
        """Returns the list of timestamps for the graph."""
        if not self.client: return []
        doc = await self.activity.find_one({'_id': name})
        return doc['log'] if doc else []

    async def get_last_seen(self, name):
        """
        Fetches the most recent IST timestamp from the DB.
        Used by /check to show accurate time.
        """
        if not self.client: return None
        doc = await self.activity.find_one({'_id': name})
        if doc and doc.get('log'):
            # Return the last item in the list (most recent)
            return doc['log'][-1]
        return None

# Auto-initialize
db = Database()
