rm WebGui/modules/events.db
python3 WebGui/modules/createMYSQLTable.py
python3 WebGui/modules/debugServer.py &
python3 WebGui/frontEnd.py &
#python3 motherCell.py 0 3 2
