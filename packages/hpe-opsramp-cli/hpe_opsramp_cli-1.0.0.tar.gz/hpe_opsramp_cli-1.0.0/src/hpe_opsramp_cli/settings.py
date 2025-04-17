PARENT_COMMAND = "hpe_opsramp_cli"
UNMANAGE_ALERT_RESOURCES_SUB_COMMAND = "unmanage_alert_resources"
ENV_HELP = "Name of environment to use, as defined in the environments.yml file"
ENV_FILE_HELP = (
    "Absolute path  of environments.yml. Refer to the help for sample environments.yml."
)
ENV_FILE_DEFAULT = "environments.yml"
OPSQL_FILE_HELP = "Absolute path  of the OpsQL.jsno, which filters resources for unmanaging. Refer to the help for the sample OpsQL.json.If not supplied, the default from the code is considered"
LOG_LEVEL_DEFAULT = "INFO"
LOG_LEVEL_HELP = "Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
"""
current_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
OPSQL_FILE_DEFAULT = os.path.join(current_dir, 'unmanage_alert_resources_opsql.json')
"""

OPSQL_FILE_DEFAULT = "unmanage_alert_resources_opsql.json"
BULK_UNMANAGE_LIMIT = 39

"""
Error messages
"""
ENV_NAME_NOT_FOUND_ERROR_MESSAGE = (
    "The environment: {envname} is not found in the environment file: {envfile}"
)
ENV_FILE_NOT_FOUND_ERROR_MESSAGE = (
    "The environment file: {envfile} is not found inside {os.getcwd()} folder"
)
INVALID_ENV_FILE_ERROR_MESSAGE = "The environment file: %s is not a valid YAML file"
