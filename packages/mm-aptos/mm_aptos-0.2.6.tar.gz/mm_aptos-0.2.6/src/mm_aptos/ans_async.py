from mm_std import DataResult, http_request


async def address_to_primary_name(address: str, timeout: float = 5, proxy: str | None = None) -> DataResult[str | None]:
    url = f"https://www.aptosnames.com/api/mainnet/v1/primary-name/{address}"
    res = await http_request(url, proxy=proxy, timeout=timeout)
    if res.is_error():
        return res.to_data_result_err()
    json_res = res.parse_json_body()
    if res.status_code == 200 and json_res == {}:
        return DataResult.ok(None, res.model_dump())
    if "name" in json_res:
        return DataResult.ok(json_res["name"], res.model_dump())
    return DataResult.err("unknown_response", res.model_dump())
