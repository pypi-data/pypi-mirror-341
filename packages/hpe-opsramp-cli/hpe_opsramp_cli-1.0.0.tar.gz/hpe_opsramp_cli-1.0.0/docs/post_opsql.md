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

* `hpe_opsramp_cli`

## `opsramp-cli hpe_opsramp_cli`

**Usage**:

```console
$ opsramp-cli hpe_opsramp_cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `post_opsql`

### `opsramp-cli hpe_opsramp_cli post_opsql`

**Usage**:

```console
$ opsramp-cli hpe_opsramp_cli post_opsql [OPTIONS]
```

**Options**:

* `--env TEXT`: Name of environment to use, as defined in your environments.yml file  [required]
* `--envfile TEXT`: Location of environments YAML file  [default: environments.yml]
* `--opsql-file TEXT`: Location of the OpsQL input payload JSON file  [default: opsql.json]
* `--help`: Show this message and exit.
