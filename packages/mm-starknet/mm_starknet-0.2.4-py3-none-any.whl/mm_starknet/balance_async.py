import aiohttp
from aiohttp_socks import ProxyConnector
from mm_std import DataResult
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.key_pair import KeyPair


async def get_balance(rpc_url: str, address: str, token: str, timeout: float = 5, proxy: str | None = None) -> DataResult[int]:
    try:
        timeout_config = aiohttp.ClientTimeout(total=timeout)
        connector = ProxyConnector.from_url(proxy) if proxy else None
        async with aiohttp.ClientSession(connector=connector, timeout=timeout_config) as session:
            client = FullNodeClient(node_url=rpc_url, session=session)
            account = Account(
                address=address,
                client=client,
                chain=StarknetChainId.MAINNET,
                key_pair=KeyPair(private_key=654, public_key=321),
            )
            balance = await account.get_balance(token_address=token)
            return DataResult(ok=balance)
    except Exception as err:
        return DataResult(err="exception", data={"exception": str(err)})
