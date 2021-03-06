"""
File Name: Serializers
Purpose: Serializers for translating database data before sending it over the API.
Comments:
"""
from rest_framework import serializers
from rest_framework.fields import empty

from api.logistics.helper_functions import calc_pending, calc_approved
from api.models import BugReport, FeedbackForm
from api.models import Student, Mentor, HourInstance, Group, StudentGroup, ActivityCategory, Notification, \
    StudentNotificationSeenStatus
from auth_backend.modules.user.serializers import UserSerializer


class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Mentor
        fields = ['id', 'user']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    pending_hour = serializers.SerializerMethodField()
    approved_hour = serializers.SerializerMethodField()

    def get_pending_hour(self, obj):
        hours = HourInstance.objects.filter(student=obj)
        return calc_pending(hours)

    def get_approved_hour(self, obj):
        hours = HourInstance.objects.filter(student=obj)
        return calc_approved(hours)

    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'class_standing', 'pending_hour', 'approved_hour']


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ['title']


class HourSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, pk=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        if kwargs['context']['request'].method == 'GET':
            setattr(self.Meta, 'depth', 1)
        else:
            setattr(self.Meta, 'depth', 0)

    class Meta:
        model = HourInstance
        fields = ['id', 'student', 'date_of_activity', 'number_of_hours', 'number_of_minutes', 'activity_description',
                  'activity_category', 'type_of_hour', 'learning_goal', 'approved', 'mentor_comment', 'approval_status']
        depth = 1


class GroupSerializer(serializers.ModelSerializer):
    """Group Serializer"""

    students = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), many=True
    )
    mentor_detail = MentorSerializer(source='mentor', read_only=True)
    pending_hour = serializers.SerializerMethodField()
    approved_hour = serializers.SerializerMethodField()

    def get_pending_hour(self, obj):
        hours = HourInstance.objects.filter(student__in=obj.students.all())
        return calc_pending(hours)

    def get_approved_hour(self, obj):
        hours = HourInstance.objects.filter(student__in=obj.students.all())
        return calc_approved(hours)

    class Meta:
        model = Group
        fields = ('id', 'name', 'mentor', 'students', 'created_at', 'mentor_detail', 'pending_hour', 'approved_hour')

    def create(self, validated_data):
        students = validated_data.pop('students', [])
        group = Group.objects.create(**validated_data)
        student_list = [
            StudentGroup(
                student=student,
                group=group
            ) for student in students
        ]
        StudentGroup.objects.bulk_create(student_list)
        return group

    def update(self, instance, validated_data):
        StudentGroup.objects.filter(group=instance).delete()
        students = validated_data.pop('students', [])
        student_list = [
            StudentGroup(
                student=student,
                group=instance
            ) for student in students
        ]
        instance.mentor = validated_data['mentor']
        instance.name = validated_data['name']
        StudentGroup.objects.bulk_create(student_list)
        instance.save()
        return instance


class StudentGroupSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True
    )
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), source='group', write_only=True
    )
    student = StudentSerializer(read_only=True)

    class Meta:
        model = StudentGroup
        fields = ('student', 'group', 'student_id', 'group_id',)
        read_only_fields = ('group',)

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        user_group_instance = super(StudentGroupSerializer, self).update(
            instance, validated_data
        )
        return user_group_instance


class FeedbackFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackForm
        exclude = []


class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        exclude = []


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title',)

    def create(self, validated_data):
        instance = super().create(validated_data)
        StudentNotificationSeenStatus.objects.bulk_create([
            StudentNotificationSeenStatus(student=student, notification=instance)
            for student in Student.objects.all()
        ])
        return instance
