import player_management.models as pm
from rest_framework import serializers


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    association_memberships = serializers.HyperlinkedIdentityField(view_name='association_membership', many=True,format='html')

    class Meta:
        model = pm.Person
        fields = ('firstname','lastname','birthdate','sex','association_memberships')