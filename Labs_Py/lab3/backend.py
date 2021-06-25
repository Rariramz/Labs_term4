import json

from backend import app, db
from flask import request
from backend.models import *

COMMANDS = {
    "help": "/help",
    "create_group": "/create_group",
    "join_group": "/join_group",
    "groups": "/groups",
    "invite": "/invite",
    "delete_group": "/delete_group",
    "group_info": "/group_info",
    "see_all_groups": "/see_all_groups",
}

fail = '❌'
notification = '📢'
waiting = '✏️'


if Group.query.get(1) is None:
    group = Group(id=1, name="main_chat", admin_id=None)
    db.session.add(group)
    db.session.commit()


@app.route('/', methods=["POST"])
def home():
    user_id = request.values["user_id"]
    message = request.values["message"]
    user = User.query.get(int(user_id))

    messages_to_users = []

    if user is None:
        user = User(id=user_id, active_group_id=1, last_command=None)
        db.session.add(user)
        user_group_rel = UserGroupRelations(user_id=user_id, group_id=1)
        db.session.add(user_group_rel)
        db.session.commit()
        messages_to_users.append((f"{notification} Вы присоединились к основной группе", user_id))

    if user.last_command is not None:
        if user.last_command == COMMANDS["create_group"]:
            group = Group.query.filter(Group.name == message).first()
            if group is None:
                create_group(message, user.id)
                messages_to_users.append((f'{notification} Создана группа "{message}"', user.id))
                messages_to_users.append((f'{notification} Вы присоединились к группе "{message}"', user.id))
            else:
                messages_to_users.append((f'{fail} Название "{message}" уже занято', user.id))
        elif user.last_command == COMMANDS["join_group"]:
            group = Group.query.filter(Group.name == message).first()
            if group is None:
                messages_to_users.append((f'{fail} Группа "{message}" не найдена', user.id))
            else:
                join_group(group.id, user.id)
                messages_to_users.append((f'{notification} Вы присоединились к группе "{group.name}"', user.id))
        elif user.last_command == COMMANDS["delete_group"]:
            group = Group.query.filter(Group.name == message).first()
            if group is None:
                messages_to_users.append((f'{fail} Группа "{message}" не найдена', user.id))
            else:
                if group.admin_id != user.id:
                    messages_to_users.append((f'{fail} Только админ может удалить группу "{message}"', user.id))
                else:
                    messages_to_users.append((f'{notification} Группа "{group.name}" удалена', user.id))
                    users = User.query.filter(User.active_group_id == group.id).filter(User.id != user.id).all()
                    for user in users:
                        messages_to_users.append((f'{notification} Группа "{group.name}" была удалена админом', user.id))
                    messages_to_users.append((f'{notification} Вы присоединились к группе "main_chat"', user.id))
                    delete_group(group.id, user.id)
        elif user.last_command == COMMANDS["invite"]:
            group = Group.query.filter(Group.id == user.active_group_id).first()
            try:
                message = int(message)
            except:
                messages_to_users.append((f'{fail} ID "{message}" не является корректным', user.id))
                user.last_command = None
                db.session.commit()
                return json.dumps(messages_to_users)
            new_user = User.query.filter(User.id == message).first()
            if new_user is None:
                messages_to_users.append((f'{fail} Пользователь с ID "{message}" не найден', user.id))
            else:
                new_user_group_rel = UserGroupRelations.query.filter(UserGroupRelations.user_id == new_user.id).\
                    filter(UserGroupRelations.group_id == group.id).first()
                if new_user_group_rel is not None:
                    messages_to_users.append((f'{notification} Пользователь с ID "{message}" уже состоит в группе "{group.name}"', user.id))
                else:
                    new_user_group_rel = UserGroupRelations(user_id=new_user.id, group_id=group.id)
                    db.session.add(new_user_group_rel)
                    join_group(group.id, new_user.id)
                    messages_to_users.append((f'{notification} Вы были приглашены в группу "{group.name}"', new_user.id))
                    messages_to_users.append((f'{notification} Вы пригласили пользователя с ID "{new_user.id}" в группу "{group.name}"', user.id))
        user.last_command = None
        db.session.commit()
    else:
        route(message, user.id, messages_to_users)
    return json.dumps(messages_to_users)


