"""
Subfamily, Genus, and Species models are currently just used for populating taxon
select boxes.
"""

from django.db import models



class Subfamily(models.Model):
    #subfamily_id = models.IntegerField(primary_key=True, db_column='subfamily_id')
    subfamily_name = models.TextField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'subfamily'


class Genus(models.Model):
    #genus_id = models.IntegerField(primary_key=True)
    genus_name = models.TextField(unique=True)
    subfamily_name = models.ForeignKey('Subfamily', db_column='subfamily_name', to_field='subfamily_name', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'genus'


class Species(models.Model):
    #species_id = models.IntegerField(primary_key=True)
    taxon_code = models.CharField(primary_key=True, max_length=99999)
    genus_name = models.ForeignKey(Genus, db_column='genus_name', to_field='genus_name', blank=True, null=True)
    species_name = models.TextField(blank=True)
    
    class Meta:
        managed = False
        db_table = 'species'


# FIXME update to new view
class Record(models.Model):
    gabi_acc_number = models.CharField(db_column='GABI_Acc_Number', primary_key=True, max_length=255)  # Field name made lowercase.
    #accession_number = models.CharField(max_length=255, blank=True)
    #reference = models.TextField(blank=True)
    #genus_name_pub = models.CharField(max_length=255, blank=True)
    lat = models.CharField(max_length=255, blank=True, db_column='dec_lat')
    lon = models.CharField(max_length=255, blank=True, db_column='dec_long')
    taxon_code = models.ForeignKey('Species', db_column='valid_taxonomy', to_field='taxon_code', blank=True, null=True)
    bentity = models.ForeignKey('Bentity', db_column='bentity', to_field='bentity2_id', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'record'


class SpeciesBentityPair(models.Model):
    # HACK: subfamily_name is not actually the primary key, Django just needs to think that there is a single-column primary key.  Don't use SpeciesBentityPair.objects.get() or anything else that needs to use the pk
    subfamily_name = models.ForeignKey('Subfamily', primary_key=True, db_column='subfamily_name', to_field='subfamily_name', blank=True)
    genus_name = models.ForeignKey(Genus, db_column='genus_name', to_field='genus_name', blank=True, null=True)
    valid_species_name = models.ForeignKey('Species', db_column='valid_species_name', to_field='taxon_code', blank=True, null=True)
    bentity = models.ForeignKey('Bentity', db_column='bentity2_id', to_field='gid', blank=True, null=True)
    category = models.CharField(max_length=2)
    
     
    class Meta:
        managed = False
        db_table = 'map_species_bentity_pair'


class Bentity(models.Model):
    gid = models.CharField(max_length=50, primary_key=True, db_column='bentity2_id')
    bentity = models.CharField(max_length=500, db_column='bentity2_name')
    
    class Meta:
        managed = False
        db_table = 'bentity2'



