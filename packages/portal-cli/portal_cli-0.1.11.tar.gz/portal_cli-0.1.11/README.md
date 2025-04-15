# Portal CLI

A command-line interface for interacting with the portal image management system.

## Installation

To install the Portal CLI, use pip:

```bash
pip install portal-cli
```

## Usage

The Portal CLI provides several commands for managing images.

### Upload

Uploads a Docker image.

```bash
portal-cli upload image --image <path/to/image.tar>
```

### Search

Searches for images.

```bash
portal-cli search by-name --name <image_name>
```

### Scan

Scans an image for vulnerabilities.

```bash
portal-cli scan vulnerabilities --image <image:tag>
```

### Chart

Retrieves a Helm chart.

```bash
portal-cli chart get --image-uid <image_uid> --image-version <image_version>
```

### Transfer

Transfers an image to a registry.

```bash
portal-cli transfer to-registry --image <image:tag> --registry <registry_url>
```

### Deploy

Deploys an image to a Kubernetes cluster.

```bash
portal-cli deploy image --image <image:tag> --namespace <namespace>
```

## Examples

### Uploading an Image

```bash
portal-cli upload image --image my_app_image.tar
```

### Searching for an Image by Name

```bash
portal-cli search by-name --name my_app_image
```

### Scanning an Image for Vulnerabilities

```bash
portal-cli scan vulnerabilities --image my_app_image:latest
```

### Getting a Helm Chart

```bash
portal-cli chart get --image-uid 7LLgaAY1M2odDy8afDbWxSNqtawaPU2LMex8Hs5mD2oY1VKgzQ436W8TU5Ux --image-version v0-0-01
```

### Transferring an Image to a Registry

```bash
portal-cli transfer to-registry --image my_app_image:latest --registry docker.example.com
```

### Deploying an Image to a Kubernetes Namespace

```bash
portal-cli deploy image --image my_app_image:latest --namespace production
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
```