from cx_Freeze import setup, Executable


executables = [Executable("main.py")]



setup(
    name="CityBulderSim",
    version="0.1",
    description="game about building",
    executables=executables

)
