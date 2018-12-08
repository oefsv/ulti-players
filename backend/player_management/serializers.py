import player_management.models as pm
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    # TODO: nested relationships. SEE https://www.django-rest-framework.org/api-guide/relations/
    association_memberships = serializers.HyperlinkedIdentityField(
        view_name='player_management:persontoassociationmembership-detail',
        many=True)

    club_memberships = serializers.HyperlinkedIdentityField(
        view_name='player_management:persontoclubmembership-detail',
        many=True)

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:person-detail")

    class Meta:
        model = pm.Person
        fields = ('url','firstname','lastname','sex','birthdate',
                  'association_memberships','club_memberships')


class AssociationSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:association-detail")

#    club_members = serializers.HyperlinkedIdentityField(
#        view_name='player_management:person-detail',
#        many=True)

    class Meta:
        model = pm.Association
        fields = ('url',) #TODO:member_clubs


class ClubSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:club-detail")

    member_persons = serializers.HyperlinkedIdentityField(
        view_name='player_management:persontoclubmembership-detail',
        many=True)

    class Meta:
        model = pm.Club
        fields = ('url','member_persons')


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:team-detail")

    member_persons = serializers.HyperlinkedIdentityField(
        view_name='player_management:persontoteammembership-detail',
        many=True)

    class Meta:
        model = pm.Team
        fields = ('url','member_persons')



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
        fields = ('url','person','team','valid_from','valid_until','role','reporter','approved_by',)

