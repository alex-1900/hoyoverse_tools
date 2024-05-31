import os
import pdfkit

from bbs import BBSSyncRole


def sync_roles():
    bbs_sync_role = BBSSyncRole()
    bbs_sync_role.update_roles_data(1187)
    bbs_sync_role.update_roles_data(2526)

    bbs_sync_role.create_roles_pdf()
