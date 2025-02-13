from django.urls import path
from . import views

urlpatterns = [
    # Home page: List all available books
    path('home/', views.home_view, name='home_view'),
    
    # Book Detail: Show details for a specific book
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # Create, update, and delete books (for users with proper permissions)
    path('book/create/', views.create_book, name='create_book'),
    path('book/<int:book_id>/update/', views.update_book, name='update_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    
    # Borrowing operations:
    path('book/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    
    # List of books borrowed by the current user (or all borrow records for staff)
    path('borrowed/', views.borrow_list, name='borrow_list'),
]

# If you're serving media files during development:
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
