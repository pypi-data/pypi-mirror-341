from mm_crypto_utils import Proxies, random_proxy
from mm_std import Err, Ok, Result, hr, hra


def address_to_primary_name(address: str, timeout: float = 5, proxies: Proxies = None, attempts: int = 3) -> Result[str | None]:
    result: Result[str | None] = Err("not_started")
    url = f"https://www.aptosnames.com/api/mainnet/v1/primary-name/{address}"
    for _ in range(attempts):
        res = hr(url, proxy=random_proxy(proxies), timeout=timeout)
        data = res.to_dict()
        try:
            if res.code == 200 and res.json == {}:
                return Ok(None, data=data)
            return Ok(res.json["name"], data=data)
        except Exception as e:
            result = Err(e, data=data)
    return result


async def address_to_primary_name_async(
    address: str, timeout: float = 5, proxies: Proxies = None, attempts: int = 3
) -> Result[str | None]:
    result: Result[str | None] = Err("not_started")
    url = f"https://www.aptosnames.com/api/mainnet/v1/primary-name/{address}"
    for _ in range(attempts):
        res = await hra(url, proxy=random_proxy(proxies), timeout=timeout)
        data = res.to_dict()
        try:
            if res.code == 200 and res.json == {}:
                return Ok(None, data=data)
            return Ok(res.json["name"], data=data)
        except Exception as e:
            result = Err(e, data=data)
    return result


def address_to_name(address: str, timeout: float = 5, proxies: Proxies = None, attempts: int = 3) -> Result[str | None]:
    result: Result[str | None] = Err("not_started")
    url = f"https://www.aptosnames.com/api/mainnet/v1/name/{address}"
    for _ in range(attempts):
        res = hr(url, proxy=random_proxy(proxies), timeout=timeout)
        data = res.to_dict()
        try:
            if res.code == 200 and res.json == {}:
                return Ok(None, data=data)
            return Ok(res.json["name"], data=data)
        except Exception as e:
            result = Err(e, data=data)
    return result


async def address_to_name_async(
    address: str, timeout: float = 5, proxies: Proxies = None, attempts: int = 3
) -> Result[str | None]:
    result: Result[str | None] = Err("not_started")
    url = f"https://www.aptosnames.com/api/mainnet/v1/name/{address}"
    for _ in range(attempts):
        res = await hra(url, proxy=random_proxy(proxies), timeout=timeout)
        data = res.to_dict()
        try:
            if res.code == 200 and res.json == {}:
                return Ok(None, data=data)
            return Ok(res.json["name"], data=data)
        except Exception as e:
            result = Err(e, data=data)
    return result
