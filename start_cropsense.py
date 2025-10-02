#!/usr/bin/env python3
"""
CropSense Startup Script
One-command startup for the entire CropSense system
"""
import subprocess
import time
import requests
import sys
import os
from datetime import datetime

def print_banner():
    """Print startup banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    🌾 CropSense Startup                      ║
    ║              AI-powered Crop Yield Prediction                ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(["docker", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is running")
            return True
        else:
            print("❌ Docker is not running. Please start Docker Desktop.")
            return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker Desktop.")
        return False

def build_images():
    """Build Docker images"""
    print("\n🔨 Building Docker images...")
    try:
        result = subprocess.run(["docker", "compose", "build"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Images built successfully")
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def start_services():
    """Start all services"""
    print("\n🚀 Starting services...")
    try:
        # Start infrastructure services first
        print("  📦 Starting RabbitMQ and Ollama...")
        subprocess.run(["docker", "compose", "up", "-d", "rabbitmq", "ollama"], check=True)
        
        # Wait a bit for services to start
        time.sleep(10)
        
        # Start all other services
        print("  🌾 Starting CropSense services...")
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        
        print("✅ All services started")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start services: {e}")
        return False

def wait_for_services():
    """Wait for services to be ready"""
    print("\n⏳ Waiting for services to be ready...")
    
    services = {
        "Collector": "http://localhost:8001/health",
        "Preprocessor": "http://localhost:8002/health", 
        "Predictor": "http://localhost:8003/health",
        "Interpreter": "http://localhost:8004/health",
        "UI": "http://localhost:8501"
    }
    
    max_wait = 120  # 2 minutes
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        all_ready = True
        
        for service, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ {service} is ready")
                else:
                    print(f"  ⏳ {service} starting...")
                    all_ready = False
            except requests.exceptions.RequestException:
                print(f"  ⏳ {service} starting...")
                all_ready = False
        
        if all_ready:
            print("✅ All services are ready!")
            return True
        
        time.sleep(5)
    
    print("⚠️ Some services may not be ready yet. Check manually.")
    return False

def show_status():
    """Show service status"""
    print("\n📊 Service Status:")
    print("  🌐 UI: http://localhost:8501")
    print("  🔧 Collector: http://localhost:8001")
    print("  ⚙️ Preprocessor: http://localhost:8002")
    print("  🤖 Predictor: http://localhost:8003")
    print("  💡 Interpreter: http://localhost:8004")
    print("  🐰 RabbitMQ: http://localhost:15672 (guest/guest)")
    print("  🧠 Ollama: http://localhost:11434")

def main():
    """Main startup function"""
    print_banner()
    
    # Check prerequisites
    if not check_docker():
        sys.exit(1)
    
    # Build images
    if not build_images():
        sys.exit(1)
    
    # Start services
    if not start_services():
        sys.exit(1)
    
    # Wait for services
    wait_for_services()
    
    # Show status
    show_status()
    
    print(f"\n🎉 CropSense is ready! Open http://localhost:8501 to start using the system.")
    print(f"📝 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
