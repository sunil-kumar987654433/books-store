from src.config import Config
from redis.asyncio import Redis
import redis.asyncio as aioredis

JTI_EXPIRY = 3600

token_blocklist = Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    # decode_responses=True,
    db=0
)

token_blocklist_2 = aioredis.from_url(Config.REDIS_URL)


async def add_jti_to_blocklist(jti: str)->None:
    await token_blocklist_2.set(
        name=jti,
        value='',
        ex=JTI_EXPIRY
    )

async def token_in_blocklist(jti: str)->bool:
    jti = await token_blocklist_2.get(jti)
    return jti is not None