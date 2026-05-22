# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.11"; 
  
  # 1. Tier 1 Tooling Fortification: Declarative Binary Implementations
  packages = [
    pkgs.python311Full
    pkgs.python311Packages.pip
    pkgs.nodejs_22
    pkgs.ripgrep
    pkgs.mdbook
  ];
  
  # Sets environment variables in the workspace
  env = {};
  
  idx = {
    # 2. Augment IDE Capabilities: Mount Code-Quality Extensions
    extensions = [
      "google.gemini-cli-vscode-ide-companion"
      "dbaeumer.vscode-eslint"
      "esbenp.prettier-vscode"
      "vscode-icons-team.vscode-icons"
    ];
    
    # 3. Configure Automated Previews and Runtime Dev Servers
    previews = {
      enable = true;
      previews = {
        web = {
          command = ["npm" "run" "dev" "--prefix" "aether-forge-app" "--" "-p" "$PORT"];
          manager = "web";
          env = {
            PORT = "$PORT";
          };
        };
      };
    };
    
    # 4. Lifecycle Management Hooks: Automated Dependency Ingestion
    workspace = {
      onCreate = {
        setup-and-format = "cd aether-forge-app && npm install";
      };
      onStart = {};
    };
  };
}