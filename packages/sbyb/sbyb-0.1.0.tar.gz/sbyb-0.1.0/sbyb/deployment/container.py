"""
Container builder component for SBYB deployment.

This module provides functionality for building and managing containers
for machine learning models.
"""

from typing import Any, Dict, List, Optional, Union, Tuple
import os
import json
import shutil
import subprocess
import tempfile
import logging

from sbyb.core.base import SBYBComponent
from sbyb.core.exceptions import ContainerError


class ContainerBuilder(SBYBComponent):
    """
    Container builder component.
    
    This component builds and manages containers for machine learning models.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the container builder.
        
        Args:
            config: Configuration dictionary for the builder.
        """
        super().__init__(config)
        self.logger = logging.getLogger("sbyb.deployment.container")
    
    def build_docker_image(self, api_dir: str, image_name: str, tag: str = "latest") -> str:
        """
        Build a Docker image for a model API.
        
        Args:
            api_dir: Directory containing the API code and Dockerfile.
            image_name: Name for the Docker image.
            tag: Tag for the Docker image.
            
        Returns:
            Full image name (name:tag).
        """
        # Check if Docker is installed
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ContainerError("Docker is not installed or not in PATH.")
        
        # Check if Dockerfile exists
        dockerfile_path = os.path.join(api_dir, "Dockerfile")
        if not os.path.exists(dockerfile_path):
            raise ContainerError(f"Dockerfile not found in {api_dir}")
        
        # Build Docker image
        full_image_name = f"{image_name}:{tag}"
        try:
            self.logger.info(f"Building Docker image {full_image_name}...")
            subprocess.run(
                ["docker", "build", "-t", full_image_name, api_dir],
                check=True,
                capture_output=True
            )
            self.logger.info(f"Docker image {full_image_name} built successfully.")
            return full_image_name
        except subprocess.SubprocessError as e:
            error_message = e.stderr.decode("utf-8") if hasattr(e, "stderr") else str(e)
            raise ContainerError(f"Failed to build Docker image: {error_message}")
    
    def run_docker_container(self, image_name: str, container_name: Optional[str] = None,
                            port_mapping: Optional[Dict[int, int]] = None,
                            environment: Optional[Dict[str, str]] = None,
                            volumes: Optional[Dict[str, str]] = None,
                            detach: bool = True) -> str:
        """
        Run a Docker container from an image.
        
        Args:
            image_name: Name of the Docker image.
            container_name: Name for the container.
            port_mapping: Mapping of container ports to host ports.
            environment: Environment variables.
            volumes: Volume mappings.
            detach: Whether to run the container in detached mode.
            
        Returns:
            Container ID.
        """
        # Check if Docker is installed
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ContainerError("Docker is not installed or not in PATH.")
        
        # Prepare command
        cmd = ["docker", "run"]
        
        # Add container name if provided
        if container_name:
            cmd.extend(["--name", container_name])
        
        # Add port mappings if provided
        if port_mapping:
            for container_port, host_port in port_mapping.items():
                cmd.extend(["-p", f"{host_port}:{container_port}"])
        
        # Add environment variables if provided
        if environment:
            for key, value in environment.items():
                cmd.extend(["-e", f"{key}={value}"])
        
        # Add volume mappings if provided
        if volumes:
            for host_path, container_path in volumes.items():
                cmd.extend(["-v", f"{host_path}:{container_path}"])
        
        # Add detach flag if requested
        if detach:
            cmd.append("-d")
        
        # Add image name
        cmd.append(image_name)
        
        # Run container
        try:
            self.logger.info(f"Running Docker container from image {image_name}...")
            result = subprocess.run(cmd, check=True, capture_output=True)
            container_id = result.stdout.decode("utf-8").strip()
            self.logger.info(f"Docker container {container_id} started successfully.")
            return container_id
        except subprocess.SubprocessError as e:
            error_message = e.stderr.decode("utf-8") if hasattr(e, "stderr") else str(e)
            raise ContainerError(f"Failed to run Docker container: {error_message}")
    
    def stop_docker_container(self, container_id: str) -> None:
        """
        Stop a Docker container.
        
        Args:
            container_id: ID or name of the container.
        """
        # Check if Docker is installed
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ContainerError("Docker is not installed or not in PATH.")
        
        # Stop container
        try:
            self.logger.info(f"Stopping Docker container {container_id}...")
            subprocess.run(
                ["docker", "stop", container_id],
                check=True,
                capture_output=True
            )
            self.logger.info(f"Docker container {container_id} stopped successfully.")
        except subprocess.SubprocessError as e:
            error_message = e.stderr.decode("utf-8") if hasattr(e, "stderr") else str(e)
            raise ContainerError(f"Failed to stop Docker container: {error_message}")
    
    def remove_docker_container(self, container_id: str, force: bool = False) -> None:
        """
        Remove a Docker container.
        
        Args:
            container_id: ID or name of the container.
            force: Whether to force removal.
        """
        # Check if Docker is installed
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ContainerError("Docker is not installed or not in PATH.")
        
        # Prepare command
        cmd = ["docker", "rm"]
        
        # Add force flag if requested
        if force:
            cmd.append("-f")
        
        # Add container ID
        cmd.append(container_id)
        
        # Remove container
        try:
            self.logger.info(f"Removing Docker container {container_id}...")
            subprocess.run(cmd, check=True, capture_output=True)
            self.logger.info(f"Docker container {container_id} removed successfully.")
        except subprocess.SubprocessError as e:
            error_message = e.stderr.decode("utf-8") if hasattr(e, "stderr") else str(e)
            raise ContainerError(f"Failed to remove Docker container: {error_message}")
    
    def push_docker_image(self, image_name: str, registry: Optional[str] = None,
                         username: Optional[str] = None, password: Optional[str] = None) -> None:
        """
        Push a Docker image to a registry.
        
        Args:
            image_name: Name of the Docker image.
            registry: Registry URL.
            username: Registry username.
            password: Registry password.
        """
        # Check if Docker is installed
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            raise ContainerError("Docker is not installed or not in PATH.")
        
        # Login to registry if credentials provided
        if registry and username and password:
            try:
                self.logger.info(f"Logging in to Docker registry {registry}...")
                login_cmd = ["docker", "login", registry, "-u", username, "--password-stdin"]
                login_process = subprocess.Popen(
                    login_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                login_process.communicate(input=password.encode("utf-8"))
                if login_process.returncode != 0:
                    raise ContainerError(f"Failed to login to Docker registry {registry}")
                self.logger.info(f"Logged in to Docker registry {registry} successfully.")
            except subprocess.SubprocessError as e:
                error_message = e.stderr.decode("utf-8") if hasattr(e, "stderr") else str(e)
                raise ContainerError(f"Failed to login to Docker registry: {error_message}")
        
        # Prepare image name with registry if provided
        full_image_name = image_name
        if registry:
            # Check if image name already includes registry
            if "/" in image_name and "." in image_name.split("/")[0]:
                # Image name already includes registry
                full_image_name = image_name
            else:
                # Add registry to image name
                full_image_name = f"{registry}/{image_name}"
            
            # Tag image with registry
            try:
                self.logger.info(f"Tagging Docker image {image_name} as {full_image_name}...")
                subprocess.run(
                    ["docker", "tag", image_name, full_image_name],
                    check=True,
                    capture_output=True
                )
                self.logger.info(f"Docker image {image_name} tagged as {full_image_name} successfully.")
            except subprocess.SubprocessError as e:
                error_message = e.stderr.decode("utf-8") if hasattr(e, "stderr") else str(e)
                raise ContainerError(f"Failed to tag Docker image: {error_message}")
        
        # Push image
        try:
            self.logger.info(f"Pushing Docker image {full_image_name}...")
            subprocess.run(
                ["docker", "push", full_image_name],
                check=True,
                capture_output=True
            )
            self.logger.info(f"Docker image {full_image_name} pushed successfully.")
        except subprocess.SubprocessError as e:
            error_message = e.stderr.decode("utf-8") if hasattr(e, "stderr") else str(e)
            raise ContainerError(f"Failed to push Docker image: {error_message}")
    
    def generate_kubernetes_deployment(self, image_name: str, deployment_name: str,
                                      replicas: int = 1, port: int = 8000,
                                      output_file: Optional[str] = None) -> str:
        """
        Generate a Kubernetes deployment YAML for a model.
        
        Args:
            image_name: Name of the Docker image.
            deployment_name: Name for the Kubernetes deployment.
            replicas: Number of replicas.
            port: Container port.
            output_file: Path to save the YAML file.
            
        Returns:
            Kubernetes deployment YAML content.
        """
        # Generate deployment YAML
        deployment_yaml = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {deployment_name}
  labels:
    app: {deployment_name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {deployment_name}
  template:
    metadata:
      labels:
        app: {deployment_name}
    spec:
      containers:
      - name: {deployment_name}
        image: {image_name}
        ports:
        - containerPort: {port}
        resources:
          limits:
            cpu: "1"
            memory: "1Gi"
          requests:
            cpu: "0.5"
            memory: "512Mi"
        readinessProbe:
          httpGet:
            path: /health
            port: {port}
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: {port}
          initialDelaySeconds: 15
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: {deployment_name}
spec:
  selector:
    app: {deployment_name}
  ports:
  - port: 80
    targetPort: {port}
  type: ClusterIP
"""
        
        # Save to file if output_file provided
        if output_file:
            with open(output_file, "w") as f:
                f.write(deployment_yaml)
        
        return deployment_yaml
    
    def generate_docker_compose(self, image_name: str, service_name: str,
                               port: int = 8000, output_file: Optional[str] = None) -> str:
        """
        Generate a Docker Compose YAML for a model.
        
        Args:
            image_name: Name of the Docker image.
            service_name: Name for the service.
            port: Container port.
            output_file: Path to save the YAML file.
            
        Returns:
            Docker Compose YAML content.
        """
        # Generate docker-compose.yml
        compose_yaml = f"""version: '3'

services:
  {service_name}:
    image: {image_name}
    ports:
      - "{port}:{port}"
    restart: unless-stopped
    environment:
      - PORT={port}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{port}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
"""
        
        # Save to file if output_file provided
        if output_file:
            with open(output_file, "w") as f:
                f.write(compose_yaml)
        
        return compose_yaml
