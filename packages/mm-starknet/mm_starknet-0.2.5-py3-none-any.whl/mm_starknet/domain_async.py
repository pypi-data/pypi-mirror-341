from mm_std import DataResult, http_request, str_contains_any


async def address_to_domain(address: str, timeout: float = 5.0, proxy: str | None = None) -> DataResult[str | None]:
    url = "https://api.starknet.id/addr_to_domain"
    res = await http_request(url, params={"addr": address}, proxy=proxy, timeout=timeout)
    if (
        res.status_code == 400
        and res.body is not None
        and str_contains_any(res.body.lower(), ["no data found", "no domain found"])
    ):
        return DataResult(ok_is_none=True, data=res.model_dump())
    if res.is_error():
        return res.to_data_result_err()
    domain = res.parse_json_body("domain")
    if domain:
        return DataResult(ok=domain, data=res.model_dump())
    return DataResult(err="unknown_response", data=res.model_dump())
