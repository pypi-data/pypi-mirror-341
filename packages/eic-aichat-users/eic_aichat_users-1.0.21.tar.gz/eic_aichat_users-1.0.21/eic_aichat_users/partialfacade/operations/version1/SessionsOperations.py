# -*- coding: utf-8 -*-
import json
import bottle

from typing import Optional, Any
from pip_services4_components.refer import Descriptor, IReferences
from pip_services4_http.controller import RestOperations, RestController
from pip_services4_components.context import Context
from pip_services4_commons.convert import TypeCode
from pip_services4_data.validate import ObjectSchema

from eic_aichat_users.sessions.data import SessionV1
from eic_aichat_users.sessions.data.SessionV1Schema import SessionV1Schema
from eic_aichat_users.accounts.logic.IAccountsService import IAccountsService
from eic_aichat_users.passwords.logic.IPasswordsService import IPasswordsService
from eic_aichat_users.sessions.logic.ISessionsService import ISessionsService
from eic_aichat_users.roles.logic.IRolesService import IRolesService
from eic_aichat_users.settings.logic.ISettingsService import ISettingsService


class SessionsOperations(RestOperations):
    def __init__(self):
        super().__init__()
        self._accounts_service: IAccountsService = None
        self._passwords_service: IPasswordsService = None
        self._sessions_service: ISessionsService = None
        self._roles_service: IRolesService = None
        self._settings_service: ISettingsService = None
        self._dependency_resolver.put("accounts-service", Descriptor('aichatusers-accounts', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("passwords-service", Descriptor('aichatusers-passwords', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("sessions-service", Descriptor("aichatusers-sessions", "service", "*", "*", "1.0"))
        self._dependency_resolver.put("roles-service", Descriptor('aichatusers-roles', 'service', '*', '*', '1.0'))
        self._dependency_resolver.put("settings-service", Descriptor('aichatusers-settings', 'service', '*', '*', '1.0'))

    def configure(self, config):
        super().configure(config)

    def set_references(self, references: IReferences):
        super().set_references(references)
        self._accounts_service = self._dependency_resolver.get_one_required('accounts-service')
        self._passwords_service = self._dependency_resolver.get_one_required('passwords-service') 
        self._sessions_service = self._dependency_resolver.get_one_required("sessions-service")
        self._roles_service = self._dependency_resolver.get_one_required("roles-service")
        self._settings_service = self._dependency_resolver.get_one_required('settings-service')

    def get_sessions(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_sessions() invoked")

        filter_params = self._get_filter_params()
        paging_params = self._get_paging_params()
        try:
            res = self._sessions_service.get_sessions(context, filter_params, paging_params)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def get_session_by_id(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------get_session_by_id() invoked")

        try:
            res = self._sessions_service.get_session_by_id(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def open_session(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------open_session() invoked")

        data = bottle.request.json or {}
        try:
            res = self._sessions_service.open_session(
                context,
                data.get("user_id"),
                data.get("user_name"),
                data.get("address"),
                data.get("client"),
                data.get("user"),
                data.get("data"),
            )
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def store_session_data(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------store_session_data() invoked")

        data = bottle.request.json or {}
        try:
            res = self._sessions_service.store_session_data(context, session_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def update_session_user(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------update_session_user() invoked")

        data = bottle.request.json or {}
        try:
            res = self._sessions_service.update_session_user(context, session_id, data)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def close_session(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------close_session() invoked")

        try:
            res = self._sessions_service.close_session(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def delete_session_by_id(self, session_id):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------delete_session_by_id() invoked")

        try:
            res = self._sessions_service.delete_session_by_id(context, session_id)
            return self._send_result(res)
        except Exception as err:
            return self._send_error(err)

    def close_expired_sessions(self):
        context = Context.from_trace_id(self._get_trace_id())
        self._logger.info(context, "----------close_expired_sessions() invoked")

        try:
            self._sessions_service.close_expired_sessions(context)
            return self._send_empty_result()
        except Exception as err:
            return self._send_error(err)

    # TODO: to finalize the logic in the methods. Tidy up the paths
    def register_routes(self, controller: RestController):
        controller.register_route("get", "/sessions", None, self.get_sessions)

        controller.register_route("get", "/sessions/<session_id>", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.get_session_by_id)

        controller.register_route("post", "/sessions/open", ObjectSchema(True)
                                  .with_required_property("user_id", TypeCode.String)
                                  .with_required_property("user_name", TypeCode.String),
                                  self.open_session)

        controller.register_route("post", "/sessions/<session_id>/data", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.store_session_data)

        controller.register_route("post", "/sessions/<session_id>/user", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.update_session_user)

        controller.register_route("post", "/sessions/<session_id>/close", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.close_session)

        controller.register_route("delete", "/sessions/<session_id>", ObjectSchema(True)
                                  .with_required_property("session_id", TypeCode.String),
                                  self.delete_session_by_id)

        controller.register_route("post", "/sessions/cleanup", None, self.close_expired_sessions)
