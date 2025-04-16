import requests
from typing import Optional, Any, Dict, List

class JMQChirpstackAPI:
    def __init__(self, base_url: str, api_key: Optional[str] = None) -> None:
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def _get_paginated_result(
        self,
        endpoint: str,
        extra_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        result = []
        limit = 100
        offset = 0
        total_count = None
        params = extra_params.copy() if extra_params else {}

        while True:
            params.update({"limit": limit, "offset": offset})
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            if total_count is None:
                total_count = int(data.get("totalCount", 0))

            batch = data.get("result", [])
            result.extend(batch)

            if len(batch) < limit:
                break
            offset += limit

        return {"total": total_count, "result": result}

    def get_tenants(self) -> List[Dict[str, Any]]:
        return self._get_paginated_result("tenants")

    def get_gateways(self, tenant_id: str) -> List[Dict[str, Any]]:
        return self._get_paginated_result("gateways", extra_params={"tenantID": tenant_id})

    def get_applications(self, tenant_id: str) -> Dict[str, Any]:
        return self._get_paginated_result("applications", extra_params={"tenant_id": tenant_id})

    def get_devices(self, application_id: str) -> Dict[str, Any]:
        return self._get_paginated_result("devices", extra_params={"application_id": application_id})

    def get_device(self, dev_eui: str) -> Dict[str, Any]:
        url = f"{self.base_url}/devices/{dev_eui}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_device_profiles(self, tenant_id: str) -> Dict[str, Any]:
        return self._get_paginated_result("device-profiles", extra_params={"tenant_id": tenant_id})

    def get_device_profile(self, device_profile_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/device-profiles/{device_profile_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_users(self) -> Dict[str, Any]:
        return self._get_paginated_result("users")

    def get_multicast_groups(self, application_id: str) -> Dict[str, Any]:
        return self._get_paginated_result("multicast-groups", extra_params={"application_id": application_id})

    def get_gateway(self, gateway_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/gateways/{gateway_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_application(self, application_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/applications/{application_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()



if __name__ == "__main__":
    api = JMQChirpstackAPI(
        base_url="http://127.0.0.1:8090/api",
        api_key="TU_API_KEY"
    )

    try:
        tenants = api.get_tenants()
        print("Tenants:", tenants)

        if tenants["result"]:
            tenant_id = tenants["result"][0]["id"]

            gateways = api.get_gateways(tenant_id)
            print("Gateways:", gateways)

            applications = api.get_applications(tenant_id)
            print("Applications:", applications)

            if applications["result"]:
                app_id = applications["result"][0]["id"]

                devices = api.get_devices(app_id)
                print("Devices:", devices)

                if devices["result"]:
                    dev_eui = devices["result"][0]["devEui"]
                    device = api.get_device(dev_eui)
                    print("Device detail:", device)

                multicast = api.get_multicast_groups(app_id)
                print("Multicast Groups:", multicast)

            dev_profiles = api.get_device_profiles(tenant_id)
            print("Device Profiles:", dev_profiles)

            users = api.get_users()
            print("Users:", users)

    except Exception as e:
        print("Error al obtener datos:", e)
