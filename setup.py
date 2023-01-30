import cx_Freeze

executables = [cx_Freeze.Executable("chess_graphics.py")]

cx_Freeze.setup(
    name="Smart Chess",
    #options={"build_exe": {"packages":["pygame"],
    #                       "include_files":["racecar.png"]}},
    executables = executables

    )