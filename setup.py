"""Fichier d'installation de notre script game_init.py."""

from cx_Freeze import setup, Executable

setup(
    name="Pokemon_Auto_Battler",
    version="0.1",
    options={"build_exe": {"packages": ["pygame", "sqlalchemy", "time", "MySQLdb", 'game', 'game.objects', 'database', 'database.models'],
                           "include_files": ["img/", "database/sql_script/"]}},
    description="Projet réalisé autour de Pokémon",
    executables=[Executable("game/game_init.py")],
)
