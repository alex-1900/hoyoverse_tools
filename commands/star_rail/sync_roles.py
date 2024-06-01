from bbs import BBSSyncRole


def sync_roles():
    bbs_sync_role = BBSSyncRole()
    bbs_sync_role.update_roles_data(1543)
    bbs_sync_role.update_roles_data(1325)
    bbs_sync_role.update_roles_data(1187)
    bbs_sync_role.update_roles_data(497)
    bbs_sync_role.create_roles_pdf(1)
    print('完成1')


    bbs_sync_role = BBSSyncRole()
    bbs_sync_role.update_roles_data(412)
    bbs_sync_role.update_roles_data(561)
    bbs_sync_role.update_roles_data(76)
    bbs_sync_role.update_roles_data(46)
    bbs_sync_role.create_roles_pdf(2)
    print('完成2')

    bbs_sync_role = BBSSyncRole()
    bbs_sync_role.update_roles_data(423)
    bbs_sync_role.update_roles_data(422)
    bbs_sync_role.update_roles_data(386)
    bbs_sync_role.update_roles_data(380)
    bbs_sync_role.create_roles_pdf(3)
    print('完成3')

    bbs_sync_role = BBSSyncRole()
    bbs_sync_role.update_roles_data(49)
    bbs_sync_role.update_roles_data(1717)
    bbs_sync_role.update_roles_data(52)
    bbs_sync_role.update_roles_data(406)
    bbs_sync_role.create_roles_pdf(4)
    print('完成4')

    bbs_sync_role = BBSSyncRole()
    bbs_sync_role.update_roles_data(48)
    bbs_sync_role.update_roles_data(1710)
    bbs_sync_role.update_roles_data(565)
    bbs_sync_role.update_roles_data(564)  # 白露
    bbs_sync_role.create_roles_pdf(5)
    print('完成5')
