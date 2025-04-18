#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/14 10:26
# @Author   : songzb

import yaml
import datetime
import os
from loguru import logger
from collections import OrderedDict
import re
import json
import requests
import asyncio


def read_config(config_path):
    """"读取配置"""
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def update_config(config, config_path):
    """"更新配置"""
    with open(config_path, 'w') as yaml_file:
        yaml.dump(config, yaml_file)
    return None


def init_logger(version, log_env, use_vllm):
    """
    初始化日志存储
    """
    now = datetime.datetime.now()
    log_env_desc = "online" if log_env else "test"
    if log_env:
        vllm_desc = "_VLLM" if use_vllm else ""
        log_dir = os.path.expanduser(f"../nohup_logs/{now.year}_{now.month}_{now.day}")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, f"{version}_{now.year}-{now.month}-{now.day}_{log_env_desc}{vllm_desc}.log")
        logger.add(log_file, enqueue=True, rotation="1 day")
        logger.info("【开始存储日志】")
        logger.info(log_file)
        return logger
    else:
        logger.info("【不存储日志】")
        return logger


def contains(items, targets, exist=True):
    """
    exist为True：则认为targets中有items中的元素 返回True 有在就是True
    exist为False：则认为items中的元素都在targets中 返回True 都在才是True
    """
    if exist:
        for item in items:
            if item in targets:
                return True
        return False
    else:
        for item in items:
            if item not in targets:
                return False
        return True


def unique_sort(items, sort=False):
    """
    列表去重并且排序
    """
    if isinstance(items, list):
        unique_items = list(OrderedDict.fromkeys(items))
        if sort:
            unique_items.sort()
        return unique_items
    else:
        return items


def has_level_type(level_list, key, extra=None):
    """

    """
    if extra:
        return True if key in [lev.split("-")[0] for lev in level_list] or contains(extra, level_list) else False
    else:
        return True if key in [lev.split("-")[0] for lev in level_list] else False


def clean(lang, text, action2comb_map, level1_action):
    """
    清理（）/()两种括号的提示内容
    """
    pattern = r'\((.*?)\)' if lang == "en" else r'（(.*?)）'
    l = '(' if lang == "en" else '（'
    r = ')' if lang == "en" else '）'
    for a in re.findall(pattern, text):
        remove = True
        for _a in a.split("、"):
            if _a not in action2comb_map.values() and _a not in level1_action and "-" not in _a \
                    and _a not in [a_map.split("-")[-1] for a_map in action2comb_map.values()]:
                remove = False
                if "问：" in _a:
                    text = text.replace(f"{l}问：", "，").replace(f"{r}", "")
                elif "问" in _a:
                    if len(text) - text.index(f"{r}") < 3:
                        text = text.replace(f"{l}", "，").replace(f"{r}", "")
                    else:
                        text = text.replace(f"{l}{_a}{r}", "")
        if remove:
            text = text.replace(f"{l}{a}{r}", "")
    if ")" in text:
        pos = text.index(")") + 1
        text = text[pos:]
    elif "、套电" in text:
        pos = text.index("、套电") + 3
        text = text[pos:]
    return text


def get_messages(history, query, system_prompt, history_action, action2comb_map, logger):
    def add_user(messages, history_list, text):
        if messages[-1]["role"] == "user":
            messages[-1]["content"] += f"<sep>{text}"
            history_list[-1] += f"<sep>{text}"
        else:
            messages.append({"role": "user", "content": text})
            history_list.append(text)
        return messages, history_list

    history_list = []
    messages = [{"role": "system", "content": system_prompt}]
    for turn, (old_query, response) in enumerate(history):
        old_query = old_query.replace("\n", "")
        response = response.replace("\n", "")
        if len(history_action) > turn:
            trans_action_list = [action2comb_map.get(a, a) for a in history_action[turn].split('、')]
            resp_prompt = f"({'、'.join(unique_sort(trans_action_list))})"
        else:
            resp_prompt = ""
        logger.info(f"Round{turn} CLIENT: {old_query}")
        logger.info(f"Round{turn} SERVER: {resp_prompt}{response}")
        if response != "":
            messages, history_list = add_user(messages, history_list, text=old_query)
            messages.append({"role": "assistant", "content": resp_prompt + response})
            history_list.append(response)
        else:
            messages.append({"role": "user", "content": old_query})
            history_list.append(old_query)
    logger.info(f"Round{len(history_list) // 2} CLIENT: {query}")
    messages, history_list = add_user(messages, history_list, text=query)
    print(messages)
    return messages, history_list


