import sys
from typing import List, Any

from rich.progress import Progress


from . import settings as s
from .opsramp_environment import OpsRampEnvironment
from hpe_opsramp_cli.singleton_logger import SingletonLogger

from collections import defaultdict
from typing import Dict
import logging

logger = SingletonLogger().get_logger()


class CLI_Utils:

    @classmethod
    def do_cmd_unmanage_alert_devices(
        cls, opsramp_env_object: OpsRampEnvironment, args: dict
    ) -> list[list[Any]]:
        """

        :param opsramp_env_object: Object of OpsRampEnviroment
        :param args:  conaining env, envfile sample {'env': 'siva', 'envfile': 'environments.yml', 'opsql_file': 'unmanage_alert_resources_opsql.json'}
        :return: list of unmanged resources
        """

        alert_only_resources = cls.get_alert_only_resources_progress_bar(
            args, opsramp_env_object
        )

        return cls.unmanage_resources_progress_bar(
            alert_only_resources, opsramp_env_object
        )

    @classmethod
    def do_cmd_unmanage_alert_devices_partner(
        cls, opsramp_env_object: OpsRampEnvironment, args: dict
    ) -> list[list[Any]]:
        """

        :param opsramp_env_object: Object of OpsRampEnviroment
        :param args:  containing env, envfile sample {'env': 'siva', 'envfile': 'environments.yml', 'opsql_file': 'unmanage_alert_resources_opsql.json'}
        :return: list of unmanged resources
        """

        alert_only_resources = cls.get_alert_only_resources_progress_bar(
            args, opsramp_env_object
        )

        per_client_alert_only_resoures: Dict[str, List[str]]
        per_client_alert_only_resoures = CLI_Utils.group_dict_by_key(
            alert_only_resources, key="clientId", value="id"
        )
        logger.debug("alert only resources are %s" % (per_client_alert_only_resoures))
        return cls.unmanage_resources_progress_bar_partner(
            per_client_alert_only_resoures, opsramp_env_object
        )

    @classmethod
    def unmanage_resources_progress_bar(
        cls, alert_only_resources, opsramp_env_object: OpsRampEnvironment
    ) -> list[list[Any]]:
        with Progress(auto_refresh=False) as unmanage_progress:
            progress_total: int = len(alert_only_resources) + 5
            unmanage_alert_resources_task = unmanage_progress.add_task(
                "[green]Unmanaging alert only resources", total=progress_total
            )
            while not unmanage_progress.finished:
                # unmanage
                unmanage_progress.console.log(
                    "Starting to unmanage %s alert only resources..."
                    % (len(alert_only_resources))
                )
                unmanage_progress.update(
                    task_id=unmanage_alert_resources_task, advance=1
                )
                unmanage_progress.refresh()

                ids_list = [
                    sub["id"] for sub in alert_only_resources
                ]  # ['bcaaa9ba-f913-4fee-8c43-8f6ccf84dd8e', 'bcea4173-46a3-4580-9f24-e278fac4edfc', '6c86b75b-2c72-4523-890f-e1c930e7a07f', '432bb193-62ad-447a-aacc-b37a4464e45d', '1e2fe7ae-e8b9-431c-acec-da1c21652207', 'd8bfca19-60f4-444f-bfa8-1f2f91f4ec87']
                unmanage_progress.update(
                    task_id=unmanage_alert_resources_task, advance=2
                )
                unmanage_progress.refresh()

                chunks: List[List] = [
                    ids_list[i : i + s.BULK_UNMANAGE_LIMIT]
                    for i in range(0, len(ids_list), s.BULK_UNMANAGE_LIMIT)
                ]
                # debugging notes chunks = [['0217c9fc-28c6-4524-b4f1-83b68305c611', 'd6ef002e-f983-4f8f-81ce-2cd591f65599', '1bbf9db3-0b23-4068-96b7-b43861d112d1', '0c3cda2e-0b18-4100-b153-9237ed784541']]

                """
                double encoding json issue.
                https://stackoverflow.com/questions/25242262/dump-to-json-adds-additional-double-quotes-and-escaping-of-quotes
                """
                completed: int = 0
                for chunk in chunks:

                    """
                    ids_list_json = json.dumps(
                        ids_list)  # '["bcaaa9ba-f913-4fee-8c43-8f6ccf84dd8e", "bcea4173-46a3-4580-9f24-e278fac4edfc", "d8bfca19-60f4-444f-bfa8-1f2f91f4ec87", "6c86b75b-2c72-4523-890f-e1c930e7a07f", "432bb193-62ad-447a-aacc-b37a4464e45d", "1e2fe7ae-e8b9-431c-acec-da1c21652207"]'
                    # Debugging notes ids_list_json ['0217c9fc-28c6-4524-b4f1-83b68305c611', 'd6ef002e-f983-4f8f-81ce-2cd591f65599', '1bbf9db3-0b23-4068-96b7-b43861d112d1', '0c3cda2e-0b18-4100-b153-9237ed784541']

                    """

                opsramp_env_object.do_post(chunk, api_name="resource_unmanage")
                completed = completed + len(chunk)
                unmanage_progress.console.log(
                    "Unmanaged %s alert only resources so far" % completed
                )
                unmanage_progress.update(
                    task_id=unmanage_alert_resources_task, advance=completed
                )
                unmanage_progress.refresh()

                unmanage_progress.console.log(
                    "Unmanage alert only resources successfully completed"
                )
                unmanage_progress.update(
                    task_id=unmanage_alert_resources_task, completed=progress_total
                )
                unmanage_progress.refresh()

            return chunks

    @classmethod
    def unmanage_resources_progress_bar_partner(
        cls,
        per_client_alert_only_resoures: Dict[str, List[str]],
        opsramp_env_object: OpsRampEnvironment,
    ) -> list[list[Any]]:
        with Progress(auto_refresh=False) as unmanage_progress:
            progress_total: int = len(per_client_alert_only_resoures) + 5
            unmanage_alert_resources_task = unmanage_progress.add_task(
                "[green]Unmanaging alert only resources", total=progress_total
            )
            while not unmanage_progress.finished:
                # unmanage
                unmanage_progress.console.log(f"Starting to unmanage alert only resources of {(len(per_client_alert_only_resoures))} clients ...")
                unmanage_progress.update(
                    task_id=unmanage_alert_resources_task, advance=1
                )
                unmanage_progress.refresh()
                """
                {
                    '78734cff-95b8-483f-a9ad-4447d70f6f91': ['99cf1edb-d2d5-4feb-ae81-842c365ee8b2', 'bef80628-9bde-4712-88df-dc7545906d65'],
                    '78734cff-95b8-483f-a9ad-4447d70f6f92': ['bef80628-9bde-4712-88df-dc7545906ded'],
                    '78734cff-95b8-483f-a9ad-4447d70f6f93': ['bef80628-9bde-4712-88df-dc7545906de93']
                }
                """
                for key, value in per_client_alert_only_resoures.items():
                    logger.debug(
                        "For loop on per_client_alert_only_resoures: %s Key: %s Value: %s "
                        % (per_client_alert_only_resoures, key, value)
                    )
                    try:
                        logger.debug(
                            "alert_only_resoures of client %s are %s:"
                            % (key, per_client_alert_only_resoures[key])
                        )

                    except TypeError as e:
                        logger.debug(
                            f"Caught an error: while finding length of alert resources of client {e}"
                        )
                        sys.exit(1)

                    chunks: List[List] = [
                        per_client_alert_only_resoures[key][
                            i : i + s.BULK_UNMANAGE_LIMIT
                        ]
                        for i in range(
                            0,
                            len(per_client_alert_only_resoures[key]),
                            s.BULK_UNMANAGE_LIMIT,
                        )
                    ]
                    logger.debug("chunks: %s" % chunks)
                    # debugging notes chunks = [['0217c9fc-28c6-4524-b4f1-83b68305c611', 'd6ef002e-f983-4f8f-81ce-2cd591f65599', '1bbf9db3-0b23-4068-96b7-b43861d112d1', '0c3cda2e-0b18-4100-b153-9237ed784541']]

                    """
                    double encoding json issue.
                    https://stackoverflow.com/questions/25242262/dump-to-json-adds-additional-double-quotes-and-escaping-of-quotes
                    """
                    completed: int = 0

                    for chunk in chunks:
                        """
                        ids_list_json = json.dumps(
                            ids_list)  # '["bcaaa9ba-f913-4fee-8c43-8f6ccf84dd8e", "bcea4173-46a3-4580-9f24-e278fac4edfc", "d8bfca19-60f4-444f-bfa8-1f2f91f4ec87", "6c86b75b-2c72-4523-890f-e1c930e7a07f", "432bb193-62ad-447a-aacc-b37a4464e45d", "1e2fe7ae-e8b9-431c-acec-da1c21652207"]'
                        # Debugging notes ids_list_json ['0217c9fc-28c6-4524-b4f1-83b68305c611', 'd6ef002e-f983-4f8f-81ce-2cd591f65599', '1bbf9db3-0b23-4068-96b7-b43861d112d1', '0c3cda2e-0b18-4100-b153-9237ed784541']

                        """
                        completed = completed + len(chunk)
                        unmanage_progress.console.log(f"Unmanaging {completed} alert only resources of client : {key} ...")
                        opsramp_env_object.do_post(
                            chunk, api_name="resource_unmanage_partner", client_id=key
                        )
                        # unmanage_progress.console.log(f"Unmanaged {completed}  alert only resources so far")
                        unmanage_progress.update(
                            task_id=unmanage_alert_resources_task, advance=completed
                        )
                        unmanage_progress.refresh()

                    """
                    unmanage_progress.console.log(
                        "Unmanage alert only resources successfully completed"
                    )
                    """
                    unmanage_progress.update(
                        task_id=unmanage_alert_resources_task, completed=progress_total
                    )
                    unmanage_progress.refresh()

            return chunks

    @classmethod
    def get_alert_only_resources_progress_bar(
        cls, args, opsramp_env_object: OpsRampEnvironment
    ):
        with Progress() as find_progress:
            find_alert_resources_task = find_progress.add_task(
                "[red]Finding out alert only resources", total=1000
            )

            while not find_progress.finished:
                ## Finding out alert only resources
                find_progress.update(find_alert_resources_task, advance=100)
                find_progress.refresh()
                # time.sleep(0.02)
                opsql_query = opsramp_env_object.get_json_from_file(args["opsql_file"])
                find_progress.update(task_id=find_alert_resources_task, advance=800)
                find_progress.refresh()
                # time.sleep(0.02)

                alert_only_resources = opsramp_env_object.do_post(
                    opsql_query, api_name="opsql"
                )
                if len(alert_only_resources) == 0:
                    find_progress.console.log(
                        "There is no alert only resources. Exiting"
                    )
                    find_progress.update(
                        task_id=find_alert_resources_task, advance=1000
                    )
                    find_progress.refresh()
                    logger.debug("There is no alert only resources. Exiting")
                    sys.exit(0)

                find_progress.update(task_id=find_alert_resources_task, advance=900)
                find_progress.refresh()
                find_progress.console.log(
                    "Found %s alert only resources ..." % (len(alert_only_resources))
                )
                logger.debug("alert_only_resources are %s" % alert_only_resources)
                find_progress.update(task_id=find_alert_resources_task, advance=1000)
                find_progress.refresh()
        return alert_only_resources

    @classmethod
    def do_cmd_post_opsql(cls, opsramp_env_object: OpsRampEnvironment, args: dict):
        """

        :param opsramp_env_object: Object of OpsRampEnviroment
        :param args:  containing env, envfile sample {'env': 'siva', 'envfile': 'environments.yml', 'opsql_file': 'unmanage_alert_resources_opsql.json'}
        :return:
        """
        opsql_query = opsramp_env_object.get_json_from_file(args["opsql_file"])
        opsramp_env_object.do_post(opsql_query, api_name="opsql")
        # rich.print("OpsQL Response")
        # rich.print_json(json.dumps(opsql_response))

    @classmethod
    def group_dict_by_key(
        cls, data: List[Dict[str, int]], key: str, value: str
    ) -> defaultdict[int, list[int]]:
        """
            groups data by key and adds value as values to the key
            {
        '78734cff-95b8-483f-a9ad-4447d70f6f91': ['99cf1edb-d2d5-4feb-ae81-842c365ee8b2', 'bef80628-9bde-4712-88df-dc7545906d65'],
        '78734cff-95b8-483f-a9ad-4447d70f6f92': ['bef80628-9bde-4712-88df-dc7545906ded'],
        '78734cff-95b8-483f-a9ad-4447d70f6f93': ['bef80628-9bde-4712-88df-dc7545906de93']
            }
        """

        grouped_data = defaultdict(list)

        for item in data:
            grouped_data[item[key]].append(item[value])

        # Convert defaultdict to a regular dict if needed
        grouped_data = dict(grouped_data)

        return grouped_data

    @classmethod
    def get_logger(name):
        # Create a custom logger
        logger = logging.getLogger(name)
        logger.setLevel(
            logging.DEBUG
        )  # Set the logger level to the lowest level you want to capture

        # Create handlers
        debug_handler = logging.StreamHandler()
        info_handler = logging.StreamHandler()

        # Set levels for handlers
        debug_handler.setLevel(logging.DEBUG)
        info_handler.setLevel(logging.INFO)

        # Create formatters and add them to handlers
        debug_format = logging.Formatter("%(asctime)s - DEBUG - %(message)s")
        info_format = logging.Formatter("%(asctime)s - INFO - %(message)s")

        debug_handler.setFormatter(debug_format)
        info_handler.setFormatter(info_format)

        # Add handlers to the logger
        logger.addHandler(debug_handler)
        logger.addHandler(info_handler)

        # Example log messages
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
