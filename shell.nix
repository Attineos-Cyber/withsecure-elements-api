{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [ pip virtualenv ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
  ];
  
  shellHook = ''
    # Créer un environnement virtuel Python
    export VENV_DIR=./.venv
    if [ ! -d "$VENV_DIR" ]; then
      ${pythonEnv}/bin/python -m venv $VENV_DIR
    fi
    source $VENV_DIR/bin/activate
    
    # Installer withsecure-elements-api depuis GitHub
    pip install .
    
    echo "Environnement prêt pour withsecure-elements-api !"
    echo "Vous pouvez maintenant importer la bibliothèque dans Python :"
    echo "from withsecure import Client"
    echo ""
    echo "Exemple d'utilisation :"
    echo "client = Client(client_id='your_client_id', secret_id='your_secret_id')"
    echo "client.authenticate()"
  '';
}
