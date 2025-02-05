import time
import logging
from api import api_request

# Configure logging
logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ccc.log"),         # Log to a ccc.log file
        logging.StreamHandler()                 # Log to console
    ]
)
logger = logging.getLogger("CCC")

class Automation:
    def __init__(self, sites):
        self.sites = sites
        self.switches = []
        self.site_uuid = []

    def get_site_uuids(self):
        """Get site UUIDs based on site names."""
        all_sites = []
        url = "/dna/intent/api/v1/site"

        for site in self.sites:
            params = {"name": site}
            ccc_sites = api_request(url, method="GET", params=params)

            if ccc_sites:
                for site in ccc_sites:
                    logging.info(f"Found site with ID '{site['id']}' and name hierarchy '{site['siteNameHierarchy']}'")
                    all_sites.append({
                        "siteId": site["id"],
                        "siteNameHierarchy": site["siteNameHierarchy"]
                    })

        self.site_uuid = all_sites 

    def get_switches_from_sites(self):
        """Get only the switches from the sites."""

        if not self.site_uuid:
            self.get_site_uuids()

        all_switches = []
        for site in self.site_uuid:
            url = f"/dna/intent/api/v1/site-member/{site['siteId']}/member"
            params = {"memberType": "networkdevice"}
            devices = api_request(url, method="GET", params=params)

            if devices:
                switches = [
                    {
                        "switchUuid": device["instanceUuid"],
                        "hostname": device["hostname"],
                        "platformId": device["platformId"],
                        "siteUuid": site["siteId"],
                        "siteNameHierarchy": site["siteNameHierarchy"]
                    }
                    for device in devices
                    if device.get("family") == "Switches and Hubs"
                ]
                all_switches.extend(switches)
            time.sleep(1)

        self.switches = all_switches  # Store switches for further use

    def get_image_status(self):
        """Checks if switch image is outdated."""
        if not self.switches:
            self.get_switches_from_sites()

        switch_software = []
        url = "/api/v2/device-image/device?"
        params = {"id": ", ".join(switch["switchUuid"] for switch in self.switches)}
        devices = api_request(url, method="GET", params=params)

        for device in devices:
            if device["deviceImageUpgradeStatus"] == "OUTDATED":
                switch_software.append({
                    "switchUuid": device["deviceId"],
                    "installedVersion": device["deviceInstalledInfo"][0]["displayVersion"],
                    "targetUuid": device["targetImageInfo"][0]["imageUuid"],
                    "targetVersion": device["targetImageInfo"][0]["displayVersion"]
                })

        switches_dict = {obj["switchUuid"]: obj for obj in self.switches}
        merged_list = [
            {**switches_dict[obj["switchUuid"]], **obj}
            for obj in switch_software if obj["switchUuid"] in switches_dict
        ]

        if merged_list:
            logger.info('Found outdated images:')
            for sw in merged_list:
                logger.info(f"Device '{sw['hostname']}' in site '{sw['siteNameHierarchy']}' will be upgraded from IOS-XE {sw['installedVersion']} to IOS-XE {sw['targetVersion']}")
            logger.info('Proceeding to distribution of the images...')
        else:
            logger.info("All looks good, nothing to upgrade")

        return merged_list

    def check_task(self, taskId):
        """Checks task status and retries until success or failure."""
        retries = 0
        delay = 120
        max_retries = 20

        while retries < max_retries:
            url = f"/dna/intent/api/v1/tasks/{taskId}/"
            response = api_request(url, method="GET")

            if response and response.get("status") == "SUCCESS":
                logger.info("Status is SUCCESS. Proceeding to activation")
                return response
            elif response and response.get("status") == "FAILURE":
                logger.error("Distribution failed.")
                return None
            else:
                retries += 1
                logger.info(f"Status is still '{response.get('status')}'. Retrying in {delay} seconds...")
                time.sleep(delay)

        logger.error("Max retries reached. Status did not become SUCCESS.")
        return None

    def upgrade(self):
        """Creates payload for image distribution."""
        outdated_switches = self.get_image_status()
        payload = []
        for switch in outdated_switches: 
            image = {}
            image["deviceUuid"] = switch["switchUuid"]
            image["imageUuid"] = switch["targetUuid"]
            payload.append(image)        

        # url = f"{CCC_BASE_URL}/dna/intent/api/v1/image/distribution"
        # request = api_request(url, method="POST", data=payload)
        # self.check_task(request['taskId'])
