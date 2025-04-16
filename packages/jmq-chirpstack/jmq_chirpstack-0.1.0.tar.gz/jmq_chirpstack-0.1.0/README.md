# Install jmq_chirpstack in Python

**Integration package with the ChirpStack API using Python.**  
This client allows easy connection to the ChirpStack REST API to retrieve information about tenants, gateways, applications, devices, device profiles, users, and more.

---

## 🚀 Installation

You can install the package locally using `pip`:

```bash
pip install jmq_chirpstack
```

Or directly from the repository:

```bash
pip install git+https://github.com/juaquicar/jmq_chirpstack.git
```

---

## 🧰 Requirements

- Python >= 3.6
- Access to the ChirpStack API with a valid API Key
- Version: v4.11.1 Testeada


---

## 📦 Usage

```python
from jmq_chirpstack import JMQChirpstackAPI

api = JMQChirpstackAPI(
    base_url="http://127.0.0.1:8090/api",
    api_key="YOUR_API_KEY"
)

tenants = api.get_tenants()
print("Tenants:", tenants)
```

---

## 🧪 Available Features

- `get_tenants()`
- `get_gateways(tenant_id)`
- `get_gateway(gateway_id)`
- `get_applications(tenant_id)`
- `get_application(application_id)`
- `get_devices(application_id)`
- `get_device(dev_eui)`
- `get_device_profiles(tenant_id)`
- `get_device_profile(device_profile_id)`
- `get_users()`
- `get_multicast_groups(application_id)`

---

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Juanma Quijada**  
📧 quijada.jm@gmail.com  
🔗 [GitHub](https://github.com/juaquicar)

---

## 🌐 Useful Resources

- [Official ChirpStack Documentation](https://www.chirpstack.io/docs/)

---

