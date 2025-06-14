from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from .models import RoutineBoard
from .forms import RoutineBoardForm, RoutineBoardUpdateForm, PasswordVerifyForm
import hashlib


def hash_password(password):
    """비밀번호를 해시화"""
    return hashlib.sha256(password.encode()).hexdigest()


def routine_list(request):
    """루틴 게시판 목록"""
    posts = RoutineBoard.objects.all()
    paginator = Paginator(posts, 10)  # 페이지당 10개씩
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "board_routine/list.html",
        {"page_obj": page_obj, "posts": page_obj.object_list},
    )


def routine_detail(request, pk):
    """루틴 게시판 상세보기"""
    post = get_object_or_404(RoutineBoard, pk=pk)
    return render(request, "board_routine/detail.html", {"post": post})


def routine_create(request):
    """루틴 게시판 글 작성"""
    if request.method == "POST":
        form = RoutineBoardForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.password = hash_password(form.cleaned_data["password"])
            post.save()
            messages.success(request, "글이 성공적으로 작성되었습니다.")
            return redirect("board_routine:detail", pk=post.pk)
    else:
        form = RoutineBoardForm()

    return render(request, "board_routine/create.html", {"form": form})


def routine_update(request, pk):
    """루틴 게시판 글 수정"""
    post = get_object_or_404(RoutineBoard, pk=pk)

    if request.method == "POST":
        # 비밀번호 확인
        if "password_verify" in request.POST:
            password_form = PasswordVerifyForm(request.POST)
            if password_form.is_valid():
                password = password_form.cleaned_data["password"]
                if hash_password(password) == post.password:
                    # 비밀번호가 맞으면 수정 폼 표시
                    form = RoutineBoardUpdateForm(instance=post)
                    return render(
                        request,
                        "board_routine/update.html",
                        {"form": form, "post": post, "password_verified": True},
                    )
                else:
                    messages.error(request, "비밀번호가 올바르지 않습니다.")

        # 실제 수정 처리
        elif "update_post" in request.POST:
            form = RoutineBoardUpdateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "글이 성공적으로 수정되었습니다.")
                return redirect("board_routine:detail", pk=post.pk)

    # 비밀번호 확인 폼 표시
    password_form = PasswordVerifyForm()
    return render(
        request,
        "board_routine/update.html",
        {"password_form": password_form, "post": post},
    )


def routine_delete(request, pk):
    """루틴 게시판 글 삭제"""
    post = get_object_or_404(RoutineBoard, pk=pk)

    if request.method == "POST":
        password_form = PasswordVerifyForm(request.POST)
        if password_form.is_valid():
            password = password_form.cleaned_data["password"]
            if hash_password(password) == post.password:
                post.delete()
                messages.success(request, "글이 성공적으로 삭제되었습니다.")
                return redirect("board_routine:list")
            else:
                messages.error(request, "비밀번호가 올바르지 않습니다.")

    password_form = PasswordVerifyForm()
    return render(
        request,
        "board_routine/delete.html",
        {"password_form": password_form, "post": post},
    )
