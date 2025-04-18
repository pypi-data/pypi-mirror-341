from enum import Enum
from typing import Dict, List, Optional, Tuple
import grpc
import certifi
from abc import ABC, abstractmethod
from .protos import exchange_pb2 as exchange
from .protos import exchange_pb2_grpc
from .protos import marketdata_pb2 as marketdata
from .protos import marketdata_pb2_grpc
from .protos import admin_pb2
from .protos import admin_pb2_grpc
import asyncio

from dataclasses import dataclass

class OrderSide(Enum):
    BUY = 0
    SELL = 1
    
class OrderTif(Enum):
    DAY = 0
    IOC = 1
    
@dataclass
class Position:
    symbol: str
    position: int
    lower_bound: float
    upper_bound: float
    

@dataclass
class PublicOrder:
    symbol: str
    size: int
    price: int

@dataclass
class TapeMessage:
    symbol: str
    price: int
    size: int
    issued_at: str

@dataclass
class OrderBook:
    bids: List[PublicOrder]
    asks: List[PublicOrder]

@dataclass
class MarketData:
    symbol: str
    tape: List[TapeMessage]
    book: OrderBook
    volume: int

@dataclass
class Order:
    id: str
    symbol: str
    logging: str
    size: int
    price: int
    side: OrderSide
    created_at: str
    
@dataclass 
class Fill:
    order_id: str
    symbol: str
    price: int
    size: int
    side: OrderSide
    issued_at: str

@dataclass
class ExchangeStatus:
    status: str
    market_symbols: List[str]

@dataclass
class Response:
    status: str
    message: str
    

@dataclass
class ResponseList:
    response: Optional[Response]
    order_responses: List[Response]

def get_channel(url, secure):
    # Load the CA bundle from certifi
    if not secure:
        return grpc.insecure_channel(url)
    else:
        with open(certifi.where(), "rb") as f:
            trusted_certs = f.read()
        # Create secure channel credentials using the trusted certificates
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        return grpc.secure_channel(url, credentials)

def get_async_channel(url, secure):
    # Load the CA bundle from certifi
    if not secure:
        return grpc.aio.insecure_channel(url)
    else:
        with open(certifi.where(), "rb") as f:
            trusted_certs = f.read()
        # Create secure channel credentials using the trusted certificates
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        return grpc.aio.secure_channel(url, credentials)
        

