# pyrsgis Documentation

This folder contains the documentation source for the pyrsgis Python package.

## Local Build Instructions

To build the documentation locally:

1. **From the project root**, activate your environment and navigate to this folder:
    ```bash
    cd docs
    ```

2. **Run the build script** to generate clean HTML docs:
    ```bash
    ./builddocs.sh
    ```

    This script:
    - Runs `sphinx-apidoc` to generate API reference files
    - Deletes summary `.rst` files that cause duplicate warnings
    - Builds the HTML documentation

3. **Open the docs**:
    - Open `_build/html/index.html` in your browser

## Troubleshooting

- If you see duplicate warnings, ensure you always use `./builddocs.sh` (not `make html` directly).
- If the script fails with permissions, run `chmod +x builddocs.sh`.

## Dependencies

- All dependencies should be listed in `rtd_env.yml`
- For doc theme customization, see `conf.py`

## Publishing

- To deploy on ReadTheDocs, just push to the repository—RTD uses the same steps.
- For other questions, check the main project `README.md`.
