#__author:  Administrator
#date:  2017/1/5
from django.db.models import Q

def table_filter(request,admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    filter_conditions = {}
    keywords_list = ["page","o","_q"]
    for k,v in request.GET.items():
        if k in keywords_list:
            continue
        if v:
            filter_conditions[k] =v

    return admin_class.model.objects.filter(**filter_conditions).order_by("-%s" %admin_class.ordering if admin_class.ordering else "-id"),filter_conditions


def table_sorted(request,object_list):
    orderby_key = request.GET.get("o")
    if orderby_key:
        if orderby_key.startswith('-'):
            orderby_key = orderby_key.strip("-")
        else:
            orderby_key = "-%s" % orderby_key
        ret = object_list.order_by(orderby_key)
    else:
        ret = object_list
    return ret,orderby_key


def table_search(request,admin_class,object_list):
    search_key = request.GET.get("_q")
    if search_key:
        q = Q()
        q.connector = "OR"
        for field in admin_class.search_fields:
            q.children.append(("%s__contains" %field,search_key))
        return object_list.filter(q)
    return object_list




