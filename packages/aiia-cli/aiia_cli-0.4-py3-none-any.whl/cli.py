import click, json, os, subprocess, shutil
from datetime import datetime
import pytz # timezones

@click.group()
def cli():
    pass

@cli.command()
@click.argument("project_name")
@click.option("--port", default="8000:8000", help="Main container port (default: 8000:8000)")
@click.option("--env", multiple=True, help="Environment variables (e.g., `API_KEY=123`)")
def new(project_name, port, env):
    """Create new project folder."""
    # 1. Copy template
    project_name = project_name.lower().replace(" ", "-")
    os.makedirs(f"projects/{project_name}")
    for file in os.listdir("projects/.template"):
        shutil.copy(f"projects/.template/{file}", f"project/{project_name}/") # copy the template in first

    # 2. Pre-fill manifest.json
    try:
        manifest = {
            "name": project_name,
            "authors": [],  # User fills later
            "created": datetime.now(pytz.timezone('Asia/Shanghai')).isoformat(),
            "ports": {"default": port},  # User-defined or default 8000
            "env_vars": dict(e.split("=") for e in env),  # Convert --env flags to dict
            "tags": []
        }
    except Exception as e:
        click.echo(f"Error creating manifest.json: {e}. Report to an admin.")
        return
    with open(f"projects/{project_name}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    # 3. This is nice for reminding people.
    click.echo(f"Project {project_name} created with port {port} and default environment variables: {env}. \nFill the README.md file as directed.")

@cli.command()
@click.argument("project_name")
@click.option("--port", default="8000:8000", help="Main container port (default: 8000:8000)")
@click.option("--env", multiple=True, help="Environment variables (e.g., `API_KEY=123`)")
def format(project_name, port, env):
    """Format a folder to fit project folder requirements."""
    project_name = project_name.lower().replace(" ", "-")

    if not os.path.exists(f"projects/{project_name}"):
        click.echo(f"Project {project_name} not found. Please create it first.")
        return

    # 1. Copy template
    for item in os.listdir("projects/.template"):
        source_item_path = f"projects/.template/{item}"
        target_item_path = f"projects/{project_name}/{item}"
        if os.path.isdir(source_item_path):
            # Handle directories
            if os.path.exists(target_item_path):
                click.echo(f"Skipping existing directory: '{target_item_path}'")
            else:
                # Create the directory in the target location
                os.makedirs(target_item_path)
                click.echo(f"Copied empty directory: '{source_item_path}' to '{target_item_path}'")
        elif os.path.isfile(source_item_path):
            if os.path.exists(target_item_path):
                if item.endswith('.md'):
                    user_input = click.prompt(
                        f"The file '{target_item_path}' already exists. Do you want to merge it with the new content? (y/n)",
                        type=click.Choice(['y', 'n'], case_sensitive=False),
                        default='n'
                    )
                    if user_input.lower() == 'y':
                        # Merge the content of both files
                        with open(source_item_path, 'r') as source_file:
                            source_content = source_file.read()
                        with open(target_item_path, 'r') as target_file:
                            target_content = target_file.read()
                        # Combine the contents
                        combined_content = source_content + "\n" + target_content
                        # Write the merged content back to the target file
                        with open(target_item_path, 'w') as target_file:
                            target_file.write(combined_content)
                        click.echo(f"Merged '{source_item_path}' into '{target_item_path}'")
                    else:
                        click.echo(f"Skipping file: '{target_item_path}'")
                        continue  # Skip to the next item
                else:
                    user_input = click.prompt(
                        f"The file '{target_item_path}' already exists. Do you want to overwrite it? (y/n)",
                        type=click.Choice(['y', 'n'], case_sensitive=False),
                        default='n'
                    )
                    if user_input.lower() == 'y':
                        # Make a backup of the existing file
                        backup_file_path = f"{target_item_path}.bak"
                        shutil.copy(target_item_path, backup_file_path)
                        click.echo(f"Backup created: '{backup_file_path}'")
                    else:
                        click.echo(f"Skipping file: '{target_item_path}'")
                        continue  # Skip to the next item
                    # Copy the file from the template directory to the project directory
                    shutil.copy(source_item_path, target_item_path)
                    click.echo(f"Copied '{source_item_path}' to '{target_item_path}'")

    # 2. Pre-fill manifest.json
    manifest = {
        "name": project_name,
        "authors": [],  # User fills later
        "created": datetime.now(pytz.timezone('Asia/Shanghai')).isoformat(),
        "ports": {"default": port},  # User-defined or default 8000
        "env_vars": dict(e.split("=") for e in env),  # Convert --env flags to dict
        "tags": []
    }
    with open(f"projects/{project_name}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    # 3. This is nice for reminding people.
    click.echo(f"\nProject {project_name} formatized with port {port} and default environment variables: {env}. \nFill the README.md file as directed.")

@cli.command()
@click.argument("message")
def submit(message):
    """Submit changes to Git repository."""
    # Run Git commands
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push"])

@cli.command()
@click.argument("project_name")
def build(build_name):
    """Build Docker image called build_name from Dockerfile."""
    subprocess.run(["docker", "build", "-t", build_name, "."])


@cli.command()
def login():
    """Authenticate with GHCR using PAT"""
    token = click.prompt("GitHub PAT", hide_input=True)
    subprocess.run(f"echo {token} | docker login ghcr.io -u USERNAME --password-stdin", shell=True)

@cli.command()
@click.option("--version", help="Version of the Docker image to build. Enter latest or leave blank for the latest build.")
@click.option("--port", help="Override default port when running")
@click.option("--env", multiple=True, help="Environment variables (e.g., `API_KEY=123`)")
def run(version, port, env):
    """Run the Docker container with optional port override."""
    # Read manifest.json
    with open("manifest.json") as f:
        manifest = json.load(f)

    if manifest["image"] == "":
        click.echo("No image found. Please build the image first.")
        return
    
    if not version or version == "latest": # if version not specified 
        build_name = manifest["image"] # use the image name in manifest.json
    else:
        build_name = f"{manifest['image'].split(":")[0]}:{version}" # use the version in manifest.json
    # Use CLI --port or fall back to manifest
    port = port or manifest["ports"]["default"]
    if not env: # if no CLI --env, use manifest
        env_dict = manifest["env_vars"]
        env = []
        for key, value in env_dict.items():
            env.append(f"{key}={value}") # a list of key=value strings

    subprocess.run(["docker", "run", "-p", f"{port}:{port}"] + env + [build_name])

@cli.command()
@click.option("--version", default="latest")
def deploy(version):
    """Build and push Docker image to GHCR."""
    # Read metadata
    try:
        with open("manifest.json") as f:
            manifest = json.load(f)
    except FileNotFoundError:
        click.echo("manifest.json not found. Please create it first.")
        return
    
    # Generate ghcr url
    org = "sjtu-aiia"
    image_name = manifest["name"].lower().replace(" ", "-")
    ghcr_url = f"ghcr.io/{org}/{image_name}:{version}"
    
    # Build/push
    build(ghcr_url)
    subprocess.run(["docker", "push", ghcr_url]) # push to ghcr
    
    # Update manifest
    manifest["image"] = ghcr_url
    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    click.echo(f"Pushed to GHCR: {ghcr_url}")

if __name__ == "__main__":
    cli()