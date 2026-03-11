from database.db import update_last_seen

async def track_activity(update, context):
    if update.effective_user:
        update_last_seen(update.effective_user.id)
