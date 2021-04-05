from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv
import os

class CreateClients(object):

    def __init__(self):
        load_dotenv(find_dotenv())
        #self.connection_string = os.getenv("DefaultEndpointsProtocol=https;AccountName=abdzallah;AccountKey=6Z2LBZjx7YJjhpzF8VRer0SREGSSHFPN5kpO10HRoV5xfk+0m2STWc06jTsrOCYQVIt1095VChtL7qJ9jy0Duw==;EndpointSuffix=core.windows.net")
        self.access_key = os.getenv("6Z2LBZjx7YJjhpzF8VRer0SREGSSHFPN5kpO10HRoV5xfk+0m2STWc06jTsrOCYQVIt1095VChtL7qJ9jy0Duw==")
        self.endpoint = os.getenv("core.windows.net")
        self.account_name = os.getenv('abdzallah --kind StorageV2')
        self.account_url = "{}.table.{}".format(self.account_name, self.endpoint)
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
            self.account_name,
            self.access_key,
            self.endpoint
        )



    def create_table_client(self):
        # Instantiate a TableServiceClient using a connection string
        # [START create_table_client]
        from azure.data.tables import TableClient
        with TableClient.from_connection_string(conn_str=self.connection_string, table_name="myTable") as table_client:
            print("Table name: {}".format(table_client.table_name))
        # [END create_table_client]

    def create_table_service_client(self):
        # Instantiate a TableServiceClient using a shared access key
        # [START create_table_service_client]
        from azure.data.tables import TableServiceClient
        with TableServiceClient.from_connection_string(conn_str=self.connection_string) as table_service:
            properties = table_service.get_service_properties()
            print("Connection String: {}".format(properties))
        with TableServiceClient(account_url=self.account_url, credential=self.access_key) as table_service:
            properties = table_service.get_service_properties()
            print("Properties: {}".format(properties))
        # [END create_table_service_client]

    def create_table(self):
        from azure.data.tables import TableServiceClient
        from azure.core.exceptions import ResourceExistsError

        # [START create_table_from_tc]
        with TableServiceClient.from_connection_string(self.connection_string) as table_service_client:
            try:
                table_item = table_service_client.create_table(table_name="myTable")
                print("Created table {}!".format(table_item.table_name))
            except ResourceExistsError:
                print("Table already exists")
        # [END create_table_from_tc]


if __name__ == '__main__':
    sample = CreateClients()
    sample.create_table_client()

    sample.create_table_service_client()
    sample.create_table()