class AdvancedTrader(ABC):
    def __init__(self, account, api_key, url, secure = True):
        # self.channel = get_channel(url, secure)
        self.async_channel = get_async_channel(url, secure)
        self.eStub = exchange_pb2_grpc.ExchangeStub(self.async_channel)
        self.mStub = marketdata_pb2_grpc.MarketDataServiceStub(self.async_channel)
        self.api_key = api_key
        self.account = account
    async def submit_order(self, symbol: str, logging: str, size: int, price: int, side: OrderSide, tif: OrderTif) -> Response:
        return await submit_order(self.eStub, symbol, logging, size, price, side, tif, self.account, self.api_key)
    
    async def cancel_order(self, order_id: str) -> Response:
        return await cancel_order(self.eStub, order_id, self.account, self.api_key)
    
    async def cancel_orders(self, order_ids: List[str]) -> ResponseList:
        return await cancel_orders(self.eStub, order_ids, self.account, self.api_key)
    
    @abstractmethod
    async def handle_md_update(self, data: MarketData):
        pass
    
    @abstractmethod
    async def handle_open_orders_update(self, data: List[Order]):
        pass
    
    @abstractmethod
    async def handle_positions_update(self, data: List[Position]):
        pass
    
    @abstractmethod
    async def handle_fill_update(self, data: Fill):
        pass
    
    @abstractmethod
    async def handle_recent_fills(self, data: List[Fill]):
        pass
    
    @abstractmethod
    async def handle_exchange_status_update(self, data):
        pass
    
    async def listen(self):
        try:
            request = marketdata.SubscriptionRequest(
                api_key=self.api_key,
                account=self.account
            )
            # Calling the streaming RPC method.
            stream = self.mStub.StreamStatus(request)
            # Iterate over the stream of responses.
            async for market_data in stream:
                field = market_data.WhichOneof("response")
                if field == "orderbook":
                    orderbook = market_data.orderbook
                    symbol = orderbook.symbol
                    bids = list(map(lambda x: PublicOrder(x.symbol, int(x.size), int(x.price)), orderbook.book.bids))
                    asks = list(map(lambda x: PublicOrder(x.symbol, int(x.size), int(x.price)), orderbook.book.asks))
                    book = OrderBook(bids, asks)
                    tape = list(map(lambda x: TapeMessage(x.symbol, int(x.price), int(x.size), x.issued_at), orderbook.tape))
                    await self.handle_md_update(MarketData(symbol, tape, book, int(orderbook.volume)))
                elif field == "orders":
                    orders = list(map(lambda x: Order(x.id, x.symbol, x.logging, int(x.size), int(x.price), OrderSide(x.side), x.created_at), market_data.orders.orders))
                    await self.handle_open_orders_update(orders)
                elif field == "positions":
                    positions = list(map(lambda x: Position(x.symbol, int(x.position), float(x.lower_bound), float(x.upper_bound)), market_data.positions.positions))
                    await self.handle_positions_update(positions)
                elif field == "fill":
                    f = market_data.fill
                    fill = Fill(f.order_id, f.symbol, int(f.price), int(f.size), OrderSide(f.side), f.issued_at)
                    await self.handle_fill_update(fill)
                elif field == "recent_fills":
                    fills = list(map(lambda f: Fill(f.order_id, f.symbol, int(f.price), int(f.size), OrderSide(f.side), f.issued_at), market_data.recent_fills.fills))
                    await self.handle_recent_fills(fills)
                elif field == "exchange_status":
                    e = market_data.exchange_status
                    status = ExchangeStatus(e.status, e.market_symbols)
                    await self.handle_exchange_status_update(status)
                else:
                    continue
                    
        except asyncio.CancelledError:
            raise

class Trader():
    def __init__(self, account, api_key, url, secure = True):
        self.channel = get_channel(url, secure)
        self.stub = exchange_pb2_grpc.ExchangeStub(self.channel)
        self.api_key = api_key
        self.account = account
    
    def submit_order(self, symbol: str, size: int, price: int, side: OrderSide, tif: OrderTif) -> Response:
        return submit_order(self.stub, symbol, "", size, price, side, tif, self.account, self.api_key)
    
    def cancel_order(self, order_id: str) -> Response:
        return cancel_order(self.stub, order_id, self.account, self.api_key)
    
    def cancel_orders(self, order_ids: List[str]) -> ResponseList:
        return cancel_orders(self.stub, order_ids, self.account, self.api_key)

class Listener():
    def __init__(self, account, api_key, url, secure = True):
        self.channel = get_async_channel(url, secure)
        self.stub = marketdata_pb2_grpc.MarketDataServiceStub(self.channel)
        self.api_key = api_key
        self.account = account
    
    async def listen(self):
        await listen(self.stub, self.account, self.api_key)
        
