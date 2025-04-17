class NoisyLoggers:

    HTTP = [
        'azure.core.pipeline.policies.http_logging_policy',
        'requests', 
        'urllib3'
    ]

    AZURE = [
        'az_command_data_logger',
        'azure',
        'azure.core.credentials',
        'azure.core.pipeline',
        'azure.core.pipeline.policies',
        'azure.core.pipeline.transport',
        'azure.identity',
        'azure.mgmt',
        'cli.azure.cli.command_modules.network.custom',
        'cli.azure.cli.command_modules.resource._bicep',
        'cli.azure.cli.command_modules.resource.custom',
        'cli.azure.cli.command_modules.role.custom',
        'cli.azure.cli.command_modules.storage._validators',
        'cli.azure.cli.command_modules.storage.custom',
        'cli.azure.cli.command_modules.vm.custom',
        'cli.azure.cli.core',
        'cli.azure.cli.core._help',
        'cli.azure.cli.core._output',
        'cli.azure.cli.core._profile',
        'cli.azure.cli.core.auth.binary_cache',
        'cli.azure.cli.core.auth.credential_adaptor',
        'cli.azure.cli.core.auth.msal_authentication',
        'cli.azure.cli.core.auth.persistence',
        'cli.azure.cli.core.azclierror',
        'cli.azure.cli.core.azlogging',
        'cli.azure.cli.core.commands.client_factory',
        'cli.azure.cli.core.decorators',
        'cli.azure.cli.core.extension',
        'cli.azure.cli.core.profiles',
        'cli.azure.cli.core.sdk.policies',
        'cli.azure.cli.core.telemetry',
        'cli.azure.cli.core.util',
        'cli.knack.cli',
        'cli.knack.cli.core',
        'msal.application',
        'msal.authority',
        'msal.telemetry',
    ]

CommonNoisyLoggers = NoisyLoggers()
