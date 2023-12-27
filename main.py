import json
from cryptography.fernet import Fernet

with open("config.json", "r") as config_json:
    config_string = config_json.read()

parsed_config = json.loads(config_string)

key = b'5tlOpu2Bvib0m_yllgmzfhYVmonJNUR7bKCcdNh827Y='
cipher = Fernet(key)

encrypted_session_key = cipher.encrypt(parsed_config["session_key"].encode())
parsed_config["session_key"] = encrypted_session_key.decode()

for i in range(len(parsed_config["admins"])):
    encrypted_admin_login = cipher.encrypt(parsed_config["admins"][i]["login"].encode())
    parsed_config["admins"][i]["login"] = encrypted_admin_login.decode()

    encrypted_admin_password = cipher.encrypt(parsed_config["admins"][i]["password"].encode())
    parsed_config["admins"][i]["password"] = encrypted_admin_password.decode()

protected_config = json.dumps(parsed_config, indent=2)

with open("protected_config.json", "w") as protected_config_json:
    protected_config_json.write(protected_config)

with open("protected_config.json", "r") as protected_config_json:
    protected_config = protected_config_json.read()

parsed_protected_config = json.loads(protected_config)

encrypted_session_key = cipher.decrypt(parsed_protected_config["session_key"].encode())
parsed_protected_config["session_key"] = encrypted_session_key.decode()

for i in range(len(parsed_protected_config["admins"])):
    encrypted_admin_login = cipher.decrypt(parsed_protected_config["admins"][i]["login"].encode())
    parsed_protected_config["admins"][i]["login"] = encrypted_admin_login.decode()

    encrypted_admin_password = cipher.decrypt(parsed_protected_config["admins"][i]["password"].encode())
    parsed_protected_config["admins"][i]["password"] = encrypted_admin_password.decode()

decrypted_config = json.dumps(parsed_protected_config, indent=2)

with open("decrypted_config.json", "w") as protected_config_json:
    protected_config_json.write(decrypted_config)