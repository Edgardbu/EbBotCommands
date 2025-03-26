# 📦 EbBotCommands

A growing collection of official, optional, plug-and-play command packages for the [EbBot](https://github.com/Edgardbu/EbBot) framework a powerful, modular, and web-integrated Discord bot.

These packages expand EbBot’s capabilities with features like games, embed management, tickets, welcome systems, auto-embeds, and more. All packages are fully configurable and support multi-language localization.

---

## 📂 What's Inside?

This repository is structured as a central hub for community and official packages. Some of the currently available command packs:

| Package         | Description                                        |
| --------------- | -------------------------------------------------- |
| Embed Manager   | Powerful custom embed builder & manager.           |
| AutoEmbeds      | Automatically send embeds in channels.             |
| TicketSystem    | Full-featured ticket system with UI.               |
| Welcome         | Custom welcome messages with triggers.             |
| Games           | Fun interactive games like TicTacToe, Minesweeper. |
| Fivem           | Fivem integration: IP, player list, RCON, more.    |
| Giveaway (beta) | Host automated giveaways (experimental).           |

Each package lives in its own folder, containing:

- Command Python file(s)
- Optional requirements.txt for dependencies
- Optional Configs in YAML format
- lang/ folder with translations (.json)

---

## 🧰 Installation Guide

All EbBot commands are optional. You install only what you want.

1. Visit: [https://github.com/Edgardbu/EbBotCommands](https://github.com/Edgardbu/EbBotCommands)
2. Pick the command pack folder you want (e.g. Embed Manager).
3. Copy the full GitHub folder link (example: [https://github.com/Edgardbu/EbBotCommands/tree/main/Embed%20Manager](https://github.com/Edgardbu/EbBotCommands/tree/main/Embed%20Manager)).
4. Go to: [https://download-directory.github.io](https://download-directory.github.io)
5. Paste the GitHub folder URL, click "Download".
6. Extract the downloaded .zip into your bot's `Bot/` directory.
   - Ensure files go into:
     - `Bot/Commands/`
     - `Bot/Configs/` (if config exists)
7. Restart the bot — and the package will auto-load 🎉

📌 Note: Some packages may install their own Python requirements.

---

## 🚫 Uninstalling a Package

1. Go to your bot’s `Bot/Commands` and `Bot/Configs` folders.
2. Delete the corresponding folder(s) for the package.
3. Restart the bot.

That's it!

---

## 🔐 Warning About Third-Party Packages

EbBotCommands is the official repository for safe, trusted packages.

If you install packages from unknown sources, you do so at your own risk.

🚨 They may contain malicious code or system-infecting payloads.

- Always review code before installation.
- If a third-party package is found malicious, format your system as a precaution.

---

## 🌐 Language Support

Each package supports translations with editable `.json` files under its `lang/` directory.

EbBot lets you edit languages directly via its web interface. You can:

- Modify strings in real-time
- Add new languages
- Duplicate templates

---

## 🧠 Custom Packages

Want to create your own package?

- Follow the folder structure in this repo.
- Include:
  - `yourcommand.py`
  - optional `requirements.txt`
  - optional config YAML
  - `lang/` folder (translations)

The `init(tree, bot, config, lang, db)` entry point will be auto-loaded by the EbBot system. You can also register lifecycle callbacks and slash commands dynamically.

---

## 📌 Requirements

- [EbBot Core](https://github.com/Edgardbu/EbBot) installed and configured
- Python 3.13+
- Running Flask-based web UI for management (comes with EbBot)

---

## 🤝 Contributions

Want to share your own command pack with the world?

- Create a well-structured folder
- Open a PR to this repository
- Or post it on your GitHub and share in our community Discord

Let’s build the ecosystem together!

---

## 📨 Support & Community

Got issues or want to suggest a feature?

Join our official Discord: [Discord Server](https://discord.gg/gRxfAQTtkP)
🇮🇱 Hebrew support available\
🌍 English section also available

