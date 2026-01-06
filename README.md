# Open WebUI Desktop 🌐

![App Demo](./demo.png)

**Open WebUI Desktop** is a cross-platform desktop application for [Open WebUI](https://github.com/open-webui/open-webui). It brings the _full-featured Open WebUI experience_ directly to your device, effectively transforming it into a powerful server—without the complexities of manual setup.

> [!WARNING]
> This project is currently in **alpha** and under active development. 🛠️ Expect frequent updates and potential changes as we refine the application.

## Download 📥

> [!NOTE]
> An internet connection is required for initial setup, but afterwards the application can be used completely offline.

Get the latest alpha release from our [releases page](https://github.com/open-webui/desktop/releases).

## Features

- **One-Click Installation**: Quickly and effortlessly install and set up Open WebUI with all its dependencies. This feature is fully functional and ready to make your setup a breeze.
- **Cross-Platform Support**: Compatible with Windows, macOS, and Linux to ensure broad accessibility.
- **Offline Capability**: After initial setup, use the application completely offline for enhanced privacy and reliability.

## Project Setup

### Install

```bash
npm install
```

### Development

```bash
npm run dev
```

### Build

```bash
# For windows
npm run build:win
# For macOS
npm run build:mac
# For Linux
npm run build:linux
```

## Terminal Campfire 🔥

If you want a local-friendly game-like REPL to hack on Python together, use the
`scripts/python_campfire.py` helper. It keeps a shared execution context, lets
players join or swap turns, and can load whole Python files into the session.

```bash
python3 scripts/python_campfire.py --session "Lan Party"
```

Useful commands inside the prompt:

- `/join <name>` – add a player and set them as active when they are the first to join
- `/switch <name>` – move the prompt to another player
- `/load <path>` – run a Python script file into the shared context
- `/history` – review recent snippets
- `/save <path>` – export the history log
- `/reset` – clear state while keeping the roster

## License 📜

This project is licensed under the **Open WebUI Sustainable Use License**. For details, see [LICENSE](LICENSE).

## Stay Tuned! 🌟

We're actively developing Open WebUI. Follow [Open WebUI](https://github.com/open-webui/open-webui) for updates, and join the [community on Discord](https://discord.gg/5rJgQTnV4s) to stay involved.