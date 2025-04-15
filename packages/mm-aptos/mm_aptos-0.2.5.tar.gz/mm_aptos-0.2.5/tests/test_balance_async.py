import pytest

from mm_aptos import balance_async
from mm_aptos.coin import APTOS_COIN_TYPE

pytestmark = pytest.mark.anyio


async def test_get_balance_async(mainnet_rpc_url, okx_address):
    res = await balance_async.get_balance(mainnet_rpc_url, okx_address, APTOS_COIN_TYPE)
    assert res.unwrap() > 1000
