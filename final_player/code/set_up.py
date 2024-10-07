from cx_Freeze import setup, Executable

setup(
    name="myscript",
    version="0.1",
    description="My application",
    executables=[Executable("main.py")]
)