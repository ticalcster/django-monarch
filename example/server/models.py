from django.db import models


class Address(models.Model):
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)


class Group(models.Model):
    address = models.ForeignKey(Address)
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def __unicode__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class District(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True)
    address = models.ForeignKey(Address)
    name = models.CharField(max_length=100)
    max_districts = models.IntegerField()
    positions = models.ManyToManyField(Position, through='DistrictPosition')

    def __unicode__(self):
        return self.name


class DistrictPosition(models.Model):
    district = models.ForeignKey(District)
    position = models.ForeignKey(Position)

##
# Legacy Tables
##

class LegacyGroup(models.Model):
    GroupID = models.AutoField(primary_key=True)
    GroupName = models.CharField(max_length=100)
    WebSite = models.URLField(max_length=100)
    Address = models.CharField(max_length=50)
    City = models.CharField(max_length=25)
    State = models.CharField(max_length=2)
    Zip = models.CharField(max_length=10)

    def __unicode__(self):
        return self.GroupName


class LegacyPosition(models.Model):
    PositionID = models.AutoField(primary_key=True)
    PositionName = models.CharField(max_length=100)
    Description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.PositionName


class LegacyDistrict(models.Model):
    DistrictID = models.AutoField(primary_key=True)
    GroupID = models.ForeignKey(LegacyGroup)
    DistrictName = models.CharField(max_length=100)
    MaxDistricts = models.IntegerField()
    positions = models.ManyToManyField(LegacyPosition, through='LegacyDistrictPosition')
    Address = models.CharField(max_length=50)
    City = models.CharField(max_length=25)
    State = models.CharField(max_length=2)
    Zip = models.CharField(max_length=10)

    def __unicode__(self):
        return self.DistrictName


class LegacyDistrictPosition(models.Model):
    DistrictID = models.ForeignKey(LegacyDistrict)
    PositionID = models.ForeignKey(LegacyPosition)

    def __unicode__(self):
        return "%s - %s" % (self.DistrictID.DistrictName, self.PositionID.PositionName)
