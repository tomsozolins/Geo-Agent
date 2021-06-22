import urllib3
from loguru import logger
from pyzabbix import ZabbixAPI


class GeoZabbix():

    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            with open('/var/run/secrets/ZABBIX_ENDPOINT') as f:
                zabbix_endpoint = f.read()
            with open('/var/run/secrets/ZABBIX_USER') as f:
                zabbix_user = f.read()
            with open('/var/run/secrets/ZABBIX_PASS') as f:
                zabbix_pass = f.read()
        except:
            # For development environment
            with open('secrets/geo_agent/.ZABBIX_ENDPOINT') as f:
                zabbix_endpoint = f.read()
            with open('secrets/geo_agent/.ZABBIX_USER') as f:
                zabbix_user = f.read()
            with open('secrets/geo_agent/.ZABBIX_PASS') as f:
                zabbix_pass = f.read()

        zapi = ZabbixAPI(f"https://{zabbix_endpoint}")
        zapi.session.verify = False
        try:
            zapi.login(zabbix_user, zabbix_pass)
            self.zapi = zapi
            logger.info('Zabbix API - connection success')
        except Exception as e:
            logger.exception(f"""Zabbix API - connection failed - {e}""")

    def get_host_data(self):

        try:
            logger.info('Zabbix API - getting host data')
            response = self.zapi.do_request(
                "host.get",
                {
                    "output": "extend",
                    "selectParentTemplates": [
                        "templateid",
                        "name"
                    ],
                    "selectInterfaces": "extend",
                    "selectInventory": "extend",
                    "selectTriggers": "extend",
                    "selectGroups": "extend"
                }
            )['result']
            return response
        except Exception as e:
            logger.error('Zabbix API - failed to get host data')
            logger.debug(e)

    def update_host_inventory(self, host_id, field, value):
        self.host_id = host_id
        self.field = field
        self.value = value
        try:
            logger.info(
                f'Zabbix API - updating host inventory field {self.field} {self.value}')
            response = self.zapi.do_request(
                "host.update",
                {
                    "hostid": self.host_id,
                    "inventory_mode": 1,
                    "inventory": {
                        self.field: self.value
                    }
                }
            )['result']
            return response
        except Exception as e:
            logger.error(
                f'Zabbix API - failed to update host inventory field {self.field} {self.value}')
            logger.debug(e)

    def logout(self):
        try:
            self.zapi.user.logout()
            logger.info('Zabbix API - closing connection')
        except Exception as e:
            logger.exception(f'Zabbix API - failed to close connection - {e}')
