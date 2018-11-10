import player_management.models as pm
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    # TODO: nested relationships. SEE https://www.django-rest-framework.org/api-guide/relations/
    association_memberships = serializers.HyperlinkedIdentityField(
       view_name='player_management:persontoassociationmembership-detail', many=True)

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:person-detail")

    class Meta:
        model = pm.Person
        fields = ('url','firstname','lastname','sex','birthdate','association_memberships')


class AssociationSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:association-detail")

    class Meta:
        model = pm.PersonToAssociationMembership
        fields = ('url','valid_from','valid_until','role')



class PersonToAssociationMembershipSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="player_management:persontoassociationmembership-detail")

    class Meta:
        model = pm.PersonToAssociationMembership
        fields = ('url','valid_from','valid_until','role','reporter','approved_by',)
