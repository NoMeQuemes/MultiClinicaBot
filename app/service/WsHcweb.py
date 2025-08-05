import requests
import xml.etree.ElementTree as ET
import json
from threading import Lock
from app.config import Config

class WsHcweb:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WsHcweb, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.url = Config.API_BASE_HCWEB
        self._initialized = True

    def call_method(self, method_name: str, parameters: dict) -> any:
        soap_action = f"http://iosepscript.excelenciadigitial.net.ar/{method_name}"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": soap_action
        }
        print("Parámetros enviados:", parameters)
        body = self._build_soap_body(method_name, parameters)
        response = requests.post(self.url, data=body, headers=headers)

        if response.status_code != 200:
            raise Exception(f"SOAP Error {response.status_code}: {response.text}")

        return self._parse_response(response.text, method_name)

    def _build_soap_body(self, method: str, params: dict) -> str:
        def serialize_param(k, v):
            if v is None:
                return f'<{k} xsi:nil="true" />'
            elif isinstance(v, list):
                return f"<{k}>" + "".join(f"<int>{item}</int>" for item in v) + f"</{k}>"
            elif isinstance(v, bool):
                return f"<{k}>{str(v).lower()}</{k}>"
            else:
                return f"<{k}>{v}</{k}>"

        xml_params = "".join(serialize_param(k, v) for k, v in params.items())
        return f"""<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <{method} xmlns="http://iosepscript.excelenciadigitial.net.ar/">
            {xml_params}
            </{method}>
        </soap:Body>
        </soap:Envelope>"""

    def _parse_response(self, xml_response: str, method: str) -> any:
        ns = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/'}
        root = ET.fromstring(xml_response)

        body = root.find('soap:Body', ns)
        if body is None:
            print("No se encontró el Body en el XML")
            return None

        base_path = f".//{{http://iosepscript.excelenciadigitial.net.ar/}}"
        contains_errors = body.find(f"{base_path}ContainsErrors")
        success_message = body.find(f"{base_path}SuccessMessage")
        error_message = body.find(f"{base_path}ErrorMessage")

        if contains_errors is None:
            print(f"No se encontró ContainsErrors en la respuesta de {method}")
            return None

        contains_errors_value = contains_errors.text.strip().lower() if contains_errors is not None else ""
        has_error = contains_errors_value == "true"

        if has_error:
            error_text = (error_message.text or "").strip() if error_message is not None else ""
            if not error_text:
                # Log o debug para analizar todo el XML de respuesta
                print("Advertencia: respuesta con error pero sin mensaje explícito.")
                print(xml_response)
                error_text = "La API devolvió un error, pero no proporcionó detalles."
            print(f"Error en la respuesta de {method}: {error_text}")
            return None



        # Si no hay errores, procesar SuccessMessage
        if success_message is None or not success_message.text:
            print(f"No se encontró SuccessMessage válido en la respuesta de {method}")
            return None

        try:
            return json.loads(success_message.text.strip())
        except Exception as e:
            print(f"Error al parsear JSON de SuccessMessage: {e}")
            return None