from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def file_create(request):
    if request.method == 'POST':
        form = FileCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('images:media_list')
    else:
        form = FileCreateForm()
    return render(request, 'images/image/create.html', {'form': form})

def media_list(request):
    media = Image.objects.all()
    return render(request, 'images/image/media_list.html', {'media': media, 'section': 'images'})

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action=='like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass

    return JsonResponse({'status': 'ok'})
