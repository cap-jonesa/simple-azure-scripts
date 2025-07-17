"""
Script Name: print_all_security_assessments.py
Author: Aaron L. Jones
Organization: Central Arizona Project
Copyright (c) 2025 Aaron L. Jones
Licensed under the 3-Clause BSD License. See LICENSE file in the project root
for full license information

Date Created: July 15, 2025
Last Modified: July 15, 2025
Description:
    This script performs a query of all accounts and then iterates through
    those accounts while collecting the security assessments. It compiles this
    data into a JSON file and writes to the local folder.

Usage:
    python print_all_security_assessments.py

Parameters:
    N/A

Functions:
    - get_subscriptions(): Returns the list of all accounts in Azure for user.
    - get_assessments(str): Returns the security assessments for each account.

Example:
    python print_all_security_assessments.py
"""

import subprocess
import json
import time
import logging
from libs.log_config import setup_logging


def get_subscriptions():
    """
    Return a JSON format list of all account identification numbers.

    Parameters:
    N/A

    Returns:
    result.stdout: A collection of account numbers in JSON format.

    Example:
    subscriptions = get_subscriptions()
    
    az cli command:
    az account list --output json
    """
    logging.info('Fetching subscriptions...')
    result = subprocess.run(['az', 'account', 'list', '--query', '[].id', '-o', 'json'],
                            capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logging.error('Failed to fetch subscriptions: %s', result.stderr)
        return []
    logging.info('Subscriptions fetched successfully.')
    return json.loads(result.stdout)

def get_assessments(subscription_id):
    """
    Set the Azure subscription and retrieve security assessments.

    Parameters:
    subscription_id (str): The ID of the Azure subscription to set.

    Returns:
    list: A list of security assessments in JSON format.

    Example:
    assessments = get_assessments('your-subscription-id')
    
    az cli command:
    az account set --subscription $subscription_id
    """
    logging.info('Setting subscription to %s', subscription_id)
    subprocess.run(['az', 'account', 'set', '--subscription', subscription_id],
                   check=True)
    logging.info('Fetching assessments for subscription %s', subscription_id)
    result = subprocess.run(['az', 'security', 'assessment', 'list', '-o', 'json'],
                            capture_output=True, text=True, check=True)
    if result.returncode != 0:
        logging.error('Failed to fetch assessments for subscription %s: %s',
                      subscription_id, result.stderr)
        return []
    logging.info('Assessments fetched successfully for subscription %s', subscription_id)
    return json.loads(result.stdout)

def main():
    """
    Main function to execute the writing of a json format file containing the
    security assessments for an account.

    This function orchestrates the gathering of the account IDs and then
    collects the security assessments. It takes no parameters and returns
    nothing. It serves as the entry point for the script when run from the
    command line. It writes to a file in the current directory.

    Example:
    if __name__ == "__main__":
        main()
    """
    setup_logging()
    logging.info('Starting the script...')
    subscriptions = get_subscriptions()
    all_assessments = {}

    for subscription_id in subscriptions:
        assessments = get_assessments(subscription_id)
        all_assessments[subscription_id] = assessments
        time.sleep(5)
    with open('../results/assessments.json', 'w', encoding='utf-8') as f:
        json.dump(all_assessments, f, indent=4)
    logging.info('Assessments written to assessments.json')

if __name__ == "__main__":
    main()