class Admin():
    def __init__(self, account, api_key, url, secure = True):
        self.channel = get_channel(url, secure)
        self.stub = admin_pb2_grpc.AdminServiceStub(self.channel)
        self.api_key = api_key
        self.account = account
    
    def add_partition(self, partition: str):
        return add_partition(
            stub=self.stub,
            partition=partition,
            account=self.account,
            api_key=self.api_key
        )

    def add_account_type_to_partition(self, partition: str, account_type: str):
        return add_account_type_to_partition(
            stub=self.stub,
            partition=partition,
            account_type=account_type,
            account=self.account,
            api_key=self.api_key
        )

    def add_symbol(self, partition: str, id: str, display_name: str):
        return add_symbol(
            stub=self.stub,
            partition=partition,
            id=id,
            name=display_name,
            account=self.account,
            api_key=self.api_key
        )

    def start_partition(self, partition: str):
        return start_partition(
            stub=self.stub,
            partition=partition,
            account=self.account,
            api_key=self.api_key
        )

    def pause_partition(self, partition: str):
        return pause_partition(
            stub=self.stub,
            partition=partition,
            account=self.account,
            api_key=self.api_key
        )

    # Analogues for the remaining Admin RPC functions:

    def end_partition(self, partition: str):
        return end_partition(
            stub=self.stub,
            partition=partition,
            account=self.account,
            api_key=self.api_key
        )

    def settle_partition(self, partition: str, settle_prices: Dict[str, int]):
        """
        settle_prices: Dict mapping symbol to price
        """
        prices = []
        for key in settle_prices:
            prices.append((key, str(settle_prices[key])))
        return settle_partition(
            stub=self.stub,
            partition=partition,
            settle_prices=prices,
            account=self.account,
            api_key=self.api_key
        )

    def open_exchange(self):
        return open_exchange(
            stub=self.stub,
            account=self.account,
            api_key=self.api_key
        )

    def close_exchange(self):
        return close_exchange(
            stub=self.stub,
            account=self.account,
            api_key=self.api_key
        )

    def set_position(self, account: str, symbol: str, value: int):
        return set_position(
            stub=self.stub,
            account=account,
            symbol=symbol,
            value=str(value),
            admin_account=self.account,
            api_key=self.api_key
        )

    def adjust_position(self, account: str, symbol: str, value: int):
        return adjust_position(
            stub=self.stub,
            account=account,
            symbol=symbol,
            value=str(value),
            admin_account=self.account,
            api_key=self.api_key
        )

    def set_account_fee(self, account: str, fee: int):
        return set_account_fee(
            stub=self.stub,
            account=account,
            fee=str(fee),
            admin_account=self.account,
            api_key=self.api_key
        )

    def set_enable_fee(self, symbol: str, enable: bool):
        return set_enable_fee(
            stub=self.stub,
            symbol=symbol,
            enable=enable,
            account=self.account,
            api_key=self.api_key
        )
    
    def set_position_limits(self, account: str, symbol: str, lower_bound: float, upper_bound: float):
        if lower_bound == -float('inf'):
            lower_bound = "-Infinity"
        else:
            lower_bound = int(lower_bound)
        if upper_bound == float('inf'):
            upper_bound = "Infinity"
        else:
            upper_bound = int(upper_bound)
        return set_position_limits(
            stub=self.stub,
            account=account,
            symbol=symbol,
            lower_bound=str(lower_bound),
            upper_bound=str(upper_bound),
            admin_account=self.account,
            api_key=self.api_key
        )

    def register_named_account(self, account: str):
        return register_named_account(
            stub=self.stub,
            account=account,
            admin_account=self.account,
            api_key=self.api_key
        )
    
    def register_bot_account(self, account: str):
        return register_bot_account(
            stub=self.stub,
            account=account,
            admin_account=self.account,
            api_key=self.api_key
        )
    
    def send_private_message(self, account: str, message: str):
        return send_private_message(
            stub=self.stub,
            account=account,
            message=message,
            admin_account=self.account,
            api_key=self.api_key
        )
    def send_public_message(self, partition: str, message: str):
        return send_public_message(
            stub=self.stub,
            partition=partition,
            message=message,
            admin_account=self.account,
            api_key=self.api_key
        )
    def get_position(self, account: str, symbol: str) -> int:
        return get_position(
            stub=self.stub,
            account=account,
            symbol=symbol,
            admin_account=self.account,
            api_key=self.api_key
        )
    def upsert_user(self, user: str) -> Response:
        return upsert_user(
            stub=self.stub,
            user=user,
            admin_account=self.account,
            api_key=self.api_key
        )
    def clear_user_accounts(self, user: str) -> Response:
        return clear_user_accounts(
            stub=self.stub,
            user=user,
            admin_account=self.account,
            api_key=self.api_key
        )
    def delete_user_from_account(self, user: str, account: str) -> Response:
        return delete_user_from_account(
            stub=self.stub,
            user=user,
            account=account,
            admin_account=self.account,
            api_key=self.api_key
        )
    def add_user_to_account(self, user: str, account: str) -> Response:
        return add_user_to_account(
            stub=self.stub,
            user=user,
            account=account,
            admin_account=self.account,
            api_key=self.api_key
        )

        
    

