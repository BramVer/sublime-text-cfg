# Sublime Text Config
It's a plugin meant to automatically set Sublime Text up the way I want.  
This means custom keybindings, settings, macros, packages I use etc.  

Figured it was easier to just install and maintain 1 package :)

## Usage
We're exposing the following Commands for use in the Command Palette:
```json
[
    { "caption": "Set Me Up: Keymap", "command": "overwrite_keymaps" },
    { "caption": "Set Me Up: Settings", "command": "overwrite_settings" },
    { "caption": "Set Me Up: Macros", "command": "install_custom_macros" },
    { "caption": "Set Me Up: Packages", "command": "install_custom_packages" },
    { "caption": "Set Me Up: Zsh", "command": "setup_zsh_functions" }
]
```

These can also be called directly in the terminal via `sublime.run_command("overwrite_keymaps")`.

### 1. OverwriteKeymap
Based on the file at `data/keybindings.json` we overwrite everything at `Packages/User/Default.sublime-keymap`

### 2. Overwrite Settings
Based on the file at `data/settings.json` we set everything in the `sublime.load_settings("Preferences.sublime-settings")` for its configured value.

### 3. Install Custom Macros
Based on the file at `data/macros.json` where the key is the name of the macro file and the value is the content of the actual macro,  
we create the files at `Packages/User/` if they don't yet exist.

### 4. Install Custom Packages
This was a difficult one, since Package Control exposes a `advanced_install_packages` that accepts `{"packages": "Pkg1,Pkg2,Pkg3"}` according to every online resource I could find.  
Which works if called through the cli like `subl --command "advanced_install_package {\"packages\": \"LSP,LSP-pyright\"}"`.  
Through `sublime.run_command` however it would not do anything.

So when all else fails, manipulate `Packages/User/Package Control.sublime-settings` file, specifically the `"installed packages"` section and overwrite it with the packages defined in `data/packages.json`.  
This usually requires a restart for Sublime Text to notice the changes and automatically download them itself.  

### 5. Setup ZSH Functions
Because I have custom behaviour running on the `on_post_save_user` hook that depends on `~/.zsh_functions`, I wanted to ensure this file gets created as well when I want to.  