def route(message, user_id, messages_to_users):
    user = User.query.get(user_id)
    if message == COMMANDS["help"]:
        user.last_command = None
        res = f"{notification} Доступные комманды:"
        for command in COMMANDS:
            res += f"\n/{command}"
        messages_to_users.append((res, user.id))
    elif message == COMMANDS["create_group"]:
        user.last_command = COMMANDS["create_group"]
        messages_to_users.append((f"{waiting} Введите название для новой группы:", user.id))
    elif message == COMMANDS["join_group"]:
        user.last_command = COMMANDS["join_group"]
        messages_to_users.append((f"{waiting} Введите название группы, к которой хотите присоединиться:", user.id))
    elif message == COMMANDS["groups"]:
        user.last_command = None
        groups = Group.query.filter(user_id == user.id).all()
        res = f"{notification} Список групп, в которых вы состоите:"
        for group in groups:
            res += f"\n{group.name}"
        messages_to_users.append((res, user.id))
    elif message == COMMANDS["invite"]:
        user.last_command = COMMANDS["invite"]
        active_group = Group.query.get(user.active_group_id)
        messages_to_users.append((f'{waiting} Введите ID пользователя, которого нужно добавить в группу "{active_group.name}":', user.id))
    elif message == COMMANDS["delete_group"]:
        user.last_command = COMMANDS["delete_group"]
        messages_to_users.append((f"{waiting} Введите название группы, которую нужно удалить:", user.id))
    elif message == COMMANDS["group_info"]:
        user.last_command = None
        active_group = Group.query.get(user.active_group_id)
        all_users = get_users_list(active_group.id)
        active_users = get_active_users_list(active_group.id)
        users_count = len(all_users)
        active_users_count = len(active_users)
        messages_to_users.append((f'\n{notification} Группа: "{active_group.name}"\nКоличество участников: {users_count}\n'
                     f'Активные участники: {active_users_count}', user.id))
    elif message == COMMANDS["see_all_groups"]:
        user.last_command = None
        groups_admins = db.session.query(User, Group).join(User, Group.admin_id == User.id).all()
        res = f"{notification} Админы:"
        for admin, group in groups_admins:
            res += f'\n{admin.id} - "{group.name}"'
        messages_to_users.append((res, user.id))
    else:
        users = User.query.filter(User.active_group_id == user.active_group_id).filter(User.id != user.id).all()
        for user in users:
            messages_to_users.append((message, user.id))
    db.session.commit()


def get_users_list(group_id):
    user_group_rel = UserGroupRelations.query.filter(UserGroupRelations.group_id == group_id).all()
    return user_group_rel


def get_active_users_list(group_id):
    active_users = User.query.filter(User.active_group_id == group_id).all()
    return active_users


def delete_group(group_id, user_id):
    group = Group.query.filter(Group.id == group_id).first()
    for member in get_active_users_list(group.id):
        join_group(1, member.id)
    UserGroupRelations.query.filter(UserGroupRelations.group_id == group.id).delete()
    Group.query.filter(Group.id == group_id).delete()
    db.session.commit()


def create_group(group_name, user_id):
    new_group = Group(name=group_name, admin_id=user_id)
    db.session.add(new_group)
    db.session.commit()
    new_user_group_rel = UserGroupRelations(user_id=user_id, group_id=new_group.id)
    db.session.add(new_user_group_rel)
    db.session.commit()
    join_group(new_group.id, user_id)


def join_group(group_id, user_id):
    group = Group.query.get(group_id)
    user = User.query.get(user_id)
    user_group_rel = UserGroupRelations.query.filter(user_id == user_id).filter(group_id == group.id).first()
    if user_group_rel is None:
        user_group_rel = UserGroupRelations(user_id=user_id, group_id=group.id)
        user.active_group_id = group.id
        db.session.add(group)
        db.session.add(user_group_rel)
    else:
        user.active_group_id = group.id
    db.session.commit()


app.run(host="0.0.0.0", port=8000)
