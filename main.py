import os
import sys
import json
import importlib
import toml


class mkLanguage:
    def translate(self):
        config = toml.load("config.toml")
        file_name = sys.argv[1]
        file_ext = config["fileExt"]
        no_ext_file_name = file_name[: -(len(file_ext))]
        with open(file_name, mode="r") as f:
            file = f.read()
        try:
            with open("extension.py", mode="r"):
                file = importlib.import_module("extension").translate(file)
        except FileNotFoundError:
            pass

        file_name = no_ext_file_name + config["compileExt"]
        with open(config["translateFile"], mode="r") as f:
            translate_table = json.load(f)
        for to, _from in translate_table.items():
            file = file.replace(_from, to)
        with open(file_name, mode="w") as f:
            f.write(file)

    def compile(self):
        config = toml.load("config.toml")
        filename = sys.argv[1]
        file_ext = config["fileExt"]
        no_ext_file_name = filename[: -(len(file_ext))]
        filename = no_ext_file_name + config["compileExt"]
        compile_command = (
            config["compileCommand"]
            .replace("{{{inputFile}}}", filename)
            .replace("{{{noExtInputFile}}}", no_ext_file_name)
        )
        clean_command = (
            config["cleanCommand"]
            .replace("{{{inputFile}}}", filename)
            .replace("{{{noExtInputFile}}}", no_ext_file_name)
        )
        os.system(compile_command)

        os.system(clean_command)

    def main(self):
        self.translate()
        self.compile()


mklanguage = mkLanguage()
mklanguage.main()
