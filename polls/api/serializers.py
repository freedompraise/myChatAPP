from polls.models import Room,Topic
from rest_framework.serializers import ModelSerializer
# the serialzer transforms our python model, room to a JSON object for use in the api view.
class serialRoom(ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'

class serialTopic(ModelSerializer):
    class Meta:
        model=Topic
        fields='__all__'
