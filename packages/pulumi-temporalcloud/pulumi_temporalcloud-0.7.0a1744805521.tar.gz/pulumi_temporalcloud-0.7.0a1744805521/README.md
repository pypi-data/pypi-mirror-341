# Temporal Cloud Resource Provider

The Temporal Cloud Resource Provider lets you manage [Temporal Cloud](https://temporal.io) resources.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @grip-security/pulumi-temporalcloud
```

or `yarn`:

```bash
yarn add @grip-security/pulumi-temporalcloud
```

### Python

To use from Python, install using `pip`:

```bash
pip install pulumi-temporalcloud
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/Grip-Security/pulumi-temporalcloud/sdk/go/...
```

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package GripSecurity.PulumiTemporalCloud
```

## Configuration

The following configuration points are available for the `temporalcloud` provider:

- `temporalcloud:allow_insecure` (environment: `TEMPORAL_CLOUD_ALLOW_INSECURE`) - (Boolean) If set to True, it allows for an insecure connection to the Temporal Cloud API. This should never be set to 'true' in production and defaults to false.
- `temporalcloud:api_key` (environment: `TEMPORAL_CLOUD_API_KEY`) - (String, Sensitive) The API key for Temporal Cloud. See [this documentation](https://docs.temporal.io/cloud/api-keys) for information on how to obtain an API key.
- `temporalcloud:endpoint` (environment: `TEMPORAL_CLOUD_ENDPOINT`) - (String) The endpoint for the Temporal Cloud API. Defaults to `saas-api.tmprl.cloud:443`.

## Reference

For detailed reference documentation, please visit [the Pulumi registry](https://www.pulumi.com/registry/packages/temporalcloud/api-docs/).
