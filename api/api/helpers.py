
from django.db import IntegrityError
import traceback
import yaml
import datetime

def safeBulkCreate(Model, data, uniqueField=[], updateFields=[]):
    createdRecords = []
    try:
        if len(uniqueField) > 0 and len(updateFields) > 0:
            createdRecords = Model.objects.bulk_create(data,update_conflicts=True, unique_fields=uniqueField,update_fields=updateFields)
        else:
            createdRecords = Model.objects.bulk_create(data)
    except IntegrityError:
        print(traceback.format_exc())
        for obj in data:
            try:
                print(obj)
                createdRecords.append(obj)
                obj.save()
            except IntegrityError as integrityErr:
                print(integrityErr)
                continue
    return createdRecords

def openFile(file_path):
    fileContent = ''
    with open(file_path,'r') as file:
        try:
            fileContent = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
    return fileContent

def writeFile(filePath, newFileContent):
    with open(filePath, 'w') as file:
        documents = yaml.dump(newFileContent, file)
    return None

def formatFileName ():
    date = datetime.now()
    ftr = [3600,60,1]
    seconds = sum([a*b for a,b in zip(ftr, map(int,date.strftime('%H:%M:%S').split(':')))])
    name = date.strftime('%Y-%m-%d') + '_' + str(seconds) + "_questrade_activities.txt"
    return name


def getActivityAction (actionDict):
    object, orderType, autoOrderType = actionDict.values()
    action = orderType.split('_')[0].capitalize() if orderType != None else None
    if object == "dividend":
        if autoOrderType == "dividend_reinvestment":
            return "DRIP"
        elif orderType == None:
            return "Cash Dividend" 
    elif (object == "order"):
        return action
    else:
        return action
    
def setActivityAmountValue (data):
    if 'filled_net_value' in data:
        return data['filled_net_value'] 
    elif data['object'] == 'dividend':
        return data['net_cash']['amount']
    else:
        return None
    
def setActivityPrice (activity):
    quantity = 0
    amount = setActivityAmountValue(activity)
    if activity['object'] == 'order' and quantity != None and amount != None:
        if 'quantity' in activity:
            quantity = activity['quantity']
        if 'fill_quantity' in activity:
            quantity = activity['fill_quantity']
        price = round(float(amount) / float(quantity),2)
        return price
    return 0

def setActivityCurrency (activity):
    currency = ''
    if 'currency' in activity:
        currency = activity['currency'].upper() 
    if activity['object'] == "order" and 'limit_price' in activity:
        currency = activity['limit_price']['currency'].upper()
    if 'account_currency' in activity:
        currency = activity['account_currency'].upper()  
    elif activity['object'] == 'dividend':
        currency = activity['market_value']['currency']
    else: 
        currency = "None"
    return currency