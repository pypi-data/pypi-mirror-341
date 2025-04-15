import json
from typing import Optional, List, Union

from sgx.attestaion import SGXAttestationVerifier
from sgx.ecdh_provider import ECDHProvider
from sgx.session import SgxSession


class SgxClient:
    """
    Client for interacting with SGX-enabled secure enclave through attested sessions

    Provides secure methods for managing exchange accounts, blockchain addresses,
    whitelists, and user permissions using remote attestation.
    """

    def __init__(
        self,
        host: str,
        port: int,
        spid: str,
        key_provider: ECDHProvider,
        attestation_verifier: Optional[SGXAttestationVerifier] = None,
    ):
        """
        Args:
        host: Enclave server hostname or IP address
        port: Enclave server port
        spid: Service Provider ID for attestation
        key_provider: Private key provider for enclave authentication (ECDHProvider instance)
        attestation_verifier: Optional attestation verifier (SGXAttestationVerifier instance)
        """
        self.host = host
        self.port = port
        self.spid = spid
        self.key_provider = key_provider
        self.attestation_verifier = attestation_verifier

    def _common_execute(self, method, params: Optional[dict] = None) -> Union[dict, list]:
        """
        Execute a JSON-RPC method with attestation verification

        Args:
            method: RPC method name to execute
            params: Dictionary of method parameters

        Returns:
            Union[dict, list]: Parsed JSON response from enclave
        """
        with SgxSession(
            method, params, self.host, self.port, self.spid, self.key_provider, self.attestation_verifier
        ) as challenge:
            return json.loads(challenge.execute())

    def call_rpc(self, method: str, params=None) -> Union[dict, list]:
        """
        Direct JSON-RPC call interface

        Args:
            method: Name of the RPC method to call
            params: Parameters for the method call

        Returns:
            Union[dict, list]: Response from enclave

        Example:
            >>> client.call_rpc("status", {"verbose": True})
        """
        return self._common_execute(method, params)

    def get_accounts(self) -> dict:
        """
        Retrieve all configured exchange accounts

        Returns:
            list: Array of account configurations with sensitive fields masked
            Example: [{
                "id": "acc_12345",
                "name": "binance_main",
                "exchange": "binance",
                "public_key": "full_public_key_visible",
                "key": "123...xyz",
                "additional_data": {"custom_setting": true},
                "sorting_key": 1681390171
            }]
        """
        return self._common_execute("v2.get_accounts")

    def add_account(
            self,
            name: str,
            exchange: str,
            public_key: str,
            key: str,
            sorting_key: int = None,
            additional_data: dict = None,
    ) -> dict:
        """
        Create new exchange account

        Args:
            name: Unique account identifier
            exchange: Exchange platform name (e.g., binance, coinbase)
            public_key: Exchange-provided API public key
            key: Exchange-provided API secret key
            sorting_key: Optional numeric sorting identifier
            additional_data: Exchange-specific configuration

        Returns:
            dict: Created account details

        """
        params = {
            'name': name,
            'exchange': exchange,
            'public_key': public_key,
            'key': key,
            'sorting_key': sorting_key,
            'additional_data': additional_data,
        }
        return self._common_execute("v2.add_account", params)

    def update_account(
            self,
            account_id: str,
            name: str = None,
            public_key: str = None,
            key: str = None,
            sorting_key: int = None,
            additional_data: dict = None,
    ) -> dict:
        """
        Modify existing exchange account

        Args:
            account_id: ID of account to update
            name: New account name (optional)
            public_key: New public key (optional)
            key: New secret key (optional)
            sorting_key: New sorting key (optional)
            additional_data: Updated additional data (optional)

        Returns:
            dict: Operation status
        """
        params = {
            'id': account_id,
            'name': name,
            'public_key': public_key,
            'key': key,
            'sorting_key': sorting_key,
            'additional_data': additional_data,
        }
        return self._common_execute("v2.update_account", params)

    def del_account(self, account_id: str) -> dict:
        """
        Remove exchange account

        Args:
            account_id: UUID of account to remove

        Returns:
            dict: Operation status
        """
        return self._common_execute("v2.del_account", {"id": account_id})

    def get_standalone_addresses(self) -> dict:
        """
        Retrieve all standalone blockchain wallet configurations

        Returns:
            list: Array of wallet objects with whitelist status and permissions
            Example: [{
                "address": "0x123...abc",
                "network": "ETHEREUM",
                "alias": "Cold Storage",
                "currencies": ["ETH", "USDT"],
                "whitelist": True,
                "multisig": False,
                "sorting_key": 1681390171
            }]
        """
        return self._common_execute("v2.get_standalones")

    def add_standalone(
            self,
            address: str,
            network: str,
            alias: str,
            whitelist: bool,
            multisig: bool,
            currencies: List[str] = None,
            sorting_key: int = None,
    ) -> dict:
        """
        Create new blockchain address

        Args:
            address: Blockchain address string
            network: Blockchain network identifier
            alias: Human-readable name
            whitelist: Enable whitelisting for this address
            multisig: Mark as multisig address
            currencies: Supported currencies (empty=all)
            sorting_key: Optional numeric sorting identifier

        Returns:
            dict: Operation status
        """
        if currencies is None:
            currencies = []
        params = {
            'address': address,
            'network': network,
            'alias': alias,
            'whitelist': whitelist,
            'multisig': multisig,
            'currencies': currencies,
            'sorting_key': sorting_key,
        }
        return self._common_execute("v2.add_standalone", params)

    def update_standalone(
            self,
            address: str,
            network: str,
            alias: str = None,
            whitelist: bool = None,
            multisig: bool = None,
            currencies: List[str] = None,
            sorting_key: int = None,
    ) -> dict:
        """
        Update blockchain address configuration

        Args:
            address: Blockchain address to update
            network: Network identifier
            alias: New alias (optional)
            whitelist: New whitelist status (optional)
            multisig: New multisig status (optional)
            currencies: Updated currency list (optional)
            sorting_key: New sorting key (optional)

        Returns:
            dict: Operation status
        """
        params = {
            'address': address,
            'network': network,
            'alias': alias,
            'whitelist': whitelist,
            'multisig': multisig,
            'currencies': currencies,
            'sorting_key': sorting_key,
        }
        return self._common_execute("v2.update_standalone", params)

    def del_standalone(self, address: str, network: str) -> dict:
        """
        Remove blockchain address

        Args:
            address: Blockchain address to remove
            network: Network identifier

        Returns:
            dict: Operation status
        """
        params = {'address': address, 'network': network}
        return self._common_execute("v2.del_standalone", params)

    def get_whitelist(self) -> dict:
        """
        Retrieve exchange withdrawal whitelist entries

        Returns:
            list: Array of whitelisted address configurations
            Example: [{
                "address": "0x456...def",
                "network": "POLYGON",
                "alias": "Hot Wallet",
                "currencies": ["MATIC"],
                "sorting_key": 1681390172
            }]
        """
        return self._common_execute("v2.get_whitelist")

    def add_whitelist(
            self,
            address: str,
            network: str,
            alias: str,
            currencies: List[str] = None,
            sorting_key: int = None,
    ) -> dict:
        """
        Add address to whitelist

        Args:
            address: Blockchain address
            network: Network identifier
            alias: Human-readable name
            currencies: Allowed currencies (empty=all)
            sorting_key: Optional sorting identifier

        Returns:
            dict: Operation status
        """
        params = {
            'address': address,
            'network': network,
            'alias': alias,
            'currencies': currencies,
            'sorting_key': sorting_key,
        }
        return self._common_execute("v2.add_whiteaddress", params)

    def update_whitelist(
            self,
            address: str,
            network: str,
            alias: str = None,
            currencies: List[str] = None,
            sorting_key: int = None
    ) -> dict:
        """
        Update whitelist entry

        Args:
            address: Blockchain address
            network: Network identifier
            alias: New alias (optional)
            currencies: Updated currency list (optional)
            sorting_key: New sorting key (optional)

        Returns:
            dict: Operation status
        """
        params = {
            'address': address,
            'network': network,
            'alias': alias,
            'currencies': currencies,
            'sorting_key': sorting_key,
        }
        return self._common_execute("v2.update_whiteaddress", params)

    def del_whitelist(self, address: str, network: str) -> dict:
        """
        Remove address from whitelist

        Args:
            address: Blockchain address
            network: Network identifier

        Returns:
            dict: Operation status
        """
        params = {'address': address, 'network': network}
        return self._common_execute("v2.del_whiteaddress", params)

    def get_users(self) -> dict:
        """
        Retrieve all registered users with security settings

        Returns:
            list: Array of user objects with authentication status
            Example: [{
                "user": "admin@company.com",
                "role": "ADMIN",
                "hotp_enabled": True,
                "hotp_counter": 42,
                "sorting_key": 1681390173
            }]
        """
        return self._common_execute("v2.get_users")

    def add_user(self, user: str, role: str, sorting_key: int = None) -> dict:
        """
        Create new user

        Args:
            user: Unique username/email
            role: Security role (READ_ONLY, USER_ACCESS, FULL_ACCESS, ADMIN)
            sorting_key: Optional numeric sorting identifier

        Returns:
            dict: Created user details
        """
        params = {
            'user': user,
            'role': role,
            'sorting_key': sorting_key,
        }
        return self._common_execute("v2.add_user", params)

    def update_user(self, user: str, role: str = None, sorting_key: int = None) -> dict:
        """
        Modify user permissions

        Args:
            user: Username to update
            role: New security role (READ_ONLY, USER_ACCESS, FULL_ACCESS, ADMIN)
            sorting_key: New sorting key (optional)

        Returns:
            dict: Operation status
        """
        params = {
            'user': user,
            'role': role,
            'sorting_key': sorting_key,
        }
        return self._common_execute("v2.update_user", params)

    def del_user(self, user: str) -> dict:
        """
        Remove user

        Args:
            user: Username to delete

        Returns:
            dict: Operation status
        """
        params = {'user': user}
        return self._common_execute("v2.del_user", params)

    def reset_user_hotp(self, user: str) -> dict:
        """
        Reset user's OTP credentials

        Args:
            user: Username to reset

        Returns:
            dict: Operation status with new OTP counter
        """
        params = {'user': user}
        return self._common_execute("v2.reset_user_hotp", params)

    def get_network_coins(self) -> dict:
        """
        Retrieve supported networks and currencies

        Returns:
            dict: Network to currency mapping
            Example: {
                "ETHEREUM": ["ETH", "USDT"],
                "BITCOIN": ["BTC"],
                "ALGORAND": ["ALGO"]
            }
        """
        return self._common_execute("v2.get_networks_coins")

    def get_status(self) -> dict:
        """
        Get enclave health status

        Returns:
            dict: Status information
            Example: {"status": "ok"}
        """
        return self._common_execute("status")
