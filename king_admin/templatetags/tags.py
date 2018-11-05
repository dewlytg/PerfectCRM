#__author:  Administrator
#date:  2017/1/5

from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(request,obj,admin_class):
    row_ele = ""
    for index,column in enumerate(admin_class.list_display):
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:#choices type
            column_data = getattr(obj,"get_%s_display" % column)()
        else:
            column_data = getattr(obj,column)

        if type(column_data).__name__ == 'datetime':
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")
        if index == 0:
            column_data = "<a href={request_path}{obj_id}/change>{data}</a>".format(request_path=request.path,obj_id=obj.id,data=column_data)
        row_ele += "<td>%s</td>" % column_data

    return mark_safe(row_ele)


@register.simple_tag
def display_pagintors(query_sets,filter_condtions,previous_order_by,search_key):
    paginators = ""
    query_str = ""
    added_dot_ele = False
    if search_key:
        query_str += "&_q=%s" % search_key
    if previous_order_by:
        query_str += "&o=%s" % previous_order_by
    for k,v in filter_condtions.items():
        query_str += "&%s=%s" %(k,v)
    for loop_counter in query_sets.paginator.page_range:
        if loop_counter < 3 or loop_counter > query_sets.paginator.count - 2 or abs(query_sets.number - loop_counter) <= 2:
            ele_class = ""
            if query_sets.number == loop_counter:
                ele_class = "active"
                added_dot_ele = False
            ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' % (ele_class, loop_counter, query_str, loop_counter)
            paginators += ele
        else:
            if added_dot_ele == False:
                ele = '''<li><a>...</a></li>'''
                added_dot_ele = True
                paginators += ele
    return mark_safe(paginators)


@register.simple_tag
def render_page_ele(loop_counter,query_sets,filter_condtions):
    query_str = ""
    for k,v in filter_condtions.items():
        query_str += "&%s=%s" %(k,v)
    if abs(query_sets.number - loop_counter) <= 1:
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' %(ele_class,loop_counter,query_str,loop_counter)

        return mark_safe(ele)

    return ''


@register.simple_tag
def render_filter_ele(filter_field,admin_class,filter_condtions):
    select_ele = '''<select class="form-control" name='{filter_field}' ><option value=''>----</option>'''
    field_obj = admin_class.model._meta.get_field(filter_field)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            if filter_condtions.get(filter_field) == str(choice_item[0]):
                selected ="selected"

            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected =''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''
    if type(field_obj).__name__ in ["DateTimeField","DateField"]:
        date_eles = []
        today_ele = datetime.now().date()
        date_eles.append(["今天",datetime.now().date()])
        date_eles.append(["昨天",today_ele - timedelta(days=1)])
        date_eles.append(["本周",today_ele - timedelta(days=7)])
        date_eles.append(["本月",today_ele.replace(day=1)])
        date_eles.append(["近30天",today_ele - timedelta(days=30)])
        date_eles.append(["近90天",today_ele - timedelta(days=90)])
        date_eles.append(["本年",today_ele.replace(month=1,day=1)])
        date_eles.append(["近一年",today_ele - timedelta(days=365)])
        for ele in date_eles:
            select_ele += '''<option value='%s'>%s</option>''' %(ele[1],ele[0])
        filter_field_value = "%s__gte" % filter_field
    else:
        filter_field_value = filter_field
        # yesterday_ele = today_ele - timedelta(days=1)
        # last7day_ele = today_ele - timedelta(days=7)
        # mtd_ele = today_ele.replace(day=1) # month to day
        # last30day_ele = today_ele - timedelta(days=30)
        # last90day_ele = today_ele - timedelta(days=90)
        # last180day_ele = today_ele - timedelta(days=180)
        # ytd_ele = today_ele.replace(month=1,day=1)
        # last365day_ele = today_ele - timedelta(days=365)
    select_ele = select_ele.format(filter_field=filter_field_value)
    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def get_table_coulumn_sorted(column,order_by):
    sort_icon = """"""
    ele = """<th><a href="?o={order_by_value}">{column}</a>{sort_icon}</th>"""
    if order_by and order_by.startswith('-') and order_by.strip('-') == column:
        order_by_value = order_by
        sort_icon = """<span class="glyphicon glyphicon-chevron-down" aria-hidden="true"></span>"""
    elif order_by and not order_by.startswith('-') and order_by == column:
        order_by_value = column
        sort_icon = """"<span class="glyphicon glyphicon-chevron-up" aria-hidden="true"></span>"""
    else:
        order_by_value = column
    return mark_safe(ele.format(order_by_value=order_by_value,column=column,sort_icon=sort_icon))


@register.simple_tag
def get_module_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_all_obj_list(form_obj,admin_class,field):
    all_obj = getattr(admin_class.model,field.name)
    all_obj_list = all_obj.rel.model.objects.all()
    if not form_obj.instance.id:
        return all_obj_list

    field_obj = getattr(form_obj.instance, field.name)
    selected_obj_list = field_obj.all()
    exclude_obj_list = list(set(all_obj_list).difference(set(selected_obj_list)))
    return exclude_obj_list



@register.simple_tag
def get_selected_obj_list(form_obj,field):
    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance,field.name)
        return field_obj.all()


def recursive_related_model(queryset_list, related_model_map,html_str=""):
    html_str += "<ul>"
    for obj in queryset_list:
        html_str += "<li>"
        html_str += str(obj)
        for related_model_name in related_model_map:  # ManyToMany or OneToMany
            if related_model_name.endswith("+"):  # ManyToMany
                obj_set = obj._meta.fields_map[related_model_name].get_accessor_name()
                m2m_class_name = (obj_set.strip("+")).split("_")[1]
                m2m_class = getattr(obj, m2m_class_name)
                sub_related_obj_list = m2m_class.all()
            else:
                obj_set = getattr(obj, related_model_map[related_model_name].get_accessor_name())
                sub_related_obj_list = obj_set.all()
            sub_related_model_map = related_model_map[related_model_name].related_model._meta.fields_map
            if sub_related_model_map:
                ret = recursive_related_model(sub_related_obj_list, sub_related_model_map,html_str="")
                html_str+=ret
            else:
                html_str += "<ul>"
                for sub_obj in sub_related_obj_list:
                    html_str += "<li>"
                    html_str += str(sub_obj)
                    html_str += "</li>"
                html_str += "</ul>"
        html_str += "</li>"
    html_str += "</ul>"
    return html_str

@register.simple_tag
def display_related_list(admin_class,obj_id):
    queryset_list = admin_class.model.objects.filter(id=obj_id)
    related_model_map = admin_class.model._meta.fields_map
    ret = recursive_related_model(queryset_list,related_model_map)
    print()
    return mark_safe(ret)
