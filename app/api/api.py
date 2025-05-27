#flask
from flask import Flask, request
#config
from util.db_utility import DatabaseUtility
from util.utility import Utility
from config.logger_config import setup_logger
#Models
from models.family import *
from models.response import ResponseEntity
from models.exceptions import *

LOGGER = setup_logger("APP")

app = Flask(__name__)
app.json.sort_keys = False  #makes json sort properly




@app.route("/test", methods=['GET'])
def t():
    task = Task("test", datetime(year=2025, month=1, day=2, hour=3, minute=4, second=5))
    DatabaseUtility.commit_new_task(task)
    return ResponseEntity.ok()


@app.route("/test1", methods=['GET'])
def t1():
    info = DatabaseUtility.get_task_by_task_id(2)
    return ResponseEntity.error(str(info))


if __name__ == '__main__':
    app.run(debug=True, port=8081)
