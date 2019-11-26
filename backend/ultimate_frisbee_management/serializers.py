import json
import hashlib
import logging

from django.contrib.auth.models import User, Group
from rest_framework import serializers, reverse
from rest_framework.fields import empty
from rest_framework import serializers

from . import models as pm

logger = logging.getLogger(__name__)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','username','email','groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    emailmd5 = serializers.SerializerMethodField()

    def get_emailmd5(self, obj):
        return hashlib.md5(str(obj.email).encode('utf-8')).hexdigest()
    
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','groups', 'emailmd5')
        read_only_fields = ('email',)


def namespaced_view(cl):
    return


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','email',)

class PersonSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(required=False,)
    #user = serializers.HyperlinkedIdentityField(view_name='user-detail',read_only=False)
    #url = serializers.HyperlinkedIdentityField(view_name=':person-detail')

    class Meta:
        model = pm.Person
        fields = ('url','id', 'firstname','lastname','sex','birthdate','user','club_memberships','team_memberships')
        # 'association_memberships','club_memberships','team_memberships'

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of person
        :return: returns a successfully created student record
        """

        #todo: the User object gets validated when trying to create this and throws an error if the user exists
        # it should not if a user is found with the credentials, just use that one (and eventually update it)
        # so a create of person should trigger just an patch of User
        user_data = self.initial_data.pop('user')
        user = User.objects.get_or_create(**user_data)[0]
        validated_data['user'] = user
        person = super(PersonSerializer,self).create(validated_data)
        return person

class ClubSerializer(serializers.HyperlinkedModelSerializer):

    # member_persons = serializers.HyperlinkedIdentityField(
    #     view_name='persontoclubmembership-detail',
    #     many=True)

    url = serializers.HyperlinkedIdentityField(view_name='club-detail')

    class Meta:
        model = pm.Club
        fields = ('url','id', 'name', 'description', 'founded_on', 'dissolved_on')

class AssociationSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="association-detail")

    board_members = PersonSerializer(many=True)
    member_clubs = ClubSerializer(many=True)

    class Meta:
        model = pm.Association
        fields = ('url','id', 'name', 'description', 'founded_on', 'dissolved_on','board_members','member_clubs')


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField( view_name='team-detail')

    club_membership = ClubSerializer(required=True)
    member_persons = PersonSerializer(many=True)

    class Meta:
        model = pm.Team
        fields = ('url','id', 'name', 'description', 'founded_on', 'dissolved_on', 'club_membership','member_persons')


class PersonToAssociationMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="persontoassociationmembership-detail")

    class Meta:
        model = pm.PersonToAssociationMembership
        fields = ('url','valid_from','valid_until','role','reporter','approved_by',)


class PersonToClubMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="persontoclubmembership-detail")

    person = serializers.HyperlinkedIdentityField(
        view_name="person-detail")

    club = serializers.HyperlinkedIdentityField(
        view_name="club-detail")

    class Meta:
        model = pm.PersonToClubMembership
        fields = ('url','person','club','valid_from','valid_until','role','reporter','approved_by',)


class PersonToTeamMembershipSerializer(serializers.HyperlinkedModelSerializer):

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="persontoteammembership-detail")

    # person = serializers.HyperlinkedIdentityField(
    #     view_name="person-detail")

    # team = serializers.HyperlinkedIdentityField(
    #     view_name="team-detail")

    class Meta:
        model = pm.PersonToTeamMembership
        fields = ('url','person','team','valid_from','valid_until','role','number','reporter','approved_by',)


class ClubToAssociationMembershipSerializer(serializers.HyperlinkedModelSerializer):

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="clubtoassociationmembership-detail")

    # club = serializers.HyperlinkedIdentityField(
    #     view_name="club-detail")

    # association = serializers.HyperlinkedIdentityField(
    #     view_name="association-detail")

    class Meta:
        model = pm.ClubToAssociationMembership
        fields = ('url','club','association','valid_from','valid_until','reporter','approved_by',)

class AssociationToAssociationMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="associationtoassociationmembership-detail")

    member = serializers.HyperlinkedIdentityField(
        view_name="association-detail")

    governor = serializers.HyperlinkedIdentityField(
        view_name="association-detail")

    class Meta:
        model = pm.AssociationToAssociationMembership
        fields = ('url','member','governor','valid_from','valid_until','reporter','approved_by',)



