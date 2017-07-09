@echo off
python "%~dp0playgame.py" --engine_seed 42 --player_seed 42 --end_wait=2.5 --verbose -I -E --log_dir game_logs --turns 150 --map_file "%~dp0maps\maze\maze_04p_01.map" %* "python ""%~dp0sample_bots\python\GreedyBot.py""" "python ""%~dp0sample_bots\python\LeftyBot.py""" "python ""%~dp0sample_bots\python\HunterBot.py""" "python ""%~dp0..\ants_py\MyBot.py"""

