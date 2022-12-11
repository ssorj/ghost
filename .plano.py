from bullseye import *

project.name = "ghost"

@command
def test():
    build()

    with project_env(), working_dir():
         run("ghost clone --owner ssorj ghost")
         run("ghost status ghost")

         remove("ghost")

         make_dir("abc")
         write("abc/README.md", "Hello!")

         run("ghost init --owner ssorj abc")
         run("ghost uninit abc")
