# coding=utf-8
import logging
from websocket_server import WebsocketServer
import sys
from importlib import reload
import pandas as pd
import numpy as np
# from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


reload(sys)
# sys.setdefaultencoding('utf-8')


def new_client(client, server):
    print("Client has joined")
    # print("Client(%d) has joined." % client['id'])


def client_left(client, server):
    print(server)
    print("Client disconnected")
    # print("Client(%d) disconnected" % client['id'])


def message_back(client, server, message):
    # data from client side
    print("Client(%d) said: %s" % (client['id'], message))
    # process the data
    f1 = int(message.split('*')[0])
    f2 = int(message.split('*')[1])
    f3 = int(message.split('*')[2])
    f4 = int(message.split('*')[2])
    f5 = int(message.split('*')[2])
    result = str(handle_feature(f1, f2, f3, f4, f5))
    # sand back to client side
    server.send_message(client, result)

# @TODO need to change the function to correct one
def handle_feature(GrLivArea, LotArea, BsmtFinSF1, OverallQual, TotalBsmtSF):
    train = pd.read_csv("train.csv")

    train['MSZoning'] = pd.factorize(train['MSZoning'])[0]
    train['Street'] = pd.factorize(train['Street'])[0]
    train['Alley'] = pd.factorize(train['Alley'])[0]
    train['LotShape'] = pd.factorize(train['LotShape'])[0]
    train['LandContour'] = pd.factorize(train['LandContour'])[0]
    train['Utilities'] = pd.factorize(train['Utilities'])[0]
    train['LotConfig'] = pd.factorize(train['LotConfig'])[0]
    train['LandSlope'] = pd.factorize(train['LandSlope'])[0]
    train['Neighborhood'] = pd.factorize(train['Neighborhood'])[0]
    train['Condition1'] = pd.factorize(train['Condition1'])[0]
    train['Condition2'] = pd.factorize(train['Condition2'])[0]
    train['BldgType'] = pd.factorize(train['BldgType'])[0]
    train['HouseStyle'] = pd.factorize(train['HouseStyle'])[0]
    train['RoofStyle'] = pd.factorize(train['RoofStyle'])[0]
    train['RoofMatl'] = pd.factorize(train['RoofMatl'])[0]
    train['Exterior1st'] = pd.factorize(train['Exterior1st'])[0]
    train['Exterior2nd'] = pd.factorize(train['Exterior2nd'])[0]
    train['MasVnrType'] = pd.factorize(train['MasVnrType'])[0]
    train['ExterQual'] = pd.factorize(train['ExterQual'])[0]
    train['ExterCond'] = pd.factorize(train['ExterCond'])[0]
    train['BsmtExposure'] = pd.factorize(train['BsmtExposure'])[0]
    train['BsmtFinType1'] = pd.factorize(train['BsmtFinType1'])[0]
    train['BsmtFinType2'] = pd.factorize(train['BsmtFinType2'])[0]
    train['Heating'] = pd.factorize(train['Heating'])[0]
    train['HeatingQC'] = pd.factorize(train['HeatingQC'])[0]
    train['CentralAir'] = pd.factorize(train['CentralAir'])[0]
    train['Electrical'] = pd.factorize(train['Electrical'])[0]
    train['KitchenQual'] = pd.factorize(train['KitchenQual'])[0]
    train['Functional'] = pd.factorize(train['Functional'])[0]
    train['FireplaceQu'] = pd.factorize(train['FireplaceQu'])[0]
    train['GarageType'] = pd.factorize(train['GarageType'])[0]
    train['GarageFinish'] = pd.factorize(train['GarageFinish'])[0]
    train['GarageQual'] = pd.factorize(train['GarageQual'])[0]
    train['GarageCond'] = pd.factorize(train['GarageCond'])[0]
    train['PavedDrive'] = pd.factorize(train['PavedDrive'])[0]
    train['PoolQC'] = pd.factorize(train['PoolQC'])[0]
    train['Fence'] = pd.factorize(train['Fence'])[0]
    train['MiscFeature'] = pd.factorize(train['MiscFeature'])[0]
    train['SaleType'] = pd.factorize(train['SaleType'])[0]
    train['SaleCondition'] = pd.factorize(train['SaleCondition'])[0]
    train['Foundation'] = pd.factorize(train['Foundation'])[0]
    train['BsmtQual'] = pd.factorize(train['BsmtQual'])[0]
    train['BsmtCond'] = pd.factorize(train['BsmtCond'])[0]

    train = train.fillna(-1)
    train = train.set_index('Id')
    X = train.loc[:, train.columns != 'SalePrice']
    y = np.array(train['SalePrice']).tolist()

    model = XGBRegressor()
    model.fit(X, y)
    feature_names = list(X.columns.values)

    array = [-1] * 79
    predict_df = pd.DataFrame([array], columns=feature_names)
    predict_df['GrLivArea'] = [GrLivArea]
    predict_df['LotArea'] = [LotArea]
    predict_df['BsmtFinSF1'] = [BsmtFinSF1]
    predict_df['OverallQual'] = [OverallQual]
    predict_df['TotalBsmtSF'] = [TotalBsmtSF]

    model.predict(predict_df)
    #print(model.predict(predict_df)[0])
    return model.predict(predict_df)[0]


# predict_price(10, 1000, 1000)


server = WebsocketServer(4200, host='')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_back)
server.run_forever()