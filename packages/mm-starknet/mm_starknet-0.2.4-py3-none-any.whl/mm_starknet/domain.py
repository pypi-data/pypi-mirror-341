from mm_crypto_utils import Proxies
from mm_std import Err, Ok, Result, hr, hra, random_str_choice, str_contains_any


def address_to_domain(address: str, timeout: float = 5, proxies: Proxies = None) -> Result[str | None]:
    url = "https://api.starknet.id/addr_to_domain"
    res = hr(url, params={"addr": address}, proxy=random_str_choice(proxies), timeout=timeout)
    data = res.to_dict()
    if res.json and res.json.get("domain"):
        return Ok(res.json.get("domain"), data=data)
    if res.code == 400 and str_contains_any(res.body.lower(), ["no data found", "no domain found"]):
        return Ok(None, data)
    return Err("unknown_response", data)


async def address_to_domain_async(address: str, timeout: float = 5, proxies: Proxies = None) -> Result[str | None]:
    url = "https://api.starknet.id/addr_to_domain"
    res = await hra(url, params={"addr": address}, proxy=random_str_choice(proxies), timeout=timeout)
    data = res.to_dict()
    if res.json and res.json.get("domain"):
        return Ok(res.json.get("domain"), data=data)
    if res.code == 400 and str_contains_any(res.body.lower(), ["no data found", "no domain found"]):
        return Ok(None, data)
    return Err("unknown_response", data)


def address_to_domain_with_retries(retries: int, address: str, timeout: float = 5, proxies: Proxies = None) -> Result[str | None]:
    res: Result[str | None] = Err("not started yet")
    for _ in range(retries):
        res = address_to_domain(address, timeout=timeout, proxies=proxies)
        if res.is_ok():
            return res
    return res


async def address_to_domain_with_retries_async(
    retries: int, address: str, timeout: float = 5, proxies: Proxies = None
) -> Result[str | None]:
    res: Result[str | None] = Err("not started yet")
    for _ in range(retries):
        res = await address_to_domain_async(address, timeout=timeout, proxies=proxies)
        if res.is_ok():
            return res
    return res
