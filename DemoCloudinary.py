import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
  cloud_name = "mxyzdl123",
  api_key = "978139117644534",
  api_secret = "F_mpzRKVelD61h5Paet2Gmp7iD4"
)


img = cloudinary.CloudinaryImage("sample_id")

print img

# result = cloudinary.uploader.upload("914.jpeg", public_id = 'sample_id')
#
# print result