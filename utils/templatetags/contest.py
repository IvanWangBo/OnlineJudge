# coding=utf-8
import json


def get_contest_status(contest):
    status = contest.status
    if status == 1:
        return "没有开始"
    elif status == -1:
        return "已经结束"
    else:
        return "正在进行"


def get_contest_status_color(contest):
    status = contest.status
    if status == 1:
        return "info"
    elif status == -1:
        return "warning"
    else:
        return "success"


def get_the_formatted_time(seconds):
    if not seconds:
        return ""
    seconds = int(seconds)
    hour = seconds / (60 * 60)
    minute = (seconds - hour * 60 * 60) / 60
    second = seconds - hour * 60 * 60 - minute * 60
    return str(hour) + ":" + str(minute) + ":" + str(second)


def get_medal_class(item, rank):
    try:
        info = json.loads(rank)
    except:
        return rank
    try:
        number = len(info)
    except:
        return 'number'
    try:
        item_number = json.loads(item)[0]['rank_number']
    except:
        item_number = 0
    if item_number == 0:
        return ''
    elif item_number <= number * 0.1:
        return ' gold'
    elif item_number <= number * 0.3:
        return ' silver'
    elif item_number <= number * 0.6:
        return ' bronze'
    else:
        return ''


def get_submission_class(rank, problem):
    submission_info = json.loads(rank["submission_info"])
    if str(problem.id) not in submission_info:
        return ""
    else:
        submission = submission_info[str(problem.id)]
        if submission["is_ac"] and submission["is_first_ac"]:
            _class = "first-achieved"
        elif submission["is_ac"]:
            _class = "has_accept"
        else:
            _class = "alert-danger"
        return _class


def get_submission_content(rank, problem):
    submission_info = json.loads(rank["submission_info"])
    if str(problem.id) not in submission_info:
        return ""
    else:
        submission = submission_info[str(problem.id)]
        if submission["is_ac"]:
            r = get_the_formatted_time(submission["ac_time"])
            if submission["error_number"]:
                r += "<br>（-" + str(submission["error_number"]) + "）"
            return r
        else:
            return "（-" + str(submission["error_number"]) + "）"


from django import template

register = template.Library()
register.filter("contest_status", get_contest_status)
register.filter("contest_status_color", get_contest_status_color)
register.filter("format_seconds", get_the_formatted_time)
register.simple_tag(get_submission_class, name="get_submission_class")
register.simple_tag(get_medal_class, name="get_medal_class")
register.simple_tag(get_submission_content, name="get_submission_content")
