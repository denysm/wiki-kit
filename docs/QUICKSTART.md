# Quickstart: your own knowledge wiki in about 30 minutes

[Русская версия](QUICKSTART.ru.md) · [Українська версія](QUICKSTART.uk.md)

You will get a private wiki on your own computer. You give it chats, notes, documents and links; an AI assistant (Claude) turns them into short articles with a source for every claim, and answers your questions from them. A set of "specialists" (a coach, help with decisions, documents, preparing for a doctor's visit, and more) works on top of it. Your data stays on your computer.

## What you need

- A Mac, a Linux computer, or Windows 10 or 11 (on Windows follow the [Windows section](#windows-10-or-11) instead of steps 2-5).
- Internet access.
- A paid Claude plan (Pro or higher) or an Anthropic API key. Installing everything is free; using the AI is not.
- A GitHub account (free) is recommended. You do not need it to install or use the kit, but you need it to send your improvements back: [Share your improvements](#share-your-improvements).

## Step 1. Install VS Code

VS Code is a free editor: you will read your wiki and talk to Claude in it.

1. Go to <https://code.visualstudio.com>, download, install, open it.
2. Left bar, square icon **Extensions** (or `Cmd+Shift+X` on a Mac, `Ctrl+Shift+X` on Linux). Search for **Claude Code**, publisher **Anthropic**, click **Install**.

## Step 2. Open the Terminal

The Terminal is a window where you paste commands. Paste a command, press Enter, wait until the cursor comes back.

- Mac: press `Cmd+Space`, type `Terminal`, press Enter.
- Linux: press `Ctrl+Alt+T`.

If a Mac asks to install "command line developer tools", click **Install** and wait; it is normal.

## Step 3. Install Claude Code and sign in

```sh
curl -fsSL https://claude.ai/install.sh | bash
```

Then type `claude` and press Enter. It opens a browser to sign in with your Claude account (or asks for an API key). After you are signed in, type `/exit` to leave.

## Step 4. Get the kit

```sh
git clone ADDRESS ~/Projects/wiki-kit
```

Replace `ADDRESS` with the kit's address: on the kit's GitHub page press the green **Code** button and copy the HTTPS address (it ends in `.git`). The kit is public: no GitHub account is needed to download it.

## Step 5. Run the installer

```sh
bash ~/Projects/wiki-kit/bootstrap.sh
```

It installs the wiki plugin, creates your wiki in the folder `~/wiki`, adds the specialists and checks itself. The last lines say how it went:

```
Done: 15 ok, 0 note(s), 0 failure(s). Hub: /Users/you/wiki
```

`0 failure(s)` means everything is ready. Each `FAIL` or `note` line says what to do; do it and run the same command again (running it twice is safe). Options: `--lang ru` for Russian rules and chat, `--hub ~/Documents/wiki` for another folder.

## Windows 10 or 11

Step 1 is the same. Instead of steps 2-5:

1. **Open PowerShell**: Start menu, type `PowerShell`, press Enter (a normal window, not "as administrator").
2. **Install Git**, then close PowerShell and open it again:

   ```powershell
   winget install --id Git.Git -e
   ```
   If `winget` is not recognised, download Git from <https://git-scm.com/download/win> and install it with the default answers.
3. **Get the kit.** Replace `ADDRESS` as in step 4.

   ```powershell
   git clone ADDRESS $HOME\Projects\wiki-kit
   ```
4. **Run the installer** (Windows blocks downloaded scripts by default; this command allows this one run):

   ```powershell
   powershell -ExecutionPolicy Bypass -File $HOME\Projects\wiki-kit\bootstrap.ps1
   ```
   It asks before installing Python and Claude Code: press Enter to agree. If it ends with a `note` about Claude Code, close PowerShell, open it again and run the same command once more.
5. **Sign in to Claude**: type `claude`, sign in in the browser, then `/exit`.

Then continue with step 6. Your wiki is the folder `wiki` in your user folder (`C:\Users\<you>\wiki`); use `Ctrl` where the text says `Cmd`.

The Windows installer is new: if any line says `FAIL`, send the log file it names on its last line (`%TEMP%\wiki-kit-bootstrap.log`) to the person who sent you the kit. The kit's PDF and Word converters use macOS tools and do not work on Windows yet.

## Step 6. Start working

1. In VS Code: **File → Open Folder…**, choose the `wiki` folder in your home folder.
2. Open Claude: the Claude icon in the top right corner of the editor, or `Cmd+Esc` / `Ctrl+Esc`.
3. Create your first topic (a topic is one area of life: personal, career, health, a hobby):

   ```
   /wiki init personal
   ```
4. Give it something to read. A link, a file, or plain text:

   ```
   /wiki:ingest https://example.com/an-article-i-liked
   /wiki:ingest ~/Downloads/notes.pdf
   ```
5. Turn the sources into articles, then ask questions:

   ```
   /wiki:compile
   /wiki:query what did I decide about the move?
   ```
6. Specialists. Ask Claude in plain words: "enable the specialists for the topic personal". After that, phrases like "coach", "help me decide", "prepare me for the doctor" or "check these facts" pick the right one in any folder. On the first conversation it asks which language you prefer.

You can always just write what you want in plain words; Claude picks the right command.

## Good habits

- **One task per conversation.** Long conversations cost more. When a task is done, start a new one (the `+` button in the Claude panel).
- **Get updates** once a week: `cd ~/Projects/wiki-kit && git pull`. The specialists in your wiki update by themselves.
- **Secrets** (passwords, keys, bank details) do not belong in a wiki. Claude replaces them with `[REDACTED:secret]` when it notices them.
- **The kit holds no data.** Your wiki is separate from the kit and has no copy on the internet.
- **Draft specialists.** Every specialist except the coach is a draft (version 0.x) and says so. The health, money, paperwork and emotional-support specialists help you prepare; they do not replace a doctor, adviser, lawyer or therapist.

## Share your improvements

The kit grows from its users' experience: a step that was unclear, a script that failed, a phrase a specialist did not understand, a lesson it should learn. Your changes come back as a *pull request*: a proposal that the kit's maintainer reviews and then adds to the kit. Only the change itself travels; your wiki never leaves your computer.

**Once:**

1. Create a free account at <https://github.com/signup>. Then open <https://github.com/settings/emails>, turn on **Keep my email addresses private**, and copy the address on that page that ends in `@users.noreply.github.com`.
2. Install the GitHub command line tool from <https://cli.github.com> (Windows: `winget install --id GitHub.cli -e`; Mac with Homebrew: `brew install gh`) and sign in: `gh auth login`, then choose GitHub.com, HTTPS and "Login with a web browser".
3. Tell git who you are, for the kit folder only (the address from step 1 keeps your real email private; a nickname is fine instead of a name):

   ```sh
   cd ~/Projects/wiki-kit
   git config user.name "Your Name"
   git config user.email "ID+USERNAME@users.noreply.github.com"
   ```
4. List the names that must never leave your computer (family, employer, clients) in `~/.config/wiki-kit/private-names.txt`, one per line. The installer turned on a check that refuses to send anything matching them or anything that looks like a password or key.

**Each change:**

1. In VS Code open the folder `~/Projects/wiki-kit` and tell Claude what should work differently.
2. When you are happy with it, ask Claude: "send my changes to the kit as a pull request". It makes your own copy of the kit on GitHub (a *fork*), puts the change on a separate branch and opens the pull request. By hand:

   ```sh
   cd ~/Projects/wiki-kit
   gh repo fork --remote            # once: your copy on GitHub; the original kit becomes "upstream"
   git switch -c short-change-name
   git add -A
   git commit -m "What changed and why"
   git push -u origin HEAD          # the leak check runs here
   gh pr create --fill              # if asked where to send it, choose the original kit, not your copy
   ```
3. The maintainer may ask questions in the pull request, then merges it. After that, go back to the main version and update: `git switch main`, then `git pull`.

Write in any language: English, Ukrainian or Russian. Lessons for specialists have their own rules (no personal details, plus an example case): [specialists/README.md](../specialists/README.md#from-personal-lesson-to-shared-principle). Everything else: [CONTRIBUTING.md](../CONTRIBUTING.md).

## If something goes wrong

| What you see | What to do |
|---|---|
| `git is missing` or `python3 is missing` | Mac: run `xcode-select --install`, wait, run the installer again. Linux: install the `git` and `python3` packages. |
| `Claude Code command line not found` | Do step 3, close and reopen the Terminal, run the installer again. |
| `git clone` asks for a password or says "not found" | The address has a typo: copy it again from the green **Code** button (step 4). |
| `plugin install failed` | Run `claude plugin install wiki@llm-wiki` and read the message. Usually it is the internet connection. |
| `/wiki` is not recognised in VS Code | Close VS Code completely and open it again. |
| Windows: "running scripts is disabled on this system" | Start the installer with the full command from the Windows section (`powershell -ExecutionPolicy Bypass -File ...`). |
| Windows: `winget` is not recognised | Install Git from <https://git-scm.com/download/win> and Python from <https://www.python.org/downloads/> (tick **Add python.exe to PATH**), then run the installer again. |
| Anything else | Copy the lines with `FAIL` and send them to the person who sent you the kit. |
