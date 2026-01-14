
###############
# PHASE 2
###############
from .form_files import Static as df
from .form_files import Base as bf

FORMHANDLER = {
    "customer": {
        "form_class": df.customer,
        "table_name": "customer",
        "buttons": {
            "submit": {
                "hx_req": "/invoice/form_view",
                "hx_vals": {"form": "customer"},
                "hx_swap": "outerHTML",
            },
        },
        "table_buttons": {
            "delete": {
                "hx_vals": {"form": "customer"},
                "hx_req": "/invoice/delete_row"
            },
            "approve": {
                "hx_vals": {"form": "customer"},
                "hx_req": "/invoice/approve_row"
            },
        }
    },
    "supplier": {
        "form_class": df.supplier,
        "table_name": "supplier",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "supplier"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        },
        "table_buttons": {
            "delete": {
                "hx_vals": {"form": "supplier"},
                "hx_req": "/invoice/delete_row"
            },
            "approve": {
                "hx_vals": {"form": "supplier"},
                "hx_req": "/invoice/approve_row"
            },
        }
    },
    "signatory": {
        "form_class": df.signatory,
        "table_name": "signatory",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "signatory"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "export_fields": {
        "form_class": df.export_fields,
        "table_name": "export",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "export_fields"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "item_category": {
        "form_class": df.item_category,
        "table_name": "category",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "item_category"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "variety": {
        "form_class": df.variety,
        "table_name": "variety",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "variety"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "item_name": {
        "form_class": df.item_name,
        "table_name": "item_name",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "item_name"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "stock": {
        "form_class": df.stock,
        "table_name": "stock",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "stock"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "units": {
        "form_class": df.units,
        "table_name": "units",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "units"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        },
        "table_buttons": {
            "delete": {
                "hx_vals": {"form": "units"},
                "hx_req": "/invoice/delete_row"
            },
            "approve": {
                "hx_vals": {"form": "units"},
                "hx_req": "/invoice/approve_row"
            },
        }
    },
    "location": {
        "form_class": df.location,
        "table_name": "location",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "location"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "stock_transfer": {
        "form_class": df.stock_transfer,
        "table_name": "stock",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "stock_transfer"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "open_bal_prod": {
        "form_class": df.open_bal_prod,
        "table_name": "production",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "open_bal_prod"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "production": {
        "form_class": df.production,
        "table_name": "production",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "production"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "prod_plus_minus": {
        "form_class": df.prod_plus_minus,
        "table_name": "production",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "prod_plus_minus"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "prod_approval": {
        "form_class": df.prod_approval,
        "table_name": "production",
        "buttons": {
            "approve": {
                "hx_vals": {"form": "prod_approval"},
                "hx_req": "/invoice/form_view",
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
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "jumbo_roll_qc": {
        "form_class": df.jumbo_roll_qc,
        "table_name": "jumbo_roll_qc",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "jumbo_roll_qc"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "lot_no_wise_qc": {
        "form_class": df.lot_no_wise_qc,
        "table_name": "lot_no_wise_qc",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "lot_no_wise_qc"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "finishing_house": {
        "form_class": df.finishing_house,
        "table_name": "finishing_house",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "finishing_house"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
    "program_planning": {
        "form_class": df.program_planing,
        "table_name": "program_planning",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "program_planning"},
                "hx_req": "/invoice/form_view",
                "hx_swap": "outerHTML",
            },
        }
    },
}

REPORT = {
    "pending_order": {
        "form_class": df.pending_order,
        "table_name": "pending_order",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "pending_order"},
                "hx_req": "/invoice/report_view"
            },
            "generate": {
                "hx_req": "/invoice/generate_report",
            },
        }
    },
    "prod_record": {
        "form_class": df.prod_record,
        "table_name": "prod_record",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "prod_record"},
                "hx_req": "/invoice/report_view"
            },
        }
    },
    "dispatch_details": {
        "form_class": df.dispatch_details,
        "table_name": "dispatch_details",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "dispatch_details"},
                "hx_req": "/invoice/report_view"
            },
        }
    },
    "stock": {
        "form_class": df.stock,
        "table_name": "stock",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "stock"},
                "hx_req": "/invoice/report_view"
            },
        }
    },
    "loader_report": {
        "form_class": df.loader_report,
        "table_name": "loader_report",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "loader_report"},
                "hx_req": "/invoice/report_view"
            },
        }
    },
    "qc_report": {
        "form_class": df.qc_report,
        "table_name": "qc_report",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "qc_report"},
                "hx_req": "/invoice/report_view"
            },
        }
    },
    "stock_plus_minus": {
        "form_class": df.stock_plus_minus,
        "table_name": "stock_plus_minus",
        "buttons": {
            "submit": {
                "hx_vals": {"form": "stock_plus_minus"},
                "hx_req": "/invoice/report_view",
            },
        }
    },
}


# NOTE: this is for when i require that the admin forms also need better structure
# ADMIN_MAP= {
#     "stock_plus_minus": {
#         "form_class": df.stock_plus_minus,
#         "table_name": "stock_plus_minus",
#         "buttons": {
#             "submit": {
#                 "hx_vals": {"form": "stock_plus_minus"},
#                 "hx_req": "/invoice/report_view",
#             },
#         }
#     },
# }
