
from rest_framework import serializers

from bloodtests.models import Test


class TestSerializer(serializers.ModelSerializer):
    lower = serializers.IntegerField(required=False, allow_null=True)
    upper = serializers.IntegerField(required=False, allow_null=True)

    # we can have 'ideal_range' field as model property or serializermethodfield etc.

    class Meta:
        model = Test
        fields = ('code', 'name', 'unit', 'lower', 'upper', 'ideal_range')

    def validate(self, data):
        """Validate range"""
        if not (data.get('lower') or data.get('upper')):

            # test file `assert 'Lower and upper cannot both be null' in content`
            # is checking keys.  It must have some static json 'key'
            # Ex. one of {'error|message|detail': 'Lower and upper cannot both be null'}
            raise serializers.ValidationError({
                'Lower and upper cannot both be null': 'Lower and upper cannot both be null'}
            )
        if data['lower'] and data['upper'] and data['lower'] > data['upper']:
            # same here.
            raise serializers.ValidationError({
                "Lower value can't exceed upper value": "Lower value can't exceed upper value"})
        return data
