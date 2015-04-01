{ nixpkgs ? import <nixpkgs> {} }:
with nixpkgs;
let
  pyjwt = buildPythonPackage rec {
    version = "0.3.2";
    name = "pyjwt-${version}";

    src = pkgs.fetchurl {
      url = "http://github.com/progrium/pyjwt/archive/${version}.tar.gz";
      sha256 = "118rzhpyvx1h4hslms4fdizyv6mnyd4g34fv089lvs116pj08k9c";
    };

    propagatedBuildInputs = with self; [ pycrypto ecdsa ];

    meta = with stdenv.lib; {
      description = "JSON Web Token implementation in Python";
      longDescription = "A Python implementation of JSON Web Token draft 01.";
      homepage = https://github.com/progrium/pyjwt;
      downloadPage = https://github.com/progrium/pyjwt/releases;
      license = licenses.mit;
      maintainers = with maintainers; [ prikhi ];
      platforms = platforms.linux;
    };
  };

in
pkgs.buildPythonPackage {
  name = "waw-login";
  srcs = ./.;
  propagatedBuildInputs = [
    pythonPackages.flask
    pythonPackages.bcrypt
    pythonPackages.cffi
    pyjwt
  ];
}
