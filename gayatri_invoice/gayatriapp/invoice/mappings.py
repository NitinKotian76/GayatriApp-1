from .formmod import DefaultForm as df
from .formmod import BaseForm as bf

FORMHANDLER = {
    "customer": {
        "form_class": df.customer,
        "table_name": "customer",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "customer"},
                "hx_req": "/invoice/form_view"
            },
            "reset": {
                "hx_vals": {"form": "customer"},
                "hx_req": "/invoice/form_view"
            },
        },
        "table_buttons":{
            "delete":{
                "hx_vals": {"form": "customer"},
                "hx_req": "/invoice/select_row"
            },
            "approve":{
                "hx_vals": {"form": "customer"},
                "hx_req": "/invoice/select_row"
            }
        }
    },
    "supplier": {
        "form_class": df.supplier,
        "table_name": "supplier",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "supplier"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "signatory": {
        "form_class": df.signatory,
        "table_name": "signatory",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "signatory"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "export_fields": {
        "form_class": df.export_fields,
        "table_name": "export_fields",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "export_fields"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "item_category": {
        "form_class": df.item_category,
        "table_name": "item_category",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "item_category"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "variety": {
        "form_class": df.variety,
        "table_name": "variety",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "variety"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "items": {
        "form_class": df.items,
        "table_name": "items",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "items"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "stock": {
        "form_class": df.stock,
        "table_name": "stock",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "stock"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "units": {
        "form_class": df.units,
        "table_name": "units",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "units"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "location": {
        "form_class": df.location,
        "table_name": "location",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "location"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "open_bal_prod": {
        "form_class": df.open_bal_prod,
        "table_name": "open_bal_prod",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "open_bal_prod"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "prod_record": {
        "form_class": df.prod_record,
        "table_name": "prod_record",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "prod_record"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "prod_plus_minus": {
        "form_class": df.prod_plus_minus,
        "table_name": "prod_plus_minus",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "prod_plus_minus"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "prod_approval": {
        "form_class": df.prod_approval,
        "table_name": "prod_approval",
        "buttons": {
            "approve": {
                "hx_vals": {"form": "prod_approval"},
                "hx_req": "/invoice/form_view"
            },
            "reject": {
                "hx_vals": {"form": "prod_approval"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "invoice": {
        "form_class": df.invoice,
        "table_name": "invoice",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "invoice_direct"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "jumbo_roll_qc": {
        "form_class": df.jumbo_roll_qc,
        "table_name": "jumbo_roll_qc",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "jumbo_roll_qc"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "lot_no_wise_qc": {
        "form_class": df.lot_no_wise_qc,
        "table_name": "lot_no_wise_qc",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "lot_no_wise_qc"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "finishing_house": {
        "form_class": df.finishing_house,
        "table_name": "finishing_house",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "finishing_house"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "program_planning": {
        "form_class": df.program_planing,
        "table_name": "program_planning",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "program_planning"},
                "hx_req": "/invoice/form_view"
            },
        }
    },
    "view_table": {
        "form_class": bf.table_view,
        "table_name": "table_view",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "table_view"},
                "hx_req": "/invoice/form_view"
            },
        }
    }
}

COMMON = {
    "pass_change": {
        "form_class": bf.changePassword,
        "buttons": {
            "submit": {
                "hx_vals": {"form": "pass_change"},
                "hx_req": "/invoice/change_password"
            },
        }
    }
}
