from django.db import models
from django.conf import settings
from django.utils import timezone
from user.models import Author
# Create your models here.
class Tag (models.Model):
    
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE ,related_name='author_profile')
    description = models.CharField(max_length=50)
    total_copies = models.PositiveIntegerField(default = 1) 
    availlable_copies =  models.PositiveIntegerField(default = 1)
    tags = models.ManyToManyField(Tag , blank = True , related_name='books' )
    
    def __str__(self):
        self.name
        
    def borrow(self):
        if self.availlable_copies > 0:
            self.availlable_copies -= 1
            self.save()
            return True
        return False
    
    def return_book(self):
        """
        Increase the available copies when a book is returned.
        """
        if self.availlable_copies < self.total_copies:
            self.availlable_copies += 1
            self.save()
            return True
        return False
    
class Borrow(models.Model):
    book = models.ForeignKey( Book , on_delete=models.CASCADE, related_name = 'borrow_records')
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name= 'borrow_records')
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower.username} borrowed {self.book.title}"
    
    def calculate_fine(self):
    
        end_date = self.returned_date or timezone.now().date()
        if end_date > self.due_date:
            overdue_days = (end_date - self.due_date).days
            fine_per_day = 1  # $1 per day fine
            return overdue_days * fine_per_day
        return 0

    def mark_returned(self, return_date=None):
        """
        Mark the borrow record as returned. Update the returned date and set is_returned to True.
        Also update the book's available copies.
        """
        if return_date is None:
            return_date = timezone.now().date()
        self.returned_date = return_date
        self.is_returned = True
        self.save()
        self.book.return_book()


class Fine(models.Model):
    """
    Stores fine details for a borrow transaction.
    (Optional: you can compute fines on the fly, but storing them may be useful for history.)
    """
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    fine_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Fine for {self.borrow.borrower.username} - ${self.amount}"