from app.models import Base, User, Group, GroupUserMap, Role, GUMRoleMap, Resources, Permission, ResourceMapping


def _insert(session):
    session.flush()
    session.commit()

def load_data(session):
    def group(name):
        group = Group(name=name)
        session.add(group)

    def user(email):
        user = User(email=email)
        session.add(user)

    def group_user_map(group_uuid, user_uuid):
        gum = GroupUserMap(group_uuid=group_uuid, user_uuid=user_uuid)
        session.add(gum)

    def role(name, is_custom):
        role = Role(name=name, is_custom=is_custom)
        session.add(role)

    def gum_role_map(gum_uuid, role_uuid):
        gumrm = GUMRoleMap(gum_uuid=gum_uuid, role_uuid=role_uuid)
        session.add(gumrm)

    def resource(type, service_type, service_name, endpoint):
        repository = Resources(type=type, service_type=service_type, service_name=service_name, endpoint=endpoint)
        session.add(repository)

    def permission(gum_role_map_uuid, resource_uuid, action):
        permission = Permission(gum_role_map_uuid=gum_role_map_uuid, resource_uuid=resource_uuid, action=action)
        session.add(permission)

    def resource_mapping(resource_uuid, url):
        rsm = ResourceMapping(resource_uuid=resource_uuid, url=url)
        session.add(rsm)

    resource_1 = Resources(type="list", service_type="", service_name="cloud-server", endpoint="cloudserver.api.list")
    resource_2 = Resources(type="get", service_type="", service_name="cloud-server", endpoint="cloudserver.api.get")
    resource_3 = Resources(type="create", service_type="", service_name="cloud-server", endpoint="cloudserver.api.create")
    resource_4 = Resources(type="update", service_type="", service_name="cloud-server",endpoint="cloudserver.api.update")
    resource_5 = Resources(type="delete", service_type="", service_name="cloud-server",endpoint="cloudserver.api.delete")
    resource_6 = Resources(type="list", service_type="", service_name="billing", endpoint="billing.api.list")
    resource_7 = Resources(type="get", service_type="", service_name="billing", endpoint="billing.api.get")
    resource_8 = Resources(type="create", service_type="", service_name="billing", endpoint="billing.api.create")
    resource_9 = Resources(type="update", service_type="", service_name="billing", endpoint="billing.api.update")
    resource_10 = Resources(type="delete", service_type="", service_name="billing", endpoint="billing.api.delete")
    resource_11 = Resources(type="list", service_type="", service_name="cloud-driver", endpoint="cloudstorage.api.list")
    resource_12 = Resources(type="get", service_type="", service_name="cloud-driver", endpoint="cloudstorage.api.get")
    resource_13 = Resources(type="create", service_type="", service_name="cloud-driver", endpoint="cloudstorage.api.create")
    resource_14 = Resources(type="update", service_type="", service_name="cloud-driver",endpoint="cloudstorage.api.update")
    resource_15 = Resources(type="delete", service_type="", service_name="cloud-driver",endpoint="cloudstorage.api.delete")
    resource_16 = Resources(type="list", service_type="", service_name="k8s", endpoint="kubernetesengine.api.list")
    resource_17 = Resources(type="get", service_type="", service_name="k8s", endpoint="kubernetesengine.api.get")
    resource_18 = Resources(type="create", service_type="", service_name="k8s", endpoint="kubernetesengine.api.create")
    resource_19 = Resources(type="update", service_type="", service_name="k8s", endpoint="kubernetesengine.api.update")
    resource_20 = Resources(type="delete", service_type="", service_name="k8s", endpoint="kubernetesengine.api.delete")

    resources = [resource_1, resource_2, resource_3, resource_4, resource_5, resource_6, resource_7, resource_8, resource_9, resource_10,
        resource_11, resource_12, resource_13, resource_14, resource_15, resource_16, resource_17, resource_18, resource_19, resource_20]

    for _resource in resources:
        session.add(_resource)
    
    user1 = User(email="owner@gmail.com")
    user2 = User(email="billing@gmail.com")
    user3 = User(email="admin@gmail.com")
    user4 = User(email="member@gmail.com")
    user5 = User(email="reader@gmail.com")
    user6 = User(email="cusrole1@gmail.com")
    user7 = User(email="cusrole2@gmail.com")
    users = [user1, user2, user3, user4, user5, user6, user7]

    for usr in users:
        session.add(usr)

    group1 = Group(name="group1")
    group2 = Group(name="group2")
    group3 = Group(name="group3")
    groups = [group1, group2, group3]
    for g in groups:
        session.add(g)

    _insert(session)

    role1 = Role(name="Owner", description="owner", is_custom=False)
    role2 = Role(name="billing", description="billing", is_custom=False)
    role3 = Role(name="admin", description="admin", is_custom=False)
    role4 = Role(name="member", description="member", is_custom=False)
    role5 = Role(name="reader", description="reader", is_custom=False)
    role6 = Role(name=f"admin_{group2.uuid}", description="custom role named admin", is_custom=True)
    role7 = Role(name=f"Owner_{group1.uuid}", description="custom role named owner", is_custom=True)
    roles = [role1, role2, role3, role4, role5, role6, role7]
    for r in roles:
        session.add(r)

    _insert(session)

    rsm1 = ResourceMapping(resource_uuid=resource_1.uuid, url="iaas-cloud/api/list-server")
    rsm2 = ResourceMapping(resource_uuid=resource_2.uuid, url="iaas-cloud/api/get-server")
    rsm3 = ResourceMapping(resource_uuid=resource_3.uuid, url="iaas-cloud/api/create-server")
    rsm4 = ResourceMapping(resource_uuid=resource_4.uuid, url="iaas-cloud/api/update-server")
    rsm5 = ResourceMapping(resource_uuid=resource_5.uuid, url="iaas-cloud/api/delete-server")
    rsm6 = ResourceMapping(resource_uuid=resource_6.uuid, url="billing/api/list-billing")
    rsm7 = ResourceMapping(resource_uuid=resource_7.uuid, url="billing/api/get-billing")
    rsm8 = ResourceMapping(resource_uuid=resource_8.uuid, url="billing/api/create-billing")
    rsm9 = ResourceMapping(resource_uuid=resource_9.uuid, url="billing/api/update-server")
    rsm10 = ResourceMapping(resource_uuid=resource_10.uuid, url="billing/api/delete-server")
    rsm11 = ResourceMapping(resource_uuid=resource_11.uuid, url="cloud-driver/api/list-cloud-driver")
    rsm12 = ResourceMapping(resource_uuid=resource_12.uuid, url="cloud-driver/api/get-cloud-driver")
    rsm13 = ResourceMapping(resource_uuid=resource_13.uuid, url="cloud-driver/api/create-cloud-driver")
    rsm14 = ResourceMapping(resource_uuid=resource_14.uuid, url="cloud-driver/api/update-cloud-driver")
    rsm15 = ResourceMapping(resource_uuid=resource_15.uuid, url="cloud-driver/api/delete-cloud-driver")
    rsm16 = ResourceMapping(resource_uuid=resource_16.uuid, url="kubernetes-engine/api/list-kubernetes-engine")
    rsm17 = ResourceMapping(resource_uuid=resource_17.uuid, url="kubernetes-engine/api/get-kubernetes-engine")
    rsm18 = ResourceMapping(resource_uuid=resource_18.uuid, url="kubernetes-engine/api/create-kubernetes-engine")
    rsm19 = ResourceMapping(resource_uuid=resource_19.uuid, url="kubernetes-engine/api/update-kubernetes-engine")
    rsm20 = ResourceMapping(resource_uuid=resource_20.uuid, url="kubernetes-engine/api/delete-kubernetes-engine")

    rsms = [rsm1, rsm2, rsm3, rsm4, rsm5, rsm6, rsm7, rsm8, rsm9, rsm10,
        rsm11, rsm12, rsm13, rsm14, rsm15, rsm16, rsm17, rsm18, rsm19, rsm20]

    for item in rsms:
        session.add(item)


    gum1 = GroupUserMap(group_uuid=group1.uuid, user_uuid=user1.uuid) #owner 
    gum2 = GroupUserMap(group_uuid=group2.uuid, user_uuid=user2.uuid) #billing
    gum3 = GroupUserMap(group_uuid=group3.uuid, user_uuid=user3.uuid) #admin
    gum4 = GroupUserMap(group_uuid=group2.uuid, user_uuid=user4.uuid) #member
    gum5 = GroupUserMap(group_uuid=group3.uuid, user_uuid=user5.uuid) #reader
    gum6 = GroupUserMap(group_uuid=group3.uuid, user_uuid=user6.uuid) #custom role 1
    gum7 = GroupUserMap(group_uuid=group3.uuid, user_uuid=user7.uuid) #custom role 2

    gums = [gum1, gum2, gum3, gum4, gum5, gum6, gum7]
    for gum in gums:
        session.add(gum)

    _insert(session)

    gum_role_map_1 = GUMRoleMap(gum_uuid=gum1.uuid, role_uuid=role1.uuid) #user 1 role owner
    gum_role_map_2 = GUMRoleMap(gum_uuid=gum2.uuid, role_uuid=role2.uuid) #user 2 role billing
    gum_role_map_3 = GUMRoleMap(gum_uuid=gum3.uuid, role_uuid=role3.uuid) #user 3 role admin
    gum_role_map_4 = GUMRoleMap(gum_uuid=gum4.uuid, role_uuid=role4.uuid) #user 4 role member
    gum_role_map_5 = GUMRoleMap(gum_uuid=gum5.uuid, role_uuid=role5.uuid) #user 5 role reader
    gum_role_map_6 = GUMRoleMap(gum_uuid=gum6.uuid, role_uuid=role6.uuid) #user 6 role custom (update and delete CS)
    gum_role_map_7 = GUMRoleMap(gum_uuid=gum7.uuid, role_uuid=role7.uuid) #user 7 role custom (delete cloud drive)
    gum_role_map_8 = GUMRoleMap(gum_uuid=gum6.uuid, role_uuid=role2.uuid) #user 6 role billing
    gum_role_map_9 = GUMRoleMap(gum_uuid=gum7.uuid, role_uuid=role5.uuid) #user 7 role reader

    gum_role_maps = [gum_role_map_1, gum_role_map_2, gum_role_map_3, gum_role_map_4, gum_role_map_5, gum_role_map_6, gum_role_map_7, gum_role_map_8, gum_role_map_9]
    for item in gum_role_maps:
        session.add(item)

    _insert(session)

    #permission owner
    permission1 = Permission(role_uuid=role1.uuid, resource_uuid=resource_1.uuid, action="allow")
    permission2 = Permission(role_uuid=role1.uuid, resource_uuid=resource_2.uuid, action="allow")
    permission3 = Permission(role_uuid=role1.uuid, resource_uuid=resource_3.uuid, action="allow")
    permission4 = Permission(role_uuid=role1.uuid, resource_uuid=resource_4.uuid, action="allow")
    permission5 = Permission(role_uuid=role1.uuid, resource_uuid=resource_5.uuid, action="allow")
    permission6 = Permission(role_uuid=role1.uuid, resource_uuid=resource_6.uuid, action="allow")
    permission7 = Permission(role_uuid=role1.uuid, resource_uuid=resource_7.uuid, action="allow")
    permission8 = Permission(role_uuid=role1.uuid, resource_uuid=resource_8.uuid, action="allow")
    permission9 = Permission(role_uuid=role1.uuid, resource_uuid=resource_9.uuid, action="allow")
    permission10 = Permission(role_uuid=role1.uuid, resource_uuid=resource_10.uuid, action="allow")
    permission11 = Permission(role_uuid=role1.uuid, resource_uuid=resource_11.uuid, action="allow")
    permission12 = Permission(role_uuid=role1.uuid, resource_uuid=resource_12.uuid, action="allow")
    permission13 = Permission(role_uuid=role1.uuid, resource_uuid=resource_13.uuid, action="allow")
    permission14 = Permission(role_uuid=role1.uuid, resource_uuid=resource_14.uuid, action="allow")
    permission15 = Permission(role_uuid=role1.uuid, resource_uuid=resource_15.uuid, action="allow")
    permission16 = Permission(role_uuid=role1.uuid, resource_uuid=resource_16.uuid, action="allow")
    permission17 = Permission(role_uuid=role1.uuid, resource_uuid=resource_17.uuid, action="allow")
    permission18 = Permission(role_uuid=role1.uuid, resource_uuid=resource_18.uuid, action="allow")
    permission19 = Permission(role_uuid=role1.uuid, resource_uuid=resource_19.uuid, action="allow")
    permission20 = Permission(role_uuid=role1.uuid, resource_uuid=resource_20.uuid, action="allow")
    #permission billing
    permission21 = Permission(role_uuid=role2.uuid, resource_uuid=resource_6.uuid, action="allow")
    permission22 = Permission(role_uuid=role2.uuid, resource_uuid=resource_7.uuid, action="allow")
    permission23 = Permission(role_uuid=role2.uuid, resource_uuid=resource_8.uuid, action="allow")
    permission24 = Permission(role_uuid=role2.uuid, resource_uuid=resource_9.uuid, action="allow")
    permission25 = Permission(role_uuid=role2.uuid, resource_uuid=resource_10.uuid, action="allow")
    #permission admin
    permission26 = Permission(role_uuid=role3.uuid, resource_uuid=resource_1.uuid, action="allow")
    permission27 = Permission(role_uuid=role3.uuid, resource_uuid=resource_2.uuid, action="allow")
    permission28 = Permission(role_uuid=role3.uuid, resource_uuid=resource_3.uuid, action="allow")
    permission29 = Permission(role_uuid=role3.uuid, resource_uuid=resource_4.uuid, action="allow")
    permission30 = Permission(role_uuid=role3.uuid, resource_uuid=resource_11.uuid, action="allow")
    permission31 = Permission(role_uuid=role3.uuid, resource_uuid=resource_12.uuid, action="allow")
    permission32 = Permission(role_uuid=role3.uuid, resource_uuid=resource_13.uuid, action="allow")
    permission33 = Permission(role_uuid=role3.uuid, resource_uuid=resource_14.uuid, action="allow")
    permission34 = Permission(role_uuid=role3.uuid, resource_uuid=resource_16.uuid, action="allow")
    permission35 = Permission(role_uuid=role3.uuid, resource_uuid=resource_17.uuid, action="allow")
    permission36 = Permission(role_uuid=role3.uuid, resource_uuid=resource_18.uuid, action="allow")
    permission37 = Permission(role_uuid=role3.uuid, resource_uuid=resource_19.uuid, action="allow")
    #permission member
    permission38 = Permission(role_uuid=role4.uuid, resource_uuid=resource_1.uuid, action="allow")
    permission39 = Permission(role_uuid=role4.uuid, resource_uuid=resource_2.uuid, action="allow")
    permission40 = Permission(role_uuid=role4.uuid, resource_uuid=resource_3.uuid, action="allow")
    permission41 = Permission(role_uuid=role4.uuid, resource_uuid=resource_11.uuid, action="allow")
    permission42 = Permission(role_uuid=role4.uuid, resource_uuid=resource_12.uuid, action="allow")
    permission43 = Permission(role_uuid=role4.uuid, resource_uuid=resource_13.uuid, action="allow")
    permission44 = Permission(role_uuid=role4.uuid, resource_uuid=resource_16.uuid, action="allow")
    permission45 = Permission(role_uuid=role4.uuid, resource_uuid=resource_17.uuid, action="allow")
    permission46 = Permission(role_uuid=role4.uuid, resource_uuid=resource_18.uuid, action="allow")
    #permission reader
    permission47 = Permission(role_uuid=role5.uuid, resource_uuid=resource_1.uuid, action="allow")
    permission48 = Permission(role_uuid=role5.uuid, resource_uuid=resource_2.uuid, action="allow")
    permission49 = Permission(role_uuid=role5.uuid, resource_uuid=resource_11.uuid, action="allow")
    permission50 = Permission(role_uuid=role5.uuid, resource_uuid=resource_12.uuid, action="allow")
    permission51 = Permission(role_uuid=role5.uuid, resource_uuid=resource_16.uuid, action="allow")
    permission52 = Permission(role_uuid=role5.uuid, resource_uuid=resource_17.uuid, action="allow")
    #permisson cusrole1
    permission53 = Permission(role_uuid=role6.uuid, resource_uuid=resource_4.uuid, action="allow")
    permission54 = Permission(role_uuid=role6.uuid, resource_uuid=resource_5.uuid, action="allow")
    #permission cusrole2
    permission55 = Permission(role_uuid=role7.uuid, resource_uuid=resource_14.uuid, action="allow")
    permission56 = Permission(role_uuid=role7.uuid, resource_uuid=resource_15.uuid, action="allow")

    permissions = [permission1, permission2, permission3, permission4, permission5, permission6,
            permission7, permission8, permission9, permission10, permission11, permission12,
            permission13, permission14, permission15, permission16, permission17, permission18,
            permission19, permission20, permission21, permission22, permission23, permission24,
            permission25, permission26, permission27, permission28, permission29, permission30,
            permission31, permission32, permission33, permission34, permission35, permission36,
            permission37, permission38, permission39, permission40, permission41, permission42,
            permission43, permission44, permission45, permission46, permission47, permission48,
            permission49, permission50, permission51, permission52, permission53, permission54,
            permission55, permission56]
    for item in permissions:
        session.add(item)
    
    _insert(session)
    session.close()