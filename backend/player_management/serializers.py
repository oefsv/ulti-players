from django.contrib.auth.models import User

from . import models as pm
from rest_framework import serializers, reverse
from rest_framework.fields import empty


def namespaced_view(cl):
    return


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
        # 'association_memberships','club_memberships','team_memberships'

class PersonSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(required=True)
    url = serializers.HyperlinkedIdentityField(view_name='player_management:person-detail')

    class Meta:
        model = pm.Person
        fields = ('url','id', 'firstname','lastname','sex','birthdate','user')
        # 'association_memberships','club_memberships','team_memberships'

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        validated_data['user'] = user
        student, created = pm.Person.objects.update_or_create(validated_data)
        return student


class ClubSerializer(serializers.HyperlinkedModelSerializer):

    # member_persons = serializers.HyperlinkedIdentityField(
    #     view_name='player_management:persontoclubmembership-detail',
    #     many=True)

    url = serializers.HyperlinkedIdentityField(view_name='player_management:club-detail')

    class Meta:
        model = pm.Club
        fields = ('url','id', 'name', 'description', 'founded_on', 'dissolved_on')

class AssociationSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:association-detail")

    board_members = PersonSerializer(many=True)
    member_clubs = ClubSerializer(many=True)

    class Meta:
        model = pm.Association
        fields = ('url','id', 'name', 'description', 'founded_on', 'dissolved_on','board_members','member_clubs')


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField( view_name='player_management:team-detail')

    club_membership = ClubSerializer(required=True)
    member_persons = PersonSerializer(many=True)

    class Meta:
        model = pm.Team
        fields = ('url','id', 'name', 'description', 'founded_on', 'dissolved_on', 'club_membership','member_persons')


class PersonToAssociationMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:persontoassociationmembership-detail")

    class Meta:
        model = pm.PersonToAssociationMembership
        fields = ('url','valid_from','valid_until','role','reporter','approved_by',)


class PersonToClubMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:persontoclubmembership-detail")

    person = serializers.HyperlinkedIdentityField(
        view_name="player_management:person-detail")

    club = serializers.HyperlinkedIdentityField(
        view_name="player_management:club-detail")

    class Meta:
        model = pm.PersonToClubMembership
        fields = ('url','person','club','valid_from','valid_until','role','reporter','approved_by',)


class PersonToTeamMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:persontoteammembership-detail")

    person = serializers.HyperlinkedIdentityField(
        view_name="player_management:person-detail")

    team = serializers.HyperlinkedIdentityField(
        view_name="player_management:team-detail")

    class Meta:
        model = pm.PersonToTeamMembership
        fields = ('url','person','team','valid_from','valid_until','role','number','reporter','approved_by',)


class ClubToAssociationMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:clubtoassociationmembership-detail")

    club = serializers.HyperlinkedIdentityField(
        view_name="player_management:club-detail")

    association = serializers.HyperlinkedIdentityField(
        view_name="player_management:association-detail")

    class Meta:
        model = pm.ClubToAssociationMembership
        fields = ('url','club','association','valid_from','valid_until','reporter','approved_by',)

class AssociationToAssociationMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:associationtoassociationmembership-detail")

    member = serializers.HyperlinkedIdentityField(
        view_name="player_management:association-detail")

    governor = serializers.HyperlinkedIdentityField(
        view_name="player_management:association-detail")

    class Meta:
        model = pm.AssociationToAssociationMembership
        fields = ('url','member','governor','valid_from','valid_until','reporter','approved_by',)



