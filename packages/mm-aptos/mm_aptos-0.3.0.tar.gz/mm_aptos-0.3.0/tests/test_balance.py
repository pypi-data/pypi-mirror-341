import pytest

from mm_aptos.balance import get_balance
from mm_aptos.coin import APTOS_COIN_TYPE

pytestmark = pytest.mark.anyio


async def test_get_balance(mainnet_rpc_url, okx_address):
    res = await get_balance(mainnet_rpc_url, okx_address, APTOS_COIN_TYPE)
    assert res.unwrap() > 1000
