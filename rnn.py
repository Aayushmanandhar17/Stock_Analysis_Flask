
import visual as vc
import os
import numpy as np
import json
import tensorflow as tf
from keras.models import load_model
from keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler

data=vc.visual_class()

class machine_learning:
    def __init__(self):
        self.model=0
        self.pred=0
        self.single_day=0
        self.bias=0
        self.scale=0
        self.start_price_sixty=0
        self.sc=MinMaxScaler(feature_range=(0,1))
        self.company_name="TSLA"
        self.set_deafult_h5_path="trained_models\TSLA.h5"
        self.set_deafult_json_file="trained_models\TSLA.json"

#TO DO
# Train multiple company stock Price
    def get_h5_json(self):
        json_file=f"trained_models\{self.company_name}.json"
        hfive_file=f"trained_models\{self.company_name}.h5"
        if self.file_exists(hfive_file):
            return json_file, hfive_file
        else:
            print("The file does not exists!!, using Tesla Trained model")
            json_file=self.set_deafult_json_file
            hfive_file=self.set_deafult_h5_path
            return json_file,hfive_file

    def file_exists(self,hfive):
        file_exists=os.path.exists(hfive)
        if file_exists:
            return True

    def load_trained_model(self):
        json_file,hfive_file=self.get_h5_json()
        with open(json_file,'r') as f:
            model_json = json.load(f)
        self.model = model_from_json(model_json)
        self.model.load_weights(hfive_file)
        self.prediction()
        self.prediction_single_day(self.company_name)


# Predicting the last 60 stock Price
    def set_rnn_datastructure(self, name):
        data_frame=data.dual_moving_average(name)
        df=data_frame[['Open','Volume']]
        sixty_day_df=data_frame[-60:]
        sixty_day_df.reset_index(inplace=True)
        Train_60_days=df.tail(120)[:60]
        Test_60_days=df.tail(60)
        sixty_day_price= np.array(df['Open'].tail(60))
        self.start_price_sixty=sixty_day_price[0]
        new_df=Train_60_days.append(Test_60_days,ignore_index=True)
        inputs=self.sc.fit_transform(new_df)
        new_x_test=[]
        for i in range(60,inputs.shape[0]):
            new_x_test.append(inputs[i-60:i])
        new_x_test=np.array(new_x_test)
        return new_x_test,sixty_day_price,sixty_day_df


    def prediction(self):
        new_x_test,sixty_day_price,sixty_day_df=self.set_rnn_datastructure(self.company_name)
        graph=tf.get_default_graph()
        with graph.as_default():
            final_prediction=self.model.predict(new_x_test)
        s=self.sc.scale_
        self.scale=s
        scaler=(1/s[0])
        final_prediction=final_prediction*scaler
        self.bias=self.start_price_sixty-final_prediction[0]
        print("The bias is",self.bias)
        final_prediction=final_prediction+self.bias
        final_prediction=final_prediction.flatten()
        predict = np.vstack((final_prediction, sixty_day_price)).T
        sixty_day_df['PREDICT'],sixty_day_df["REAL"]=predict[:,0],predict[:,1]
        self.pred = sixty_day_df[['Date','PREDICT','REAL']]


    def prediction_single_day(self,name):
        graph=tf.get_default_graph()
        data_frame=data.dual_moving_average(name)
        last_30_days=data_frame[['Open','Volume']][-60:]
        inputs_single=self.sc.fit_transform(last_30_days)
        Single_data=[]
        for i in range(60,61):
            Single_data.append(inputs_single[i-60:i])
        Single_data=np.array(Single_data)
        Single_final_prediction=self.model.predict(Single_data)
        s=self.sc.scale_
        scaler=(1/self.scale[0])
        Single_final_prediction=(Single_final_prediction*scaler)+self.bias
        self.single_day= Single_final_prediction
