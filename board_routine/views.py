from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from .models import RoutineBoard, Like
from .forms import RoutineBoardForm, RoutineBoardUpdateForm, PasswordVerifyForm
import hashlib
from django.views.decorators.http import require_POST
from django.utils import timezone


def hash_password(password):
    """비밀번호를 해시화"""
    return hashlib.sha256(password.encode()).hexdigest()


def routine_list(request):
    """루틴 게시판 목록"""
    posts = RoutineBoard.objects.all()
    paginator = Paginator(posts, 9)  # 페이지당 9개씩
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
    client_ip = request.META.get('REMOTE_ADDR')
    can_like = post.can_like(client_ip)
    like_count = post.get_like_count()
    return render(request, 'board_routine/detail.html', {
        'post': post,
        'can_like': can_like,
        'like_count': like_count
    })


def routine_create(request):
    """루틴 게시판 글 작성"""
    if request.method == "POST":
        print('시작')
        form = RoutineBoardForm(request.POST, request.FILES)
        print(f"Form errors: {form.errors}")  # 디버깅용
        if form.is_valid():
            print('유효')
            try:
                routine = form.save(commit=False)
                routine.password = hash_password(form.cleaned_data['password'])
                routine.save()
                messages.success(request, "글이 성공적으로 작성되었습니다.")
                return redirect("board_routine:detail", pk=routine.pk)
            except Exception as e:
                print(f"Error saving routine: {str(e)}")  # 디버깅용
                messages.error(request, f"글 저장 중 오류가 발생했습니다: {str(e)}")
        else:
            print(f"Form is not valid: {form.errors}")  # 디버깅용
            messages.error(request, "입력하신 정보에 오류가 있습니다.")
    else:
        form = RoutineBoardForm()

    return render(request, "board_routine/create.html", {"form": form})


def routine_update(request, pk):
    """루틴 게시판 글 수정"""
    post = get_object_or_404(RoutineBoard, pk=pk)

    if request.method == "POST":
        print(f"POST data: {request.POST}")  # 디버깅용

        # 실제 수정 처리 (비밀번호 검증 완료된 경우)
        if "update_post" in request.POST and "password_verified" in request.POST:
            print("Processing update...")  # 디버깅용
            form = RoutineBoardUpdateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                print("Form is valid, saving...")  # 디버깅용
                try:
                    updated_post = form.save(commit=False)
                    # 비밀번호는 그대로 유지
                    updated_post.save()
                    messages.success(request, "글이 성공적으로 수정되었습니다.")
                    return redirect("board_routine:detail", pk=post.pk)
                except Exception as e:
                    print(f"Error saving post: {str(e)}")  # 디버깅용
                    messages.error(request, f"글 저장 중 오류가 발생했습니다: {str(e)}")
            else:
                print(f"Form errors: {form.errors}")  # 디버깅용
                # 폼 에러가 있으면 에러 메시지와 함께 다시 수정 폼 표시
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        if field == "__all__":
                            error_messages.append(f"{error}")
                        else:
                            field_label = form.fields[field].label or field
                            error_messages.append(f"{field_label}: {error}")

                error_message = "입력하신 정보에 오류가 있습니다: " + "; ".join(
                    error_messages
                )
                messages.error(request, error_message)
                return render(
                    request,
                    "board_routine/update.html",
                    {"form": form, "post": post, "password_verified": True},
                )

        # 비밀번호 확인
        elif "password_verify" in request.POST:
            print("Verifying password...")  # 디버깅용
            password_form = PasswordVerifyForm(request.POST)
            if password_form.is_valid():
                password = password_form.cleaned_data["password"]
                if hash_password(password) == post.password:
                    print("Password correct, showing update form...")  # 디버깅용
                    # 비밀번호가 맞으면 수정 폼 표시
                    form = RoutineBoardUpdateForm(instance=post)
                    return render(
                        request,
                        "board_routine/update.html",
                        {"form": form, "post": post, "password_verified": True},
                    )
                else:
                    print("Password incorrect")  # 디버깅용
                    messages.error(request, "비밀번호가 올바르지 않습니다.")

        # 비밀번호 검증 없이 수정 시도하는 경우
        elif "update_post" in request.POST:
            print("Update attempted without password verification")  # 디버깅용
            messages.error(request, "비밀번호 검증이 필요합니다. 다시 시도해주세요.")
        else:
            print("No valid action found")  # 디버깅용

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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_POST
def like_routine(request, pk):
    print(f"Like request received for post {pk}")  # 디버깅용
    try:
        routine = get_object_or_404(RoutineBoard, pk=pk)
        client_ip = get_client_ip(request)
        print(f"Client IP: {client_ip}")  # 디버깅용
        
        if not routine.can_like(client_ip):
            print(f"Like not allowed for IP {client_ip} - 5 minute cooldown")  # 디버깅용
            return JsonResponse({
                'status': 'error',
                'message': '5분 후에 다시 시도해주세요.'
            })
        
        print(f"Creating like for post {pk} from IP {client_ip}")  # 디버깅용
        Like.objects.create(
            routine=routine,
            ip_address=client_ip
        )
        
        like_count = routine.get_like_count()
        print(f"New like count: {like_count}")  # 디버깅용
        
        return JsonResponse({
            'status': 'success',
            'like_count': like_count
        })
    except Exception as e:
        print(f"Error in like_routine: {str(e)}")  # 디버깅용
        return JsonResponse({
            'status': 'error',
            'message': f'좋아요 처리 중 오류가 발생했습니다'
        }, status=500)
