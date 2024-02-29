class BucketAccess:

    @classmethod
    def create_presigned_post_url(cls, client, bucket_name: str, object_name: str, expiration=360):
        response = client.generate_presigned_post(
            bucket_name, object_name,
            ExpiresIn=expiration
        )
        return response
