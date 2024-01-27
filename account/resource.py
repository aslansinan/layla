from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from account.models import Il, Ilce, Mahalle


class IlResource(resources.ModelResource):

    class Meta:
        model = Il
        fields = ('isim', 'kod')


class IlceResource(resources.ModelResource):
    il = fields.Field(column_name='il', attribute='il', widget=ForeignKeyWidget(Il, 'kod'))

    class Meta:
        model = Ilce
        fields = ('id', 'il', 'isim', 'kod')
        
class MahalleResource(resources.ModelResource):
    ilce = fields.Field(column_name='ilce', attribute='ilce', widget=ForeignKeyWidget(Ilce, 'kod'))

    class Meta:
        model = Mahalle
        fields = ('id', 'ilce', 'isim', 'kod')
