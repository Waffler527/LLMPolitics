{
  description = "Python dev env";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        python = pkgs.python312.withPackages (ps: with ps; [
          requests
        ]);
      in {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.python312Packages.virtualenv
          ];

          shellHook = ''
            if [ ! -d .venv ]; then
              python -m venv .venv
            fi
            . .venv/bin/activate
          '';
        };
      });
}