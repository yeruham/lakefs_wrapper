from fastapi import APIRouter

app = APIRouter()


@app.get(
    '/repositories/{repository}/branch_protection',
    response_model=List[BranchProtectionRule],
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def internal_get_branch_protection_rules(
    repository: str,
) -> Union[List[BranchProtectionRule], Error]:
    """
    get branch protection rules
    """
    pass


@app.post(
    '/repositories/{repository}/branch_protection',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def internal_create_branch_protection_rule(
    repository: str, body: BranchProtectionRule = ...
) -> Union[None, Error]:
    pass


@app.delete(
    '/repositories/{repository}/branch_protection',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def internal_delete_branch_protection_rule(
    repository: str, body: RepositoriesRepositoryBranchProtectionDeleteRequest = ...
) -> Union[None, Error]:
    pass


@app.get(
    '/repositories/{repository}/branch_protection/set_allowed',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        '409': {'model': Error},
        'default': {'model': Error},
    },
    tags=['internal'],
)
def create_branch_protection_rule_preflight(repository: str) -> Union[None, Error]:
    pass


@app.get(
    '/repositories/{repository}/settings/branch_protection',
    response_model=List[BranchProtectionRule],
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '404': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def get_branch_protection_rules(
    repository: str,
) -> Union[List[BranchProtectionRule], Error]:
    """
    get branch protection rules
    """
    pass


@app.put(
    '/repositories/{repository}/settings/branch_protection',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '412': {'model': Error},
        'default': {'model': Error},
    },
    tags=['repositories'],
)
def set_branch_protection_rules(
    if__match: Optional[str] = Header(None, alias='If-Match'),
    repository: str = ...,
    body: List[BranchProtectionRule] = ...,
) -> Union[None, Error]:
    pass