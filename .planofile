from bullseye import *

project.name = "ghost"
project.excluded_modules = ["bullseye"]

@command
def test(app):
    build(app)

    with project_env(), working_dir():
         run("ghost clone --owner ssorj ghost")
         run("ghost status ghost")

         remove("ghost")

         make_dir("abc")
         write("abc/README.md", "Hello!")

         run("ghost init --owner ssorj abc")
         run("ghost uninit abc")
