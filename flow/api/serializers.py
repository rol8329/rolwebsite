# serializers.py
from rest_framework import serializers
from flow.models import FlowChart, Node, Edge, FlowVersion


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

    def to_representation(self, instance):
        """Convert to React Flow node format"""
        return {
            'id': instance.node_id,
            'type': instance.node_type,
            'position': {
                'x': instance.position_x,
                'y': instance.position_y
            },
            'data': instance.data,
            'style': instance.style,
            'draggable': instance.draggable,
            'selectable': instance.selectable,
            'deletable': instance.deletable,
            'width': instance.width,
            'height': instance.height,
        }


class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = '__all__'

    def to_representation(self, instance):
        """Convert to React Flow edge format"""
        edge_data = {
            'id': instance.edge_id,
            'type': instance.edge_type,
            'source': instance.source_node_id,
            'target': instance.target_node_id,
            'data': instance.data,
            'style': instance.style,
            'animated': instance.animated,
            'deletable': instance.deletable,
        }

        if instance.source_handle:
            edge_data['sourceHandle'] = instance.source_handle
        if instance.target_handle:
            edge_data['targetHandle'] = instance.target_handle
        if instance.label:
            edge_data['label'] = instance.label
            edge_data['labelStyle'] = instance.label_style

        return edge_data


class FlowChartSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)
    edges = EdgeSerializer(many=True, read_only=True)

    class Meta:
        model = FlowChart
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at', 'version')


class FlowChartDetailSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True)
    edges = EdgeSerializer(many=True, read_only=True)

    class Meta:
        model = FlowChart
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at')




