{ pkgs, ... }: {
  channel = "stable-24.11";

  packages = [
    pkgs.nodejs_20

    (pkgs.python311.withPackages (ps: with ps; [
      pip
      fastapi
      uvicorn
      python-multipart
      google-generativeai
      google-cloud-speech
      google-cloud-spanner
    ]))
  ];

  env = {
    GEMINI_API_KEY = "PASTE_YOUR_REAL_GEMINI_KEY_HERE";
  };

  idx = {
    extensions = [
      "ms-python.python"
      "google.gemini-cli-vscode-ide-companion"
    ];
    previews = { enable = true; };
  };
}
