from django.shortcuts import render


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.conf import settings

from .models import Book, Tag, Borrow, Fine

# ---------------------------
#   BOOK VIEWS
# ---------------------------

def home_view(request):
    """Display a list of all books."""
    books = Book.objects.all()
    return render(request, 'library/home.html', {'books': books})

def book_detail(request, book_id):
    """Display the details of a single book along with active borrow records."""
    book = get_object_or_404(Book, id=book_id)
    borrows = Borrow.objects.filter(book=book, is_returned=False)
    return render(request, 'library/book_detail.html', {'book': book, 'borrows': borrows})

@login_required
def create_book(request):
    """
    Create a new book.
    Only users with an associated author_profile that has can_add_books == True can create books.
    """
    # Check if the user has an author profile and the permission to add books
    if not hasattr(request.user, 'author_profile') or not request.user.author_profile.can_add_books:
        return HttpResponseForbidden("You do not have permission to add books.")

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        total_copies = int(request.POST.get('total_copies', 1))
        
        # Create the Book instance. available_copies is set to total_copies initially.
        book = Book.objects.create(
            title=title,
            author=request.user.author_profile,
            description=description,
            total_copies=total_copies,
            availlable_copies=total_copies
        )
        
        # Process tags if provided (as comma-separated values)
        tags_str = request.POST.get('tags', '')
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                book.tags.add(tag)
                
        return redirect('book_detail', book_id=book.id)
    
    return render(request, 'library/create_book.html')

@login_required
def update_book(request, book_id):
    """Update a book's details."""
    book = get_object_or_404(Book, id=book_id)
    # Check permission: only authors with permission can update a book.
    if not hasattr(request.user, 'author_profile') or not request.user.author_profile.can_add_books:
        return HttpResponseForbidden("You do not have permission to update this book.")

    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author_name = request.POST.get('author_name')
        book.isbn = request.POST.get('isbn')
        book.description = request.POST.get('description', '')
        new_total = int(request.POST.get('total_copies', book.total_copies))
        diff = new_total - book.total_copies
        book.total_copies = new_total
        # Adjust available copies, ensuring it doesn't go negative or above total copies.
        book.availlable_copies = max(0, min(book.availlable_copies + diff, new_total))
        book.save()

        # Update tags
        tags_str = request.POST.get('tags', '')
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            # Clear current tags
            book.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                book.tags.add(tag)
        return redirect('book_detail', book_id=book.id)
    
    return render(request, 'library/update_book.html', {'book': book})

@login_required
def delete_book(request, book_id):
    """Delete a book. Only permitted for users with author permission."""
    book = get_object_or_404(Book, id=book_id)
    if not hasattr(request.user, 'author_profile') or not request.user.author_profile.can_add_books:
        return HttpResponseForbidden("You do not have permission to delete this book.")
    
    if request.method == "POST":
        book.delete()
        return redirect('home_view')
    
    return render(request, 'library/delete_book.html', {'book': book})

# ---------------------------
# BORROW VIEWS
# ---------------------------

@login_required
def borrow_book(request, book_id):
    """
    Create a borrow transaction for a given book.
    Decrements the available copies of the book if available.
    Expects a due_date from the POST data in 'YYYY-MM-DD' format.
    """
    book = get_object_or_404(Book, id=book_id)
    if book.availlable_copies < 1:
        # If no copies are available, show an error on the book detail page.
        return render(request, 'library/book_detail.html', {
            'book': book,
            'error': 'Book is not available for borrowing.'
        })
    
    
    if request.method == "POST":
        due_date = request.POST.get('due_date')
        # Attempt to borrow the book. The borrow() method on Book should decrement available_copies.
        if book.borrow():
            borrow = Borrow.objects.create(
                book=book,
                borrower=request.user,
                due_date=due_date
            )
            return redirect('book_detail', book_id=book.id)
        else:
            return render(request, 'library/book_detail.html', {
                'book': book,
                'error': 'Unable to borrow the book at this time.'
            })
    
    return render(request, 'library/borrow_book.html', {'book': book})

@login_required
def return_book(request, borrow_id):
    """
    Mark a borrow record as returned.
    This view calculates any applicable fine and increases the book's available copies.
    Only the borrower or a staff member can mark the book as returned.
    """
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if request.user != borrow.borrower and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to return this book.")
    
    if request.method == "POST":
        borrow.mark_returned()  # This method should update returned_date, is_returned, and book availability.
        return redirect('book_detail', book_id=borrow.book.id)
    
    return render(request, 'library/return_book.html', {'borrow': borrow})

@login_required
def borrow_list(request):
    """
    List all borrow records.
    - For staff, show all borrow records.
    - For regular users, show only their own borrow records.
    """
    if request.user.is_staff:
        borrows = Borrow.objects.all()
    else:
        borrows = Borrow.objects.filter(borrower=request.user)
    return render(request, 'library/borrow_list.html', {'borrows': borrows})
