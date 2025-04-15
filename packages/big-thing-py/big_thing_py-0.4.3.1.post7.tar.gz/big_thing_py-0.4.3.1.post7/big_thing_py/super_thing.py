from big_thing_py.big_thing import *
from big_thing_py.super import *
import threading


class MXSuperThing(MXBigThing):
    DEFAULT_NAME = 'default_super_thing'
    REFRESH_CYCLE_SCALER = 2.1

    # Super Service Execution 요청이 들어왔을때 mapping_table에 있는 super_request를 찾기 위한 super_service_request_key 리스트
    # Super Service는 자신의 이름으로 super_request_key를 찾을 수 있다.
    # {
    #     'super_service_request_key1': ['sub_service_request_key1', 'sub_service_request_key2', ...]},
    #     'super_service_request_key2': ['sub_service_request_key3', 'sub_service_request_key4', ...]},
    #      ...
    # }
    _SUPER_SERVICE_REQUEST_KEY_TABLE: Dict[str, List[str]] = dict()

    def __init__(
        self,
        name: str = MXThing.DEFAULT_NAME,
        nick_name: str = MXThing.DEFAULT_NAME,
        category: DeviceCategory = DeviceCategory.SuperThing,
        device_type: MXDeviceType = MXDeviceType.NORMAL,
        desc: str = '',
        version: str = sdk_version(),
        service_list: List[MXService] = [],
        alive_cycle: int = 60,
        is_super: bool = True,
        is_ble_wifi: bool = False,
        is_parallel: bool = True,
        is_builtin: bool = False,
        is_manager: bool = False,
        is_staff: bool = False,
        is_matter: bool = False,
        ip: str = '127.0.0.1',
        port: int = 1883,
        ssl_ca_path: str = '',
        ssl_cert_path: str = '',
        ssl_key_path: str = '',
        log_path: str = '',
        log_enable: bool = True,
        log_mode: MXPrintMode = MXPrintMode.ABBR,
        async_log: bool = False,
        append_mac_address: bool = True,
        no_wait_request_register: bool = False,
        kvs_storage_path: str = DEFAULT_KVS_STORAGE_PATH,
        reset_kvs: bool = False,
        refresh_cycle: float = 30,
    ):
        self._global_service_table: Dict[str, Union[List[MXFunction], List[MXValue]]] = dict(values=[], functions=[])
        self._SUPER_SERVICE_REQUEST_KEY_TABLE = dict()

        super().__init__(
            name=name,
            nick_name=nick_name,
            category=category,
            device_type=device_type,
            desc=desc,
            version=version,
            service_list=service_list,
            alive_cycle=alive_cycle,
            is_super=is_super,
            is_ble_wifi=is_ble_wifi,
            is_parallel=is_parallel,
            is_builtin=is_builtin,
            is_manager=is_manager,
            is_staff=is_staff,
            is_matter=is_matter,
            ip=ip,
            port=port,
            ssl_ca_path=ssl_ca_path,
            ssl_cert_path=ssl_cert_path,
            ssl_key_path=ssl_key_path,
            log_path=log_path,
            log_enable=log_enable,
            log_mode=log_mode,
            async_log=async_log,
            append_mac_address=append_mac_address,
            no_wait_request_register=no_wait_request_register,
            kvs_storage_path=kvs_storage_path,
            reset_kvs=reset_kvs,
        )

        self._refresh_cycle = refresh_cycle
        self._last_refresh_time = 0

        self._receive_queue: Dict[MXProtocolType, asyncio.Queue] = {
            k: asyncio.Queue()
            for k in [
                MXProtocolType.Base.MT_REQUEST_REGISTER_INFO,
                MXProtocolType.Base.MT_REQUEST_UNREGISTER,
                MXProtocolType.Base.MT_RESULT_REGISTER,
                MXProtocolType.Base.MT_RESULT_UNREGISTER,
                MXProtocolType.Base.MT_RESULT_BINARY_VALUE,
                MXProtocolType.Super.MS_RESULT_SCHEDULE,
                MXProtocolType.Super.MS_RESULT_EXECUTE,
                MXProtocolType.Super.MS_RESULT_SERVICE_LIST,
                MXProtocolType.Super.MS_SCHEDULE,
                MXProtocolType.Super.MS_EXECUTE,
                MXProtocolType.Base.MT_EXECUTE,
                MXProtocolType.WebClient.ME_NOTIFY_CHANGE,
                MXProtocolType.WebClient.ME_RESULT_HOME,
            ]
        }

        self._super_task_list: List[Dict[str, asyncio.Task]] = []

    def __eq__(self, o: 'MXSuperThing'):
        instance_check = isinstance(o, MXSuperThing)
        refresh_cycle_check = self._refresh_cycle == o._refresh_cycle

        return super().__eq__(o) and instance_check and refresh_cycle_check

    def __getstate__(self):
        state = super().__getstate__()

        state['_refresh_cycle'] = self._refresh_cycle

        del state['_last_refresh_time']

        return state

    def __setstate__(self, state):
        super().__setstate__(state)

        self._refresh_cycle = state['_refresh_cycle']

        self._last_refresh_time = 0

    @override
    async def _setup(self) -> 'MXSuperThing':
        self._extract_sub_service_request_info()
        return await super()._setup()

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    @override
    async def _RUNNING_state_process(self):
        # MQTT receive handling
        if not self._receive_queue_empty():
            recv_msg = await self._receive_queue_get()
            error = await self._handle_mqtt_message(recv_msg, target_thing=self._thing_data)
            if not error in MXBigThing.HANDLE_MQTT_MESSAGE_IGNORE_ERROR_LIST:
                MXLOG_CRITICAL(f'[{get_current_function_name()}] MQTT Message handling failed, error: {error}')

        # Value publish handling
        current_time = get_current_datetime()
        for value in self.value_list:
            # NOTE (thsvkd): If Thing is not Manager of Staff, I think event-based value feature is not needed...
            # elif current_time - value.last_update_time > value.cycle and value.cycle != 0:
            if not value.is_initialized or current_time - value.last_update_time > value.cycle:
                new_value = await value.async_update()
                if new_value is None:
                    continue

                self._send_TM_VALUE_PUBLISH(value)

        # Alive handling
        if current_time - self.last_alive_time > self.alive_cycle / MXBigThing.ALIVE_CYCLE_SCALER:
            self._send_TM_ALIVE(self._thing_data)

        # Refresh handling
        if current_time - self._last_refresh_time > self._refresh_cycle / MXSuperThing.REFRESH_CYCLE_SCALER:
            self._send_SM_REFRESH()

    # ======================================================================================================================= #
    #  _    _                    _  _         __  __   ____  _______  _______   __  __                                        #
    # | |  | |                  | || |       |  \/  | / __ \|__   __||__   __| |  \/  |                                       #
    # | |__| |  __ _  _ __    __| || |  ___  | \  / || |  | |  | |      | |    | \  / |  ___  ___  ___   __ _   __ _   ___    #
    # |  __  | / _` || '_ \  / _` || | / _ \ | |\/| || |  | |  | |      | |    | |\/| | / _ \/ __|/ __| / _` | / _` | / _ \   #
    # | |  | || (_| || | | || (_| || ||  __/ | |  | || |__| |  | |      | |    | |  | ||  __/\__ \\__ \| (_| || (_| ||  __/   #
    # |_|  |_| \__,_||_| |_| \__,_||_| \___| |_|  |_| \___\_\  |_|      |_|    |_|  |_| \___||___/|___/ \__,_| \__, | \___|   #
    #                                                                                                         __/ |           #
    #                                                                                                         |___/           #
    # ======================================================================================================================= #

    @override
    async def _handle_mqtt_message(self, msg: MQTTMessage, target_thing: MXThing, state_change: bool = True) -> bool:
        topic_string = decode_MQTT_message(msg)[0]
        protocol = MXProtocolType.get(topic_string)

        if protocol == MXProtocolType.Super.MS_RESULT_SCHEDULE:
            error = self._handle_MS_RESULT_SCHEDULE(msg)
        elif protocol == MXProtocolType.Super.MS_RESULT_EXECUTE:
            error = self._handle_MS_RESULT_EXECUTE(msg)
        elif protocol == MXProtocolType.Super.MS_RESULT_SERVICE_LIST:
            error = self._handle_MS_RESULT_SERVICE_LIST(msg)
        elif protocol == MXProtocolType.Super.MS_SCHEDULE:
            error = await self._handle_MS_SCHEDULE(msg)
        elif protocol == MXProtocolType.Super.MS_EXECUTE:
            error = self._handle_MS_EXECUTE(msg)
        elif protocol == MXProtocolType.WebClient.ME_NOTIFY_CHANGE:
            error = self._handle_ME_NOTIFY(msg)
        elif protocol == MXProtocolType.Base.MT_EXECUTE:
            MXLOG_WARN(f'[{get_current_function_name()}] Not permitted topic! topic: {topic_string}')
            return False
        else:
            error = await super()._handle_mqtt_message(msg, target_thing=target_thing, state_change=state_change)

        return error

    # ================
    # ___  ___ _____
    # |  \/  |/  ___|
    # | .  . |\ `--.
    # | |\/| | `--. \
    # | |  | |/\__/ /
    # \_|  |_/\____/
    # ================

    async def _handle_MS_SCHEDULE(self, msg: MQTTMessage) -> MXErrorCode:
        super_schedule_msg = MXSuperScheduleMessage(msg)
        target_super_service = self._get_function(super_schedule_msg.super_service_name)

        if not target_super_service:
            MXLOG_ERROR(f'[{get_current_function_name()}] Super Service {super_schedule_msg.super_service_name} does not exist...')
            return MXErrorCode.TARGET_NOT_FOUND
        if self.name != super_schedule_msg.super_thing_name:
            MXLOG_ERROR(f'[{get_current_function_name()}] Super Thing name {super_schedule_msg.super_thing_name} is not matched...')
            return MXErrorCode.TARGET_NOT_FOUND
        if self.middleware_name != super_schedule_msg.super_middleware_name:
            MXLOG_ERROR(f'[{get_current_function_name()}] Super Middleware name {super_schedule_msg.super_middleware_name} is not matched...')
            return MXErrorCode.TARGET_NOT_FOUND
        if super_schedule_msg.topic_error or super_schedule_msg.payload_error:
            MXLOG_ERROR(f'[{get_current_function_name()}] super_schedule_msg Message has error!')
            return MXErrorCode.FAIL
        if not self._is_super_service_available(target_super_service):
            MXLOG_ERROR(f'[{get_current_function_name()}] Super Service {target_super_service.name} is not available...')

            return MXErrorCode.TARGET_NOT_FOUND

        def super_schedule_callback(task: asyncio.Task):
            if task.cancelled():
                MXLOG_ERROR(f'[{get_current_function_name()}] Super Schedule cancelled...')
            if task.exception():
                exception = task.exception()
                if exception == asyncio.TimeoutError:
                    MXLOG_ERROR(f'[{get_current_function_name()}] Super Schedule timeout...')
                MXLOG_ERROR(f'[{get_current_function_name()}] Super Schedule failed...')
                self._publish(super_schedule_msg.topic, super_schedule_msg.payload)
            if task.done():
                if task.result() == MXErrorCode.NO_ERROR:
                    MXLOG_DEBUG(f'[{get_current_function_name()}] Super Schedule success...')
                    self._publish(super_schedule_msg.topic, super_schedule_msg.payload)
                else:
                    MXLOG_ERROR(f'[{get_current_function_name()}] Super Schedule failed...')
                    self._publish(super_schedule_msg.topic, super_schedule_msg.payload)

        task = asyncio.create_task(target_super_service.schedule())
        task = asyncio.wait_for(task, timeout=self)
        task.add_done_callback(super_schedule_callback)
        result = await task

        return result

        schedule_thread = target_super_service.start_super_schedule_thread(super_schedule_msg, self._global_service_table, timeout=1000)
        if not schedule_thread:
            return MXErrorCode.FAIL
        elif schedule_thread.is_alive():
            return MXErrorCode.NO_ERROR
        else:
            return MXErrorCode.FAIL

    def _handle_MS_EXECUTE(self, msg: MQTTMessage) -> MXErrorCode:
        super_execute_msg = MXSuperExecuteMessage(msg)
        target_super_service = self._get_function(super_execute_msg.super_service_name)

        if not target_super_service:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Service {super_execute_msg.super_service_name} does not exist...',
                'red',
            )
            return MXErrorCode.TARGET_NOT_FOUND
        if self.name != super_execute_msg.super_thing_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Thing name {super_execute_msg.super_thing_name} is not matched...',
                'red',
            )
            return MXErrorCode.TARGET_NOT_FOUND
        if self.middleware_name != super_execute_msg.super_middleware_name:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Middleware name {super_execute_msg.super_middleware_name} is not matched...',
                'red',
            )
            return MXErrorCode.TARGET_NOT_FOUND
        if super_execute_msg.topic_error or super_execute_msg.payload_error:
            MXLOG_DEBUG(f'[{get_current_function_name()}] super_execute_msg Message has error!', 'red')
            return MXErrorCode.FAIL

        # 중복된 시나리오로부터 온 실행 요청이면 -4 에러코드를 보낸다.
        if super_execute_msg.scenario in target_super_service.running_scenario_list:
            target_super_service._send_SM_RESULT_EXECUTE(
                super_service_name=super_execute_msg.super_service_name,
                super_thing_name=super_execute_msg.super_thing_name,
                super_middleware_name=super_execute_msg.super_middleware_name,
                requester_middleware_name=super_execute_msg.requester_middleware_name,
                scenario=super_execute_msg.scenario,
                error=MXErrorCode.DUPLICATE,
            )
            return MXErrorCode.NO_ERROR

        super_execute_thread = target_super_service.start_super_execute_thread(super_execute_msg, self._SUPER_SERVICE_REQUEST_KEY_TABLE)
        if not super_execute_thread:
            return MXErrorCode.FAIL
        else:
            return MXErrorCode.NO_ERROR

    def _handle_MS_RESULT_SCHEDULE(self, msg: MQTTMessage) -> MXErrorCode:
        subschedule_result_msg = MXSubScheduleResultMessage(msg)
        subschedule_result_msg.set_timestamp()
        super_service_request_key = make_super_request_key(
            scenario_name=subschedule_result_msg.scenario,
            requester_middleware_name=subschedule_result_msg.requester_middleware_name,
        )
        sub_service_request_key = make_sub_service_request_key(
            sub_service_name=subschedule_result_msg.sub_service_name,
            sub_service_request_order=subschedule_result_msg.sub_service_request_order,
        )

        target_super_service = self._get_function(subschedule_result_msg.super_service_name)
        if not target_super_service:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Service {subschedule_result_msg.super_service_name} does not exist...',
                'yellow',
            )
            return MXErrorCode.TARGET_NOT_FOUND

        result = target_super_service.put_subschedule_result(super_service_request_key, sub_service_request_key, subschedule_result_msg)
        return result

    def _handle_MS_RESULT_EXECUTE(self, msg: MQTTMessage) -> MXErrorCode:
        sub_service_execute_result_msg = MXSubExecuteResultMessage(msg)
        sub_service_execute_result_msg.set_timestamp()
        super_service_request_key = make_super_request_key(
            scenario_name=sub_service_execute_result_msg.scenario,
            requester_middleware_name=sub_service_execute_result_msg.requester_middleware_name,
        )
        sub_service_request_key = make_sub_service_request_key(
            sub_service_name=sub_service_execute_result_msg.sub_service_name,
            sub_service_request_order=sub_service_execute_result_msg.sub_service_request_order,
        )

        target_super_service = self._get_function(sub_service_execute_result_msg.super_service_name)
        if not target_super_service:
            MXLOG_DEBUG(
                f'[{get_current_function_name()}] Super Service {sub_service_execute_result_msg.super_service_name} does not exist...',
                'yellow',
            )
            return MXErrorCode.TARGET_NOT_FOUND

        result = target_super_service.put_sub_service_execute_result(
            super_service_request_key, sub_service_request_key, sub_service_execute_result_msg
        )
        return result

    def _handle_MS_RESULT_SERVICE_LIST(self, msg: MQTTMessage) -> MXErrorCode:
        try:
            service_list = MXSuperServiceListResultMessage(msg)
            service_list.set_timestamp()

            for middleware in service_list.service_list:
                hierarchy_type = middleware['hierarchy']
                if not hierarchy_type in ['local', 'child']:
                    MXLOG_DEBUG(f'[{get_current_function_name()}] Parent middleware is not supported', 'red')
                    return MXErrorCode.FAIL

                middleware_name = middleware['middleware']
                if not middleware_name:
                    MXLOG_DEBUG(f'[{get_current_function_name()}] Middleware name does not exist', 'red')
                    return MXErrorCode.FAIL

                thing_list = middleware['things']
                for thing in thing_list:
                    is_alive = thing['is_alive']
                    if is_alive != 1:
                        continue

                    is_super = thing['is_super']
                    alive_cycle = thing['alive_cycle']

                    # value 정보를 추출
                    value_service_list = self._extract_value_info(thing=thing, middleware_name=middleware_name)
                    self._global_service_table['values'].extend(value_service_list)

                    function_service_list = self._extract_function_info(thing_info=thing, middleware_name=middleware_name)
                    self._global_service_table['functions'].extend(function_service_list)

            self._last_refresh_time = get_current_datetime()
            return MXErrorCode.NO_ERROR
        except KeyError as e:
            print_error(e)
            MXLOG_DEBUG(f'[{get_current_function_name()}] KeyError', 'red')
            return MXErrorCode.FAIL
        except ValueError as e:
            print_error(e)
            MXLOG_DEBUG(f'[{get_current_function_name()}] ValueError', 'red')
            return MXErrorCode.FAIL
        except Exception as e:
            print_error(e)
            MXLOG_DEBUG(f'[{get_current_function_name()}] Unknown Exception', 'red')
            return MXErrorCode.FAIL

    # ===================
    #   __  __   ______
    #  |  \/  | |  ____|
    #  | \  / | | |__
    #  | |\/| | |  __|
    #  | |  | | | |____
    #  |_|  |_| |______|
    # ===================

    def _handle_ME_NOTIFY(self, msg: MQTTMessage) -> MXErrorCode:
        notify_msg = MXNotifyMessage(msg)
        notify_msg.set_timestamp()
        self._send_SM_REFRESH()

        return MXErrorCode.NO_ERROR

    # ================
    #  _____ ___  ___
    # /  ___||  \/  |
    # \ `--. | .  . |
    #  `--. \| |\/| |
    # /\__/ /| |  | |
    # \____/ \_|  |_/
    # ================

    def _send_SM_EXECUTE(self, sub_service_execute_msg: MXSubExecuteMessage) -> None:
        sub_service_execute_mqtt_msg = sub_service_execute_msg.mqtt_message()
        self._publish(sub_service_execute_mqtt_msg.topic, sub_service_execute_mqtt_msg.payload)

    def _send_SM_REFRESH(self):
        super_refresh_msg = self.generate_super_refresh_message()
        super_refresh_mqtt_msg = super_refresh_msg.mqtt_message()
        self._publish(super_refresh_mqtt_msg.topic, super_refresh_mqtt_msg.payload)
        self._last_refresh_time = get_current_datetime()

    # ===================================================================================
    # ___  ___ _____  _____  _____   _____         _  _  _                   _
    # |  \/  ||  _  ||_   _||_   _| /  __ \       | || || |                 | |
    # | .  . || | | |  | |    | |   | /  \/  __ _ | || || |__    __ _   ___ | | __ ___
    # | |\/| || | | |  | |    | |   | |     / _` || || || '_ \  / _` | / __|| |/ // __|
    # | |  | |\ \/' /  | |    | |   | \__/\| (_| || || || |_) || (_| || (__ |   < \__ \
    # \_|  |_/ \_/\_\  \_/    \_/    \____/ \__,_||_||_||_.__/  \__,_| \___||_|\_\|___/
    # ===================================================================================

    @override
    async def _on_message(self, client: MQTTClient, topic, payload, qos, properties):
        # topic, payload = decode_MQTT_message(msg)
        self._print_packet(topic=topic, payload=payload, direction=Direction.RECEIVED, mode=self._log_mode)
        msg = encode_MQTT_message(topic, payload)

        protocol = MXProtocolType.get(topic)
        if protocol in [
            MXProtocolType.Base.MT_REQUEST_REGISTER_INFO,
            MXProtocolType.Base.MT_REQUEST_UNREGISTER,
            MXProtocolType.Base.MT_RESULT_REGISTER,
            MXProtocolType.Base.MT_RESULT_UNREGISTER,
            MXProtocolType.Base.MT_RESULT_BINARY_VALUE,
            MXProtocolType.Super.MS_RESULT_SCHEDULE,
            MXProtocolType.Super.MS_RESULT_EXECUTE,
            MXProtocolType.Super.MS_RESULT_SERVICE_LIST,
            MXProtocolType.Super.MS_SCHEDULE,
            MXProtocolType.Super.MS_EXECUTE,
            MXProtocolType.Base.MT_EXECUTE,
            MXProtocolType.WebClient.ME_NOTIFY_CHANGE,
            MXProtocolType.WebClient.ME_RESULT_HOME,
        ]:
            await self._receive_queue[protocol].put(msg)
        else:
            MXLOG_CRITICAL(f'[{get_current_function_name()}] Unexpected topic! topic: {topic}')

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def generate_super_refresh_message(self) -> MXSuperRefreshMessage:
        super_refresh_msg = MXSuperRefreshMessage(self.name)
        return super_refresh_msg

    @override
    def _get_function(self, function_name: str) -> MXSuperFunction:
        for function in self.function_list:
            if function.name == function_name:
                return function

    @override
    def _subscribe_init_topic_list(self, thing_data: MXThing):
        super()._subscribe_init_topic_list(thing_data)

        topic_list = [
            MXProtocolType.Super.MS_RESULT_SERVICE_LIST.value % "#",
        ]

        for topic in topic_list:
            self._subscribe(topic)

    @override
    def _subscribe_service_topic_list(self, thing_data: MXThing):
        topic_list = []
        for function in thing_data.function_list:
            # Super Schedule, Super Execute에 필요한 토픽들을 미리 구독을 해놓는다.
            topic_list += [
                MXProtocolType.Super.MS_SCHEDULE.value % (function.name, thing_data.name, thing_data.middleware_name, '#'),
                MXProtocolType.Super.MS_RESULT_SCHEDULE.value % ('+', '+', '#'),
                MXProtocolType.Super.MS_EXECUTE.value % (function.name, thing_data.name, thing_data.middleware_name, '#'),
                MXProtocolType.Super.MS_RESULT_EXECUTE.value % ('+', '+', '#'),
            ]

        for topic in topic_list:
            self._subscribe(topic)

    def _request_sub_service_execute(self, sub_service_execute_request: MXSubExecuteRequest) -> None:
        if not isinstance(sub_service_execute_request, MXSubExecuteRequest):
            raise MXTypeError(f'[{get_current_function_name()}] Invalid type of sub_service_execute_request: {type(sub_service_execute_request)}')

        sub_service_execute_msg = sub_service_execute_request.trigger_msg
        self._send_SM_EXECUTE(sub_service_execute_msg)

    # 하나의 sub_service_request에 있는 sub_service_execute_request들을 병렬로 실행한다.
    def _sub_service_execute_parallel(
        self, sub_service_execute_request_list: List[MXSubExecuteRequest], arg_list: List[MXDataType]
    ) -> List[MXDataType]:
        result_list = []
        for i, sub_service_execute_request in enumerate(sub_service_execute_request_list):
            sub_service_execute_request.timer_start()
            sub_service_execute_request.trigger_msg.arguments = tuple(arg_list)

            sub_service_execute_msg = sub_service_execute_request.trigger_msg
            MXLOG_DEBUG(
                f'[SUB_EXECUTE START] {sub_service_execute_msg.sub_service_name}|{sub_service_execute_msg.target_middleware_name}|{sub_service_execute_msg.scenario}|{i}',
                'cyan',
            )
            self._request_sub_service_execute(sub_service_execute_request)

        for i, sub_service_execute_request in enumerate(sub_service_execute_request_list):
            sub_service_execute_request.result_msg = sub_service_execute_request.get_result_msg()
            sub_service_execute_request.timer_end()
            rc_msg = sub_service_execute_request.result_msg

            sub_service_execute_msg: MXSubExecuteMessage = sub_service_execute_request.trigger_msg
            sub_service_execute_result_msg: MXSubExecuteResultMessage = sub_service_execute_request.result_msg
            result_list.append(
                dict(
                    scenario=sub_service_execute_result_msg.scenario,
                    return_type=sub_service_execute_result_msg.return_type,
                    return_value=sub_service_execute_result_msg.return_value,
                    error=sub_service_execute_result_msg.error,
                )
            )

            MXLOG_DEBUG(
                f'[SUB_EXECUTE END] {sub_service_execute_msg.sub_service_name}|{sub_service_execute_msg.target_middleware_name}|{sub_service_execute_msg.scenario}|{i}'
                f'duration: {sub_service_execute_request.duration():.4f} Sec',
                'cyan',
            )

        return result_list

    def _get_sub_service_from_global_service_table(self, sub_service_name: str) -> MXFunction:
        for function in self._global_service_table['functions']:
            if function.name == sub_service_name:
                return function
        return None

    def _is_sub_service_available(self, sub_service_name: str, return_type: MXType):
        global_sub_service = self._get_sub_service_from_global_service_table(sub_service_name)
        if not global_sub_service:
            return False
        if not global_sub_service.return_type == return_type:
            return False

        return True

    def _check_req_valid(
        self,
        sub_service_name: str,
        tag_list: List[str],
        arg_list: Union[Tuple[MXArgument], Tuple],
        return_type: MXType,
        service_type: MXServiceType,
        range_type: MXRangeType,
    ):
        if not sub_service_name:
            raise MXValueError(f'sub_service_name must be not empty')
        if not tag_list:
            raise MXValueError(f'tag_list must be not empty')
        if not all(tag_list):
            raise MXValueError(f'tag in tag_list must be not empty string')
        if not service_type in [MXServiceType.VALUE, MXServiceType.FUNCTION]:
            raise MXTypeError(f'Invalid service_type: {service_type}')
        if not return_type in [MXType.INTEGER, MXType.DOUBLE, MXType.STRING, MXType.BOOL, MXType.BINARY, MXType.VOID]:
            raise MXTypeError(f'Invalid return_type: {return_type}')
        elif service_type == MXServiceType.VALUE and return_type == MXType.VOID:
            raise MXTypeError(f'Value service cannot have a return_type of void')
        if not range_type in [MXRangeType.SINGLE, MXRangeType.ALL]:
            raise MXTypeError(f'Invalid range_type: {range_type}')

        return True

    def _check_req_return_type(self, sub_service_return_type: MXType, req_return_type: MXType, service_type: MXServiceType):
        if req_return_type in [MXType.INTEGER, MXType.DOUBLE] and sub_service_return_type in [
            MXType.INTEGER,
            MXType.DOUBLE,
        ]:
            return True
        elif req_return_type == MXType.VOID and service_type == MXServiceType.VALUE:
            raise MXTypeError(f'Not matched return_type. Value service cannot have a return_type of void: {sub_service_return_type}')
        elif req_return_type != sub_service_return_type:
            raise MXTypeError(f'Not matched return_type: {sub_service_return_type} != {req_return_type}')

        return True

    def _is_super_service_available(self, super_service: MXSuperFunction):
        sub_service_status_map = {}
        for sub_service_request in super_service.sub_service_request_list:
            if len(sub_service_request.candidate_request_list) == 0:
                continue

            sub_service_name = sub_service_request.candidate_request_list[0].trigger_msg.sub_service_name
            sub_service_status = self._is_sub_service_available(
                sub_service_request._sub_service_type.name,
                sub_service_request._sub_service_type.return_type,
            )
            sub_service_status_map[sub_service_name] = sub_service_status

        available = False
        try:
            if not sub_service_status_map:
                MXLOG_WARN(
                    f'\tSub Services {", ".join([req.sub_service_type.name for req in super_service.sub_service_request_list])} is not exist', 'red'
                )
                return False

            unavailable_sub_service_list = [sub_service_name for sub_service_name, status in sub_service_status_map.items() if not status]
            if all([sub_service_status for sub_service_status in sub_service_status_map.keys()]):
                available = True
                return available
            else:
                for unavailable_sub_service_name in unavailable_sub_service_list:
                    MXLOG_WARN(f'\tSub Service {unavailable_sub_service_name} is not available', 'red')
                return False
        finally:
            if available:
                return True
            else:
                return False

    def req(
        self,
        sub_service_name: str,
        tag_list: List[str],
        arg_list: Union[Tuple[MXArgument], Tuple] = [],
        return_type: MXType = MXType.UNDEFINED,
        service_type: MXServiceType = MXServiceType.FUNCTION,
        range_type: MXRangeType = MXRangeType.SINGLE,
    ) -> Union[List[dict], bool]:
        # Detect fatal errors.
        # If an error occurs, the program terminates by raising an exception.
        if not self._check_req_valid(
            sub_service_name=sub_service_name,
            tag_list=tag_list,
            arg_list=arg_list,
            return_type=return_type,
            service_type=service_type,
            range_type=range_type,
        ):
            return False

        super_service_name = get_upper_function_name()
        target_super_service = self._get_function(super_service_name)
        target_sub_service = self._get_sub_service_from_global_service_table(sub_service_name)

        # Convert tag of type [str] to [MXTag]
        tag_list = [MXTag(str_tag) for str_tag in tag_list]

        if service_type == MXServiceType.VALUE:
            sub_service_name = f'__{sub_service_name}'
        elif service_type == MXServiceType.FUNCTION:
            sub_service_name = sub_service_name

        # When initiate a super thing, extract information about the super service.
        if not target_super_service.get_is_scanned():
            target_super_service.add_sub_service_request_info(
                sub_service_name=sub_service_name,
                arg_list=arg_list,
                tag_list=tag_list,
                return_type=return_type,
                range_type=range_type,
            )
            return []
        else:
            if not self._is_sub_service_available(sub_service_name, return_type):
                MXLOG_DEBUG(f'sub_service {sub_service_name} is not callable', 'red')
                return False
            if not self._compare_arg_list(target_sub_service.arg_list, list(arg_list)):
                MXLOG_DEBUG(f'Not matched arg_list')
                return False
            if not self._check_req_return_type(target_sub_service.return_type, req_return_type=return_type, service_type=service_type):
                MXLOG_DEBUG(f'Not matched return_type')
                return False

            current_thread = threading.current_thread()
            scenario_name = current_thread.user_data['scenario']
            requester_middleware_name = current_thread.user_data['requester_middleware']
            # super_service_request_key = scenario_name@requester_middleware_name
            super_service_request_key = make_super_request_key(scenario_name, requester_middleware_name)

            MXLOG_DEBUG(
                f'[DEBUG] before pop SUPER_SERVICE_REQUEST_KEY_TABLE: \n{dict_to_json_string(self._SUPER_SERVICE_REQUEST_KEY_TABLE, pretty=True)}'
                f'\n super_service_request_key: {super_service_request_key} '
            )
            sub_service_request_key_list = self._SUPER_SERVICE_REQUEST_KEY_TABLE[super_service_request_key]
            # sub_service_request_key = sub_service_name@sub_service_request_order
            sub_service_request_key = sub_service_request_key_list.pop(0)
            MXLOG_DEBUG(
                f'[DEBUG] after pop SUPER_SERVICE_REQUEST_KEY_TABLE: \n{dict_to_json_string(self._SUPER_SERVICE_REQUEST_KEY_TABLE, pretty=True)}'
                f'\n super_service_request_key: {super_service_request_key} '
            )
            if len(sub_service_request_key_list) == 0:
                self._SUPER_SERVICE_REQUEST_KEY_TABLE.pop(super_service_request_key)

            super_service_execute_request = target_super_service._mapping_table[super_service_request_key]
            sub_service_execute_request_list = super_service_execute_request._sub_service_request_table[sub_service_request_key]._target_request_list

            result_list = self._sub_service_execute_parallel(sub_service_execute_request_list, arg_list)
            return result_list

    # TODO: implement this
    def r(self, line: str = None, *arg_list) -> Union[List[dict], bool]:
        super_service_name = get_upper_function_name()

        range_type = 'all' if 'all' in line else 'single'
        function_name = line.split('.')[1][0 : line.split('.')[1].find('(')]
        bracket_parse: List[str] = re.findall(r'\(.*?\)', line)
        tags = [tag[1:] for tag in bracket_parse[0][1:-1].split(' ')]

        arguments = []
        for bracket_inner_element in bracket_parse[1][1:-1].split(','):
            bracket_inner_element = bracket_inner_element.strip(' ')
            if bracket_inner_element == '':
                continue
            else:
                arguments.append(bracket_inner_element)

        for i, arg in enumerate(arguments):
            if '$' in arg:
                index = int(arg[1:])
                arguments[i] = arg_list[index - 1]

        arguments = tuple(arguments)

    def _extract_sub_service_request_info(self) -> None:
        for function in self.function_list:
            if self.is_super and not function.get_is_scanned():
                arg_list = function.arg_list
                try:
                    MXLOG_DEBUG(f'Detect super service: {function.name}', 'green')
                    function._func(*tuple(arg_list))
                except MXError as e:
                    # req를 실행하다가 MySSIXError와 관련된 에러가 발생한다는 것은 req명세가 잘못
                    # 되었다는 것을 의미한다. 만약 MySSIXError에러가 아닌 다른 예외가 발생한 경우,
                    # super service안에 있는 코드 중, req() 코드 부분이 아닌 코드에 의한 예외이므로
                    # 정상적으로 req()에 대한 정보를 추출한 것이다.
                    raise e
                else:
                    function.set_is_scanned(True)

    def _extract_value_info(self, thing: dict, middleware_name: str) -> List[MXValue]:
        thing_name = thing['name']
        value_list = thing['values']

        value_service_list = []
        for value_info in value_list:
            value_tag_list = [MXTag(tag['name']) for tag in value_info['tags']]

            # TODO: cycle info is omit in service list
            value_service = MXValue(
                func=dummy_func(arg_list=[]),
                type=MXType.get(value_info['type']),
                bound=(float(value_info['bound']['min_value']), float(value_info['bound']['max_value'])),
                cycle=None,
                name=value_info['name'],
                tag_list=value_tag_list,
                desc=value_info['description'],
                thing_name=thing_name,
                middleware_name=middleware_name,
                format=value_info['format'] if not '(null)' in value_info['format'] else '',
            )
            if value_service not in self._global_service_table['values']:
                value_service_list.append(value_service)

        return value_service_list

    def _extract_function_info(self, thing_info: dict, middleware_name: str) -> List[MXFunction]:
        thing_name = thing_info['name']
        function_list = thing_info['functions']

        function_service_list = []
        for function_info in function_list:
            function_tag_list = [MXTag(tag['name']) for tag in function_info['tags']]
            arg_list = []
            if function_info['use_arg']:
                for argument in function_info['arguments']:
                    arg_list.append(
                        MXArgument(
                            name=argument['name'],
                            type=MXType.get(argument['type']),
                            bound=(float(argument['bound']['min_value']), float(argument['bound']['max_value'])),
                        )
                    )

            function_service = MXFunction(
                func=dummy_func(arg_list=arg_list),
                return_type=MXType.get(function_info['return_type']),
                name=function_info['name'],
                tag_list=function_tag_list,
                desc=function_info['description'],
                thing_name=thing_name,
                middleware_name=middleware_name,
                arg_list=arg_list,
                exec_time=function_info['exec_time'],
            )
            if function_service not in self._global_service_table['functions']:
                function_service_list.append(function_service)

        return function_service_list

    # ====================================
    #               _    _
    #              | |  | |
    #   __ _   ___ | |_ | |_   ___  _ __
    #  / _` | / _ \| __|| __| / _ \| '__|
    # | (_| ||  __/| |_ | |_ |  __/| |
    #  \__, | \___| \__| \__| \___||_|
    #   __/ |
    #  |___/
    # ====================================

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================
