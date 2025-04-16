# shell.nix
let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2025-03-05. Check for new commits at https://status.nixos.org.
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/6af28b834daca767a7ef99f8a7defa957d0ade6f.tar.gz") {};
in pkgs.mkShell {
  packages = [
    pkgs.pre-commit
    (pkgs.python311.withPackages (python-pkgs: [
      # select Python packages here
      python-pkgs.build
      python-pkgs.hatchling
      python-pkgs.pip
      python-pkgs.setuptools
      python-pkgs.typer
      python-pkgs.twine
      python-pkgs.wheel
    ]))
  ];
}
