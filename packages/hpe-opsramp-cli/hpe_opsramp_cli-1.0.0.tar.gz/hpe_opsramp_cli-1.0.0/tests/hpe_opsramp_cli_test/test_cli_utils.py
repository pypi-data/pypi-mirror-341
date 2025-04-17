from hpe_opsramp_cli.cli_utils import CLI_Utils, OpsRampEnvironment, SingletonLogger
import rich

SingletonLogger().get_logger(log_level="DEBUG")


def test_group_dict_by_key() -> None:
    data = [
        {
            "id": "99cf1edb-d2d5-4feb-ae81-842c365ee8b2",
            "name": "DC134",
            "type": "Other",
            "clientId": "78734cff-95b8-483f-a9ad-4447d70f6f91",
        },
        {
            "id": "bef80628-9bde-4712-88df-dc7545906d65",
            "name": "DC143",
            "type": "Other",
            "clientId": "78734cff-95b8-483f-a9ad-4447d70f6f91",
        },
        {
            "id": "bef80628-9bde-4712-88df-dc7545906ded",
            "name": "DC143",
            "type": "Other",
            "clientId": "78734cff-95b8-483f-a9ad-4447d70f6f92",
        },
        {
            "id": "bef80628-9bde-4712-88df-dc7545906de93",
            "name": "DC143",
            "type": "Other",
            "clientId": "78734cff-95b8-483f-a9ad-4447d70f6f93",
        },
    ]
    new_dict = CLI_Utils.group_dict_by_key(data=data, key="clientId", value="id")
    rich.print(new_dict)


def test_unmanage_resources_progress_bar_partner() -> None:
    per_client_alert_only_resoures = {
        "b1838501-9d66-4c09-99e0-7db0b8812a7e": [
            "f9427f70-d76e-4c1d-b585-5068c3306093",
            "f53e6c1f-df66-4be0-9462-1fdf0d59b795",
            "ed1ad8d5-6c7f-4f61-b3de-f257847eaa64",
            "6777387a-df21-4523-b294-fcb134897731",
            "9814b490-8e61-4cfc-8919-8b24c4339088",
        ],
        "649c8df6-569e-4aab-8b1d-c132290b602c": [
            "65443f03-6c07-4be9-a69f-6a898c1dcd90",
            "7eb11544-b924-458d-8101-9bcb9b3da324",
        ],
        "cc0c2a2e-9c63-46b5-9db2-ec9f6d7dbcbd": [
            "5d4cac04-a8b0-4a73-bfb4-d1db9e8a7867",
            "93a90c21-bd56-4674-9790-801b38c51e95",
            "d47807a1-71da-4c79-b8ef-643cc581501c",
            "d92c999d-eace-4502-884f-4ac8799dfc08",
        ],
    }

    env = OpsRampEnvironment(envname="UAT_National_INC")

    CLI_Utils.unmanage_resources_progress_bar_partner(
        per_client_alert_only_resoures=per_client_alert_only_resoures,
        opsramp_env_object=env,
    )

def test_unmanage_resources_progress_bar_partner_POD7() -> None:
    per_client_alert_only_resoures = {
        "32b50e46-6ef8-4cb6-9902-400dca670304": [
            "be09bb86-1d29-4d44-af26-da4d98954346",
            "9760f946-2125-44b1-8a33-be160ffaea83",
            "6f449f3e-e872-4e4f-87ec-e2ca2a509ba0"],
        "b2ddde6f-327a-49e7-b63b-11f818c662ea": [
            "1e2fe7ae-e8b9-431c-acec-da1c21652207",
            "6c86b75b-2c72-4523-890f-e1c930e7a07f",
            "bcea4173-46a3-4580-9f24-e278fac4edfc",
        ]
    }

    env = OpsRampEnvironment(envname="POD7_GLP_Flex_Partner")

    CLI_Utils.unmanage_resources_progress_bar_partner(
        per_client_alert_only_resoures=per_client_alert_only_resoures,
        opsramp_env_object=env,
    )
