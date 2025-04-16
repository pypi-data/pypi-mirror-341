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
    # 1. Copy template
    os.makedirs(f"projects/{project_name}")
    for file in os.listdir(".templates"):
        shutil.copy(f".template/{file}", f"project/{project_name}/") # copy the template in first

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
    click.echo(f"Project {project_name} created with port {port} and default environment variables: {env}")

@cli.command()
@click.argument("message")
def submit(message):
    # Run Git commands
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push"])

@cli.command()
@click.argument("project_name")
def build(project_name):
    """Build Docker image called project_name from Dockerfile."""
    subprocess.run(["docker", "build", "-t", project_name, "."])

@cli.command()
@click.argument("project_name")
@click.option("--port", help="Override default port when running")
@click.option("--env", multiple=True, help="Environment variables (e.g., `API_KEY=123`)")
def run(project_name, port, env):
    """Run the Docker container with optional port override."""
    # Read manifest.json
    with open("manifest.json") as f:
        manifest = json.load(f)

    # Use CLI --port or fall back to manifest
    port = port or manifest["ports"]["default"]
    if not env: # if no CLI --env, use manifest
        env_dict = manifest["env_vars"]
        env = []
        for key, value in env_dict.items():
            env.append(f"{key}={value}") # a list of key=value strings

    subprocess.run(["docker", "run", "-p", f"{port}:{port}", env.join(" "), project_name])

if __name__ == "__main__":
    cli()