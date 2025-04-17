import click, json, os, subprocess, shutil
from datetime import datetime
import pytz # timezones
import semver

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

    if os.path.exists(f"projects/{project_name}") and os.listdir(f"projects/{project_name}") != []:
        click.echo(f"Project '{project_name}' already exists. Please choose a different name.")
        return
    
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
            # Handles files
            shutil.copy(source_item_path, target_item_path)
            click.echo(f"Copied '{source_item_path}' to '{target_item_path}'")

    # 2. Pre-fill manifest.json
    try:
        manifest = {
            "name": project_name,
            "authors": [],  # User fills later
            "created": datetime.now(pytz.timezone('Asia/Shanghai')).isoformat(),
            "ports": {"default": port},  # User-defined or default 8000
            "env_vars": dict(e.split("=") for e in env),  # Convert --env flags to dict
            "tags": [],
            "image": "",
            "version": "0.0.0"  # Initial version
        }
    except Exception as e:
        click.echo(f"Error creating manifest.json: {e}. Report to an admin.")
        return
    with open(f"projects/{project_name}/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    # 3. This is nice for reminding people.
    click.echo(f"""\nProject '{project_name}' successfully created!

Project location: projects/{project_name}
Default port: {port}
Environment variables: {env if env else "None set"}

Next steps:
1. Edit the README.md to describe your project
2. Add your code to the src/ directory
3. Fill in authors and tags in manifest.json
4. (Optional) Add tests to the tests/ directory

Use `proj-cli submit` when ready to contribute!""")

@cli.command()
@click.argument("repo_url")
@click.option("--port", default="8000:8000", help="Main container port (default: 8000:8000)")
@click.option("--env", multiple=True, help="Environment variables (e.g., `API_KEY=123`)")
@click.option("--branch", default="main", help="Git branch to clone (default: main)")
def import_repo(repo_url, port, env, branch):
    """Import an existing GitHub repository as a new project. The project name will be taken from the old repository."""
    try:
        # 1. Extract project name from URL
        repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        project_name = repo_name.lower().replace(" ", "-")
        project_path = f"projects/{project_name}"
        
        # 2. Clone the repository
        click.echo(f"Cloning {repo_url}...")
        subprocess.run(["git", "clone", "--branch", branch, "--depth", "1", repo_url, project_path], check=True)
        
        # 3. Remove .git directory to avoid nested repos
        shutil.rmtree(os.path.join(project_path, ".git"), ignore_errors=True)
        
        # 4. Create manifest.json
        manifest = {
            "name": project_name,
            "source_repo": repo_url,
            "authors": [],  # Can be populated later
            "created": datetime.now(pytz.timezone('Asia/Shanghai')).isoformat(),
            "last_imported": datetime.now(pytz.timezone('Asia/Shanghai')).isoformat(),
            "ports": {"default": port},
            "env_vars": dict(e.split("=") for e in env),
            "tags": [],
            "image": "",
            "version": "0.0.0"  # Initial version
        }
        
        # 5. Write manifest
        with open(f"{project_path}/manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
            
        click.echo(f"""\nSuccessfully imported {repo_name}!
- Project path: {project_path}
- Default port: {port}
- Remember to:
  1. Fill in authors in manifest.json
  2. Add relevant tags
  3. Update README.md if needed""")
    
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to clone repository: {e}\nMake sure:")
        click.echo("- The URL is correct (e.g., https://github.com/user/repo)")
        click.echo("- You have git installed")
        click.echo("- The repository exists and is public")
    except Exception as e:
        click.echo(f"Error during import: {e}\nPlease report this to an admin.")
        # Clean up partially imported project
        if os.path.exists(project_path):
            shutil.rmtree(project_path)

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
        "tags": [],
        "image": "",
        "version": "0.0.0"  # Initial version
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

# utility function
def build(build_name):
    """(DEPRECATED) Build Docker image called build_name from Dockerfile."""
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
@click.option("--bump", type=click.Choice(["major", "minor", "patch"]), default="patch")
def deploy(bump):
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
    current_version = manifest["version"]
    new_version = semver.bump_<bump>(current_version)
    ghcr_url = f"ghcr.io/{org}/{image_name}:{new_version}"

    if not os.path.isfile("Dockerfile"):
        click.echo("Dockerfile not found. Please create it first.")
        return
        
    # Build/push
    try:
        build(ghcr_url)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error building Docker image: {e}")
        return
    subprocess.run(["docker", "push", ghcr_url]) # push to ghcr
    
    # Update manifest
    manifest["image"] = ghcr_url
    manifest["version"] = new_version
    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    click.echo(f"\nPushed to GHCR: {ghcr_url}")

if __name__ == "__main__":
    cli()