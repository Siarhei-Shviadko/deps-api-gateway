import json

USER_DICT = {
    "pk": "string",
    "username": "username",
    "email": "email@email.com",
    "firstName": "firstName",
    "lastName": "lastName",
    "organisation": "organisation",
    "creationDate": "2025-01-13T14:07:11.766Z",
}
USER_JSON = json.dumps(USER_DICT)


ORGANISATION_DICT = {"pk": "string", "name": "name", "customizationUrl": "customizationUrl"}
ORGANISATION_JSON = json.dumps(ORGANISATION_DICT)

ORGANISATIONS_DICT = {"organisations": [{"pk": "string", "name": "name", "customizationUrl": "customizationUrl"}]}
ORGANISATIONS_JSON = json.dumps([ORGANISATION_DICT])

ORGANISATION_USERS_DICT = {
    "meta": {"total": 1, "size": 1},
    "result": [
        {
            "pk": "string",
            "username": "username",
            "email": "email",
            "firstName": "firstName",
            "lastName": "lastName",
            "organisation": "organisation",
            "creationDate": "2025-01-13T15:09:48.243Z",
        }
    ],
}
ORGANISATION_USERS_JSON = json.dumps(ORGANISATION_USERS_DICT)

ORGANISATION_INVITEES_DICT = {"meta": {"total": 1, "size": 1}, "result": [{"email": "string"}]}
ORGANISATION_INVITEES_JSON = json.dumps(ORGANISATION_INVITEES_DICT)
