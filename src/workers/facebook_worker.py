from src.workers.base import BaseWorker
from src.workers.facebook_autoposter import FacebookAutoPoster
import logging

logger = logging.getLogger(__name__)

class FacebookWorker(BaseWorker):
    """Facebook Worker wrapper for FacebookAutoPoster"""
    
    def __init__(self, queue, user_id=None):
        super().__init__(queue, f"facebook_{user_id or 'system'}")
        self.user_id = user_id
        self.poster = FacebookAutoPoster()
    
    async def process(self, task):
        """Process Facebook posting task"""
        task_type = task.get("type", "post")
        
        if task_type == "post_to_page":
            return await self._post_to_page(task.get("data", {}))
        elif task_type == "post_to_group":
            return await self._post_to_group(task.get("data", {}))
        
        return False
    
    async def _post_to_page(self, data):
        """Post to Facebook page"""
        try:
            result = await self.poster.post_to_page(
                page_id=data.get("page_id"),
                message=data.get("message"),
                image_url=data.get("image_url"),
                link=data.get("link")
            )
            logger.info(f"Posted to page: {result}")
            return True
        except Exception as e:
            logger.error(f"Failed to post: {e}")
            return False
    
    async def _post_to_group(self, data):
        """Post to Facebook group"""
        # TODO: Implement group posting
        logger.warning("Group posting not yet implemented")
        return False
