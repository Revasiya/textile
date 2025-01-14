import frappe
from frappe.utils import cint, flt


def calculate_panel_qty_for_taxes_and_totals(self):
	calculate_panel_qty(self.doc)


def calculate_panel_qty(self):
	item_meta = frappe.get_meta(self.doctype + " Item")

	if not (
		item_meta.has_field('panel_length_meter') and
		item_meta.has_field('panel_based_qty') and
		item_meta.has_field('panel_qty')
	):
		return

	for row in self.items:
		if cint(row.panel_based_qty) and flt(row.panel_length_meter):
			row.panel_qty = flt(flt(row.stock_qty) / flt(row.panel_length_meter), row.precision("panel_qty"))
		else:
			row.panel_qty = 0
