# Tractoray

The tool for running [Ray](https://www.ray.io/) clusters on [Tracto.ai](https://tracto.ai/). Allows you to easily deploy and manage Ray clusters within YT infrastructure.

## Features

- Launch Ray clusters with configurable resources
- Support native ray dashboard and ray client
- Flexible Docker image configuration

## Installation

```bash
pip install -U tractoray
```

## Usage

### Basic Commands

To use `tractoray`, you need to specify the working directory, for example your homedir `//home/<login>/tractoray`.

Start a cluster:
```bash
tractoray start --workdir //your/cypress/path --node-count 2
```

return an instruction to connect to the cluster:

Check cluster status:
```bash
tractoray status --workdir //your/yt/path
```

also supports output in JSON format:
```bash
tractoray status --workdir //your/cypress/path --format json
```

Stop the cluster:
```bash
tractoray stop --workdir //your/cypress/path
```

For detailed information about task submission, log reading, and other operations, please check the `ray status` command output.

## Using Custom Docker Images

You have two options for Docker images:

1. Use the default image as base (recommended):
   ```dockerfile
   FROM cr.eu-north1.nebius.cloud/e00faee7vas5hpsh3s/tractoray/default:2025-04-10-21-17-47-7f93a1500
   
   # Add your dependencies
   RUN pip install your-package
   ```

2. Build from scratch:
   - Install `tractoray` via pip
   - Make sure to use the same version as in your local environment and all necessary dependencies for CUDA and infiniband
   ```dockerfile
   FROM python:3.9
   
   RUN pip install tractoray==<your-local-version>
   # Add other dependencies
   ```

The default image includes all necessary dependencies and configurations for Ray cluster operation for machine learning tasks. Using it as a base image is recommended to ensure compatibility.

## Environment Variables

- `YT_LOG_LEVEL`: Set logging level

## Limitations

- Some Ray CLI options, such as `ray status`, may not function properly due to Ray authentication constraints. It is recommended to use Ray dashboard and Ray SDK instead.
- Ray Serve is not supported.
- Observability features are disabled by default. You can enable and configure them in your custom image.
