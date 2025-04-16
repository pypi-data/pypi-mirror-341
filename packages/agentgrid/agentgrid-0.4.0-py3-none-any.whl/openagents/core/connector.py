from typing import Dict, Any, Optional, Callable, Awaitable, List, Set
import logging
import json
import asyncio
import websockets
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed
from omniagents.utils.message_util import parse_message_dict
from omniagents.models.messages import BaseMessage, BroadcastMessage, DirectMessage, ProtocolMessage
from .system_commands import send_system_request as send_system_request_impl
from .system_commands import REGISTER_AGENT, LIST_AGENTS, LIST_PROTOCOLS, GET_PROTOCOL_MANIFEST

logger = logging.getLogger(__name__)

class NetworkConnector:
    """Handles network connections and message passing for agents.
    
    Responsible for establishing connections to network servers and
    handling message sending/receiving.
    """
    
    def __init__(self, host: str, port: int, agent_id: str, metadata: Optional[Dict[str, Any]] = None):
        """Initialize a network connector.
        
        Args:
            host: Server host address
            port: Server port
            metadata: Agent metadata to send during registration
        """
        self.host = host
        self.port = port
        self.agent_id = agent_id
        self.metadata = metadata
        self.connection = None
        self.is_connected = False
        self.message_handlers: Dict[str, List[Callable[[Any], Awaitable[None]]]] = {}
        self.system_handlers = {}
    
    async def connect_to_server(self) -> bool:
        """Connect to a network server.
        
        Args:
            host: Server host address
            port: Server port
            metadata: Agent metadata to send during registration
            
        Returns:
            bool: True if connection successful
        """
        try:
            self.connection = await connect(f"ws://{self.host}:{self.port}")
            
            # Register with server using system_request
            await send_system_request_impl(
                self.connection, 
                REGISTER_AGENT, 
                agent_id=self.agent_id, 
                metadata=self.metadata
            )
            
            # Wait for registration response
            response = await self.connection.recv()
            data = json.loads(response)
            
            if data.get("type") == "system_response" and data.get("command") == REGISTER_AGENT and data.get("success"):
                self.is_connected = True
                logger.info(f"Connected to network: {data.get('network_name')}")
                
                # Start message listener
                asyncio.create_task(self._listen_for_messages())
                return True
            
            await self.connection.close()
            return False
            
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from the network server.
        
        Returns:
            bool: True if disconnection was successful
        """
        if self.connection:
            try:
                await self.connection.close()
                self.connection = None
                self.is_connected = False
                logger.info(f"Agent {self.agent_id} disconnected from network")
                return True
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")
                return False
        return False
    
    def register_message_handler(self, message_type: str, handler: Callable[[Any], Awaitable[None]]) -> None:
        """Register a handler for a specific message type.
        
        Args:
            message_type: Type of message to handle
            handler: Async function to call when message is received
        """
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        
        # Add handler to the list if it's not already there
        if handler not in self.message_handlers[message_type]:
            self.message_handlers[message_type].append(handler)
            logger.debug(f"Registered handler for message type: {message_type}")
    
    def unregister_message_handler(self, message_type: str, handler: Callable[[Any], Awaitable[None]]) -> bool:
        """Unregister a handler for a specific message type.
        
        Args:
            message_type: Type of message to handle
            handler: The handler function to remove
            
        Returns:
            bool: True if handler was removed, False if not found
        """
        if message_type in self.message_handlers and handler in self.message_handlers[message_type]:
            self.message_handlers[message_type].remove(handler)
            logger.debug(f"Unregistered handler for message type: {message_type}")
            
            # Clean up empty lists
            if not self.message_handlers[message_type]:
                del self.message_handlers[message_type]
                
            return True
        return False
    
    def register_system_handler(self, command: str, handler: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        """Register a handler for a specific system command response.
        
        Args:
            command: Type of system command response to handle
            handler: Async function to call when system response is received
        """
        self.system_handlers[command] = handler
        logger.debug(f"Registered handler for system command: {command}")
    
    async def _listen_for_messages(self) -> None:
        """Listen for messages from the server."""
        try:
            while self.is_connected:
                message = await self.connection.recv()
                data = json.loads(message)
                
                # Handle different message types
                if data.get("type") == "message":
                    message_data = data.get("data", {})
                    message_obj = parse_message_dict(message_data)
                    
                    logger.debug(f"Received message from {message_obj.sender_id} with ID {message_obj.message_id}")
                    
                    # Call the appropriate message handler
                    await self.consume_message(message_obj)
                
                # Handle system responses
                elif data.get("type") == "system_response":
                    command = data.get("command")
                    if command in self.system_handlers:
                        await self.system_handlers[command](data)
                    else:
                        logger.debug(f"Received system response for command {command}")
            

        except ConnectionClosed:
            self.is_connected = False
            logger.info("Disconnected from server")
        except Exception as e:
            logger.error(f"Error in message listener: {e}")
            self.is_connected = False
    
    async def consume_message(self, message: BaseMessage) -> None:
        """Consume a message on the agent side.
        
        Args:
            message: Message to consume
        """
        if isinstance(message, ProtocolMessage):
            message.relevant_agent_id = self.agent_id
            
        message_type = message.message_type
        if message_type in self.message_handlers:
            # Call all handlers for this message type
            for handler in reversed(self.message_handlers[message_type]):
                try:
                    await handler(message)
                except Exception as e:
                    logger.error(f"Error in message handler for {message_type}: {e}")
    
    async def send_message(self, message: BaseMessage) -> bool:
        """Send a message to another agent.
        
        Args:
            message: Message to send (must be a BaseMessage instance)
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.is_connected:
            logger.warning(f"Agent {self.agent_id} is not connected to a network")
            return False
            
        try:
            # Ensure sender_id is set
            if not message.sender_id:
                message.sender_id = self.agent_id
            
            if isinstance(message, ProtocolMessage):
                message.relevant_agent_id = self.agent_id
                
            # Send the message
            await self.connection.send(json.dumps({
                "type": "message",
                "data": message.model_dump()
            }))
            
            logger.debug(f"Message sent: {message.message_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    async def send_direct_message(self, message: DirectMessage) -> bool:
        """Send a direct message to another agent.
        
        Args:
            message: Direct message to send
        """
        return await self.send_message(message)
    
    async def send_broadcast_message(self, message: BroadcastMessage) -> bool:
        """Send a broadcast message to all connected agents.
        
        Args:
            message: Broadcast message to send

        Returns:
            bool: True if message sent successfully, False otherwise
        """
        return await self.send_message(message)
    
    async def send_protocol_message(self, message: ProtocolMessage) -> bool:
        """Send a protocol message to another agent.
        
        Args:
            message: Protocol message to send
        """
        return await self.send_message(message)
    
    async def wait_protocol_message(self, protocol_name: str, filter_dict: Optional[Dict[str, Any]] = None, timeout: float = 5.0) -> Optional[ProtocolMessage]:
        """Wait for a protocol message from the specified protocol that matches the filter criteria.
        
        Args:
            protocol_name: The protocol name to match
            filter_dict: Optional dictionary of key-value pairs to match in the message content
            timeout: Maximum time to wait for a response in seconds
            
        Returns:
            Optional[ProtocolMessage]: The matching message, or None if no matching message received within timeout
        """
        if not self.is_connected:
            logger.warning(f"Agent {self.agent_id} is not connected to a network")
            return None
            
        # Create a future to store the response
        response_future = asyncio.Future()
        
        async def temp_protocol_handler(msg: ProtocolMessage) -> None:
            # Check if this is the message we're waiting for
            if (msg.protocol == protocol_name and 
                msg.relevant_agent_id == self.agent_id):
                
                # If filter_dict is provided, check if all key-value pairs match in the content
                if filter_dict:
                    matches = True
                    for key, value in filter_dict.items():
                        if key not in msg.content or msg.content[key] != value:
                            matches = False
                            break
                    
                    if matches:
                        response_future.set_result(msg)
                else:
                    # No filter, accept any message from this protocol
                    response_future.set_result(msg)
        
        # Register the temporary handler
        self.register_message_handler("protocol_message", temp_protocol_handler)
        
        try:
            # Wait for the response with timeout
            try:
                response = await asyncio.wait_for(response_future, timeout)
                return response
            except asyncio.TimeoutError:
                filter_str = f" with filter {filter_dict}" if filter_dict else ""
                logger.warning(f"Timeout waiting for protocol message: {protocol_name}{filter_str}")
                return None
                
        finally:
            # Unregister the temporary handler
            self.unregister_message_handler("protocol_message", temp_protocol_handler)
    
    async def wait_direct_message(self, sender_id: str, timeout: float = 5.0) -> Optional[DirectMessage]:
        """Wait for a direct message from the specified sender.
        
        Args:
            sender_id: The ID of the sender to wait for
            timeout: Maximum time to wait for a response in seconds
            
        Returns:
            Optional[DirectMessage]: The received message or None if timeout occurs
        """
        # Create a future to be resolved when the message is received
        response_future = asyncio.Future()
        
        # Create a temporary handler that will resolve the future when the message arrives
        async def temp_direct_handler(msg: DirectMessage) -> None:
            # Check if this is the message we're waiting for
            if msg.sender_id == sender_id:
                response_future.set_result(msg)
        
        # Register the temporary handler
        self.register_message_handler("direct_message", temp_direct_handler)
        
        try:
            # Wait for the response with timeout
            try:
                response = await asyncio.wait_for(response_future, timeout)
                return response
            except asyncio.TimeoutError:
                logger.warning(f"Timeout waiting for direct message from: {sender_id}")
                return None
                
        finally:
            # Unregister the temporary handler
            self.unregister_message_handler("direct_message", temp_direct_handler)
    
    async def send_system_request(self, command: str, **kwargs) -> bool:
        """Send a system request to the network server.
        
        Args:
            command: The system command to send
            **kwargs: Additional parameters for the command
            
        Returns:
            bool: True if request was sent successfully
        """
        if not self.is_connected:
            logger.warning(f"Agent {self.agent_id} is not connected to a network")
            return False
            
        return await send_system_request_impl(self.connection, command, **kwargs)
    
    async def list_agents(self) -> bool:
        """Request a list of agents from the network server.
        
        Returns:
            bool: True if request was sent successfully
        """
        return await self.send_system_request(LIST_AGENTS)
    
    async def list_protocols(self) -> bool:
        """Request a list of protocols from the network server.
        
        Returns:
            bool: True if request was sent successfully
        """
        return await self.send_system_request(LIST_PROTOCOLS)

    async def get_protocol_manifest(self, protocol_name: str) -> bool:
        """Request a protocol manifest from the network server.
        
        Args:
            protocol_name: Name of the protocol to get the manifest for
            
        Returns:
            bool: True if request was sent successfully
        """
        return await self.send_system_request(GET_PROTOCOL_MANIFEST, protocol_name=protocol_name)