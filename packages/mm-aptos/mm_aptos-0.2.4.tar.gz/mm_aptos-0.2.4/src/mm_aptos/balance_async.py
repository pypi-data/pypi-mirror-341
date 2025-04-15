from mm_std import DataResult, http_request


async def get_balance(
    node: str, account_address: str, coin_type: str, timeout: float = 5.0, proxy: str | None = None
) -> DataResult[int]:
    url = f"{node}/accounts/{account_address}/resource/0x1::coin::CoinStore%3C{coin_type}%3E"
    res = await http_request(url, proxy=proxy, timeout=timeout)
    try:
        json_res = res.parse_json_body()
        if json_res.get("error_code") == "resource_not_found":
            return DataResult(ok=0, data=res.model_dump())
        return DataResult(ok=int(json_res["data"]["coin"]["value"]), data=res.model_dump())
    except Exception as err:
        return DataResult(err="exception", data={"response": res.model_dump(), "exception": str(err)})
