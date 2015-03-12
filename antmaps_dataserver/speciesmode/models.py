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
    taxon_code = models.CharField(unique=True, max_length=-1)
    genus_name = models.ForeignKey(Genus, db_column='genus_name', to_field='genus_name', blank=True, null=True)
    genus_name_text = models.TextField(blank=True, db_column='genus_name') # hack so Django can get the actual text of the genus_name without retrieving the related object
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
    taxon_code = models.ForeignKey('Species', db_column='valid_taxonomy', to_field='taxon_code', blank=True, null=True)
    #bentity = models.ForeignKey(BentitiesHighres, db_column='bentity', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'record'


