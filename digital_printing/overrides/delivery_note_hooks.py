import frappe
from frappe import _
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote


class DeliveryNoteDP(DeliveryNote):
	def update_previous_doc_status(self):
		super().update_previous_doc_status()

		print_orders = [d.print_order for d in self.items if d.get('print_order')]
		print_order_row_names = [d.print_order_item for d in self.items if d.get('print_order_item')]

		for name in print_orders:
			doc = frappe.get_doc("Print Order", name)
			doc.set_delivered_status(update=True)

			doc.validate_delivered_qty(from_doctype=self.doctype, row_names=print_order_row_names)

			doc.set_status(update=True)
			doc.notify_update()


def map_print_order_reference_in_delivery_note_item(mapper):
	if not mapper.get("Delivery Note Item"):
		return

	field_map = mapper["Delivery Note Item"]["field_map"]
	field_map["print_order"] = "print_order"
	field_map["print_order_item"] = "print_order_item"
