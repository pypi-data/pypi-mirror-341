from typing import Optional, Dict, Any
import asyncio
import zmq
import zmq.asyncio
from .proxy import XPubXSubProxy
from .metadata_responder import MetadataResponder
from ..utils.shared_state import SharedState
from ..utils.logger import logger
from ..utils.helpers import start_single_external_subscriber, stop_single_external_subscriber

class Orcustrator:
    """
    Orchestrates XPubXSubProxy proxy, MetadataResponder, and dynamically loaded External Subscribers.
    Manages core components and uses SharedState for configuration.
    Implemented as a singleton.
    """
    _instance: Optional['Orcustrator'] = None

    @classmethod
    def get_instance(cls) -> 'Orcustrator':
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the Orcustrator. Private, use get_instance()."""
        if Orcustrator._instance is not None:
            raise RuntimeError("Orcustrator is a singleton. Use get_instance() instead.")
        
        self.shared_state = SharedState.get_instance()
        self.ctx = zmq.asyncio.Context.instance()
        
        # Core component instances and state flags
        self.proxy: Optional[XPubXSubProxy] = None 
        self.proxy_started = False
        self.metadata_responder: Optional[MetadataResponder] = None
        self.metadata_responder_started = False
        # self.command_socket = None # Removed: Orcustrator should not publish external commands

        # External subscribers tracking
        self._external_subscribers: Dict[str, Dict[str, Any]] = {} # {"key": {"instance": obj, "task": task}}
        
        self._running = False # General running state (maybe less useful with ensure methods)
        self._core_tasks = [] # Tasks for proxy, metadata

    # --- Port Properties --- 
    @property
    def xpub_port(self) -> Optional[int]:
        """Get the XPUB port from shared state."""
        return self.shared_state.get("Orcustrator.XPub")
    
    @property
    def xsub_port(self) -> Optional[int]:
        """Get the XSUB port from shared state."""
        return self.shared_state.get("Orcustrator.XSub")
    
    @property
    def metadata_port(self) -> Optional[int]:
        """Get the metadata responder port from shared state."""
        # Use the property access within the class
        return self.shared_state.get("Orcustrator.MetadataResponder")
        
    @property
    def command_port(self) -> Optional[int]:
         """Get the command port from shared state."""
         return self.shared_state.get("Orcustrator.CommandPort")

    # --- Ensure Component Methods (like old structure) --- 

    async def ensure_proxy_started(self): # Simplified from old version, assumes ports exist
        """Ensure the ZeroMQ proxy is started using ports from SharedState."""
        if self.proxy_started:
             logger.debug("Proxy already started.")
             return
        xpub = self.xpub_port
        xsub = self.xsub_port
        if xpub is None or xsub is None:
            self.proxy = XPubXSubProxy()
            # Run start in a background task managed by the Orcustrator
            proxy_task = asyncio.create_task(self.proxy.start())
            self._core_tasks.append(proxy_task)
            self.proxy_started = True
        else: 
            pass            
       

    async def ensure_metadata_responder_started(self):
        """Ensure the metadata responder is started using port from SharedState."""
        if self.metadata_responder_started:
            logger.debug("Metadata Responder already started.")
            return
            
        m_port = self.metadata_port # Use property
        if m_port is None:
            # Assuming MetadataResponder is NOT a singleton, instantiate directly
            self.metadata_responder = MetadataResponder()
            metadata_task = asyncio.create_task(self.metadata_responder.start())
            self._core_tasks.append(metadata_task)
            self.metadata_responder_started = True
            logger.info("Metadata Responder start task created.")
        else:
            pass
            

    async def _ensure_external_subscribers_started(self):
        """Dynamically load, instantiate, and start external subscribers."""
        subscriber_configs = self.shared_state.get("ExternalSubscriberList", [])
        if not subscriber_configs:
            logger.info("No external subscribers configured.")
            return

        logger.info(f"Found {len(subscriber_configs)} external subscriber configurations. Starting...")
        
        m_port = self.metadata_port # Get metadata port once using property
        if m_port is None:
             logger.error("Cannot start external subscribers: Metadata port not found in SharedState.")
             return
             
        for config_item in subscriber_configs: # Renamed loop variable
            # Use the helper function to start the subscriber
            result = await start_single_external_subscriber(config_item, m_port)

            if result:
                 subscriber_key, sub_data = result

                 # Check if already running (safety check, helper might fail before key check)
                 if subscriber_key in self._external_subscribers:
                      logger.warning(f"External subscriber {subscriber_key} already running. Skipping.")
                      # If task was created, cancel it? Helper should handle this ideally.
                      # For now, just skip storing.
                      continue

                 # Store instance and task
                 self._external_subscribers[subscriber_key] = sub_data
            # else: Helper function logged the error

    # --- Combined Start Logic (Optional, could be called externally) ---
    async def start_all(self):
         """Ensure all core components and external subscribers are started."""
         logger.info("Orcustrator starting all components...")
         await self.ensure_proxy_started()
         await self.ensure_metadata_responder_started()
         await self._ensure_external_subscribers_started()
         self._running = True # Set flag indicating components have been started
         logger.info("Orcustrator finished starting components.")
         # Note: This doesn't block, tasks run in background.

    # --- Shutdown Logic --- 
    async def shutdown(self):
        """Stop all components and clean up resources."""
        logger.info("Orcustrator shutting down...")
        
        # 1. Stop external subscribers
        logger.info(f"Stopping {len(self._external_subscribers)} external subscribers...")
        external_tasks_to_wait = []
        for key, sub_data in list(self._external_subscribers.items()): # Iterate over copy
            # Use helper to stop instance and cancel task
            cancelled_task = await stop_single_external_subscriber(key, sub_data["instance"], sub_data["task"])
            if cancelled_task:
                 external_tasks_to_wait.append(cancelled_task)

            # Remove from dict after processing
            del self._external_subscribers[key]

        if external_tasks_to_wait:
             logger.debug("Waiting for external subscriber tasks...")
             await asyncio.gather(*external_tasks_to_wait, return_exceptions=True)
             logger.debug("External subscriber tasks finished.")
             
        # self._external_subscribers should be empty now

        # 2. Stop Metadata Responder
        if self.metadata_responder_started and self.metadata_responder:
            logger.debug("Stopping metadata responder...")
            try:
                # Await the stop method if it's async
                await self.metadata_responder.stop() 
            except Exception as e:
                 logger.error(f"Error stopping metadata responder: {e}")
            self.metadata_responder = None 
            self.metadata_responder_started = False
            # Optionally clear port in shared state if this Orcustrator is responsible
            # self.shared_state.set("Orcustrator.MetadataResponder", None)
            logger.info("Metadata responder stopped")

        # 3. Stop Proxy
        if self.proxy_started and self.proxy:
            logger.debug("Stopping ZeroMQ proxy...")
            try:
                # Await the stop method if it's async
                await self.proxy.stop() 
            except Exception as e:
                 logger.error(f"Error stopping ZeroMQ proxy: {e}")
            self.proxy = None
            self.proxy_started = False
            # Optionally clear ports in shared state if this Orcustrator is responsible
            # self.shared_state.set("Orcustrator.XPub", None)
            # self.shared_state.set("Orcustrator.XSub", None)
            logger.info("ZeroMQ proxy stopped")
        
        # 4. Cancel remaining core tasks (proxy, metadata)
        logger.debug("Cancelling core tasks...")
        tasks_to_cancel = list(self._core_tasks) # Copy list
        self._core_tasks = [] # Clear original
        for task in tasks_to_cancel:
             if task and not task.done():
                 task.cancel()
        if tasks_to_cancel:
            logger.debug("Waiting for core tasks...")
            await asyncio.gather(*tasks_to_cancel, return_exceptions=True)
            logger.debug("Core tasks finished.")
             
        self._running = False
        logger.info("Orcustrator shutdown complete.")

# Example usage remains similar, but uses get_instance()
async def main():
    # Configuration loading should happen before getting the instance
    # if using a config file
    # SharedState.get_instance().load_yaml_config("main.yaml") 
    
    orcustrator = Orcustrator.get_instance()
    try:
        await orcustrator.start_all()
        await asyncio.Event().wait() 
    except asyncio.CancelledError:
        logger.info("Main task cancelled.")
    finally:
        await orcustrator.shutdown()

if __name__ == '__main__': 
    try:
        # Ensure config is loaded if needed before running main
        SharedState.get_instance().load_yaml_config("main.yaml")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    except FileNotFoundError:
         logger.error("main.yaml not found. Orcustrator cannot start.")