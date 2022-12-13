# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "frappe_s3_attachment"
app_title = "Frappe S3 Attachment"
app_publisher = "Extension Technologies"
app_description = "Frappe app to make file upload to Digital Ocean Spaces through attach file option."
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hello@extensionerp.com"
#dev_email = "sameer@extensioncrm.com"
app_license = "MIT"
app_version = "1.0.1"

doctype_list_js = {
    "S3 Attachment Settings": ["frappe_s3_attachment/doctype/s3_attachment_settings/s3_attachment_settings.js"]
}

doc_events = {
    "File": {
        "after_insert": "frappe_s3_attachment.controller.file_upload_to_s3",
        "on_trash": "frappe_s3_attachment.controller.delete_from_cloud"
    }
}
