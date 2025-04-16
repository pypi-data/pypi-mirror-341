#!/usr/bin/env python3
"""Configuration utilities for loading and processing configuration files."""
import os
from typing import Dict, Any
from omegaconf import OmegaConf


def load_config(config_path: str) -> OmegaConf:
    """
    Load configuration with OmegaConf with resolution.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        OmegaConf: Configuration object with resolved values
        
    Example:
        >>> config = load_config("path/to/config.yaml")
        >>> print(config.some_key)
    """
    config_path = os.path.abspath(config_path)
    cfg = OmegaConf.load(config_path)
    
    # Resolve all variables in the config
    cfg = OmegaConf.create(OmegaConf.to_yaml(cfg, resolve=True))
    return cfg