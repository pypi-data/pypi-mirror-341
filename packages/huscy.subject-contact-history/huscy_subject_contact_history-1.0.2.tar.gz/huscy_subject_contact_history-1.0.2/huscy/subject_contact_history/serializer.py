from rest_framework import serializers

from huscy.subject_contact_history.models import ContactHistoryItem
from huscy.subject_contact_history.services import create_contact_history_item


class ContactHistorySerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creator_username = serializers.SerializerMethodField(source='get_creator_username')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    project_title = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ContactHistoryItem
        fields = (
            'created_at',
            'creator',
            'creator_username',
            'project',
            'project_title',
            'status',
            'status_display',
        )

    def create(self, validated_data):
        return create_contact_history_item(**validated_data)

    def get_creator_username(self, contact_history_item):
        return contact_history_item.creator.username

    def get_project_title(self, contact_history_item):
        project = contact_history_item.project
        return (project and project.title) or 'Deleted project'
