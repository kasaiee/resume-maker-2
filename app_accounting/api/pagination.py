from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class StandardResultsPagination(PageNumberPagination):
    page_size = 10  # تعداد آیتم‌ها در هر صفحه
    page_size_query_param = 'page_size'  # اجازه تغییر تعداد آیتم‌ها از طریق URL
    max_page_size = 100  # حداکثر تعداد آیتم‌ها در هر صفحه


# class StandardResultsPagination(LimitOffsetPagination):
#     default_limit = 10  # تعداد پیش‌فرض آیتم‌ها در هر صفحه
#     max_limit = 100  # حداکثر تعداد آیتم‌ها در هر صفحه


# class StandardResultsPagination(CursorPagination):
#     page_size = 10  # تعداد پیش‌فرض آیتم‌ها در هر صفحه
#     ordering = 'id'  # ترتیب‌بندی بر اساس فیلد id