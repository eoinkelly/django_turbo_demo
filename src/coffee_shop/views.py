from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Post
from .forms import PostForm
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)


class PostList(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        posts = Post.objects.all()
        return render(request, "coffee_shop/post_list.html", {"posts": posts})


class PostDetail(View):
    def get(self, request: HttpRequest, pk) -> HttpResponse:
        post = get_object_or_404(Post, pk=pk)
        return render(request, "coffee_shop/post_detail.html", {"post": post})


class PostCreate(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = PostForm()
        return render(request, "coffee_shop/post_form.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post_list")
        return render(request, "coffee_shop/post_form.html", {"form": form})


class PostUpdate(View):
    def get(self, request: HttpRequest, pk) -> HttpResponse:
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, "coffee_shop/post_form.html", {"form": form})

    def post(self, request: HttpRequest, pk) -> HttpResponse:
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_list")
        return render(request, "coffee_shop/post_form.html", {"form": form})


class PostDelete(View):
    def get(self, request: HttpRequest, pk) -> HttpResponse:
        post = get_object_or_404(Post, pk=pk)
        return render(request, "coffee_shop/post_confirm_delete.html", {"post": post})

    def post(
        self, _request: HttpRequest, pk
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect("post_list")
