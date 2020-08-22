from datetime import datetime

from bson import ObjectId

from app.adapters.db_adapter import update
from app.models.grouppaymentmodel import GroupPaymentModel
from app.models.paymentmodel import PaymentModel

LOG_PATH = "/home/cs807/properit/logs/paylogs.log"


def write_log(path, data):
    with open(path, "a") as file:
        file.write(data + "\n")


def pay_service():
    all_group_payments = GroupPaymentModel.objects()
    for gp in all_group_payments:
        if gp.is_periodic:
            if gp.is_approved:
                for payment_id in gp.payments:
                    payment = PaymentModel.objects.get(id=ObjectId(payment_id))
                    if payment.is_open:
                        if payment.deadline == datetime.now().month:
                            payment.is_open = False
                            payment.when_payed = datetime.now().replace(microsecond=0)
                            update(payment)
                            write_log(LOG_PATH, "payment paid: " + str(payment.id) + " in group_payment: " + str(
                                gp.id) + " at: " + str(payment.when_payed) + " (deadline: " + str(
                                payment.deadline) + ")")


pay_service()