def format_dialogs(dialog_record, keyword="", history_action_list=None):
    """
    将dialog_record整理成输入模型所需的格式
    """

    def get_sep_token(tmp_round, use_action=True):
        if use_action:
            return "、" if len(tmp_round) > 1 else ""
        else:
            return "<sep>" if len(tmp_round) > 1 else ""

    use_history_action = True if "action" in dialog_record[1].keys() else False if len(dialog_record) > 1 else False
    history, tmp_history, tmp_round = [], [], []
    history_action, tmp_history_action, tmp_round_action = [], [], []
    current_role = ""
    for i, context in enumerate(dialog_record):
        if i == 0 and context["role"] == "SEARCH":
            keyword = context["sentence"]
            context["role"] = "CLIENT"
        if context["role"] == "CLIENT":
            if current_role == "SERVER":
                tmp_history.append(f"{get_sep_token(tmp_round, use_action=False)}".join(tmp_round))  # 拼接server
                history.append(tmp_history)
                if use_history_action:
                    tmp_history_action.append(f"{get_sep_token(tmp_round_action)}".join(tmp_round_action))
                    history_action.append("、".join(tmp_history_action))
                tmp_history, tmp_round, tmp_history_action, tmp_round_action = [], [], [], []
            if i == len(dialog_record) - 1:
                tmp_round.append(context["sentence"])
                tmp_history.append(f"{get_sep_token(tmp_round, use_action=False)}".join(tmp_round))
                tmp_history.append("")  # 最后一句为client的情况，需要补充一句空字符串的server
                history.append(tmp_history)
            tmp_round.append(context["sentence"])
            current_role = context["role"]
        elif context["role"] == "SERVER":
            if i == 0:
                tmp_history.append(keyword)
                if use_history_action and len(context["action"]) > 0:
                    if isinstance(context["action"][0], list):
                        tmp_history_action.extend(context["action"][0])
                    else:
                        tmp_history_action.append(context["action"][0])
            else:
                if current_role == "CLIENT":
                    tmp_history.append(f"{get_sep_token(tmp_round, use_action=False)}".join(tmp_round))  # 拼接client
                    tmp_round = []
            tmp_round.append(context["sentence"])
            if use_history_action and len(context["action"]) > 0:
                tmp_round_action.append("、".join(context["action"][0]))
            current_role = context["role"]
            if i == len(dialog_record) - 1:
                tmp_history.append(f"{get_sep_token(tmp_round, use_action=False)}".join(tmp_round))
                history.append(tmp_history)
                if use_history_action:
                    tmp_history_action.append(f"{get_sep_token(tmp_round_action)}".join(tmp_round_action))
                    history_action.append("、".join(tmp_history_action))
    if history_action_list is None:
        history_action_list = []
    if len(history_action_list) > 0 and len(history_action) == 0:
        history_action = history_action_list
    return history, history_action


def nlu_async_service(text, domain, url, logger, tasks):
    def request_nlu(text, domain, url, logger, task="intent"):
        data = {"sentence": text, "domain": domain, "task": task}
        try:
            return requests.post(url, data=json.dumps(data), timeout=3).json()['response']
        except Exception as e:
            logger.error(f"[{task}]请求接口失败：{e} ---{url}")
            return {} if task == "ner" else dict(zip(text, [""] * len(text)))

    async def async_nlu(text, domain, url, logger, task):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, request_nlu, text, domain, url, logger, task)
        return result

    async def nlu_thread(text, domain, url, logger, task):
        logger.debug(f"[START]========== Task: {task} ==========")
        result = await async_nlu(text=text, domain=domain, url=url, logger=logger, task=task)
        return result

    coros = []
    for task in tasks:
        coros.append(nlu_thread(text=text, domain=domain, url=url, logger=logger, task=task))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    threads = [loop.create_task(coro) for coro in coros]
    loop.run_until_complete(asyncio.wait(threads))
    outputs = {}
    for task, thread in zip(tasks, threads):
        outputs[task] = thread.result()
    return outputs
