from bugpy.data import upload_filelist
from bugpy.ingestion import collect_metadata
from bugpy.utils import get_credentials
def upload_recordings(db, partial_upload=True):
    """ Uploads a list of recordings from local storage

        :param db: bugpy.Connection object
        :param partial_upload: Whether to tolerate a partial upload
        :return: list of files which failed to upload
    """
    df = collect_metadata(db)

    df['filename'] = df['file_loc'].str.split('/').str[-1]
    df['file_path'] = 'project_'+df['project_id'].astype(str)+'/experiment_'+df['experiment_id'].astype(str)+'/'+df['filename']

    bucket = get_credentials('s3_web', 'BUCKET')
    fails = upload_filelist(df['file_loc'],bucket, uploadnames=df['file_path'])

    if len(fails)>0 and not partial_upload:
        print(f"{len(fails)} files failed to upload - check and retry")
        return fails
    df = df[~df['file_loc'].isin(fails)]

    db.insert('recordings',df)

    return fails