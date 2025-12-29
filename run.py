import uvicorn
import asyncio
import socket
from app.core.database import init_db
from app.models import models  # Import models to register them

def get_network_addresses(port=8000):
    """Get all network IP addresses for the server"""
    addresses = []
    
    # Add localhost
    addresses.append(f"http://localhost:{port}/")
    
    # Get all network interfaces
    try:
        hostname = socket.gethostname()
        # Get all IP addresses for this machine
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
        
        for ip in ip_addresses:
            if not ip.startswith("127."):  # Skip localhost IPs
                addresses.append(f"http://{ip}:{port}/")
    except Exception as e:
        print(f"Could not detect network addresses: {e}")
    
    return addresses

async def startup():
    """Initialize database on startup"""
    await init_db()
    print("Database initialized successfully!")

if __name__ == "__main__":
    PORT = 8000
    
    # Initialize database
    asyncio.run(startup())
    
    # Get and display all network addresses
    addresses = get_network_addresses(PORT)
    
    print("\n  BACKEND API ready\n")
    print(f"  ->  Local:   http://localhost:{PORT}/")
    
    # Display network addresses (same format as Vite frontend)
    network_addresses = [addr for addr in addresses if not addr.startswith("http://localhost")]
    if network_addresses:
        for addr in network_addresses:
            print(f"  ->  Network: {addr}")
    
    print("")  # Empty line like Vite
    
    # Run server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )

