from django.contrib.auth.models import User

import player_management.models as pm
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
        # 'association_memberships','club_memberships','team_memberships'


class PersonSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = pm.Person
        fields = ('id', 'firstname','lastname','sex','birthdate','user')
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


class AssociationSerializer(serializers.HyperlinkedModelSerializer):

    #url = serializers.HyperlinkedIdentityField(
    #    view_name="player_management:association-detail")

    #board_members = serializers.HyperlinkedIdentityField(
    #    view_name='player_management:persontoassociationmembership-detail',
    #    many=True)

    #member_clubs = serializers.HyperlinkedIdentityField(
    #    view_name='player_management:clubtoassociationmembership-detail',
    #    many=True)

#   TODO: this is an asymmetrical relationship. we actually want to have to fields here: governor and
#   TODO: member. For some reaoson it does not accept those fieldnames. maybe because the are not hard
#   TODO: coded. we might need to overwrite the lookup of the original HyperlinkRelatedField by changing
#   TODO: the query set or use this workaround: https://stackoverflow.com/questions/22958058/how-to-change-field-name-in-django-rest-framework
    #governing_associations = serializers.HyperlinkedIdentityField(
    #    view_name='player_management:associationtoassociationmembership-detail',
    #    many=True)

    class Meta:
        model = pm.Association
        fields = ('id', 'name', 'description', 'founded_on', 'dissolved_on') #'url','member_persons'
        #fields = ('url','board_members','member_clubs','governing_associations')

class ClubSerializer(serializers.HyperlinkedModelSerializer):

    # member_persons = serializers.HyperlinkedIdentityField(
    #     view_name='player_management:persontoclubmembership-detail',
    #     many=True)

    class Meta:
        model = pm.Club
        fields = ('id', 'name', 'description', 'founded_on', 'dissolved_on') #'url','member_persons'


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    club_membership = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    
    #url = serializers.HyperlinkedIdentityField(
    #    view_name="player_management:team-detail")

    #member_persons = serializers.HyperlinkedIdentityField(
    #    view_name='player_management:persontoteammembership-detail',
    #    many=True)

    class Meta:
        model = pm.Team
        fields = ('id', 'name', 'description', 'founded_on', 'dissolved_on', 'club_membership') #'url','member_persons'
        #fields = ('id', 'name', 'description', 'url','member_persons')

class PersonToAssociationMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:persontoassociationmembership-detail")

    person = serializers.HyperlinkedIdentityField(
        view_name="player_management:person-detail")

    association = serializers.HyperlinkedIdentityField(
        view_name="player_management:association-detail")

    class Meta:
        model = pm.PersonToAssociationMembership
        fields = ('url','person','association','valid_from','valid_until','role','reporter','approved_by',)


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

