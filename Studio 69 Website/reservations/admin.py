from django.contrib import admin
from .models import ProofOfPayment, Booking

class ProofOfPaymentInline(admin.StackedInline):
    model = ProofOfPayment
    extra = 1

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = [ProofOfPaymentInline]
    
    list_display = ('id', 'user', 'room', 'start_date', 'end_date', 'has_proof_of_payment')
    list_filter = ('start_date', 'end_date')
    
    def has_proof_of_payment(self, obj):
        return bool(obj.proof_of_payment)
    has_proof_of_payment.boolean = True
    has_proof_of_payment.short_description = 'Proof of Payment Uploaded'
