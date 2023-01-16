import crud
import datetime

connector = crud.BotConnector('localhost', 'gruzin', '78632145', 'bonks')

connector.delete_all_bonks_before_date(datetime.datetime.now())