async def submit_order(stub: exchange_pb2_grpc.ExchangeStub, symbol: str, logging: str, size: int, price: int, side: OrderSide, tif: OrderTif, account: str, api_key: str) -> Response: 
    request = exchange.OrderRequest(symbol = symbol, logging = logging, size = str(size), price = str(price), side = side.value, tif = tif.value, account = account, api_key = api_key)
    response = await stub.SubmitOrder(request)
    return Response(status = response.status, message = response.message)
    

    
async def cancel_order(stub: exchange_pb2_grpc.ExchangeStub, order_id: str, account: str, api_key: str) -> Response:
    request = exchange.CancelOrderRequest(order_id = order_id, account = account, api_key = api_key)
    response = await stub.CancelOrder(request)
    return Response(status = response.status, message = response.message)

async def cancel_orders(stub: exchange_pb2_grpc.ExchangeStub, order_ids: List[str], account: str, api_key: str) -> ResponseList:
    request = exchange.CancelOrdersRequest(order_ids = order_ids, account = account, api_key = api_key)
    response = await stub.CancelOrders(request)
    if response.HasField("response"):
        return ResponseList(response = response.response, order_responses = response.order_responses)
    else:
        return ResponseList(response = None, order_responses = response.order_responses)
    
def add_account_type_to_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account_type: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.AddAccountTypeToPartitionRequest(
        partition=partition, 
        account_type=account_type, 
        auth=auth
    )
    response = stub.AddAccountTypeToPartition(request)
    return Response(status=response.status, message=response.message)

def end_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.EndPartitionRequest(
        partition=partition, 
        auth=auth
    )
    response = stub.EndPartition(request)
    return Response(status=response.status, message=response.message)

def pause_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.PausePartitionRequest(
        partition=partition, 
        auth=auth
    )
    response = stub.PausePartition(request)
    return Response(status=response.status, message=response.message)

def start_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.StartPartitionRequest(
        partition=partition, 
        auth=auth
    )
    response = stub.StartPartition(request)
    return Response(status=response.status, message=response.message)

def settle_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    settle_prices: List[Tuple[str, str]], 
    account: str, 
    api_key: str
) -> Response:
    """
    settle_prices: list of tuples (symbol, price)
    """
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    settlements = [
        admin_pb2.Settlement(symbol=symbol, price=price)
        for symbol, price in settle_prices
    ]
    request = admin_pb2.SettlePartitionRequest(
        partition=partition, 
        settle_prices=settlements, 
        auth=auth
    )
    response = stub.SettlePartition(request)
    return Response(status=response.status, message=response.message)

