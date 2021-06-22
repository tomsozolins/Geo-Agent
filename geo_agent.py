import asyncio
import sys
import time
from contextlib import suppress

import urllib3
from loguru import logger

from geo_elastic import Elastic
from geo_minio import MinioApi
from geo_zabbix import GeoZabbix

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")


async def main():
    # Gather host data from Zabbix API
    zbx = GeoZabbix()
    zabbix_data = zbx.get_host_data()

    # Minio API
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        with open('/var/run/secrets/MINIO_ENDPOINT') as f:
            minio_endpoint = f.read()
        with open('/var/run/secrets/MINIO_ACCESS_KEY') as f:
            minio_access_key = f.read()
        with open('/var/run/secrets/MINIO_SECRET_KEY') as f:
            minio_secret_key = f.read()
    except:
        # For development environment
        with open('secrets/geo_agent/.MINIO_ENDPOINT') as f:
            minio_endpoint = f.read()
        with open('secrets/geo_agent/.MINIO_ACCESS_KEY') as f:
            minio_access_key = f.read()
        with open('secrets/geo_agent/.MINIO_SECRET_KEY') as f:
            minio_secret_key = f.read()

    client = MinioApi(
        endpoint=minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        http_client=urllib3.PoolManager(cert_reqs='CERT_NONE')
    )

    minio_url = f'https://{minio_endpoint}/photos/'
    minio_dict = client.get_minio_images()

    for host in zabbix_data:
        if host['host'] in minio_dict.keys():
            img_name = host['host']
            img_type = minio_dict.get(img_name)
            img_url = f'{minio_url}{img_name}.{img_type}'
            if img_url != host['inventory']['url_a']:
                zbx.update_host_inventory(host['hostid'], 'url_a', img_url)

    # Elasticsearch API - connect to one of the available elasticsearch nodes
    try:
        with open('/var/run/secrets/ELASTIC_ENDPOINT_1') as f:
            elastic_endpoint_1 = f.read()
        with open('/var/run/secrets/ELASTIC_ENDPOINT_2') as f:
            elastic_endpoint_2 = f.read()
        with open('/var/run/secrets/ELASTIC_ENDPOINT_3') as f:
            elastic_endpoint_3 = f.read()
        with open('/var/run/secrets/ELASTIC_USER') as f:
            elastic_user = f.read()
        with open('/var/run/secrets/ELASTIC_PASS') as f:
            elastic_pass = f.read()
    except:
        # For development environment
        with open('secrets/geo_agent/.ELASTIC_ENDPOINT_1') as f:
            elastic_endpoint_1 = f.read()
        with open('secrets/geo_agent/.ELASTIC_ENDPOINT_2') as f:
            elastic_endpoint_2 = f.read()
        with open('secrets/geo_agent/.ELASTIC_ENDPOINT_3') as f:
            elastic_endpoint_3 = f.read()
        with open('secrets/geo_agent/.ELASTIC_USER') as f:
            elastic_user = f.read()
        with open('secrets/geo_agent/.ELASTIC_PASS') as f:
            elastic_pass = f.read()

    el = Elastic(
        [elastic_endpoint_1, elastic_endpoint_2, elastic_endpoint_3],
        http_auth=(elastic_user, elastic_pass),
        scheme="https",
        port=9200,
        verify_certs=False)

    await el.delete_geo_points()

    await el.create_geo_index()

    await el.update_geo_index_mapping()

    async_tasks = []

    logger.info(f'Elastic API - creating geo points...')
    # iterate all hosts and create geo points
    for host in zabbix_data:

        # EAFP, try to assign coordinates to vars. If coordinates does not exist pass.
        with suppress(Exception):
            el.location_lat = host['inventory']['location_lat']

        with suppress(Exception):
            el.location_lon = host['inventory']['location_lon']

        # Create single geo point if latitude and logitude data exists.
        if el.location_lat and el.location_lon:
            with suppress(Exception):
                el.host = host['host']

            with suppress(Exception):
                el.hostid = host['hostid']

            with suppress(Exception):
                el.visible_name = host['name']

            with suppress(Exception):
                el.interface = host['interfaces'][0]['ip']

            with suppress(Exception):
                el.status = host['status']

            with suppress(Exception):
                el.group_name = host['groups'][0]['name']

            with suppress(Exception):
                el.snmp_port = host['interfaces'][1]['port']

            with suppress(Exception):
                el.alias = host['inventory']['alias']

            with suppress(Exception):
                el.asset_tag = host['inventory']['asset_tag']

            with suppress(Exception):
                el.chassis = host['inventory']['chassis']

            with suppress(Exception):
                el.contact = host['inventory']['contact']

            with suppress(Exception):
                el.contract_number = host['inventory']['contract_number']

            with suppress(Exception):
                el.date_hw_decomm = host['inventory']['date_hw_decomm']

            with suppress(Exception):
                el.date_hw_expiry = host['inventory']['date_hw_expiry']

            with suppress(Exception):
                el.date_hw_install = host['inventory']['date_hw_install']

            with suppress(Exception):
                el.date_hw_purchase = host['inventory']['date_hw_purchase']

            with suppress(Exception):
                el.deployment_status = host['inventory']['deployment_status']

            with suppress(Exception):
                el.hardware = host['inventory']['hardware']

            with suppress(Exception):
                el.hardware_full = host['inventory']['hardware_full']

            with suppress(Exception):
                el.host_netmask = host['inventory']['host_netmask']

            with suppress(Exception):
                el.host_networks = host['inventory']['host_networks']

            with suppress(Exception):
                el.host_router = host['inventory']['host_router']

            with suppress(Exception):
                el.hostid = host['inventory']['hostid']

            with suppress(Exception):
                el.hw_arch = host['inventory']['hw_arch']

            with suppress(Exception):
                el.installer_name = host['inventory']['installer_name']

            with suppress(Exception):
                el.inventory_mode = host['inventory']['inventory_mode']

            with suppress(Exception):
                el.location = host['inventory']['location']

            with suppress(Exception):
                el.location_lat = host['inventory']['location_lat']

            with suppress(Exception):
                el.location_lon = host['inventory']['location_lon']

            with suppress(Exception):
                el.macaddress_a = host['inventory']['macaddress_a']

            with suppress(Exception):
                el.macaddress_b = host['inventory']['macaddress_b']

            with suppress(Exception):
                el.model = host['inventory']['model']

            with suppress(Exception):
                el.name = host['inventory']['name']

            with suppress(Exception):
                el.notes = host['inventory']['notes']

            with suppress(Exception):
                el.oob_ip = host['inventory']['oob_ip']

            with suppress(Exception):
                el.oob_netmask = host['inventory']['oob_netmask']

            with suppress(Exception):
                el.oob_router = host['inventory']['oob_router']

            with suppress(Exception):
                el.os = host['inventory']['os']

            with suppress(Exception):
                el.os_full = host['inventory']['os_full']

            with suppress(Exception):
                el.os_short = host['inventory']['os_short']

            with suppress(Exception):
                el.poc_1_cell = host['inventory']['poc_1_cell']

            with suppress(Exception):
                el.poc_1_email = host['inventory']['poc_1_email']

            with suppress(Exception):
                el.poc_1_name = host['inventory']['poc_1_name']

            with suppress(Exception):
                el.poc_1_notes = host['inventory']['poc_1_notes']

            with suppress(Exception):
                el.poc_1_phone_a = host['inventory']['poc_1_phone_a']

            with suppress(Exception):
                el.poc_1_phone_b = host['inventory']['poc_1_phone_b']

            with suppress(Exception):
                el.poc_1_screen = host['inventory']['poc_1_screen']

            with suppress(Exception):
                el.poc_2_cell = host['inventory']['poc_2_cell']

            with suppress(Exception):
                el.poc_2_email = host['inventory']['poc_2_email']

            with suppress(Exception):
                el.poc_2_name = host['inventory']['poc_2_name']

            with suppress(Exception):
                el.poc_2_notes = host['inventory']['poc_2_notes']

            with suppress(Exception):
                el.poc_2_phone_a = host['inventory']['poc_2_phone_a']

            with suppress(Exception):
                el.poc_2_phone_b = host['inventory']['poc_2_phone_b']

            with suppress(Exception):
                el.poc_2_screen = host['inventory']['poc_2_screen']

            with suppress(Exception):
                el.serialno_a = host['inventory']['serialno_a']

            with suppress(Exception):
                el.serialno_b = host['inventory']['serialno_b']

            with suppress(Exception):
                el.site_address_a = host['inventory']['site_address_a']

            with suppress(Exception):
                el.site_address_b = host['inventory']['site_address_b']

            with suppress(Exception):
                el.site_address_c = host['inventory']['site_address_c']

            with suppress(Exception):
                el.site_city = host['inventory']['site_city']

            with suppress(Exception):
                el.site_country = host['inventory']['site_country']

            with suppress(Exception):
                el.site_notes = host['inventory']['site_notes']

            with suppress(Exception):
                el.site_rack = host['inventory']['site_rack']

            with suppress(Exception):
                el.site_state = host['inventory']['site_state']

            with suppress(Exception):
                el.site_zip = host['inventory']['site_zip']

            with suppress(Exception):
                el.software = host['inventory']['software']

            with suppress(Exception):
                el.software_app_a = host['inventory']['software_app_a']

            with suppress(Exception):
                el.software_app_b = host['inventory']['software_app_b']

            with suppress(Exception):
                el.software_app_c = host['inventory']['software_app_c']

            with suppress(Exception):
                el.software_app_d = host['inventory']['software_app_d']

            with suppress(Exception):
                el.software_app_e = host['inventory']['software_app_e']

            with suppress(Exception):
                el.software_full = host['inventory']['software_full']

            with suppress(Exception):
                el.tag = host['inventory']['tag']

            with suppress(Exception):
                el.type = host['inventory']['type']

            with suppress(Exception):
                el.type_full = host['inventory']['type_full']

            with suppress(Exception):
                el.url_a = host['inventory']['url_a']

            with suppress(Exception):
                el.url_b = host['inventory']['url_b']

            with suppress(Exception):
                el.url_c = host['inventory']['url_c']

            with suppress(Exception):
                el.vendor = host['inventory']['vendor']

            # ICMP STATUS CUSTOM FIELD
            try:
                # create icmp_status field for host icmp status visualization in Kibana Map
                for trigger in host['triggers']:
                    # if icmp status is 0, then icmp status is UP
                    if 'timeout' in trigger['description']:
                        if trigger['value'] == '0':
                            el.icmp_status = '0'
                        else:
                            # else assign host icmp status DOWN
                            el.icmp_status = '1'
            except Exception as e:
                logger.exception(
                    f"""Zabbix API - failed to create icmp_status field - {e}""")

            task = el.create_geo_point()
            async_tasks.append(asyncio.create_task(task))

            await asyncio.sleep(0)

    # create geo points from async_tasks list
    await asyncio.gather(*async_tasks)

    # When all tasks are gathered close sessions
    logger.info('Elastic API - geo point creation finished')
    await el.close()
    zbx.logout()

# daemon loop, keep running even if exception occcurs
while True:
    try:
        logger.info('Starting loop cycle')

        start = time.time()

        asyncio.run(main())

        end = time.time()

        logger.info(f"Loop cycle finished in {round(end - start, 2)} seconds")

        logger.info(f'Next loop cycle in 1h...')

        time.sleep(3600)
    except Exception as e:
        logger.exception(e)
        time.sleep(3)
        continue
