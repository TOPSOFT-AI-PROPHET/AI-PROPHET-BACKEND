from celery import shared_task
from common.ai.traditional import train_model
from common.utils.cos import write_model
from .models import AIModel
import base64
from io import BytesIO


@shared_task
def ml_traditional(file_str, uuid_str, ai_id):
    dataset_file = BytesIO(base64.b64decode(file_str))

    model = train_model(dataset_file, 0.2)

    write_model(uuid_str, model)
    ai_instance = AIModel.objects.get(ai_id=ai_id)
    ai_instance.ai_status = 100
    ai_instance.save()
