#!/usr/bin/env python3
"""
Fortran Web Assembly Compiler Script

This script compiles Fortran code to WebAssembly using a Docker container with the Flang/LLVM toolchain.
It manages the build process, directory creation, logging, and Docker interaction.

Usage:
    ./compileToWasm.py

Requirements:
    - Docker installed and in PATH
    - Docker image 'ghcr.io/r-wasm/flang-wasm:main' must be available
    - Write permissions to create build and cache directories
"""
import subprocess
import os
import pathlib
import shlex
import datetime
import sys
import time

# Get user and group IDs for Docker
uid = os.getuid()
gid = os.getgid()

# Configuration
current_dir = pathlib.Path(__file__).parent.resolve()
build_dir = current_dir / "build"
cache_dir = current_dir / "cache"
log_file = build_dir / "compile.log"

# Create necessary directories
build_dir.mkdir(parents=True, exist_ok=True)
cache_dir.mkdir(parents=True, exist_ok=True)

# Configure cache directory permissions
os.chown(cache_dir, uid, gid)
os.chmod(cache_dir, 0o755)

# Setup log file
try:
    with open(log_file, "w") as f:
        f.write(f"# Compilation Log - {datetime.datetime.now()}\n\n")
except OSError as e:
    print(f"❌ Error creating log file: {e}")
    sys.exit(1)

def log_to_file(message):
    """Adds a message to the log file
    
    Args:
        message (str): The message to be logged
    """
    try:
        with open(log_file, "a") as f:
            f.write(f"{message}\n")
    except OSError as e:
        print(f"⚠️ Warning: Could not write to log file: {e}")

def run_docker(command, description):
    """Executes a command in the Docker container
    
    Args:
        command (str): The command to run inside the container
        description (str): Description of the action for logs
        
    Returns:
        str: Standard output from the command
        
    Raises:
        SystemExit: If Docker command fails
    """
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{current_dir}:/src:z",
        "-v", f"{cache_dir}:/cache:z",
        "-e", f"UID={uid}",
        "-e", f"GID={gid}",
        "-e", "EM_CACHE=/cache/emsdk",  # Define Emscripten environment variable
        "-w", "/src",
        "--user", f"{uid}:{gid}",
        "ghcr.io/r-wasm/flang-wasm:main",
        "bash", "-c", command
    ]
    
    log_to_file(f"\n\n==== {description} ====")
    log_to_file(f"Command: {' '.join(shlex.quote(str(c)) for c in docker_cmd[:-1])} {shlex.quote(docker_cmd[-1])}")
    
    print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(docker_cmd, capture_output=True, text=True, check=False)
        
        if result.stdout:
            log_to_file("\nSTDOUT:")
            log_to_file(result.stdout)
        
        if result.stderr:
            log_to_file("\nSTDERR:")
            log_to_file(result.stderr)
        
        if result.returncode != 0:
            print(f"❌ Error executing Docker command (exit code: {result.returncode}). See log file for details.")
            log_to_file(f"\nERROR: Command failed with exit code {result.returncode}")
            sys.exit(1)
            
        return result.stdout
    except FileNotFoundError:
        print("❌ Error: 'docker' command not found. Is Docker installed and in PATH?")
        log_to_file("\nERROR: Docker not found on system")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error executing Docker: {e}")
        log_to_file(f"\nUNEXPECTED ERROR: {e}")
        sys.exit(1)

# Record start time
start_time = time.time()

# Compile project using make
print("🔨 Compiling project...")
run_docker(
    "source /opt/emsdk/emsdk_env.sh > /dev/null 2>&1 && " +
    "mkdir -p /cache/emsdk && " +
    "chmod 755 /cache/emsdk && " +
    "cd src && make all",
    "Compiling project with make"
)

# Calculate total time
total_time = time.time() - start_time
minutes = int(total_time // 60)
seconds = total_time % 60

log_to_file(f"\nCompilation completed in {minutes}min {seconds:.2f}s")
print(f"\n✅ Compilation completed in {minutes}min {seconds:.2f}s")
print(f"Check the log file ({log_file.name}) for complete process details.")
