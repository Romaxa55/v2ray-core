import json
import os
import uuid

CONFIG_FILE = "/etc/v2ray/template.json"
SAVE_CONFIG_FILE = "/etc/v2ray/config.json"

# Получаем идентификаторы клиентов из переменных окружения
CLIENT_IDS = {key: value for key, value in os.environ.items() if key.startswith("CLIENT_ID")}

# Если переменные окружения не заданы, генерируем случайные UUID
if not CLIENT_IDS:
    for i in range(1, 4):  # Предположим, что нужно три клиента по умолчанию
        CLIENT_IDS[f"CLIENT_ID{i}"] = str(uuid.uuid4())

# Глобальные значения для alterId и security
ALTER_ID = int(os.getenv("ALTER_ID", 64))
SECURITY = os.getenv("SECURITY", "auto")


# Функция проверки валидности UUID
def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=4)
        return str(uuid_obj) == uuid_to_test
    except ValueError:
        return False


def add_clients():
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)

    for inbound in config["inbounds"]:
        if inbound["protocol"] == "vmess":
            for key, client_id in CLIENT_IDS.items():
                if is_valid_uuid(client_id):
                    client = {
                        "id": client_id,
                        "alterId": ALTER_ID,
                        "security": SECURITY
                    }
                    inbound["settings"]["clients"].append(client)
                    print(f"Added client {key}: {client_id}")
                else:
                    print(f"Invalid UUID {key}: {client_id}")

    with open(SAVE_CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)


if __name__ == "__main__":
    add_clients()
