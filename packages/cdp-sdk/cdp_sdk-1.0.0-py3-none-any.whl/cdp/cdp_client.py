from cdp.__version__ import __version__
from cdp.api_clients import ApiClients
from cdp.evm_client import EvmClient
from cdp.openapi_client.cdp_api_client import CdpApiClient
from cdp.constants import SDK_DEFAULT_SOURCE
from cdp.solana_client import SolanaClient


class CdpClient:
    """The CdpClient class is responsible for configuring and managing the CDP API client."""

    def __init__(
        self,
        api_key_id: str,
        api_key_secret: str,
        wallet_secret: str,
        debugging: bool = False,
        base_path: str = "https://api.cdp.coinbase.com/platform",
        max_network_retries: int = 3,
        source: str = SDK_DEFAULT_SOURCE,
        source_version: str = __version__,
    ):
        """Instantiate the CdpClient.

        Args:
            api_key_id (str): The API key ID.
            api_key_secret (str): The API key secret.
            wallet_secret (str): The wallet secret.
            debugging (bool, optional): Whether to enable debugging. Defaults to False.
            base_path (str, optional): The base path. Defaults to "https://api.cdp.coinbase.com/platform".
            max_network_retries (int, optional): The maximum number of network retries. Defaults to 3.
            source (str, optional): The source. Defaults to SDK_DEFAULT_SOURCE.
            source_version (str, optional): The source version. Defaults to __version__.
        """
        self.api_key_id = api_key_id
        self.api_key_secret = api_key_secret
        self.wallet_secret = wallet_secret
        self.debugging = debugging
        self.cdp_api_client = CdpApiClient(
            api_key_id,
            api_key_secret,
            wallet_secret,
            debugging,
            base_path,
            max_network_retries,
            source,
            source_version,
        )
        self.api_clients = ApiClients(self.cdp_api_client)
        self._evm = EvmClient(self.api_clients)
        self._solana = SolanaClient(self.api_clients)

    @property
    def evm(self) -> EvmClient:
        """Get the EvmClient instance."""
        return self._evm

    @property
    def solana(self) -> SolanaClient:
        """Get the SolanaClient instance."""
        return self._solana

    async def close(self):
        """Close the CDP client."""
        await self.api_clients.close()
        return None
