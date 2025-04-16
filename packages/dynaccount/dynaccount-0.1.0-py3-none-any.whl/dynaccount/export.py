import os
import json
import csv
import logging
from datetime import datetime
from .logging_config import setup_logger
from .util import format_bound_groups

class Exporter:

    def __init__(self, export_path='./', log_level='INFO'):
        setup_logger(__name__, log_level)
        self.logger = logging.getLogger(__name__)
        self.export_path = export_path    

    def policies_to_json(self, data, indent_level=4):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f'policies_{timestamp}.json'
        full_path = os.path.join(self.export_path, file_name)        
        with open(full_path, 'w') as file:
            json.dump(data, file, indent=indent_level)
        self.logger.info(f"Data exported to {file_name}")

    def policies_to_csv(self, data):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f'policies_{timestamp}.csv'
        full_path = os.path.join(self.export_path, file_name)        
        with open(full_path, 'w', newline='') as file:
            fieldnames = ['Policy UUID', 'Policy Name', 'Policy Description', 'Policy Statement Query', 'Bound Groups']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for policy in data:
                bound_groups = ''
                if policy['bindings']:
                    bound_groups = format_bound_groups(policy)
                writer.writerow({
                    'Policy UUID': policy['details']['uuid'],
                    'Policy Name': policy['details']['name'],
                    'Policy Description': policy['details']['description'],
                    'Policy Statement Query': policy['details']['statementQuery'],
                    'Bound Groups': bound_groups
                })
        self.logger.info(f"Data exported to {file_name}")