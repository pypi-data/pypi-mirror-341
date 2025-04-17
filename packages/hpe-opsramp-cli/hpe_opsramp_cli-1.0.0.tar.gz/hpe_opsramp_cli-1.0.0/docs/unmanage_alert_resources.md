# `opsramp-cli`

**Usage**:

```console
$ opsramp-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `unmanage_alert_resources`: # Unmanage Alert Resources Command ## This...

## `opsramp-cli unmanage_alert_resources`

# Unmanage Alert Resources Command
## This command does the following
- Identifies the resources transitioned from unmanaged to managed due to alerts
- Unmanage them again
## sample enviroment.yaml
```yaml
- name: PRODurl: https://acme.api.opsramp.com
partner: -e7f3-40cc-ed0d8f51-b117-63847a3cc9cc
tenant: 78734cff--483f-a9ad-4495b847d70f6f91
client_id: N3Hp43TC9UCjbu7NkYExvvkZF4SfUbtS
client_secret: 2mKQTDwvtA4WybgMkDnWJEU6xSp5SjQjggHDD
- name: UAT
url: https://uat.opsramp.com
partner: ed0d8f51--40cc-b117-63847a3cc9cc
tenant: cc0c2a2e-9c63--9db2-ec9f6d7dbcbd
client_id: n9PQE42zUQKFUPfZce7f39QXpczhjbJaKEdp
client_secret: mBA3v2FjQ8xdue7f3qbHAuQxU9226xehznJj9Xu9tCjbtPmwtq3RCHTqRz68QzCj
```
### Sample opsql.json
```json
{
&quot;objectType&quot;: &quot;resource&quot;,
&quot;fields&quot;: [
    &quot;id&quot;
],
&quot;filterCriteria&quot;: &quot;tags.name = &quot;Managed By&quot;  AND tags.value = &quot;Alert&quot; &quot;,
&quot;pageNo&quot;: 1,
&quot;pageSize&quot;: 500
}
```

**Usage**:

```console
$ opsramp-cli unmanage_alert_resources [OPTIONS]
```

**Options**:

* `--env TEXT`: Name of environment to use, as defined in the environments.yml file  [required]
* `--env-file TEXT`: Absolute path  of environments.yml. Refer to the help for sample environments.yml.  [default: environments.yml]
* `--opsql-file TEXT`: Absolute path  of the OpsQL.jsno, which filters resources for unmanaging. Refer to the help for the sample OpsQL.json.If not supplied, the default from the code is considered  [default: unmanage_alert_resources_opsql.json]
* `--help`: Show this message and exit.
