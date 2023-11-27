import re
import json
from pathlib import Path

import sublime
import sublime_plugin


def plugin_loaded(*args, **kwargs):
    sublime.status_message(
        "🐍🤖 Configuration Plugin loaded, use 'Set Me Up' to get started 🐍🤖"
    )


def _clean_trailing_commas(text):
    text = re.sub(",[ \t\r\n]+}", "}", text)
    return re.sub(",[ \t\r\n]+\]", "]", text)


class OverwriteSettingsCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        print("-- Overwriting Default Sublime Text Settings --")
        settings = sublime.load_settings("Preferences.sublime-settings")

        resource = "Packages/sublime-text-cfg/data/settings.json"
        print(f"Loading {resource} as json")
        try:
            custom_settings = json.loads(sublime.load_resource(resource))
        except Exception as e:
            print(f"Could not load the file as a json file!\n{e}")
            sublime.message_dialog(
                f"Could not load {resource} as file, aborting."
            )
            return

        for name, value in custom_settings.items():
            if settings.has(name):
                print(f"Setting {name} as {value}")
                settings.set(name, value)

        sublime.save_settings("Preferences.sublime-settings")


class OverwriteKeymapsCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        print("-- Overwriting Default Sublime Text Keymap --")

        resource = "Packages/sublime-text-cfg/data/keybindings.json"
        print(f"Loading {resource} as json")
        try:
            custom_keymap = sublime.load_resource(resource)
        except Exception as e:
            print(f"Could not load the file!\n{e}")
            sublime.message_dialog(
                f"Could not load {resource} as file, aborting."
            )
            return

        new_path = (
            Path(sublime.packages_path()) / "User" / "Default.sublime-keymap"
        )
        new_path.write_text(custom_keymap)


class SetupZshFunctionsCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        print("-- Setting up your ZSH functions --")

        resource = "Packages/sublime-text-cfg/data/zsh_functions"
        print(f"Loading {resource}")
        try:
            zsh_functions = sublime.load_resource(resource)
        except Exception as e:
            print(f"Could not load the file!\n{e}")
            sublime.message_dialog(f"Could not load {resource}, aborting!")
            return

        new_path = Path.home() / ".zsh_functions"
        if new_path.exists():
            sublime.message_dialog(f"{new_path} already exists, aborting.")
            return

        new_path.write_text(zsh_functions)


class InstallCustomMacrosCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        print("-- Sets up your custom macros if they do not yet exist --")

        resource = "Packages/sublime-text-cfg/data/macros.json"
        print(f"Loading {resource}")
        try:
            content = _clean_trailing_commas(sublime.load_resource(resource))
            macros = json.loads(content)
        except Exception as e:
            print(f"Could not load the file!\n{e}")
            sublime.message_dialog(f"Could not load {resource}, aborting!")
            return

        for name, content in macros.items():
            fpath = Path(sublime.packages_path()) / "User" / name
            if fpath.exists():
                print(f"{fpath} already exists, skipping!")
                continue

            print(f"Creating macro {name} at {fpath}")
            fpath.write_text(json.dumps(content, indent=4))


class InstallCustomPackagesCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        print("-- Installing your custom packages in order --")

        pkgs_fpath = "Packages/sublime-text-cfg/data/packages.json"
        pkg_ctrl_fpath = "Packages/User/Package Control.sublime-settings"
        print(f"Loading {pkgs_fpath} and {pkg_ctrl_fpath}")

        try:
            pkgs_text = sublime.load_resource(pkgs_fpath)
            pkg_ctrl_text = sublime.load_resource(pkg_ctrl_fpath)
        except Exception as e:
            print(f"Could not load the file\n{e}")

        try:
            packages = json.loads(_clean_trailing_commas(pkgs_text))
            pkg_ctrl = json.loads(_clean_trailing_commas(pkg_ctrl_text))
        except Exception as e:
            print(f"Could not load the content as valid JSON!\n{e}")
            msg = (
                "Something went wrong loading your packages.json and/or your "
                "User/Package Control.sublime-settings file as JSON.\n"
                "Ensure they're valid JSON with no trailing commas whatsoever "
                "so Python's `json.loads` can load them."
            )
            sublime.message_dialog(msg)
            return

        pkg_ctrl["installed_packages"] = packages
        new_fpath = Path(sublime.packages_path()).parent / pkg_ctrl_fpath

        with open(new_fpath, "w") as file:
            json.dump(pkg_ctrl, file, indent=4)

        msg = (
            "Great success 👍👍 Restart Sublime Text "
            "for the changes to take effect."
        )
        sublime.message_dialog(msg)
