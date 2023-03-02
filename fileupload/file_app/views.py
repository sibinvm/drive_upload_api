from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission

permission =  GoogleDriveFilePermission(
   GoogleDrivePermissionRole.READER,
   GoogleDrivePermissionType.USER,
   "foo@mailinator.com"
)

gd_storage = GoogleDriveStorage(permissions=(permission, ))

class Map(models.Model):
    id = models.AutoField( primary_key=True)
    map_name = models.CharField(max_length=200)
    map_data = models.FileField(upload_to='maps/', storage=gd_storage)