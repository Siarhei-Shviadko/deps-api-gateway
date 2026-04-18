import datetime
import json
import uuid

from faker import Faker

fake = Faker()


OUTPUTS_DICT = {
    "outputs": [
        {
            "id": uuid.uuid4().hex,
            "tenantId": uuid.uuid4().hex,
            "profileInfo": {"id": uuid.uuid4().hex, "version": uuid.uuid4().hex},
            "documentId": uuid.uuid4().hex,
            "state": "ready",
            "filePath": fake.uri_path(),
            "creationDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
    ]
}
OUTPUTS_JSON = json.dumps(OUTPUTS_DICT)

OUTPUT_PROFILES_RESPONSE_DICT = {
    "profiles": [
        {
            "id": "string",
            "name": "string",
            "creationDate": "2024-11-20",
            "schema": {"fields": ["string"], "needsValidationResults": True},
            "version": "1",
            "format": "excel",
            "externalStoragesInfo": [{"code": "Salesforce"}],
        }
    ]
}
OUTPUT_PROFILES_RESPONSE_JSON = json.dumps(OUTPUT_PROFILES_RESPONSE_DICT)

OUTPUT_PROFILE_RESPONSE_DICT = {
    "id": uuid.uuid4().hex,
    "tenantId": uuid.uuid4().hex,
    "profileInfo": {"id": uuid.uuid4().hex, "version": uuid.uuid4().hex},
    "documentId": uuid.uuid4().hex,
    "state": "ready",
    "filePath": fake.uri_path(),
    "creationDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
}

OUTPUT_PROFILE_RESPONSE_JSON = json.dumps(OUTPUT_PROFILE_RESPONSE_DICT)
