import os
import logging
import redis.asyncio as redis
from shared_architecture.connections.timescaledb import TimescaleDBConnection
from shared_architecture.connections.rabbitmq import RabbitMQConnection
from shared_architecture.connections.mongodb import MongoDBConnection

# Setup logging
logging.basicConfig(
    level=os.getenv("LOGGING_LEVEL", "INFO"),
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class AsyncConnectionManager:
    """
    Manages and provides async connections for databases and message queues.
    """
    def __init__(self, config: dict):
        self.config = config
        self._timescaledb_conn = None
        self._redis_pool = None
        self._rabbitmq_conn = None
        self._mongodb_conn = None

    async def initialize(self):
        """
        Initializes all shared connections and pools.
        """
        logging.info("Initializing connection pools and shared services...")

        # Initialize connections
        await self._initialize_timescaledb()
        await self._initialize_redis()
        self._initialize_rabbitmq()
        await self._initialize_mongodb()

        logging.info("All connections initialized.")

    async def _initialize_timescaledb(self):
        """
        Initialize TimescaleDB connection pool.
        """
        try:
            self._timescaledb_conn = TimescaleDBConnection(config=self.config)
            if not self._timescaledb_conn.is_connected():
                logging.warning("TimescaleDB connection failed during initialization.")
        except Exception as e:
            logging.error(f"Error initializing TimescaleDB connection: {e}")

    async def _initialize_redis(self):
        """
        Initialize Redis connection pool (async).
        """
        try:
            redis_url = f"redis://{self.config.get('redis_host', 'localhost')}:{self.config.get('redis_port', 6379)}"
            self._redis_pool = redis.from_url(
                redis_url,
                db=int(self.config.get("redis_db", 0)),
                decode_responses=True
            )
            await self._redis_pool.ping()
            logging.info("Redis connection initialized successfully.")
        except Exception as e:
            logging.error(f"Redis connection failed during initialization: {e}")
            self._redis_pool = None

    def _initialize_rabbitmq(self):
        """
        Initialize RabbitMQ connection.
        """
        try:
            self._rabbitmq_conn = RabbitMQConnection(config=self.config)
            self._rabbitmq_conn.connect()
            if not self._rabbitmq_conn.is_connected():
                logging.warning("RabbitMQ connection failed during initialization.")
        except Exception as e:
            logging.error(f"Error initializing RabbitMQ connection: {e}")

    async def _initialize_mongodb(self):
        """
        Initialize MongoDB connection.
        """
        try:
            self._mongodb_conn = MongoDBConnection(config=self.config)
            if not self._mongodb_conn.is_connected():
                logging.warning("MongoDB connection failed during initialization.")
        except Exception as e:
            logging.error(f"MongoDB connection error: {e}")

    async def get_redis_connection(self):
        """
        Provides an async Redis connection from the pool.
        """
        if not self._redis_pool:
            logging.error("Redis connection pool is not initialized.")
            return None

        try:
            if not await self._redis_pool.ping():
                logging.error("Redis connection is unavailable.")
                return None
            return self._redis_pool
        except Exception as e:
            logging.error(f"Error retrieving Redis connection: {e}")
            return None

    def get_timescaledb_session(self):
        """
        Provides a database session from the TimescaleDB pool.
        """
        if not self._timescaledb_conn or not self._timescaledb_conn.is_connected():
            logging.error("TimescaleDB connection is unavailable.")
            return None
        return self._timescaledb_conn.get_session()

    def get_rabbitmq_connection(self):
        """
        Provides the RabbitMQ connection.
        """
        if not self._rabbitmq_conn or not self._rabbitmq_conn.is_connected():
            logging.error("RabbitMQ connection is unavailable.")
            return None
        return self._rabbitmq_conn.get_connection()

    def get_mongodb_connection(self):
        """
        Provides the MongoDB connection.
        """
        if not self._mongodb_conn or not self._mongodb_conn.is_connected():
            logging.error("MongoDB connection is unavailable.")
            return None
        return self._mongodb_conn.get_database()

    async def close_connections(self):
        """
        Closes all connections gracefully.
        """
        try:
            if self._redis_pool:
                await self._redis_pool.close()
                logging.info("Redis connection pool closed.")

            logging.info("All connections closed successfully.")
        except Exception as e:
            logging.error(f"Error closing connections: {e}")


# Singleton instance of ConnectionManager
connection_manager = None


async def initialize_service(service_name: str, config: dict):
    """
    Initializes the ConnectionManager for shared resources.

    Args:
        service_name (str): The name of the microservice.
        config (dict): The configuration for the service.
    """
    global connection_manager
    if connection_manager is None:
        connection_manager = AsyncConnectionManager(config=config)
        await connection_manager.initialize()
        logging.info(f"Service '{service_name}' initialized.")