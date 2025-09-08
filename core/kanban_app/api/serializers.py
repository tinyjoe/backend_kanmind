from rest_framework import serializers
from kanban_app.models import Board, BoardTask, TaskComment

class BoardSerializer(serializers.ModelSerializer):
    members = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    class Meta: 
        model= Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members']
        read_only_fields = ['id', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        # TODO: Anpassen, wenn Tickets ins Modell kommen
        return 0

    def get_tasks_to_do_count(self, obj):
        # TODO: Anpassen
        return 0

    def get_tasks_high_prio_count(self, obj):
        # TODO: Anpassen
        return 0