import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Set
from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException
import ccxt.async_support as ccxt
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """
    WebSocket connection manager for real-time market data.
    """
    
    def __init__(self):
        """Initialize the connection manager."""
        self.active_connections: List[WebSocket] = []
        self.subscriptions: Dict[WebSocket, Set[str]] = {}
        self.exchange_connections: Dict[str, Any] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
    
    async def connect(self, websocket: WebSocket):
        """Connect a WebSocket client."""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.subscriptions[websocket] = set()
        logger.info(f"WebSocket client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        if websocket in self.subscriptions:
            # Unsubscribe from all channels
            for channel in list(self.subscriptions[websocket]):
                self._unsubscribe(websocket, channel)
            
            del self.subscriptions[websocket]
        
        logger.info(f"WebSocket client disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: Any, websocket: WebSocket):
        """Send a message to a specific client."""
        try:
            if isinstance(message, dict) or isinstance(message, list):
                await websocket.send_json(message)
            else:
                await websocket.send_text(str(message))
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Any):
        """Broadcast a message to all connected clients."""
        for connection in self.active_connections:
            await self.send_personal_message(message, connection)
    
    def _get_channel_key(self, exchange_id: str, symbol: str, channel: str) -> str:
        """Get a unique key for a subscription channel."""
        return f"{exchange_id}:{symbol}:{channel}"
    
    async def subscribe(self, websocket: WebSocket, exchange_id: str, symbol: str, channel: str):
        """Subscribe a client to a market data channel."""
        channel_key = self._get_channel_key(exchange_id, symbol, channel)
        
        # Add to client's subscriptions
        if websocket in self.subscriptions:
            self.subscriptions[websocket].add(channel_key)
        
        # Start the data stream if not already running
        if channel_key not in self.running_tasks:
            task = asyncio.create_task(
                self._stream_market_data(exchange_id, symbol, channel, channel_key)
            )
            self.running_tasks[channel_key] = task
        
        logger.info(f"Client subscribed to {channel_key}")
        
        # Send confirmation
        await self.send_personal_message(
            {
                "type": "subscription",
                "status": "subscribed",
                "exchange": exchange_id,
                "symbol": symbol,
                "channel": channel,
                "timestamp": datetime.utcnow().isoformat()
            },
            websocket
        )
    
    def _unsubscribe(self, websocket: WebSocket, channel_key: str):
        """Unsubscribe a client from a channel."""
        if websocket in self.subscriptions and channel_key in self.subscriptions[websocket]:
            self.subscriptions[websocket].remove(channel_key)
            
            # Check if any clients are still subscribed to this channel
            active_subscribers = sum(1 for subs in self.subscriptions.values() if channel_key in subs)
            
            # If no more subscribers, stop the data stream
            if active_subscribers == 0 and channel_key in self.running_tasks:
                self.running_tasks[channel_key].cancel()
                del self.running_tasks[channel_key]
                
                # Close exchange connection if needed
                exchange_id = channel_key.split(":")[0]
                if exchange_id in self.exchange_connections:
                    asyncio.create_task(self._close_exchange(exchange_id))
            
            logger.info(f"Client unsubscribed from {channel_key}")
    
    async def unsubscribe(self, websocket: WebSocket, exchange_id: str, symbol: str, channel: str):
        """Unsubscribe a client from a market data channel."""
        channel_key = self._get_channel_key(exchange_id, symbol, channel)
        self._unsubscribe(websocket, channel_key)
        
        # Send confirmation
        await self.send_personal_message(
            {
                "type": "subscription",
                "status": "unsubscribed",
                "exchange": exchange_id,
                "symbol": symbol,
                "channel": channel,
                "timestamp": datetime.utcnow().isoformat()
            },
            websocket
        )
    
    async def _get_exchange(self, exchange_id: str):
        """Get or create an exchange connection."""
        if exchange_id not in self.exchange_connections:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                exchange = exchange_class({
                    'enableRateLimit': True,
                })
                self.exchange_connections[exchange_id] = exchange
                logger.info(f"Created connection to exchange: {exchange_id}")
            except Exception as e:
                logger.error(f"Error creating exchange connection for {exchange_id}: {e}")
                raise
        
        return self.exchange_connections[exchange_id]
    
    async def _close_exchange(self, exchange_id: str):
        """Close an exchange connection."""
        if exchange_id in self.exchange_connections:
            try:
                await self.exchange_connections[exchange_id].close()
                del self.exchange_connections[exchange_id]
                logger.info(f"Closed connection to exchange: {exchange_id}")
            except Exception as e:
                logger.error(f"Error closing exchange connection for {exchange_id}: {e}")
    
    async def _stream_market_data(self, exchange_id: str, symbol: str, channel: str, channel_key: str):
        """Stream market data for a specific channel."""
        try:
            exchange = await self._get_exchange(exchange_id)
            
            # Different handling based on channel type
            if channel == "ticker":
                await self._stream_ticker(exchange, exchange_id, symbol, channel_key)
            elif channel == "orderbook":
                await self._stream_orderbook(exchange, exchange_id, symbol, channel_key)
            elif channel == "trades":
                await self._stream_trades(exchange, exchange_id, symbol, channel_key)
            else:
                logger.error(f"Unsupported channel: {channel}")
                return
                
        except asyncio.CancelledError:
            logger.info(f"Streaming task for {channel_key} was cancelled")
        except Exception as e:
            logger.error(f"Error in market data stream for {channel_key}: {e}")
            
            # Notify subscribers about the error
            error_message = {
                "type": "error",
                "exchange": exchange_id,
                "symbol": symbol,
                "channel": channel,
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            for websocket in self.active_connections:
                if websocket in self.subscriptions and channel_key in self.subscriptions[websocket]:
                    asyncio.create_task(self.send_personal_message(error_message, websocket))
    
    async def _stream_ticker(self, exchange, exchange_id: str, symbol: str, channel_key: str):
        """Stream ticker data."""
        while True:
            try:
                # Fetch ticker
                ticker = await exchange.fetch_ticker(symbol)
                
                # Format message
                message = {
                    "type": "ticker",
                    "exchange": exchange_id,
                    "symbol": symbol,
                    "data": {
                        "bid": ticker["bid"],
                        "ask": ticker["ask"],
                        "last": ticker["last"],
                        "high": ticker["high"],
                        "low": ticker["low"],
                        "volume": ticker["volume"],
                        "change": ticker["change"] if "change" in ticker else None,
                        "percentage": ticker["percentage"] if "percentage" in ticker else None,
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                # Send to subscribers
                for websocket in self.active_connections:
                    if websocket in self.subscriptions and channel_key in self.subscriptions[websocket]:
                        asyncio.create_task(self.send_personal_message(message, websocket))
                
                # Wait before next update
                await asyncio.sleep(1)  # Adjust based on rate limits
                
            except Exception as e:
                logger.error(f"Error fetching ticker for {symbol} on {exchange_id}: {e}")
                await asyncio.sleep(5)  # Wait longer on error
    
    async def _stream_orderbook(self, exchange, exchange_id: str, symbol: str, channel_key: str):
        """Stream order book data."""
        while True:
            try:
                # Fetch order book
                orderbook = await exchange.fetch_order_book(symbol)
                
                # Format message
                message = {
                    "type": "orderbook",
                    "exchange": exchange_id,
                    "symbol": symbol,
                    "data": {
                        "bids": orderbook["bids"][:10],  # Top 10 bids
                        "asks": orderbook["asks"][:10],  # Top 10 asks
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                # Send to subscribers
                for websocket in self.active_connections:
                    if websocket in self.subscriptions and channel_key in self.subscriptions[websocket]:
                        asyncio.create_task(self.send_personal_message(message, websocket))
                
                # Wait before next update
                await asyncio.sleep(2)  # Adjust based on rate limits
                
            except Exception as e:
                logger.error(f"Error fetching orderbook for {symbol} on {exchange_id}: {e}")
                await asyncio.sleep(5)  # Wait longer on error
    
    async def _stream_trades(self, exchange, exchange_id: str, symbol: str, channel_key: str):
        """Stream recent trades data."""
        last_trade_id = None
        
        while True:
            try:
                # Fetch recent trades
                trades = await exchange.fetch_trades(symbol)
                
                # Filter new trades
                if last_trade_id:
                    new_trades = [trade for trade in trades if trade["id"] > last_trade_id]
                else:
                    new_trades = trades[:5]  # First time, just get the 5 most recent
                
                if new_trades:
                    # Update last trade ID
                    last_trade_id = max(trade["id"] for trade in new_trades if "id" in trade)
                    
                    # Format message
                    message = {
                        "type": "trades",
                        "exchange": exchange_id,
                        "symbol": symbol,
                        "data": [
                            {
                                "id": trade["id"] if "id" in trade else None,
                                "price": trade["price"],
                                "amount": trade["amount"],
                                "side": trade["side"],
                                "timestamp": trade["timestamp"]
                            }
                            for trade in new_trades
                        ],
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    # Send to subscribers
                    for websocket in self.active_connections:
                        if websocket in self.subscriptions and channel_key in self.subscriptions[websocket]:
                            asyncio.create_task(self.send_personal_message(message, websocket))
                
                # Wait before next update
                await asyncio.sleep(3)  # Adjust based on rate limits
                
            except Exception as e:
                logger.error(f"Error fetching trades for {symbol} on {exchange_id}: {e}")
                await asyncio.sleep(5)  # Wait longer on error

# Create a connection manager instance
manager = ConnectionManager()

async def handle_websocket(websocket: WebSocket):
    """Handle WebSocket connections and messages."""
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "subscribe":
                await manager.subscribe(
                    websocket,
                    message["exchange"],
                    message["symbol"],
                    message["channel"]
                )
            elif message["type"] == "unsubscribe":
                await manager.unsubscribe(
                    websocket,
                    message["exchange"],
                    message["symbol"],
                    message["channel"]
                )
            elif message["type"] == "ping":
                await manager.send_personal_message({"type": "pong"}, websocket)
            else:
                await manager.send_personal_message(
                    {
                        "type": "error",
                        "message": f"Unsupported message type: {message['type']}",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    websocket
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
