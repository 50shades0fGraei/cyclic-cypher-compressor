# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }:
let
  # Create a Python environment with Flask available.
  # This is the idiomatic Nix way to handle Python dependencies.
  pythonWithFlask = pkgs.python311.withPackages (ps: [
    ps.flask
  ]);
in
{
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    # This places the Python interpreter (with Flask) onto the PATH.
    pythonWithFlask,
    pkgs.ffmpeg
  ];

  # Sets environment variables in the workspace
  env = {
    # Add the project root to the Python path to allow imports of local modules.
    PYTHONPATH = ".";
    # Set the Flask app to be the 'app' object in the 'backend.py' file
    FLASK_APP = "backend";
  };

  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "google.gemini-cli-vscode-ide-companion"
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
        web = {
          # This command now uses the Python interpreter defined in 'packages' above,
          # which has Flask installed.
          command = ["flask" "run" "--port" "$PORT" "--host" "0.0.0.0"];
          manager = "web";
        };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        default.openFiles = [ ".idx/dev.nix" "README.md" "backend.py" "web/index.html" ];
      };
      # Runs when the workspace is (re)started
      onStart = {};
    };
  };
}
