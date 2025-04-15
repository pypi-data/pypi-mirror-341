
# Kwasa CLI

## Notice

Kwasa CLI is a command-line tool designed for bundling the Django starter template from [django-starter-template](https://github.com/dlion4/django-quick-starter.git), but can be used to clone and update **any** repository. It helps automate the process of cloning, updating, and working with repositories with minimal effort.

## Features

- Clone the repository into the current empty directory.
- Clone a repository into a specified directory.
- Update the repository whenever the source code is updated.
- Use it as a Django starter template bundler, or for general-purpose repository management.

## Requirements

- Python 3.13 or higher
- `pip` for package management
- A virtual environment to install and run the package.

## Installation

### 1. Create a Virtual Environment

To begin, create a virtual environment for your project. You can do this by running:

```bash
python -m venv .venv
```

Then, activate the virtual environment.

- On **Windows**:

    ```bash
    .\.venv\Scripts\activate
    ```

- On **Linux/macOS**:

    ```bash
    source .venv/bin/activate
    ```

### 2. Install Kwasa CLI as a pip Package

Once the virtual environment is activated, install the Kwasa CLI tool by running:

```bash
pip install kwasa-cli
# if you have uv
# ---
# uv add kwasa-cli --dev
```

### 3. Clone a Repository

After installing Kwasa CLI, you can start using it to clone repositories.

- **Clone the **[default repository](https://github.com/dlion4/django-quick-starter.git)** into the current empty directory**:

    ```bash
    kwasa clone .
    ```

- **Clone a repository into a specific directory**:
    `This will install the starter template into the directory specified`

    ```bash
    kwasa clone <directory>
    ```

- **Clone a different repository into a specific directory**:

    ```bash
    kwasa clone <directory> --repository <repository_url>
    ```

Replace `<directory>` with the target directory path and `<repository_url>` with the repository URL (e.g., `https://github.com/username/repository`).

### 4. Update the Repository

If you have previously cloned a repository and would like to update it to the latest changes, you can use the same command. Kwasa CLI will automatically pull the latest changes from the remote repository.

```bash
kwasa update
```

This will ensure the repository is up-to-date.

## Usage Examples

### Example 1: Clone the Django Starter Template

To clone the Django starter template into the current empty directory:

```bash
kwasa clone .
```

### Example 2: Clone into a Specific Directory

To clone the Django starter template into a directory called `my_django_project`:

```bash
kwasa clone my_django_project
```

### Example 3: Clone a Custom Repository

If you want to clone a repository from another URL (e.g., `https://github.com/another-user/some-repo`), use:

```bash
kwasa clone my_custom_repo --repo https://github.com/dlion4/django-quick-starter.git
```

## Development

If you'd like to contribute or modify the tool, you can clone this repository and install it locally:

1. Clone the repository:

    ```bash
    git clone https://github.com/dlion4/kwasa-cli.git
    cd kwasa-cli
    ```

2. Install the development dependencies:

    ```bash
    pip install -e .[dev]
    ```

3. Run tests and ensure everything works:

    ```bash
    pytest
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues or submit pull requests with enhancements or fixes. Contributions are welcome!

## Contact

For any issues or suggestions, feel free to open an issue on the GitHub repository: [Kwasa CLI GitHub](https://github.com/dlion4/kwasa-cli)

---

Enjoy using Kwasa CLI! 😊
