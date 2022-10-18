import sys, time
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QMenu, QMainWindow, QListWidget, QDialog, QLabel, QMessageBox, QListWidgetItem
from PyQt5.QtCore import QThread, QTimer, QDateTime, pyqtSignal
import requests
import json
import threading
from threading import Timer
from random import sample
from time import sleep
from datetime import date, datetime
import cgitb
cgitb.enable(format='text')


class ui_demo_project (QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi("demoProject.ui", self)
        self.pbRequest.clicked.connect(self.fn_request)
        self.lwCharacters.itemClicked.connect(self.show_item_selected)
        self.lblDate.setText(str(date.today()))  
        self.fn_update_hour()

    def show_item_selected(self):
        print("Was selected")
        print(self.lwCharacters.currentItem().text())

    def fn_update_hour(self):
        hour = datetime.now()
        hour = hour.strftime("%H:%M:%S")
        self.lblHour.setText(hour)
        self.timer=Timer(1,self.fn_update_hour)
        self.timer.start()
    
    # def _fill_list(self, dataJson):
    #     index =0
    #     for res in dataJson["results"]:
    #         print(res["name"])
    #         QListWidgetItem(str(res["name"]), self.lwCharacters)

    def _get_name(self, url, index_character):
        url_new=url
        url_new+=str(index_character)
        print(f'1url_new: {url_new}')
        
        try:
            response = requests.request('GET', url_new)
            if response.status_code == 200:            
                dataJson=response.json() 
                # print(f"dataJson: {dataJson}")
                name=dataJson["name"]
                # print(name)
            elif response.status_code == 404:
                print('Not Found.')
            else:
                print("Error request status_code!!")
            response.raise_for_status()
        except requests.ConnectionError as error:
            print(f"Error ConnectionError: {error}")
        except requests.exceptions.Timeout as error:
            print(f"Error Timeout: {error}")
        except requests.exceptions.RequestException as error:
            print(f"Error RequestException: {error}")
            raise SystemExit(error)
        except Exception as err:
            print("General Error")

        return name


        

    def _fill_list(self,url, listRandom):
        for item in listRandom:
            print(f'item:{item}')
            sleep(0.05)
            # name=self._get_name(url,item)
            # print(name)
            # QListWidgetItem(name, self.lwCharacters)             
        



    def fn_request(self):
        print("Presionando REQUEST")
        url = "https://swapi.dev/api/people/"

        totalCharacters=0
        try:
            req = requests.request('GET', url, timeout=10)
            if req.status_code == 200:     
                dataJson=req.json()
                # print(dataJson)        
                totalCharacters=dataJson["count"]
                # characters =dataJson["results"]
                req.raise_for_status()
            elif req.status_code == 404:
                print('Not Found.')
            else:
                print("Error request status_code!!")
        except requests.ConnectionError as error:
            print(f"Error ConnectionError: {error}")
        except requests.exceptions.Timeout as error:
            print(f"Error Timeout: {error}")
        except requests.exceptions.RequestException as error:
            print(f"Error RequestException: {error}")
            raise SystemExit(error)
        except Exception as err:
            print("General Error")
        
        if(totalCharacters>0):
            print(f'totalCharacters: {totalCharacters}')
            listRandom=sample([x for x in range(1,totalCharacters)],10)
            listRandom=sorted(listRandom)
            print(f"sorted listRandom: {listRandom}")
            self._fill_list(url,listRandom)

            # QMessageBox.information(self,"Ventana Secundaria",str(characters))





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = ui_demo_project()
    ui.show()
    sys.exit(app.exec_())
    