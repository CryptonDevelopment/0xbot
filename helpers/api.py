import aiohttp
from config import API_ENDPOINT, BEARER_TOKEN
from bot_setup import logger


headers: dict = {"Authorization": BEARER_TOKEN}


async def api_url(route: str) -> str:
    return API_ENDPOINT + route


async def get_request(url: str) -> dict:
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(await api_url(url), timeout=5) as response:
                return await response.json()
    except Exception as e:
        logger.error(f"get request error \n{e}")
        return {}


async def post_request(url: str, data: dict) -> dict:
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(await api_url(url), data=data) as response:
                    if response.status == 204:
                        return {"success": True, "status": 204}
                    else:
                        return await response.json()
    except Exception as e:
        logger.error(f"post request error \n{e}")
        return {}


from typing import Any, Tuple, Union

async def extract_summary(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "name": item.get("name").split(" ")[0],
        "duration": item.get("duration").get("id"),
        "price": item.get("price"),
        "individualPrice": item.get("individualPrice"),
        "baseDiscountAmount": item.get("baseDiscountAmount"),
        "baseDiscount": item.get("baseDiscount")
    }


async def get_subs(user_id: int) -> dict[str, list[dict[str, Any]]]:
    result = {}
    items = await get_request(f"/api/v1/subscriptions/get-active?user_id={user_id}")
    for it in items:
        sub_type = (it.get("kind") or {}).get("name")
        if sub_type:
            if sub_type not in result:
                result[sub_type] = []
            result[sub_type].append(await extract_summary(it))
    return result


async def calculate_final_price(subscription: dict[str, Any], discount: dict[str, Any] = None) -> Tuple[int, int]:
    base_price = subscription.get("individualPrice") or (subscription.get("price"))
    base_price -= (subscription.get("baseDiscountAmount", 0) or 0)
    
    subscription_id = subscription.get("id")
    
    if not discount:
        return (int(base_price), subscription_id)
    
    if subscription_id not in discount.get("validForSubscriptions", []):
        return (int(base_price), subscription_id)
    
    discount_amount = discount.get("discountAmount", 0)
    discount_kind = discount.get("discountKind", {}).get("id")
    
    if discount_kind == "PERCENT":
        final_price = base_price * (1 - discount_amount)
    else:
        final_price = base_price - discount_amount
    
    return (int(round(final_price)), subscription_id)