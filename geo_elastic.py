import inspect

from elasticsearch import AsyncElasticsearch
from loguru import logger


class Elastic(AsyncElasticsearch):
    # https://elasticsearch-py.readthedocs.io/en/v7.11.0/async.html
    async def delete_geo_points(self):
        try:
            logger.info('Elastic API - deleting all documents from geo index')
            await self.delete_by_query(index='geo-hosts', body={"query": {"match_all": {}}})
        except Exception as e:
            logger.exception(
                'Elastic API - failed to delete documents from geo index')

    async def create_geo_index(self):
        try:
            logger.info('Elastic API - creating geo index')
            await self.indices.create(index='geo-hosts', ignore=400)
        except Exception as e:
            logger.exception('Elastic API - failed to create geo index')

    async def update_geo_index_mapping(self):

        self.payload = """
    {
    "properties": {
        "coordinates": {
            "type": "geo_point"
            }
        }
    }
    """
        try:
            logger.info('Elastic API - updating geo index mapping')
            await self.indices.put_mapping(index='geo-hosts', ignore=400, body=self.payload)
        except Exception as e:
            logger.exception(
                f'Elastic API - failed to update geo index mapping - {e}')

    async def create_geo_point(self):
        self.payload = f"""
            {{
            "coordinates" : {{
                "lat": "{self.location_lat}",
                "lon": "{self.location_lon}"
                }},
            "host": "{self.host}",
            "visible_name": "{self.visible_name}",
            "interface": "{self.interface}",
            "status": "{self.status}",
            "group_name": "{self.group_name}",
            "snmp_port": "{self.snmp_port}",
            "icmp_status": "{self.icmp_status}",
            "alias": "{self.alias}",
            "asset_tag": "{self.asset_tag}",
            "chassis": "{self.chassis}", 
            "contact": "{self.contact}",
            "contract_number": "{self.contract_number}",
            "date_hw_decomm": "{self.date_hw_decomm }",
            "date_hw_expiry": "{self.date_hw_expiry}",
            "date_hw_install": "{self.date_hw_install}",
            "date_hw_purchase": "{self.date_hw_purchase}",
            "deployment_status": "{self.deployment_status}",
            "hardware": "{self.hardware}",
            "hardware_full": "{self.hardware_full}",
            "host_netmask": "{self.host_netmask}",
            "host_networks": "{self.host_networks}",
            "host_router": "{self.host_router}",
            "hostid": "{self.hostid}",
            "hw_arch": "{self.hw_arch}",
            "installer_name": "{self.installer_name}",
            "inventory_mode": "{self.inventory_mode}",
            "location": "{self.location}",
            "location_lat": "{self.location_lat}",
            "location_lon": "{self.location_lon}",
            "macaddress_a": "{self.macaddress_a}",
            "macaddress_b": "{self.macaddress_b}",
            "model": "{self.model}",
            "name": "{self.name}",
            "notes": "{self.notes}",
            "oob_ip": "{self.oob_ip}",
            "oob_netmask": "{self.oob_netmask}",
            "oob_router": "{self.oob_router}",
            "os": "{self.os}",
            "os_full": "{self.os_full}",
            "os_short": "{self.os_short}",
            "poc_1_cell": "{self.poc_1_cell}",
            "poc_1_email": "{self.poc_1_email}",
            "poc_1_name": "{self.poc_1_name}",
            "poc_1_notes": "{self.poc_1_notes}",
            "poc_1_phone_a": "{self.poc_1_phone_a}",
            "poc_1_phone_b": "{self.poc_1_phone_b}",
            "poc_1_screen": "{self.poc_1_screen}",
            "poc_2_cell": "{self.poc_2_cell}",
            "poc_2_email": "{self.poc_2_email}", 
            "poc_2_name": "{self.poc_2_name}", 
            "poc_2_notes": "{self.poc_2_notes}",
            "poc_2_phone_a": "{self.poc_2_phone_a}", 
            "poc_2_phone_b": "{self.poc_2_phone_b}", 
            "poc_2_screen": "{self.poc_2_screen}", 
            "serialno_a": "{self.serialno_a}", 
            "serialno_b": "{self.serialno_b}",
            "site_address_a": "{self.site_address_a}", 
            "site_address_b": "{self.site_address_b}", 
            "site_address_c": "{self.site_address_c}", 
            "site_city": "{self.site_city}", 
            "site_country": "{self.site_country}", 
            "site_notes": "{self.site_notes}", 
            "site_rack": "{self.site_rack}", 
            "site_state": "{self.site_state}", 
            "site_zip": "{self.site_zip}", 
            "software": "{self.software}",
            "software_app_a": "{self.software_app_a}", 
            "software_app_b": "{self.software_app_b}", 
            "software_app_c": "{self.software_app_c}", 
            "software_app_d": "{self.software_app_d}", 
            "software_app_e": "{self.software_app_e}", 
            "software_full": "{self.software_full}", 
            "tag": "{self.tag}", 
            "type": "{self.type}", 
            "type_full": "{self.type_full}", 
            "url_a": "{self.url_a}", 
            "url_b": "{self.url_b}", 
            "url_c": "{self.url_c}", 
            "vendor": "{self.vendor}"
            }}
            """

        # Fix for valid JSON data - replace special characters with space
        self.payload = self.payload.replace(
            '\n', ' ').replace('\r', ' ').replace('\r\n', ' ')

        # remove multiline string spaces from payload
        self.payload = inspect.cleandoc(self.payload)
        try:
            await self.index(index='geo-hosts', body=self.payload, request_timeout=30)
        except Exception as e:
            logger.exception(f'Elastic API - failed to create geo point - {e}')
