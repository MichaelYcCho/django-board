from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from .models import PhotoBoard
from .forms import PhotoBoardForm, PhotoBoardUpdateForm, PasswordVerifyForm
import hashlib


def hash_password(password):
    """비밀번호를 해시화"""
    return hashlib.sha256(password.encode()).hexdigest()


def photo_list(request):
    """사진 게시판 목록"""
    posts = PhotoBoard.objects.all()
    paginator = Paginator(posts, 10)  # 페이지당 10개씩
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'board_photo/list.html', {
        'page_obj': page_obj,
        'posts': page_obj.object_list
    })


def photo_detail(request, pk):
    """사진 게시판 상세보기"""
    post = get_object_or_404(PhotoBoard, pk=pk)
    return render(request, 'board_photo/detail.html', {'post': post})


def photo_create(request):
    """사진 게시판 글 작성"""
    if request.method == 'POST':
        form = PhotoBoardForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.password = hash_password(form.cleaned_data['password'])
            post.save()
            messages.success(request, '글이 성공적으로 작성되었습니다.')
            return redirect('board_photo:detail', pk=post.pk)
    else:
        form = PhotoBoardForm()
    
    return render(request, 'board_photo/create.html', {'form': form})


def photo_update(request, pk):
    """사진 게시판 글 수정"""
    post = get_object_or_404(PhotoBoard, pk=pk)
    
    if request.method == 'POST':
        # 비밀번호 확인
        if 'password_verify' in request.POST:
            password_form = PasswordVerifyForm(request.POST)
            if password_form.is_valid():
                password = password_form.cleaned_data['password']
                if hash_password(password) == post.password:
                    # 비밀번호가 맞으면 수정 폼 표시
                    form = PhotoBoardUpdateForm(instance=post)
                    return render(request, 'board_photo/update.html', {
                        'form': form, 
                        'post': post,
                        'password_verified': True
                    })
                else:
                    messages.error(request, '비밀번호가 올바르지 않습니다.')
        
        # 실제 수정 처리
        elif 'update_post' in request.POST:
            form = PhotoBoardUpdateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, '글이 성공적으로 수정되었습니다.')
                return redirect('board_photo:detail', pk=post.pk)
    
    # 비밀번호 확인 폼 표시
    password_form = PasswordVerifyForm()
    return render(request, 'board_photo/update.html', {
        'password_form': password_form,
        'post': post
    })


def photo_delete(request, pk):
    """사진 게시판 글 삭제"""
    post = get_object_or_404(PhotoBoard, pk=pk)
    
    if request.method == 'POST':
        password_form = PasswordVerifyForm(request.POST)
        if password_form.is_valid():
            password = password_form.cleaned_data['password']
            if hash_password(password) == post.password:
                post.delete()
                messages.success(request, '글이 성공적으로 삭제되었습니다.')
                return redirect('board_photo:list')
            else:
                messages.error(request, '비밀번호가 올바르지 않습니다.')
    
    password_form = PasswordVerifyForm()
    return render(request, 'board_photo/delete.html', {
        'password_form': password_form,
        'post': post
    })
