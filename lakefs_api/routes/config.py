from fastapi import APIRouter

app = APIRouter()




@app.get(
    '/config',
    response_model=Config,
    responses={'401': {'model': Error}},
    tags=['config'],
)
def get_config() -> Union[Config, Error]:
    pass


@app.get(
    '/config/garbage-collection',
    response_model=GarbageCollectionConfig,
    responses={'401': {'model': Error}},
    tags=['internal'],
)
def get_garbage_collection_config() -> Union[GarbageCollectionConfig, Error]:
    pass


@app.get(
    '/config/storage',
    response_model=StorageConfig,
    responses={'401': {'model': Error}},
    tags=['internal'],
)
def get_storage_config() -> Union[StorageConfig, Error]:
    pass


@app.get(
    '/config/version',
    response_model=VersionConfig,
    responses={'401': {'model': Error}},
    tags=['internal'],
)
def get_lake_f_s_version() -> Union[VersionConfig, Error]:
    pass



@app.get(
    '/usage-report/summary',
    response_model=InstallationUsageReport,
    responses={
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def get_usage_report_summary() -> Union[InstallationUsageReport, Error]:
    """
    get usage report summary
    """
    pass