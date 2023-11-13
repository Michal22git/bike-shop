from datetime import datetime

import requests


class InvoiceGenerator:
    def __init__(self, order):
        self.order = order

    def generate_invoice(self):
        delivery = (
            f"{self.order.address.name}\n"
            f"{self.order.address.first_name} {self.order.address.last_name}\n"
            f"{self.order.address.street} {self.order.address.house}"
            f"{'' if not self.order.address.apartment else f'/ {self.order.address.apartment}'}\n"
            f"{self.order.address.city}, {self.order.address.postal_code}\n"
            f"{self.order.address.country}, {self.order.address.phone}"
        )

        order_data = {
            "header": "Order invoice",
            "from": "BikeShop Ltd",
            "logo": "http://cdn.onlinewebfonts.com/svg/img_531624.png",
            "to": delivery,
            "number": self.order.pk,
            "date": datetime.now().strftime("%b %d, %Y"),
            "currency": "PLN",
            "balance_title": "Total costs",
            "balance": float(self.order.total_price)
        }

        data = {**order_data}

        response = requests.post(
            "https://invoice-generator.com",
            data=data
        )

        if response.status_code == 200:
            pdf_content = response.content
            return response.status_code, pdf_content
        else:
            return response.status_code, None
