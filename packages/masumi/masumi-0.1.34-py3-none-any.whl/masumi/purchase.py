from dataclasses import dataclass
from typing import List, Dict, Optional
import logging
import aiohttp
from .config import Config
import hashlib
from .helper_functions import _hash_input


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@dataclass
class PurchaseAmount:
    amount: str
    unit: str = "lovelace"

class Purchase:
    DEFAULT_NETWORK = "Preprod"
    DEFAULT_PAYMENT_TYPE = "Web3CardanoV1"
    
    def __init__(
        self,
        config: Config,
        blockchain_identifier: str,
        seller_vkey: str,
        agent_identifier: str,
        submit_result_time: int,  # Unix timestamp
        unlock_time: int,         # Unix timestamp
        external_dispute_unlock_time: int,  # Unix timestamp
        amounts: Optional[List[PurchaseAmount]] = None,
        smart_contract_address: Optional[str] = None,
        identifier_from_purchaser: Optional[str] = None,
        network: str = DEFAULT_NETWORK,
        payment_type: str = DEFAULT_PAYMENT_TYPE,
        input_data: Optional[dict] = None
    ):
        self.config = config
        self.blockchain_identifier = blockchain_identifier
        self.seller_vkey = seller_vkey
        self.smart_contract_address = smart_contract_address
        self.amounts = amounts
        self.agent_identifier = agent_identifier
        self.identifier_from_purchaser = identifier_from_purchaser or "default_purchaser_id"
        self.network = network
        self.payment_type = payment_type
        self.submit_result_time = submit_result_time
        self.unlock_time = unlock_time
        self.external_dispute_unlock_time = external_dispute_unlock_time
        self.input_hash = _hash_input(input_data, self.identifier_from_purchaser) if input_data else None
        
        self._headers = {
            "token": config.payment_api_key,
            "Content-Type": "application/json"
        }
        
        logger.debug(f"Purchase initialized for agent: {agent_identifier}")
        logger.debug(f"Using blockchain identifier: {blockchain_identifier}")
        logger.debug(f"Network: {network}")
        logger.debug(f"Time values - Submit: {submit_result_time}, Unlock: {unlock_time}, Dispute: {external_dispute_unlock_time}")
        if self.input_hash:
            logger.debug(f"Input hash: {self.input_hash}")

    async def create_purchase_request(self) -> Dict:
        """Create a new purchase request"""
        logger.info("Creating purchase request")
        
        payload = {
            "identifierFromPurchaser": self.identifier_from_purchaser,
            "blockchainIdentifier": self.blockchain_identifier,
            "network": self.network,
            "sellerVkey": self.seller_vkey,
            "paymentType": self.payment_type,
            "submitResultTime": str(self.submit_result_time),
            "unlockTime": str(self.unlock_time),
            "externalDisputeUnlockTime": str(self.external_dispute_unlock_time),
            "agentIdentifier": self.agent_identifier
        }

        # Add amounts only if they're provided
        if self.amounts:
            payload["Amounts"] = [
                {"amount": amt.amount, "unit": amt.unit}
                for amt in self.amounts
            ]
            logger.debug(f"Added amounts to payload: {payload['Amounts']}")

        # Add smart contract address only if it's provided
        if self.smart_contract_address:
            payload["smartContractAddress"] = self.smart_contract_address
            logger.debug(f"Added smart contract address to payload: {self.smart_contract_address}")

        # Add input hash to payload if available
        if self.input_hash:
            payload["inputHash"] = self.input_hash
            logger.debug(f"Added input hash to payload: {self.input_hash}")
        
        # Add detailed logging of the complete payload
        logger.info("Purchase request payload created")
        logger.debug(f"Full purchase request payload: {payload}")
        
        # Log each field separately for easier debugging
        logger.debug(f"identifierFromPurchaser: {payload['identifierFromPurchaser']}")
        logger.debug(f"blockchainIdentifier: {payload['blockchainIdentifier']}")
        logger.debug(f"network: {payload['network']}")
        logger.debug(f"sellerVkey: {payload['sellerVkey']}")
        if self.smart_contract_address:
            logger.debug(f"smartContractAddress: {payload['smartContractAddress']}")
        #logger.debug(f"amounts: {payload['Amounts']}")
        logger.debug(f"paymentType: {payload['paymentType']}")
        logger.debug(f"submitResultTime: {payload['submitResultTime']}")
        logger.debug(f"unlockTime: {payload['unlockTime']}")
        logger.debug(f"externalDisputeUnlockTime: {payload['externalDisputeUnlockTime']}")
        logger.debug(f"agentIdentifier: {payload['agentIdentifier']}")
        if self.input_hash:
            logger.debug(f"inputHash: {payload['inputHash']}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.config.payment_service_url}/purchase/",
                    headers=self._headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Purchase request failed: {error_text}")
                        raise ValueError(f"Purchase request failed: {error_text}")
                    
                    result = await response.json()
                    logger.info("Purchase request created successfully")
                    logger.debug(f"Purchase response: {result}")
                    return result
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error during purchase request: {str(e)}")
            raise
