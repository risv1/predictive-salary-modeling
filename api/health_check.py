import socket
import time
import logging
from typing import List, Tuple
import docker

logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self):
        self.client = docker.from_env()
        
    def check_port(self, host: str, port: int, timeout: int = 5) -> bool:
        """Check if a port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False

    def check_container_status(self, container_name: str) -> bool:
        """Check if a container is running and healthy"""
        try:
            container = self.client.containers.get(container_name)
            return container.status == 'running'
        except:
            return False

    def wait_for_services(self, timeout: int = 300) -> bool:
        """Wait for all required services to be ready"""
        services = [
            ("spark-spark-1", None),  
            ("namenode", 9000),               
        ]
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            all_ready = True
            
            for container, port in services:
                if not self.check_container_status(container):
                    logger.info(f"Waiting for container {container}...")
                    all_ready = False
                    break
                    
                if port and not self.check_port("localhost", port):
                    logger.info(f"Waiting for port {port} on {container}...")
                    all_ready = False
                    break
            
            if all_ready:
                logger.info("All services are ready!")
                return True
                
            time.sleep(5)
        
        logger.error("Timeout waiting for services")
        return False