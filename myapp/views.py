from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,HttpRequest
from myapp.models import Post,Comment
from django.views.generic.edit import CreateView
from myapp.forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
	# process the data
	posts = Post.objects.all()
	context = {'posts':posts}
	return render(request,'index.html',context)

class PostCreate(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title','description','image']
	template_name = 'create.html'
	success_url = '/'

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super().form_valid(form)
@login_required
def detail(request,pk):
    p = Post.objects.get(pk = pk)
    comments = Comment.objects.filter(post_id = pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            comment = form.cleaned_data['comment']
            c = Comment(post_id = pk,comment = comment,user = request.user)
            c.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('myapp:detail', kwargs = {'pk':pk}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    return render(request, 'detail.html', {'form': form,'p':p,'comments':comments})



