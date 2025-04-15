# The Service Registry

# AsyncRegistryServer Documentation

## Overview

The `AsyncRegistryServer` is an asynchronous service registry implementation for
microservices architectures that are using ZeroMQ for communication and
providing persistent storage through pluggable backends. It enables service
discovery, registration, and health monitoring in distributed systems.

The server exposes two ZeroMQ sockets:

- A REQ-REP socket for service registration, discovery, and management
- A PUB-SUB socket for broadcasting service events (registrations,
  de-registrations, expirations)

The server uses a pluggable backend for storing the service registrations. 
An `AsyncInMemoryBackend` is provided for in-memory storage as long as 
the server is running. For persistent storage of service registrations, use 
the `AsyncSLQiteBackend` 

## Basic Usage

```python
import asyncio

from egse.registry.server import AsyncSQLiteBackend
from egse.registry.server import AsyncRegistryServer


async def run_server():
    # Create and initialize a backend
    backend = AsyncSQLiteBackend("service_registry.db")
    await backend.initialize()

    # Create the server
    server = AsyncRegistryServer(
        req_port=5556,
        pub_port=5557,
        backend=backend
    )

    # Start the server
    await server.start()


if __name__ == "__main__":
    asyncio.run(run_server())
```

## Configuration

### Constructor Parameters

| Parameter          | Type                  | Default                | Description                                          |
|--------------------|-----------------------|------------------------|------------------------------------------------------|
| `req_port`         | int                   | 5556                   | Port for the REQ-REP socket (service requests)       |
| `pub_port`         | int                   | 5557                   | Port for the PUB socket (event notifications)        |
| `backend`          | AsyncRegistryBackend  | `AsyncSQLiteBackend`   | Storage backend implementation                       |
| `cleanup_interval` | int                   | 10                     | Interval in seconds for cleaning up expired services |

### Storage Backends

The server works with any backend that implements the `AsyncRegistryBackend`
protocol. Two implementations are provided:

- `AsyncSQLiteBackend`: Persistent storage using SQLite
- `AsyncInMemoryBackend`: In-memory storage for testing or simple deployments

## API Reference

### Server Methods

#### `__init__(req_port=5556, pub_port=5557, backend, db_path, cleanup_interval=10)`

Initializes the registry server with the specified settings.

```python
server = AsyncRegistryServer(
    req_port=5556,
    pub_port=5557,
    backend=backend,
    db_path='service_registry.db',
    cleanup_interval=10
)
```

#### `async initialize()`

Initializes the server and its components. Called automatically by `start()`.

```python
await server.initialize()
```

#### `async start()`

Starts the server and begins processing requests. This method runs indefinitely
until `stop()` is called.

```python
await server.start()
```

#### `async stop()`

Gracefully stops the server, canceling all tasks and releasing resources.

```python
await server.stop()
```

### Service Registration Protocol

The server accepts requests in JSON format through its REQ-REP socket. Each
request must have an `action` field specifying the operation.

#### Registration

```json
{
  "action": "register",
  "service_info": {
    "name": "example-service",
    "host": "192.168.1.10",
    "port": 8080,
    "type": "web",
    "tags": [
      "web",
      "api"
    ],
    "metadata": {
      "version": "1.0.0"
    }
  },
  "ttl": 30
}
```

Response:

```json
{
  "success": true,
  "service_id": "example-service-f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": "Service registered successfully"
}
```

#### Deregistration

