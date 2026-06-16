import joblib
from asyncio import Queue
from .netsniffer import capture_and_flow_control as capture
import warnings
from collections import Counter
from datetime import datetime


warnings.filterwarnings("ignore", category=UserWarning)



model = joblib.load("utils/ml_ids/models/bestmodel.pkl")


now = datetime.now()
sql_format = now.strftime('%Y-%m-%d %H:%M:%S')


def flow_verify(details):
    prediction = model.predict([details])
    print(details)
    if prediction[0] != "Benign":
        print(prediction)
        return {
            "src_port": details[0],
            "protocol": details[2],
            "event": prediction[0]
        }
