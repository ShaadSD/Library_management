from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DetailView
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView,ListView
from Book.models import BOOK,BorrowedBook
from transactions.models import Review
from django.contrib import messages
from transactions.forms import ReviewForm


class Home(TemplateView):
    template_name = 'home_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        
        if category_slug:
            context['book'] = BOOK.objects.filter(category=category_slug)
        else:
            context['book'] = BOOK.objects.all() 
        return context


class BookDetaiView(DetailView):
    model=BOOK
    template_name='view_details.html'
    context_object_name='book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(book=self.object)
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = self.object
            review.save()
            return redirect('book_detail',pk=self.object.pk)
        else:
            return self.get(request,*args,**kwargs)

class ProfileView(ListView):
    model = BorrowedBook
    template_name = 'profile.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        return BorrowedBook.objects.filter(user=self.request.user)


def return_book(request, pk):
    book = get_object_or_404(BOOK, pk=pk)
    account = request.user.account
    borrowed_book = BorrowedBook.objects.filter(user=request.user, book=book).first()

    if borrowed_book:
        book.quantity += 1
        book.save()
        account.balance += book.Borrowing_Price
        account.save()
    
        borrowed_book.delete()
        messages.success(request, f'You have successfully returned {book.Title}!')
    else:
        messages.error(request, 'You have not borrowed this book.')

    return redirect('profile')


