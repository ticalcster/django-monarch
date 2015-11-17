from django.contrib import admin

from server import models


@admin.register(models.LegacyGroup)
class LegacyGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LegacyDistrict)
class LegacyDistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LegacyPosition)
class LegacyPositionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LegacyDistrictPosition)
class LegacyDistrictPositionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DistrictPosition)
class DistrictPositionAdmin(admin.ModelAdmin):
    pass
