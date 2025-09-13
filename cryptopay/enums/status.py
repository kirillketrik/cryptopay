from enum import Enum


class InvoiceStatus(str, Enum):
    """Invoice status enumeration."""
    
    PENDING = "PENDING"
    PAID = "PAID"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
