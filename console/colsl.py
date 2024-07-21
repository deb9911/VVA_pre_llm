import os
import sys


class CommandPrompt:
    def __init__(self):
        self.commands = {
            'help': self.help,
            'exit': self.exit,
            'list': self.list_files,
            'echo': self.echo,
            'mkdir': self.make_directory,
            'rmdir': self.remove_directory,
            'cd': self.change_directory,
            'pwd': self.print_working_directory,
            'del': self.delete_file
        }

    def help(self, args):
        print("Available commands:")
        for command in self.commands:
            print(f"  {command}")

    def exit(self, args):
        print("Exiting...")
        sys.exit(0)

    def list_files(self, args):
        path = args[0] if args else '.'
        try:
            files = os.listdir(path)
            for file in files:
                print(file)
        except FileNotFoundError:
            print(f"Directory '{path}' not found.")
        except NotADirectoryError:
            print(f"'{path}' is not a directory.")

    def echo(self, args):
        print(' '.join(args))

    def make_directory(self, args):
        if not args:
            print("Error: Missing directory name.")
            return
        try:
            os.makedirs(args[0], exist_ok=True)
            print(f"Directory '{args[0]}' created.")
        except Exception as e:
            print(f"Error creating directory '{args[0]}': {e}")

    def remove_directory(self, args):
        if not args:
            print("Error: Missing directory name.")
            return
        try:
            os.rmdir(args[0])
            print(f"Directory '{args[0]}' removed.")
        except FileNotFoundError:
            print(f"Directory '{args[0]}' not found.")
        except OSError as e:
            print(f"Error removing directory '{args[0]}': {e}")

    def change_directory(self, args):
        if not args:
            print("Error: Missing directory name.")
            return
        try:
            os.chdir(args[0])
            print(f"Changed directory to '{args[0]}'.")
        except FileNotFoundError:
            print(f"Directory '{args[0]}' not found.")
        except NotADirectoryError:
            print(f"'{args[0]}' is not a directory.")
        except Exception as e:
            print(f"Error changing directory to '{args[0]}': {e}")

    def print_working_directory(self, args):
        print(os.getcwd())

    def delete_file(self, args):
        if not args:
            print("Error: Missing file name.")
            return
        try:
            os.remove(args[0])
            print(f"File '{args[0]}' deleted.")
        except FileNotFoundError:
            print(f"File '{args[0]}' not found.")
        except IsADirectoryError:
            print(f"'{args[0]}' is a directory.")
        except Exception as e:
            print(f"Error deleting file '{args[0]}': {e}")

    def run(self):
        print("Command Prompt - Type 'help' for a list of commands")
        while True:
            try:
                user_input = input("> ").strip()
                if user_input:
                    self.process_command(user_input)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break

    def process_command(self, user_input):
        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command in self.commands:
            self.commands[command](args)
        else:
            print(f"Unknown command: {command}. Type 'help' for a list of commands.")


if __name__ == "__main__":
    CommandPrompt().run()
