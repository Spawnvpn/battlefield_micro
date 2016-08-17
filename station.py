import socket
import json
import threading
import time
from battle import Battlefield


def send_data():
    while battlefield.armies_active:
        result_str = str()
        for army in battlefield.armies:
            result_str += 'Army {}: \n'.format(battlefield.armies.index(army) + 1)
            for squad in army.squads:
                result_str += 'Squad {} \n: '.format(army.squads.index(squad) + 1)
                for unit in squad.units:
                    result_str += 'Health of {} unit: '.format(squad.units.index(unit) + 1) + str(round(unit.health, 0))
        sock.send(str.encode(result_str))
    time.sleep(1)

if __name__ == '__main__':
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(100)
    conn, addr = sock.accept()

    print('connected:', addr)
    threading.Thread()

    data = conn.recv(1024)
    decode_data = bytes.decode(data)
    decode_data = json.loads(decode_data)
    print(decode_data)
    battlefield = Battlefield(
        quan_armies=decode_data['quan_armies'],
        units=decode_data['units'],
        squads=decode_data['squads'],
        strategy=decode_data['strategy']
    )
    do_battle = threading.Thread(target=battlefield.start)
    sending = threading.Thread(target=send_data)
    do_battle.start()
    sending.start()
