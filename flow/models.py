# models.py
from django.db import models
from django.contrib.auth.models import User


class FlowChart(models.Model):
    """Main flow chart container"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Viewport and flow settings
    viewport = models.JSONField(default=dict, help_text="Viewport position and zoom")
    flow_settings = models.JSONField(default=dict, help_text="React Flow settings and configurations")

    # Metadata
    is_public = models.BooleanField(default=False)
    version = models.IntegerField(default=1)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} (v{self.version})"


class Node(models.Model):
    """Individual nodes in the flow chart"""
    NODE_TYPES = [
        ('default', 'Default'),
        ('input', 'Input'),
        ('output', 'Output'),
        ('custom', 'Custom'),
    ]

    flow_chart = models.ForeignKey(FlowChart, related_name='nodes', on_delete=models.CASCADE)
    node_id = models.CharField(max_length=100)  # React Flow node ID
    node_type = models.CharField(max_length=50, choices=NODE_TYPES, default='default')

    # Position
    position_x = models.FloatField()
    position_y = models.FloatField()

    # Node data (flexible JSON field for custom properties)
    data = models.JSONField(default=dict)

    # Style and dimensions
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    style = models.JSONField(default=dict, blank=True)

    # Behavior
    draggable = models.BooleanField(default=True)
    selectable = models.BooleanField(default=True)
    deletable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('flow_chart', 'node_id')

    def __str__(self):
        return f"Node {self.node_id} in {self.flow_chart.name}"


class Edge(models.Model):
    """Connections between nodes"""
    EDGE_TYPES = [
        ('default', 'Default'),
        ('straight', 'Straight'),
        ('step', 'Step'),
        ('smoothstep', 'Smooth Step'),
        ('bezier', 'Bezier'),
        ('custom', 'Custom'),
    ]

    flow_chart = models.ForeignKey(FlowChart, related_name='edges', on_delete=models.CASCADE)
    edge_id = models.CharField(max_length=100)  # React Flow edge ID
    edge_type = models.CharField(max_length=50, choices=EDGE_TYPES, default='default')

    # Connection points
    source_node_id = models.CharField(max_length=100)
    target_node_id = models.CharField(max_length=100)
    source_handle = models.CharField(max_length=100, blank=True)
    target_handle = models.CharField(max_length=100, blank=True)

    # Edge data and styling
    data = models.JSONField(default=dict, blank=True)
    style = models.JSONField(default=dict, blank=True)
    label = models.CharField(max_length=200, blank=True)
    label_style = models.JSONField(default=dict, blank=True)

    # Behavior
    animated = models.BooleanField(default=False)
    deletable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('flow_chart', 'edge_id')

    def __str__(self):
        return f"Edge {self.edge_id} in {self.flow_chart.name}"


class FlowVersion(models.Model):
    """Version history for flow charts"""
    flow_chart = models.ForeignKey(FlowChart, related_name='versions', on_delete=models.CASCADE)
    version_number = models.IntegerField()
    snapshot_data = models.JSONField()  # Complete flow state
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    change_description = models.TextField(blank=True)

    class Meta:
        unique_together = ('flow_chart', 'version_number')
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.flow_chart.name} v{self.version_number}"