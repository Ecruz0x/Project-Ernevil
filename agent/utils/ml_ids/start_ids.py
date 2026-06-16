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

alerts = Queue()

def flow_verify(details):
    prediction = model.predict([details])

    if prediction[0] != "Benign":
        alerts.put_nowait({
            "src_port": details["src_port"],
            "protocol": details["protocol"],
            "event": prediction[0]
        })