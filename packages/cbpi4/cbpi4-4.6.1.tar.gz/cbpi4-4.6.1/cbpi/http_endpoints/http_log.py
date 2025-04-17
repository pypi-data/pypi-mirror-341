import json
import logging
import os

from aiohttp import web
from cbpi.api import request_mapping
from cbpi.utils.encoder import ComplexEncoder
from cbpi.utils.utils import json_dumps


class LogHttpEndpoints:

    def __init__(self, cbpi):
        self.cbpi = cbpi
        self.cbpi.register(self, url_prefix="/log")

    @request_mapping(path="/{name}/zip", method="POST", auth_required=False)
    async def create_zip_names(self, request):
        """
        ---
        description: Zip Log files for sensor
        tags:
        - Log
        parameters:
        - name: "name"
          in: "path"
          description: "Sensor ID"
          required: true
          type: "integer"
          format: "int64"
        produces:
        - application/json
        responses:
            "204":
                description: successful operation. Return "pong" text
        """

        log_name = request.match_info["name"]
        data = self.cbpi.log.zip_log_data(log_name)

        return web.json_response(dict(filename=data), dumps=json_dumps)

    @request_mapping(path="/{name}/zip", method="DELETE", auth_required=False)
    async def clear_zip_names(self, request):
        """
        ---
        description: Delete all zip files for sensor
        tags:
        - Log
        parameters:
        - name: "name"
          in: "path"
          description: "Sensor ID"
          required: true
          type: "integer"
          format: "int64"
        responses:
            "204":
                description: successful operation.
        """
        log_name = request.match_info["name"]
        self.cbpi.log.clear_zip(log_name)
        return web.Response(status=204)

    @request_mapping(path="/zip/download/{name}", method="GET", auth_required=False)
    async def download_zip(self, request):
        """
        ---
        description: Download a sensor zip file
        tags:
        - Log
        parameters:
        - name: "name"
          in: "path"
          description: "Zip File name"
          required: true
          type: "integer"
          format: "int64"
        responses:
            "204":
             description: successful operation.
        """

        response = web.StreamResponse(
            status=200,
            reason="OK",
            headers={"Content-Type": "application/zip"},
        )
        await response.prepare(request)
        log_name = request.match_info["name"]
        with open(
            os.path.join(self.cbpi.logsFolderPath, "%s.zip" % log_name), "rb"
        ) as file:
            for line in file.readlines():
                await response.write(line)

        await response.write_eof()
        return response

    @request_mapping(path="/{name}/zip", method="GET", auth_required=False)
    async def get_zip_names(self, request):
        """
        ---
        description: Zip available zip file names for sensor
        tags:
        - Log
        parameters:
        - name: "name"
          in: "path"
          description: "Sensor ID"
          required: true
          type: "integer"
          format: "int64"
        produces:
        - application/json
        responses:
            "200":
                description: successful operation.
        """
        log_name = request.match_info["name"]
        data = self.cbpi.log.get_all_zip_file_names(log_name)
        return web.json_response(data, dumps=json_dumps)

    @request_mapping(path="/{name}/files", method="GET", auth_required=False)
    async def get_file_names(self, request):
        """
        ---
        description: Available log file names for sensor
        tags:
        - Log
        parameters:

        - name: "name"
          in: "path"
          description: "Sensor ID"
          required: true
          type: "integer"
          format: "int64"
        produces:
        - application/json
        responses:
            "200":
                description: successful operation.
        """
        log_name = request.match_info["name"]

        data = self.cbpi.log.get_logfile_names(log_name)
        return web.json_response(data, dumps=json_dumps)

    @request_mapping(path="/{name}", method="GET", auth_required=False)
    async def get_log(self, request):
        """
        ---
        description: delete log data for sensor
        tags:
        - Log
        parameters:
        - name: "name"
          in: "path"
          description: "Sensor ID"
          required: true
          type: "integer"
          format: "int64"
        produces:
        - application/json
        responses:
            "200":
                description: successful operation.
        """
        log_name = request.match_info["name"]
        data = await self.cbpi.log.get_data(log_name)
        return web.json_response(data, dumps=json_dumps)

    @request_mapping(path="/", method="POST", auth_required=False)
    async def get_log2(self, request):
        """
        ---
        description: delete log data for sensor
        tags:
        - Log
        parameters:
        - in: body
          name: body
          description: Sensor Ids
          required: true
          schema:
            type: array
            items:
              type: string
        produces:
        - application/json
        responses:
            "200":
                description: successful operation.
        """
        data = await request.json()
        values = await self.cbpi.log.get_data2(data)
        return web.json_response(values, dumps=json_dumps)

    @request_mapping(path="/{name}", method="DELETE", auth_required=False)
    async def clear_log(self, request):
        """
        ---
        description: Get log data for sensor
        tags:
        - Log
        parameters:
        - name: "name"
          in: "path"
          description: "Sensor ID"
          required: true
          type: "integer"
          format: "int64"
        responses:
            "204":
                description: successful operation.
        """
        log_name = request.match_info["name"]
        self.cbpi.log.clear_log(log_name)
        return web.Response(status=204)

    @request_mapping(path="/logs", method="POST", auth_required=False)
    async def get_logs(self, request):
        """
        ---
        description: Get Logs
        tags:
        - Log
        parameters:
        - in: body
          name: body
          description: Sensor Ids
          required: true
          schema:
            type: array
            items:
              type: string
        produces:
        - application/json
        responses:
            "200":
                description: successful operation.
        """
        data = await request.json()

        result = await self.cbpi.log.get_data(data)
        # print("JSON")
        # print(json.dumps(result, cls=ComplexEncoder))
        # print("JSON----")
        return web.json_response(result, dumps=json_dumps)
