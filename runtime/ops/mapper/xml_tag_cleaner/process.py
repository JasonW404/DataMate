#!/user/bin/python
# -*- coding: utf-8 -*-

"""
Description: XML标签去除
Create: 2025/01/15
"""
import time
from typing import Dict, Any
from xml.parsers.expat import ExpatError

import xmltodict
from loguru import logger

from datamate.core.base_op import Mapper


class XMLTagCleaner(Mapper):
    """XML 标签去除插件，只对文件拓展名为xml的文件做标签去除"""

    @staticmethod
    def _format_list(list_data, indentation=""):
        formatted_string = []
        for item in list_data:
            if isinstance(item, dict):
                formatted_string.append("\n" + XMLTagCleaner._format_dict(item, indentation + " "))
            else:
                formatted_string.append(f"{item}")
        return "".join(formatted_string)

    @staticmethod
    def _format_dict(dict_data, indentation=""):
        """字典格式转换为字符串"""
        formatted_lines = []
        for key, value in dict_data.items():
            line = f"{indentation}{key}: "
            if isinstance(value, dict):
                line += "\n" + XMLTagCleaner._format_dict(value, indentation + " ")
            elif isinstance(value, list):
                line += XMLTagCleaner._format_list(value, indentation + " ")
            else:
                line += f"{value}\n"
            formatted_lines.append(line)
        return "".join(formatted_lines)

    @staticmethod
    def _tag_clean_xml(byte_io):
        """标签去除"""
        byte_io = byte_io.encode()
        dict_data = xmltodict.parse(byte_io)
        return XMLTagCleaner._format_dict(dict_data).strip()

    def execute(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        file_name = sample[self.filename_key]
        if sample[self.filetype_key] == "xml":
            try:
                sample[self.text_key] = self._tag_clean_xml(sample[self.text_key])
                logger.info(f"fileName: ｛file_name｝, method: XMLTagCleaner costs {time.time() - start:6f} s")
            except ExpatError as err:
                logger.error(f"fileName: {file_name} is abnormal xml form: ｛err｝")
                raise RuntimeError(81001, str(err)) from None
            except Exception as err:
                logger.error(f"fileName {file_name}, method: XMLTagCleaner causes other error: {err}")
                raise RuntimeError(81002, str(err)) from None
        else:
            logger.info(f"fileName: {file_name}, method: XMLTagCleaner, The file is not xml!")
        return sample
