import asyncio
import json
from typing import Any, Optional, List, Dict, Union

from grok3api.history import History, SenderType
from grok3api.types.GrokResponse import GrokResponse
from grok3api import driver
from grok3api.grok3api_logger import logger


class GrokClient:
    """
    Клиент для работы с Grok.

    :param use_xvfb: Флаг для использования Xvfb. По умолчанию True. Имеет значения только на Linux.
    :param proxy: (str) URL Прокси сервера, используется только в случае региональной блокировки.
    :param history_msg_count: Количество сообщений в истории (по умолчанию `0` - сохранение истории отключено).
    :param history_path: Путь к файлу с историей в JSON-формате. По умолчанию: "chat_histories.json"
    :param history_as_json: Отправить ли в Grok историю в формате JSON (для history_msg_count > 0). По умолчанию: True
    :param history_auto_save: Автоматическая перезапись истории в файл после каждого сообщения. По умолчанию: True
    :param timeout: Максимальное время на инициализацию клиента. По умолчанию: 120 секунд
    """

    NEW_CHAT_URL = "https://grok.com/rest/app-chat/conversations/new"
    def __init__(self,
                 cookies: Union[Union[str, List[str]], Union[dict, List[dict]]],
                 use_xvfb: bool = True,
                 proxy: Optional[str] = None,
                 history_msg_count: int = 0,
                 history_path: str = "chat_histories.json",
                 history_as_json: bool = True,
                 history_auto_save: bool = True,
                 timeout: int = driver.TIMEOUT):
        try:
            self.cookies = cookies
            self.proxy = proxy
            self.use_xvfb: bool = use_xvfb
            self.history = History(history_msg_count=history_msg_count,
                                   history_path=history_path,
                                   history_as_json=history_as_json)
            self.history_auto_save: bool = history_auto_save
            self.proxy_index = 0

            driver.init_driver(use_xvfb=self.use_xvfb, timeout=timeout, proxy=self.proxy)
        except Exception as e:
            logger.error(f"В GrokClient.__init__: {e}")
            raise e

    def _send_request(self,
                      payload,
                      headers,
                      timeout=driver.TIMEOUT):
        try:
            """Отправляем запрос через браузер с таймаутом."""

            headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Content-Type": "application/json",
                "Origin": "https://grok.com",
                "Referer": "https://grok.com/",
                "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            })

            fetch_script = f"""
            const controller = new AbortController();
            const signal = controller.signal;
            setTimeout(() => controller.abort(), {timeout * 1000});
        
            const payload = {json.dumps(payload)};
            return fetch('{self.NEW_CHAT_URL}', {{
                method: 'POST',
                headers: {json.dumps(headers)},
                body: JSON.stringify(payload),
                credentials: 'include',
                signal: signal
            }})
            .then(response => {{
                if (!response.ok) {{
                    return response.text().then(text => 'Error: HTTP ' + response.status + ' - ' + text);
                }}
                return response.text();
            }})
            .catch(error => {{
                if (error.name === 'AbortError') {{
                    return 'TimeoutError';
                }}
                return 'Error: ' + error;
            }});
            """

            response = driver.DRIVER.execute_script(fetch_script)

            if isinstance(response, str) and response.startswith('Error:'):
                error_data = handle_str_error(response)
                if isinstance(error_data, dict):
                    return error_data

            if response and 'This service is not available in your region' in response:
                return 'This service is not available in your region'
            final_dict = {}
            for line in response.splitlines():
                try:
                    parsed = json.loads(line)
                    if "modelResponse" in parsed["result"]["response"]:
                        final_dict = parsed
                        break
                except (json.JSONDecodeError, KeyError):
                    continue
            logger.debug(f"Получили ответ: {final_dict}")
            return final_dict
        except Exception as e:
            logger.error(f"В _send_request: {e}")
            return {}

    def send_message(self,
            message: str,
            history_id: Optional[str] = None,
            proxy: Optional[str] = driver.def_proxy,
            **kwargs: Any) -> GrokResponse:
        """Устаревший метод отправки сообщения. Используйте ask() напрямую."""

        return self.ask(message=message,
                   history_id=history_id,
                   proxy=proxy,
                   **kwargs)

    def ask(self,
            message: str,
            history_id: Optional[str] = None,
            proxy: Optional[str] = driver.def_proxy,
            timeout: int = 120,
            temporary: bool = False,
            modelName: str = "grok-3",
            fileAttachments: Optional[List[Dict[str, str]]] = None,
            imageAttachments: Optional[List[Dict[str, str]]] = None,
            customInstructions: str = "",
            deepsearch_preset: str = "",
            disableSearch: bool = False,
            enableImageGeneration: bool = True,
            enableImageStreaming: bool = True,
            enableSideBySide: bool = True,
            imageGenerationCount: int = 4,
            isPreset: bool = False,
            isReasoning: bool = False,
            returnImageBytes: bool = False,
            returnRawGrokInXaiRequest: bool = False,
            sendFinalMetadata: bool = True,
            toolOverrides: Optional[Dict[str, Any]] = None
            ) -> GrokResponse:
        """
        Отправляет запрос к API Grok с одним сообщением и дополнительными параметрами.

        Args:
            message (str): Сообщение пользователя для отправки в API.
            history_id (Optional[str]): Идентификатор для определения, какую историю чата использовать.
            proxy (Optional[str]): URL прокси-сервера, используется только в случае региональной блокировки.
            timeout (int): Таймаут (в секундах) на ожидание ответа. По умолчанию: 120.
            temporary (bool): Указывает, является ли сессия или запрос временным. По умолчанию False.
            modelName (str): Название модели ИИ для обработки запроса. По умолчанию "grok-3".
            fileAttachments (Optional[List[Dict[str, str]]]): Список вложений файлов. Каждый элемент — словарь с ключами "name" и "content".
            imageAttachments (Optional[List[Dict[str, str]]]): Список вложений изображений, аналогично fileAttachments.
            customInstructions (str): Дополнительные инструкции или контекст для модели. По умолчанию пустая строка.
            deepsearch_preset (str): Предустановка для глубокого поиска. По умолчанию пустая строка.
            disableSearch (bool): Отключить функцию поиска модели. По умолчанию False.
            enableImageGeneration (bool): Включить генерацию изображений в ответе. По умолчанию True.
            enableImageStreaming (bool): Включить потоковую передачу изображений. По умолчанию True.
            enableSideBySide (bool): Включить отображение информации бок о бок. По умолчанию True.
            imageGenerationCount (int): Количество генерируемых изображений. По умолчанию 4.
            isPreset (bool): Указывает, является ли сообщение предустановленным. По умолчанию False.
            isReasoning (bool): Включить режим рассуждений в ответе модели. По умолчанию False.
            returnImageBytes (bool): Возвращать данные изображений в виде байтов. По умолчанию False.
            returnRawGrokInXaiRequest (bool): Возвращать необработанный вывод от модели. По умолчанию False.
            sendFinalMetadata (bool): Отправлять финальные метаданные с запросом. По умолчанию True.
            toolOverrides (Optional[Dict[str, Any]]): Словарь для переопределения настроек инструментов. По умолчанию пустой словарь.

        Return:
            GrokResponse: Ответ от API Grok в виде объекта.
        """
        try:
            base_headers = {
                "Content-Type": "application/json",
                "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"),
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Origin": "https://grok.com",
                "Referer": "https://grok.com/",
            }

            headers = base_headers.copy()

            if (self.history.history_msg_count < 1 and self.history.main_system_prompt is None
                    and history_id not in self.history.system_prompts):
                message_payload = message
            else:
                message_payload = self.history.get_history(history_id) + '\n' + message
                if self.history.history_msg_count > 0:
                    self.history.add_message(history_id, SenderType.ASSISTANT, message)
                    if self.history_auto_save:
                        self.history.to_file()

            payload = {
                "temporary": temporary,
                "modelName": modelName,
                "message": message_payload,
                "fileAttachments": fileAttachments if fileAttachments is not None else [],
                "imageAttachments": imageAttachments if imageAttachments is not None else [],
                "customInstructions": customInstructions,
                "deepsearch preset": deepsearch_preset,
                "disableSearch": disableSearch,
                "enableImageGeneration": enableImageGeneration,
                "enableImageStreaming": enableImageStreaming,
                "enableSideBySide": enableSideBySide,
                "imageGenerationCount": imageGenerationCount,
                "isPreset": isPreset,
                "isReasoning": isReasoning,
                "returnImageBytes": returnImageBytes,
                "returnRawGrokInXaiRequest": returnRawGrokInXaiRequest,
                "sendFinalMetadata": sendFinalMetadata,
                "toolOverrides": toolOverrides if toolOverrides is not None else {}
            }

            logger.debug(f"Grok payload: {payload}")

            max_tries = 5
            try_index = 0
            response = ""

            is_list_cookies = isinstance(self.cookies, list)

            while try_index < max_tries:
                logger.debug(f"Попытка {try_index + 1} из {max_tries}")
                cookies_used = 0

                while cookies_used < (len(self.cookies) if is_list_cookies else 1):
                    current_cookies = self.cookies[0] if is_list_cookies else self.cookies
                    driver.set_cookies(current_cookies)

                    logger.debug(
                        f"Отправляем запрос (cookie[{cookies_used}]): headers={headers}, payload={payload}, timeout={timeout} секунд")
                    response = self._send_request(payload, headers, timeout)

                    if isinstance(response, dict) and response:
                        str_response = str(response)
                        if 'Too many requests' in str_response:
                            if is_list_cookies and len(self.cookies) > 1:
                                self.cookies.append(self.cookies.pop(0))
                            else:
                                try_index = max_tries - 1
                            cookies_used += 1
                            continue
                        elif 'This service is not available in your region' in str_response:
                            driver.set_proxy(proxy)
                            break
                        elif 'Just a moment' in str_response or '403' in str_response:
                            driver.close_driver()
                            driver.init_driver()
                            break
                        else:
                            response = GrokResponse(response)
                            assistant_message = response.modelResponse.message

                            if self.history.history_msg_count > 0:
                                self.history.add_message(history_id, SenderType.ASSISTANT, assistant_message)
                                if self.history_auto_save:
                                    self.history.to_file()

                            return response
                    else:
                        break

                if is_list_cookies and cookies_used >= len(self.cookies):
                    break

                try_index += 1

                if try_index == max_tries - 1:
                    driver.close_driver()
                    driver.init_driver()

                driver.restart_session()

            logger.error("In ask: No answer")
            driver.restart_session()
            return GrokResponse(response) if isinstance(response, dict) else {}
        except Exception as e:
            logger.error(f"In ask: {e}")
            return GrokResponse({})

    async def _async_send_request(self,
                            payload,
                            headers,
                            timeout=driver.TIMEOUT):
        try:
            """Отправляем запрос через браузер с таймаутом."""

            headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Content-Type": "application/json",
                "Origin": "https://grok.com",
                "Referer": "https://grok.com/",
                "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            })

            fetch_script = f"""
            const controller = new AbortController();
            const signal = controller.signal;
            setTimeout(() => controller.abort(), {timeout * 1000});

            const payload = {json.dumps(payload)};
            return fetch('{self.NEW_CHAT_URL}', {{
                method: 'POST',
                headers: {json.dumps(headers)},
                body: JSON.stringify(payload),
                signal: signal
            }})
            .then(response => {{
                if (!response.ok) {{
                    return response.text().then(text => 'Error: HTTP ' + response.status + ' - ' + text);
                }}
                return response.text();
            }})
            .catch(error => {{
                if (error.name === 'AbortError') {{
                    return 'TimeoutError';
                }}
                return 'Error: ' + error;
            }});
            """

            response = await asyncio.to_thread(driver.DRIVER.execute_script, fetch_script)
            if isinstance(response, str) and response.startswith('Error:'):
                error_data = handle_str_error(response)
                if isinstance(error_data, dict):
                    return error_data

            if response and 'This service is not available in your region' in response:
                return 'This service is not available in your region'
            final_dict = {}
            for line in response.splitlines():
                try:
                    parsed = json.loads(line)
                    if "modelResponse" in parsed["result"]["response"]:
                        final_dict = parsed
                        break
                except (json.JSONDecodeError, KeyError):
                    continue
            logger.debug(f"Получили ответ: {final_dict}")
            return final_dict
        except Exception as e:
            logger.error(f"В _send_request: {e}")
            return {}

    async def async_ask(self,
                        message: str,
                        history_id: Optional[str] = None,
                        proxy: Optional[str] = driver.def_proxy,
                        timeout: int = driver.TIMEOUT,
                        temporary: bool = False,
                        modelName: str = "grok-3",
                        fileAttachments: Optional[List[Dict[str, str]]] = None,
                        imageAttachments: Optional[List[Dict[str, str]]] = None,
                        customInstructions: str = "",
                        deepsearch_preset: str = "",
                        disableSearch: bool = False,
                        enableImageGeneration: bool = True,
                        enableImageStreaming: bool = True,
                        enableSideBySide: bool = True,
                        imageGenerationCount: int = 4,
                        isPreset: bool = False,
                        isReasoning: bool = False,
                        returnImageBytes: bool = False,
                        returnRawGrokInXaiRequest: bool = False,
                        sendFinalMetadata: bool = True,
                        toolOverrides: Optional[Dict[str, Any]] = None
                        ) -> GrokResponse:
        """
        Отправляет запрос к API Grok с одним сообщением и дополнительными параметрами.

        Args:
            message (str): Сообщение пользователя для отправки в API.
            history_id (Optional[str]): Идентификатор для определения, какую историю чата использовать.
            proxy (Optional[str]): URL прокси-сервера, используется только в случае региональной блокировки.
            timeout (int): Таймаут (в секундах) на ожидание ответа. По умолчанию: driver.TIMEOUT.
            temporary (bool): Указывает, является ли сессия или запрос временным. По умолчанию False.
            modelName (str): Название модели ИИ для обработки запроса. По умолчанию "grok-3".
            fileAttachments (Optional[List[Dict[str, str]]]): Список вложений файлов. Каждый элемент — словарь с ключами "name" и "content".
            imageAttachments (Optional[List[Dict[str, str]]]): Список вложений изображений, аналогично fileAttachments.
            customInstructions (str): Дополнительные инструкции или контекст для модели. По умолчанию пустая строка.
            deepsearch_preset (str): Предустановка для глубокого поиска. По умолчанию пустая строка.
            disableSearch (bool): Отключить функцию поиска модели. По умолчанию False.
            enableImageGeneration (bool): Включить генерацию изображений в ответе. По умолчанию True.
            enableImageStreaming (bool): Включить потоковую передачу изображений. По умолчанию True.
            enableSideBySide (bool): Включить отображение информации бок о бок. По умолчанию True.
            imageGenerationCount (int): Количество генерируемых изображений. По умолчанию 4.
            isPreset (bool): Указывает, является ли сообщение предустановленным. По умолчанию False.
            isReasoning (bool): Включить режим рассуждений в ответе модели. По умолчанию False.
            returnImageBytes (bool): Возвращать данные изображений в виде байтов. По умолчанию False.
            returnRawGrokInXaiRequest (bool): Возвращать необработанный вывод от модели. По умолчанию False.
            sendFinalMetadata (bool): Отправлять финальные метаданные с запросом. По умолчанию True.
            toolOverrides (Optional[Dict[str, Any]]): Словарь для переопределения настроек инструментов. По умолчанию пустой словарь.

        Return:
            GrokResponse: Ответ от API Grok в виде объекта.
        """
        try:
            base_headers = {
                "Content-Type": "application/json",
                "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"),
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "ru-RU,ru;q=0.9",
                "Origin": "https://grok.com",
                "Referer": "https://grok.com/",
            }

            headers = base_headers.copy()

            if (self.history.history_msg_count < 1 and self.history.main_system_prompt is None
                    and history_id not in self.history.system_prompts):
                message_payload = message
            else:
                message_payload = self.history.get_history(history_id) + '\n' + message
                if self.history.history_msg_count > 0:
                    self.history.add_message(history_id, SenderType.ASSISTANT, message)
                    if self.history_auto_save:
                        await asyncio.to_thread(self.history.to_file)

            payload = {
                "temporary": temporary,
                "modelName": modelName,
                "message": message_payload,
                "fileAttachments": fileAttachments if fileAttachments is not None else [],
                "imageAttachments": imageAttachments if imageAttachments is not None else [],
                "customInstructions": customInstructions,
                "deepsearch preset": deepsearch_preset,
                "disableSearch": disableSearch,
                "enableImageGeneration": enableImageGeneration,
                "enableImageStreaming": enableImageStreaming,
                "enableSideBySide": enableSideBySide,
                "imageGenerationCount": imageGenerationCount,
                "isPreset": isPreset,
                "isReasoning": isReasoning,
                "returnImageBytes": returnImageBytes,
                "returnRawGrokInXaiRequest": returnRawGrokInXaiRequest,
                "sendFinalMetadata": sendFinalMetadata,
                "toolOverrides": toolOverrides if toolOverrides is not None else {}
            }

            logger.debug(f"Grok payload: {payload}")

            max_tries = 5
            try_index = 0
            response = ""

            is_list_cookies = isinstance(self.cookies, list)

            while try_index < max_tries:
                logger.debug(f"Попытка {try_index + 1} из {max_tries}")
                cookies_used = 0
                total_cookies = len(self.cookies) if is_list_cookies else 1

                while cookies_used < total_cookies:
                    current_cookies = self.cookies[0] if is_list_cookies else self.cookies
                    await asyncio.to_thread(driver.set_cookies, current_cookies)

                    logger.debug(
                        f"Отправляем запрос (cookie[{cookies_used}]): headers={headers}, payload={payload}, timeout={timeout} секунд")
                    response = await self._async_send_request(payload, headers, timeout)

                    if isinstance(response, dict) and response:
                        str_response = str(response)

                        if 'Too many requests' in str_response:
                            if is_list_cookies and total_cookies > 1:
                                self.cookies.append(self.cookies.pop(0))
                                cookies_used += 1
                                continue
                            else:
                                try_index = max_tries - 1
                                break
                        elif 'This service is not available in your region' in str_response:
                            await asyncio.to_thread(driver.set_proxy, proxy)
                            break
                        elif 'Just a moment' in str_response or '403' in str_response:
                            await asyncio.to_thread(driver.close_driver)
                            await asyncio.to_thread(driver.init_driver)
                            break
                        else:
                            response = GrokResponse(response)
                            assistant_message = response.modelResponse.message

                            if self.history.history_msg_count > 0:
                                self.history.add_message(history_id, SenderType.ASSISTANT, assistant_message)
                                if self.history_auto_save:
                                    await asyncio.to_thread(self.history.to_file)

                            return response
                    else:
                        logger.warning("Пустой или некорректный ответ, пробуем заново...")
                        break

                if is_list_cookies and cookies_used >= total_cookies:
                    break

                try_index += 1

                if try_index == max_tries - 1:
                    await asyncio.to_thread(driver.close_driver)
                    await asyncio.to_thread(driver.init_driver)

                await asyncio.to_thread(driver.restart_session)

            logger.error("В ask: неожиданный формат ответа от сервера")
            await asyncio.to_thread(driver.restart_session)
            return GrokResponse(response) if isinstance(response, dict) else GrokResponse({})
        except Exception as e:
            logger.error(f"В ask: {e}")
            return GrokResponse({})


def handle_str_error(response_str):
    try:
        json_str = response_str.split(" - ")[1]
        response = json.loads(json_str)
        if isinstance(response, dict) and 'error' in response:
            error_code = response['error'].get('code')
            error_message = response['error'].get('message', 'Unknown error')
            error_details = response['error'].get('details', [])

            error_data = {
                "error_code": error_code,
                "error": error_message,
                "details": error_details,
            }
            return error_data

    except Exception:
        return {"error_code": "Unknown", "error": response_str, "details": []}