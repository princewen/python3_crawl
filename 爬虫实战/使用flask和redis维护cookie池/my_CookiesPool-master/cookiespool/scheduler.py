from cookiespool.api import app
from cookiespool.config import *
from cookiespool.generator import *
from cookiespool.tester import *
from multiprocessing import Process
import time

class Scheduler(object):

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print ('generate cookies')
            try:
                for name,cls in GENERATOR_MAP.items():
                    generator = eval(cls+'()')
                    generator.run()
                    print ('Generator finished')
                    generator.close()
                    print ('Generator closed')
                    time.sleep(cycle)
            except Exception as e:
                print (e.args)

    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Checking Cookies')
            try:
                for name, cls in TESTER_MAP.items():
                    tester = eval(cls + '()')
                    tester.run()
                    print('Tester Finished')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        app.run(host=API_HOST, port=API_PORT)




    def run(self):
        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()

        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()