def open_exchange(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.OpenExchangeRequest(auth=auth)
    response = stub.OpenExchange(request)
    return Response(status=response.status, message=response.message)

def close_exchange(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.CloseExchangeRequest(auth=auth)
    response = stub.CloseExchange(request)
    return Response(status=response.status, message=response.message)

def add_symbol(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    id: str, 
    name: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.AddSymbolRequest(
        partition=partition, 
        id=id, 
        name=name, 
        auth=auth
    )
    response = stub.AddSymbol(request)
    return Response(status=response.status, message=response.message)

def set_position(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    symbol: str, 
    value: str, 
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SetPositionRequest(
        account=account, 
        symbol=symbol, 
        value=value, 
        auth=auth
    )
    response = stub.SetPosition(request)
    return Response(status=response.status, message=response.message)

def adjust_position(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    symbol: str, 
    value: str, 
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.AdjustPositionRequest(
        account=account, 
        symbol=symbol, 
        value=value, 
        auth=auth
    )
    response = stub.AdjustPosition(request)
    return Response(status=response.status, message=response.message)

def set_account_fee(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    fee: str, 
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SetAccountFeeRequest(
        account=account, 
        fee=fee, 
        auth=auth
    )
    response = stub.SetAccountFee(request)
    return Response(status=response.status, message=response.message)

def set_enable_fee(
    stub: admin_pb2_grpc.AdminServiceStub, 
    symbol: str, 
    enable: bool, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.SetEnableFeeRequest(
        symbol=symbol, 
        enable=enable, 
        auth=auth
    )
    response = stub.SetEnableFee(request)
    return Response(status=response.status, message=response.message)

def set_position_limits(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    symbol: str, 
    lower_bound: str, 
    upper_bound: str, 
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SetPositionLimitsRequest(
        account=account, 
        symbol=symbol, 
        lower_bound=lower_bound, 
        upper_bound=upper_bound, 
        auth=auth
    )
    response = stub.SetPositionLimits(request)
    return Response(status=response.status, message=response.message)

def register_named_account(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str,
    admin_account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.RegisterNamedAccountRequest(
        account=account, 
        auth=auth
    )
    response = stub.RegisterNamedAccount(request)
    return Response(status=response.status, message=response.message)

def register_bot_account(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str,
    admin_account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.RegisterBotAccountRequest(
        account=account, 
        auth=auth
    )
    response = stub.RegisterBotAccount(request)
    return Response(status=response.status, message=response.message)

def add_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.AddPartitionRequest(
        partition=partition, 
        auth=auth
    )
    response = stub.AddPartition(request)
    return Response(status=response.status, message=response.message)

def send_private_message(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    message: str,
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SendPrivateMessageRequest(
        account=account, 
        message=message,
        auth=auth
    )
    response = stub.SendPrivateMessage(request)
    return Response(status=response.status, message=response.message)

def send_public_message(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    message: str,
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SendPublicMessageRequest(
        partition=partition, 
        message=message,
        auth=auth
    )
    response = stub.SendPublicMessage(request)
    return Response(status=response.status, message=response.message)

def get_position(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    symbol: str,
    admin_account: str,
    api_key: str
) -> int:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.GetPositionRequest(
        account=account, 
        symbol=symbol,
        auth=auth
    )
    response = stub.GetPosition(request)
    return int(response.message)

def upsert_user(
    stub: admin_pb2_grpc.AdminServiceStub,
    user: str,
    admin_account: str,
    api_key: str,
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.UpsertUserRequest(
        user=user,
        auth=auth
    )
    response = stub.UpsertUser(request)
    return Response(status=response.status, message=response.message)

def upsert_user(
    stub: admin_pb2_grpc.AdminServiceStub,
    user: str,
    admin_account: str,
    api_key: str,
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.UpsertUserRequest(
        user=user,
        auth=auth
    )
    response = stub.UpsertUser(request)
    return Response(status=response.status, message=response.message)

def add_user_to_account(
    stub: admin_pb2_grpc.AdminServiceStub,
    user: str,
    account: str,
    admin_account: str,
    api_key: str,
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.AddUserToAccountRequest(
        user=user,
        account=account,
        auth=auth
    )
    response = stub.AddUserToAccount(request)
    return Response(status=response.status, message=response.message)

def clear_user_accounts(
    stub: admin_pb2_grpc.AdminServiceStub,
    user: str,
    admin_account: str,
    api_key: str,
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.ClearUserAccountsRequest(
        user=user,
        auth=auth
    )
    response = stub.ClearUserAccounts(request)
    return Response(status=response.status, message=response.message)

def delete_user_from_account(
    stub: admin_pb2_grpc.AdminServiceStub,
    user: str,
    account: str,
    admin_account: str,
    api_key: str,
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.DeleteUserFromAccountRequest(
        user=user,
        account=account,
        auth=auth
    )
    response = stub.DeleteUserFromAccount(request)
    return Response(status=response.status, message=response.message)

    
async def listen(stub: marketdata_pb2_grpc.MarketDataServiceStub, account: str, api_key: str):
    # Build your subscription request. Adjust fields as needed.
    request = marketdata.SubscriptionRequest(
        api_key=api_key,
        account=account
    )
    
    # Calling the streaming RPC method.
    stream = stub.StreamStatus(request)
    
    # Iterate over the stream of responses.
    async for market_data in stream:
        print("Received market data:", market_data)