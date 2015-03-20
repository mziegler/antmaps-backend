"""
Subfamily, Genus, and Species models are currently just used for populating taxon
select boxes.
"""

from django.db import models



class Subfamily(models.Model):
    subfamily_id = models.IntegerField(primary_key=True, db_column='subfamily_id')
    subfamily_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'subfamily'


class Genus(models.Model):
    genus_id = models.IntegerField(primary_key=True)
    genus_name = models.TextField(unique=True)
    subfamily_name = models.ForeignKey('Subfamily', db_column='subfamily_name', to_field='subfamily_name', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'genus'


class Species(models.Model):
    species_id = models.IntegerField(primary_key=True)
    taxon_code = models.CharField(unique=True, max_length=99999)
    genus_name = models.ForeignKey(Genus, db_column='genus_name', to_field='genus_name', blank=True, null=True)
    species_name = models.TextField(blank=True)
    subspecies_name = models.TextField(blank=True)
    
    class Meta:
        managed = False
        db_table = 'species'


class Record(models.Model):
    gabi_acc_number = models.CharField(db_column='GABI_Acc_Number', primary_key=True, max_length=255)  # Field name made lowercase.
    accession_number = models.CharField(max_length=255, blank=True)
    reference = models.TextField(blank=True)
    genus_name_pub = models.CharField(max_length=255, blank=True)
    lat = models.CharField(max_length=255, blank=True, db_column='dec_lat')
    lon = models.CharField(max_length=255, blank=True, db_column='dec_long')
    taxon_code = models.ForeignKey('Species', db_column='valid_taxonomy', to_field='taxon_code', related_name='point', blank=True, null=True)
    bentity = models.ForeignKey('Bentity', db_column='bentity', to_field='gid', related_name='point', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'record'


class Bentity(models.Model):
    gid = models.IntegerField(primary_key=True)
    bentity = models.CharField(max_length=41, blank=True)
    # geog = models.GeometryField(blank=True, srid=4326) # requires geodjango
    
    class Meta:
        managed = False
        db_table = 'bentities_highres'



