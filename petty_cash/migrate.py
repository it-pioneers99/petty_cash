# -*- coding: utf-8 -*-
# Copyright (c) 2020, GreyCube Technologies and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.desk.page.setup_wizard.setup_wizard import make_records

def update_dashboard_link_for_core_doctype(doctype,link_doctype,link_fieldname,group=None):
    print(doctype,link_doctype,link_fieldname,group)
    try:
        d = frappe.get_doc("Customize Form")
        if doctype:
            d.doc_type = doctype
        d.run_method("fetch_to_customize")
        for link in d.get('links'):
            if link.link_doctype==link_doctype and link.link_fieldname==link_fieldname:
                # found so just return
                return
        d.append('links', dict(link_doctype=link_doctype, link_fieldname=link_fieldname,table_fieldname=None,group=group))
        d.run_method("save_customization")
        frappe.clear_cache()
    except Exception:
        frappe.log_error(frappe.get_traceback())

def after_migrate():
    custom_fields = {
        "Employee": [
            dict(
                fieldname="maximum_balance_for_petty_cash_cf",
                label="Max Balance For Petty Cash",
                fieldtype="Currency",
                insert_after="branch",
                translatable=0,
                is_system_generated=0,
                is_custom_field=1,
            ),
        ],

        "Purchase Invoice": [
            dict(
                fieldname="custom_pc_clearance_reference",
                label="PC Clearance Reference",
                fieldtype="Link",
                options="PC Clearance",
                insert_after="represents_company",
                translatable=0,
                is_system_generated=0,
                is_custom_field=1,
		    ),
        ],

        "Journal Entry": [
            dict(
                fieldname="custom_pc_clearance_reference",
                label="PC Clearance Reference",
                fieldtype="Link",
                options="PC Clearance",
                insert_after="inter_company_journal_entry_reference",
                translatable=0,
                is_system_generated=0,
                is_custom_field=1,
            ),
        ],
        
    }
    print("Creating custom fields for app petty cash:")
    for dt, fields in custom_fields.items():
        print("*******\n %s: " % dt, [d.get("fieldname") for d in fields])
    create_custom_fields(custom_fields)
    update_dashboard_link_for_core_doctype(doctype='Project',link_doctype='PC Request',link_fieldname='project',group="Petty Cash")
    update_dashboard_link_for_core_doctype(doctype='Project',link_doctype='PC Clearance',link_fieldname='project',group="Petty Cash")
