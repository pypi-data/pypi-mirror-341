import typer
import subprocess
from pathlib import Path
import json

app = typer.Typer(help="""
    Run a Quantum Machine locally using Python.

    Example:
        quantum run machine HelloWorld
    """
)

REQUIRED_KEYS = {"machine_name", "input_data", "output", "depends_machine"}

@app.command()
def machine(machine_name: str):
    """
    Run a Quantum Machine locally using Python.

    Example:
        quantum run machine HelloWorld
    """
    # ✅ Check for core engine only when running the machine
    try:
        from quantum.CoreEngine import CoreEngine  # Only needed when actually running the machine
    except ImportError:
        typer.secho("❌ Missing dependency: 'quantum-core-engine' is required. Please install it separately.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.echo(f"🚀 Starting Quantum Machine: {machine_name}")

    machine_path = Path(machine_name).resolve()

    main_script = machine_path / "main.py"
    if not main_script.exists():
        typer.secho("❌ main.py not found in machine directory.", fg=typer.colors.RED)
        raise typer.Exit(1)

    input_json_path = machine_path / "input.json"
    if not input_json_path.exists():
        typer.secho("❌ input.json file not found in the machine directory.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # ✅ Load and validate input.json structure
    try:
        with open(input_json_path) as f:
            input_data = json.load(f)
    except json.JSONDecodeError:
        typer.secho("❌ input.json is not valid JSON.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # ✅ Check for all required keys
    missing_keys = REQUIRED_KEYS - input_data.keys()
    if missing_keys:
        typer.secho(f"❌ input.json is missing required keys: {', '.join(missing_keys)}", fg=typer.colors.RED)
        raise typer.Exit(1)

    command = [
        "python",
        f"./{machine_name}/main.py",
        json.dumps(input_data)
    ]

    typer.echo(f"Running machine '{machine_name}' with env='dev'")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Stream logs line by line
    for line in process.stdout:
        print(line, end='')

    process.wait()

    if process.returncode == 0:
        typer.echo("✅ Machine executed successfully")
        typer.echo(process.stdout)
    else:
        typer.echo("❌ Machine execution failed", err=True)
        typer.echo(process.stderr, err=True)

    #"""Run a Quantum Machine using Docker"""
    # file_path = Path(file).resolve()
    # folder = file_path.parent

    # docker_cmd = [
    #     "docker", "run", "--rm",
    #     "-v", f"{folder}:/app",
    #     "quantumdatalytica/quantum-core:latest",
    #     "python", f"/app/{file_path.name}"
    # ]

    # try:
    #     subprocess.run(docker_cmd, check=True)
    # except subprocess.CalledProcessError as e:
    #     typer.secho(f"❌ Docker execution failed: {e}", fg=typer.colors.RED)