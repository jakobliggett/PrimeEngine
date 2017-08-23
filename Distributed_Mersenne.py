import socket
import thread
import math
import logging
import LucasLehmer
import os

valid = False
i = 0
while not valid:
    if not os.path.isfile('distributed_mersenne_master'+str(i)+'.txt'):
        valid = True
    else:
        i += 1
filename = 'distributed_mersenne_master'+str(i)+'.txt'

append_lock = thread.allocate_lock()

def InputLoop(strng, cast_type, invalid_text='invalid argument', valid_answers = None):
    done = None
    while not done:
        value = raw_input(strng)
        try:
            if cast_type == 'int':
                new_value = int(value)
            elif cast_type == 'alpha':
                new_value = str(value).lower()
                if not new_value.isalpha():
                    #print('not alpha')
                    raise Exception
            if valid_answers != None:
                if new_value not in valid_answers:
                    #print('not in valid')
                    raise Exception
            done = True
        except:
            print(invalid_text)
    return new_value

def threaded_client_worker(conn):
    print('Client started')
    #conn.sendall('TEST')
    while True:
        try:
            en_data = conn.recv(2048)
            data = (en_data.decode('utf-8'))
            current_working_queue.append(data)
        except:
            pass

            '''
            logging.debug('Data {}, threaded_worker'.format(data))
            result = LucasLehmer.mersenne_test(data)
            logging.debug('Result {}, threaded_worker'.format(result))
            to_send = str.encode('{},{}'.format(data, result))
            conn.sendall(to_send)
            logging.info('Successfully recieved, processed, and sent data for number: m{}'.format(data))
        except:
            print('err')
            #logging.error('Error recieving and processing next job: \n {}'.format(str(e)))
            '''

def threaded_client_server(conn):
    ##What the server sends to the worker
    print('threaded_client_server started')
    working = False
    while True:
        try:
            if working == True:
                en_data = conn.recv(2048)
                data = en_data.decode('utf-8')
                #print(data)
                checked, result = data.split(',')
                checked = int(checked)
                if result == 'True':
                    result = True
                elif result == 'False':
                    result = False
                with master_results_lock:
                    master_results.append([checked, result])
                with append_lock:
                    with open(filename, 'a') as f:
                        f.write(str([checked, result]))
                working = False

            elif working == False:

                with queue_grab_lock:
                    job = str(len(server_check_queue)+1)
                    server_check_queue.append(job)
                conn.sendall(job)
                working = True
                logging.info('Gave worker job for checking {}'.format(job))

        except Exception as e:
            #print(str(e))
            pass

def threaded_admin_control():
    pass
    #while True:
        #command = raw_input()

logging.basicConfig(level=logging.DEBUG)
max_connections = 50

server_check_queue = []
queue_grab_lock = thread.allocate_lock()

current_working_queue = []

master_results = []
master_results_lock = thread.allocate_lock()

def continue_distributed(mode, ip = None, port = None, host_port = 8888):
    if mode == 'master':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)

        bound = False

        try_port = host_port
        host = ''
        while not bound:
            try:
                server.bind((host, try_port))
                bound = True
                logging.info('Bound to port {} sucessfully'.format(try_port))
            except socket.error:
                logging.error('Failed to bind to port {}, trying next one'.format(try_port))
            try_port += 1

        server.listen(max_connections)

        while True:
            try:
                conn, addr = server.accept()
                logging.info('Connected to {}:{}'.format(addr[0], addr[1]))
                thread.start_new(threaded_client_server, (conn,))
            except:
                pass #yes I know this is bad, but I don't understand how to handle for blocking mode yet

    elif mode == 'worker':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
            host = (raw_input('Enter Host IP: '))
            port = int(raw_input('Enter Host Port: '))
            try:
                client.connect((host, port))
                connected = True
                thread.start_new_thread(threaded_client_worker, (client,))
                logging.info('Connected Successfully')
            except socket.error:
                print('Could not connect, try again \n')
        while True:
            if len(current_working_queue) > 0:
                #print(current_working_queue)
                to_check = int(current_working_queue.pop(0))
                result = LucasLehmer.mersenne_test(to_check)
                logging.info('LLT returned {} for {}'.format(result, to_check))
                to_send = str.encode('{},{}'.format(to_check, result))
                client.sendall(to_send)





if __name__ == '__main__':
    mode = str(raw_input('Mode: '))
    continue_distributed(mode)