```json
{
  "action": "deregister",
  "service_id": "example-service-f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

Response:

```json
{
  "success": true,
  "message": "Service deregistered successfully"
}
```

#### Service Renewal (Heartbeat)

```json
{
  "action": "renew",
  "service_id": "example-service-f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

Response:

```json
{
  "success": true,
  "message": "Service renewed successfully"
}
```

#### Get Service

```json
{
  "action": "get",
  "service_id": "example-service-f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

Response:

```json
{
  "success": true,
  "service": {
    "id": "example-service-f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "name": "example-service",
    "host": "192.168.1.10",
    "port": 8080,
    "type": "web",
    "tags": [
      "web",
      "api"
    ],
    "metadata": {
      "version": "1.0.0"
    },
    "ttl": 30,
    "last_heartbeat": 1617293054,
    "health": "passing"
  }
}
```

#### List Services

```json
{
  "action": "list",
  "service_type": "web"
  // Optional, filter by type
}
```

Response:

```json
{
  "success": true,
  "services": [
    {
      "id": "service-1",
      "name": "example-service",
      "host": "192.168.1.10",
      "port": 8080,
      "type": "web",
      "tags": [
        "web",
        "api"
      ],
      "metadata": {
        "version": "1.0.0"
      },
      "ttl": 30,
      "last_heartbeat": 1617293054,
      "health": "passing"
    }
    // ... more services
  ]
}
```

#### Discover Service

```json
{
  "action": "discover",
  "service_type": "web"
}
```

Response:

```json
{
  "success": true,
  "service": {
    "id": "service-1",
    "name": "example-service",
    "host": "192.168.1.10",
    "port": 8080,
    "type": "web",
    "tags": [
      "web",
      "api"
    ],
    "metadata": {
      "version": "1.0.0"
    },
    "ttl": 30,
    "last_heartbeat": 1617293054,
    "health": "passing"
  }
}
```

#### Health Check

```json
{
  "action": "health"
}
```

Response:

```json
{
  "success": true,
  "status": "ok",
  "timestamp": 1617293054
}
```

### Event Broadcasting

The server publishes events to its PUB socket whenever services are registered,
deregistered, or expire. Events have the following format:

```json
{
    "type": "register",   // or "deregister", "expire"
    "timestamp": 1617293054,
    "data": {
        "service_id": "service-1",
        "service_info": {
            // Service information
        }
    }
}
```

Clients can subscribe to these events to maintain a local cache of service
information.

## Advanced Usage

### Running with Signal Handling

This example shows how to gracefully handle termination signals:

```python
import asyncio
import signal
from async_registry_backend import AsyncSQLiteBackend
from async_registry_server import AsyncRegistryServer


async def run_server():
    # Create and initialize a backend
    backend = AsyncSQLiteBackend("service_registry.db")
    await backend.initialize()

    # Create the server
    server = AsyncRegistryServer(
        req_port=5556,
        pub_port=5557,
        backend=backend
    )

    # Setup signal handlers
    loop = asyncio.get_running_loop()

    def signal_handler():
        asyncio.create_task(server.stop())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    # Start the server
    await server.start()

    # Cleanup
    await backend.close()


if __name__ == "__main__":
    asyncio.run(run_server())
```

### Using with Docker

Example Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install ZeroMQ development libraries
RUN apt-get update && apt-get install -y libzmq3-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 5556 5557

# Run the server
CMD ["python", "run_server.py"]
```

Start with:

```bash
docker run -p 5556:5556 -p 5557:5557 -v ./data:/app/data registry-server
```

## Service Discovery Patterns

### Load Balancing

The `discover_service` action implements a simple load balancing strategy by
default, returning a random healthy service of the requested type. For more
advanced load balancing strategies, you can:

1. Extend `AsyncRegistryBackend` with custom discovery logic
2. Implement client-side load balancing in your service clients
3. Use a dedicated load balancer in front of your services

### Circuit Breaking

When services become unhealthy (failing to send heartbeats), they will be
automatically marked as "critical" and excluded from discovery results. This
provides a basic circuit breaking mechanism.

For more sophisticated circuit breaking, consider using a dedicated library
like `pybreaker` in your client applications.

## Troubleshooting

### Common Issues

#### "Resource temporarily unavailable" Error

This typically indicates a ZeroMQ socket is in an invalid state or connection
issues:

- Ensure ports are not in use by other applications
- Check network connectivity between services
- Use longer timeouts for high-latency environments

#### Services Not Being Discovered

If services register successfully but can't be discovered:

- Verify services are sending heartbeats regularly
- Check that services include the proper type and tags
- Ensure TTL values are appropriate for your environment

#### High CPU Usage

If the server shows high CPU usage:

- Increase the cleanup interval to reduce the frequency of expired service
  checks
- Use a more efficient backend implementation for large service counts
- Consider distributing the registry across multiple nodes

### Logging

To enable debug logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

## Performance Considerations

### Scaling

For high-scale deployments:

- Use a more robust backend like a dedicated database server
- Deploy multiple registry servers behind a load balancer
- Implement regional registries for geographically distributed services

### Resource Usage

The server's resource consumption is primarily affected by:

- Number of registered services
- Frequency of service heartbeats
- Cleanup interval for expired services

For large deployments, monitor memory usage and adjust these parameters
accordingly.

### ZeroMQ Socket Configuration

For high-throughput environments, consider tuning ZeroMQ socket options:

```python
socket.setsockopt(zmq.RCVHWM, 10000)  # Receive high-water mark
socket.setsockopt(zmq.SNDHWM, 10000)  # Send high-water mark
```

## Security Considerations

The basic implementation does not include authentication or encryption. For
production use, consider:

- Using ZeroMQ's built-in security mechanisms (CurveZMQ)
- Placing the registry server in a secure network segment
- Implementing application-level authentication for service registration

Example with CurveZMQ (requires additional setup):

```python
public_key, secret_key = zmq.curve_keypair()
socket.setsockopt(zmq.CURVE_SECRETKEY, secret_key)
socket.setsockopt(zmq.CURVE_PUBLICKEY, public_key)
socket.setsockopt(zmq.CURVE_SERVER, True)
```

## Contributing

Contributions to improve `AsyncRegistryServer` are welcome. Areas for
enhancement include:

- Additional backend implementations
- More sophisticated service discovery algorithms
- Enhanced security features
- Performance optimizations for large deployments

## License

This software is provided under the [appropriate license for your project].
