from django.shortcuts import render,redirect
import importlib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.utils import table_filter,table_sorted,table_search
# Create your views here.
from king_admin import king_admin
from king_admin.forms import create_model_form


def index(request):
    #print(king_admin.enabled_admins['crm']['customerfollowup'].model )
    return render(request, "king_admin/table_index.html",{'table_list':king_admin.enabled_admins})


def display_table_objs(request,app_name,table_name):

    #models_module = importlib.import_module('%s.models'%(app_name))
    #model_obj = getattr(models_module,table_name)
    admin_class = king_admin.enabled_admins[app_name][table_name]
    #admin_class = king_admin.enabled_admins[crm][userprofile]

    #object_list = admin_class.model.objects.all()
    object_list,filter_condtions = table_filter(request,admin_class)

    search_objct_list = table_search(request,admin_class,object_list)

    sorted_object_list,order_by = table_sorted(request,search_objct_list)

    paginator = Paginator(sorted_object_list, admin_class.list_per_page) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)

    return render(request,"king_admin/table_objs.html",{"admin_class":admin_class,
                                                        "query_sets":query_sets,
                                                        "filter_condtions":filter_condtions,
                                                        "order_by":order_by,
                                                        "previous_order_by":request.GET.get("o",""),
                                                        "search_key":request.GET.get("_q","")})


def table_obj_change(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    if request.method == "GET":
        form_obj = model_form_class(instance=admin_class.model.objects.get(id=obj_id))
    elif request.method == "POST":
        form_obj = model_form_class(request.POST,instance=admin_class.model.objects.get(id=obj_id))
        if form_obj.is_valid():
            form_obj.save()

    return render(request,"king_admin/table_obj_change.html",{"form_obj":form_obj,
                                                              "admin_class":admin_class,
                                                              "app_name":app_name,
                                                              "table_name":table_name,"obj_id":obj_id
                                                              })


def table_obj_add(request,app_name,table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    if request.method == "GET":
        form_obj = model_form_class()
    elif request.method == "POST":
        form_obj = model_form_class(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path.replace("/add",""))
    return render(request,"king_admin/table_obj_add.html",{"form_obj":form_obj,"admin_class":admin_class})


def table_obj_delete(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    print(app_name,table_name,obj_id)
    return render(request,"king_admin/table_obj_delete.html",{"admin_class":admin_class,"obj_id":obj_id})

