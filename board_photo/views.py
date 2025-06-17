from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from .models import PhotoBoard, Like
from .forms import PhotoBoardForm, PhotoBoardUpdateForm, PasswordVerifyForm
import hashlib
from django.views.decorators.http import require_POST


def hash_password(password):
    """비밀번호를 해시화"""
    return hashlib.sha256(password.encode()).hexdigest()


def photo_list(request):
    """사진 게시판 목록"""
    posts = PhotoBoard.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 9)  # 한 페이지에 9개씩 표시
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'board_photo/list.html', {'posts': posts})


def photo_detail(request, pk):
    """사진 게시판 상세보기"""
    post = get_object_or_404(PhotoBoard, pk=pk)
    client_ip = request.META.get('REMOTE_ADDR')
    can_like = post.can_like(client_ip)
    like_count = post.get_like_count()
    return render(request, 'board_photo/detail.html', {
        'post': post,
        'can_like': can_like,
        'like_count': like_count
    })


def photo_create(request):
    """사진 게시판 글 작성"""
    if request.method == "POST":
        form = PhotoBoardForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                photo = form.save(commit=False)
                photo.password = hash_password(form.cleaned_data['password'])  # 비밀번호 해시화하여 저장
                photo.save()
                messages.success(request, '게시글이 성공적으로 작성되었습니다.')
                return redirect('board_photo:detail', pk=photo.pk)
            except Exception as e:
                print(f"Error saving photo: {str(e)}")  # 디버깅용
                messages.error(request, f'게시글 저장 중 오류가 발생했습니다: {str(e)}')
    else:
        form = PhotoBoardForm()

    return render(request, "board_photo/create.html", {"form": form})


def photo_update(request, pk):
    """사진 게시판 글 수정"""
    post = get_object_or_404(PhotoBoard, pk=pk)

    if request.method == "POST":
        # 실제 수정 처리 (비밀번호 검증 완료된 경우)
        if "update_post" in request.POST and "password_verified" in request.POST:
            form = PhotoBoardUpdateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                try:
                    photo = form.save(commit=False)
                    # 비밀번호가 변경된 경우에만 업데이트
                    if form.cleaned_data.get('password'):
                        photo.password = form.cleaned_data['password']
                    photo.save()
                    messages.success(request, '게시글이 성공적으로 수정되었습니다.')
                    return redirect('board_photo:detail', pk=photo.pk)
                except Exception as e:
                    print(f"Error updating photo: {str(e)}")  # 디버깅용
                    messages.error(request, f'게시글 수정 중 오류가 발생했습니다: {str(e)}')
            else:
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
                    "board_photo/update.html",
                    {"form": form, "post": post, "password_verified": True},
                )

        # 비밀번호 확인
        elif "password_verify" in request.POST:
            password_form = PasswordVerifyForm(request.POST)
            if password_form.is_valid():
                password = password_form.cleaned_data["password"]
                if hash_password(password) == post.password:
                    # 비밀번호가 맞으면 수정 폼 표시
                    form = PhotoBoardUpdateForm(instance=post)
                    return render(
                        request,
                        "board_photo/update.html",
                        {"form": form, "post": post, "password_verified": True},
                    )
                else:
                    messages.error(request, "비밀번호가 올바르지 않습니다.")

        # 비밀번호 검증 없이 수정 시도하는 경우
        elif "update_post" in request.POST:
            messages.error(request, "비밀번호 검증이 필요합니다. 다시 시도해주세요.")

    # 비밀번호 확인 폼 표시
    password_form = PasswordVerifyForm()
    return render(
        request,
        "board_photo/update.html",
        {"password_form": password_form, "post": post},
    )


def photo_delete(request, pk):
    """사진 게시판 글 삭제"""
    post = get_object_or_404(PhotoBoard, pk=pk)

    if request.method == "POST":
        # 비밀번호 확인 로직 추가
        password_form = PasswordVerifyForm(request.POST)
        if password_form.is_valid():
            password = password_form.cleaned_data["password"]
            if hash_password(password) == post.password:
                try:
                    post.delete()
                    messages.success(request, '게시글이 성공적으로 삭제되었습니다.')
                    return redirect('board_photo:list')
                except Exception as e:
                    print(f"Error deleting photo: {str(e)}")  # 디버깅용
                    messages.error(request, f'게시글 삭제 중 오류가 발생했습니다: {str(e)}')
            else:
                messages.error(request, "비밀번호가 올바르지 않습니다.")
        else:
            messages.error(request, "비밀번호를 입력해주세요.")

    password_form = PasswordVerifyForm()
    return render(
        request,
        "board_photo/delete.html",
        {"password_form": password_form, "post": post},
    )


@require_POST
def like_photo(request, pk):
    print(f"Like request received for photo {pk}")  # 디버깅용
    try:
        photo = get_object_or_404(PhotoBoard, pk=pk)
        client_ip = request.META.get('REMOTE_ADDR')
        print(f"Client IP: {client_ip}")  # 디버깅용
        
        if not photo.can_like(client_ip):
            print(f"Like not allowed for IP {client_ip} - 5 minute cooldown")  # 디버깅용
            return JsonResponse({
                'status': 'error',
                'message': '5분 후에 다시 시도해주세요.'
            })
        
        print(f"Creating like for photo {pk} from IP {client_ip}")  # 디버깅용
        Like.objects.create(
            photo=photo,
            ip_address=client_ip
        )
        
        like_count = photo.get_like_count()
        print(f"New like count: {like_count}")  # 디버깅용
        
        return JsonResponse({
            'status': 'success',
            'like_count': like_count
        })
    except Exception as e:
        print(f"Error in like_photo: {str(e)}")  # 디버깅용
        return JsonResponse({
            'status': 'error',
            'message': f'좋아요 처리 중 오류가 발생했습니다'
        }, status=500)
