
from __future__ import absolute_import, unicode_literals
from celery.task import task

from AI.newML import Data_split
from AI.newML import my_Cross_Validation
from AI.newML import Machine_Learning

from utils.cos import write_model,read_model
import uuid
from .models import Task, AIModel
from .models import UserProfile
import time
import base64
from io import BytesIO




@task
def ML_Traditional(file_str,uuid_str,ai_id):
    
    dataset_file = BytesIO(base64.b64decode(file_str))

    model = Machine_Learning(dataset_file, 0.2)

    write_model(uuid_str,model)
    ai_instance = AIModel.objects.get(ai_id=ai_id)
    ai_instance.ai_status = 100
    ai_instance.save()
    

@task
def test():
    time.sleep(10)
    print("finished!")
    return 'hello'