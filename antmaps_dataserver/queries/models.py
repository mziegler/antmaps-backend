"""
Database tables used by AntMaps.

queries/views.py contains some raw-SQL queries, so if you change the database tables,
you have to update the queries in views.py as well as updating this file.
"""

from django.db import models



class Subfamily(models.Model):
    #subfamily_id = models.IntegerField(primary_key=True, db_column='subfamily_id')
    subfamily_name = models.TextField(primary_key=True)

    class Meta:
        managed = False # this means Django should never alter this table
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
    genus_name = models.CharField(max_length=255)
    #genus_name = models.ForeignKey(Genus, db_column='genus_name', to_field='genus_name', blank=True, null=True)
    species_name = models.CharField(max_length=255)
    subfamily_name = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'map_taxonomy_list'




class Record(models.Model):
    gabi_acc_number = models.CharField(db_column='gabi_acc_number', primary_key=True, max_length=255)  # Field name made lowercase.
    #accession_number = models.CharField(max_length=255, blank=True)
    #reference = models.TextField(blank=True)
    #genus_name_pub = models.CharField(max_length=255, blank=True)
    lat = models.CharField(max_length=255, blank=True, db_column='dec_lat')
    lon = models.CharField(max_length=255, blank=True, db_column='dec_long')
    valid_species_name = models.ForeignKey('Species', db_column='valid_species_name', to_field='taxon_code', blank=True, null=True)
    #bentity = models.ForeignKey('Bentity', db_column='bentity2_id', to_field='bentity2_id', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'map_record'




class SpeciesBentityPair(models.Model):
    # GROSS HACK: the 'bentity' field is not actually the primary key, Django just needs to think that there is a single-column primary key.  Don't use SpeciesBentityPair.objects.get() or any other Django functions that rely on the PK
    
    subfamily_name = models.ForeignKey('Subfamily', db_column='subfamily_name', to_field='subfamily_name', blank=True)
    genus_name = models.ForeignKey(Genus, db_column='genus_name', to_field='genus_name', blank=True, null=True)
    valid_species_name = models.ForeignKey('Species', db_column='valid_species_name', to_field='taxon_code', blank=True, null=True)
    bentity = models.ForeignKey('Bentity', primary_key=True, db_column='bentity2_id', to_field='gid', blank=True)
    category = models.CharField(max_length=2)
    num_records = models.IntegerField()
    literature = models.IntegerField()
    museum_specimen = models.IntegerField()
    database_collection = models.IntegerField()
     
    class Meta:
        managed = False
        db_table = 'map_species_bentity_pair'




class Bentity(models.Model):
    gid = models.CharField(max_length=50, primary_key=True, db_column='bentity2_id')
    bentity = models.CharField(max_length=500, db_column='bentity2_name')
    
    class Meta:
        managed = False
        db_table = 'bentity2'



