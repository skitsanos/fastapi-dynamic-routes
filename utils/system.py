"""
This module contains utility functions for system-related tasks.
"""
import os


def check_env(env_vars):
    """
    Checks if all specified environment variables are present.

    :param env_vars: List of environment variable names to check.
    :return: True if all environment variables are present, False otherwise.
    """
    return all(var in os.environ for var in env_vars)
