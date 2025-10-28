from .all_views.admin_views import (
    create_table,
    table_list,
    admin_company
)
from .all_views.form_views import (
    form_view,
    table_data_view,
    select_row,
    reset_selected_row,
    delete_row,
    approve_row,
    field_setup,
    form_config,
    form_delete,
    form_edit,
    form_list
)
from .all_views.report_views import (
    report_view,
    report_list,
    new_report,
    edit_report,
    del_report
)

from .all_views.auth_views import (
    login_user,
    change_password,
    logout_user
)
from .all_views.common_views import (
    add_formset_field,
    index,
    profile_user,
    get_notifications
)
# Import specific views from the organized files
