
# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from flow.models import FlowChart, Node, Edge, FlowVersion
from .serializers import FlowChartSerializer, FlowChartDetailSerializer


class FlowChartViewSet(viewsets.ModelViewSet):
    serializer_class = FlowChartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FlowChart.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FlowChartDetailSerializer
        return FlowChartSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def save_flow(self, request, pk=None):
        """Save complete flow state (nodes + edges + viewport)"""
        flow_chart = self.get_object()
        data = request.data

        try:
            with transaction.atomic():
                # Update viewport and settings
                flow_chart.viewport = data.get('viewport', {})
                flow_chart.flow_settings = data.get('flowSettings', {})
                flow_chart.version += 1
                flow_chart.save()

                # Clear existing nodes and edges
                flow_chart.nodes.all().delete()
                flow_chart.edges.all().delete()

                # Create new nodes
                nodes_data = data.get('nodes', [])
                for node_data in nodes_data:
                    Node.objects.create(
                        flow_chart=flow_chart,
                        node_id=node_data['id'],
                        node_type=node_data.get('type', 'default'),
                        position_x=node_data['position']['x'],
                        position_y=node_data['position']['y'],
                        data=node_data.get('data', {}),
                        style=node_data.get('style', {}),
                        width=node_data.get('width'),
                        height=node_data.get('height'),
                        draggable=node_data.get('draggable', True),
                        selectable=node_data.get('selectable', True),
                        deletable=node_data.get('deletable', True),
                    )

                # Create new edges
                edges_data = data.get('edges', [])
                for edge_data in edges_data:
                    Edge.objects.create(
                        flow_chart=flow_chart,
                        edge_id=edge_data['id'],
                        edge_type=edge_data.get('type', 'default'),
                        source_node_id=edge_data['source'],
                        target_node_id=edge_data['target'],
                        source_handle=edge_data.get('sourceHandle', ''),
                        target_handle=edge_data.get('targetHandle', ''),
                        data=edge_data.get('data', {}),
                        style=edge_data.get('style', {}),
                        label=edge_data.get('label', ''),
                        label_style=edge_data.get('labelStyle', {}),
                        animated=edge_data.get('animated', False),
                        deletable=edge_data.get('deletable', True),
                    )

                # Create version snapshot
                FlowVersion.objects.create(
                    flow_chart=flow_chart,
                    version_number=flow_chart.version,
                    snapshot_data=data,
                    created_by=request.user,
                    change_description=data.get('changeDescription', '')
                )

            return Response({'message': 'Flow saved successfully', 'version': flow_chart.version})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def export_flow(self, request, pk=None):
        """Export flow in React Flow format"""
        flow_chart = self.get_object()
        serializer = FlowChartDetailSerializer(flow_chart)

        # Transform to React Flow format
        flow_data = {
            'nodes': [NodeSerializer(node).to_representation(node) for node in flow_chart.nodes.all()],
            'edges': [EdgeSerializer(edge).to_representation(edge) for edge in flow_chart.edges.all()],
            'viewport': flow_chart.viewport,
            'flowSettings': flow_chart.flow_settings,
        }

        return Response(flow_data)