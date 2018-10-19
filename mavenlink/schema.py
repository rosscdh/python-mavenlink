from marshmallow import Schema, fields, pprint


class ExternalReference(Schema):
    service_name = fields.String()
    service_model = fields.String()
    service_model_ref = fields.String()
    status = fields.String()
    external_status = fields.String()
    external_link = fields.String()
    locked = fields.Boolean(default=False)


class TimeEntrySchema(Schema):
    workspace_id = fields.Integer()
    date_performed = fields.Date()
    time_in_minutes = fields.Integer()
    billable = fields.Boolean(default=True)
    rate_in_cents = fields.Integer()
    notes = fields.String()
    role_id = fields.Integer()
    story_id = fields.Integer()
    user_id = fields.Integer()
    external_reference = fields.Nested(ExternalReference)