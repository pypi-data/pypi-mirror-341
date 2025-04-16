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
    for file in os.listdir(".templates"):
        shutil.copy(f".template/{file}", f"project/{project_name}/") # copy the template in first

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
@click.option("version", help="Version of the Docker image to build. Enter latest or leave blank for the latest build.")
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