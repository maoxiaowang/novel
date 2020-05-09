from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from base.models import Novel, Chapter
from base.models.novel import Volume, Paragraph
from general.forms.mixin import FormValidationMixin
from general.utils.text import calc_word_count
from general.views import JSONDeleteView
from portal.forms.author import NovelCreationForm, ChapterUpdateForm, ChapterCreateForm, VolumeCreateForm


class NovelCreate(CreateView):
    model = Novel
    form_class = NovelCreationForm
    template_name = 'portal/author/novel/create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = self.model.STATUS['active']
        self.object = form.save()

        context = dict()
        works = self.request.user.novel_set.select_related(
            'sub_category__category').prefetch_related('volume_set__chapter_set')
        context.update(works=works)
        return render(self.request, 'portal/user/home/parts/workbench.html', context=context)


class ChapterUpdate(LoginRequiredMixin, UpdateView):
    """
    作家小说更新页面
    列出所有章节标题
    """
    model = Chapter
    pk_url_kwarg = 'chapter_id'
    form_class = ChapterUpdateForm
    template_name = 'portal/author/novel/edit_chapters.html'

    def dispatch(self, request, *args, **kwargs):
        novel = Novel.objects.get(id=kwargs.get('novel_id'))
        if novel.author_id != self.request.user.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.model.objects.prefetch_related('volume__novel')
        return super().get_queryset()

    def get_object(self, queryset=None):
        chapter_id = self.kwargs['chapter_id']
        if not chapter_id:
            # prevent raising error
            return
        return super().get_object(queryset=queryset)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            # 获取不到object，则重定向到第一个章节
            novel_id = self.kwargs['novel_id']
            self.object = Chapter.objects.filter(volume__novel_id=novel_id).order_by('id').first()
            return HttpResponseRedirect(
                reverse(
                    'portal:novel_chapter_update',
                    kwargs={'novel_id': novel_id, 'chapter_id': self.object.id}
                )
            )
        if self.object.volume.novel.author != request.user:
            raise PermissionDenied
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(chapter=self.object, novel=self.object.volume.novel)
        context.update(form=self.form_class(
            initial={'title': self.object.title, 'content': self.object.content}
        ))
        return context

    def get_success_url(self):
        status = self.object.status
        if status == self.model.STATUS['saved']:
            msg = '保存成功'
        elif status == self.model.STATUS['submitted']:
            msg = '发布成功'
        else:
            msg = '操作成功'

        messages.add_message(self.request, messages.SUCCESS, msg)
        return reverse(
            'portal:novel_chapter_update',
            kwargs={
                'novel_id': self.object.volume.novel_id,
                'chapter_id': self.kwargs['chapter_id']
            }
        )

    def form_valid(self, form):
        content = form.cleaned_data['content']
        # 过滤掉空行，去掉行首尾空字符
        paragraph_lines = content.splitlines()
        paragraph_set = self.object.paragraph_set
        paragraph_count = paragraph_set.count()
        lines_count = len(paragraph_lines)
        novel = self.object.volume.novel
        for i, (paragraph, line) in enumerate(zip(paragraph_set.all(), paragraph_lines)):
            # paragraph
            old_count = paragraph.word_count
            new_count = calc_word_count(line)
            changed_count = new_count - old_count

            # put this behind words counting
            paragraph.content = line

            paragraph.serial = i + 1
            paragraph.save()

            # novel
            if changed_count != 0:
                form.instance.word_count += changed_count
                novel.word_count += changed_count
                novel.save()
        if paragraph_count > lines_count:
            # delete
            d_paragraphs = paragraph_set.filter(serial__gt=lines_count)
            count = 0
            for p in d_paragraphs:
                count += p.word_count

            form.instance.word_count -= count
            novel.word_count -= count
            novel.save()

            d_paragraphs.delete()
        elif paragraph_count < lines_count:
            # add
            paragraph_data = list()
            for i, line in enumerate(paragraph_lines[paragraph_count:]):
                word_count = calc_word_count(line)
                paragraph_data.append(
                    Paragraph(
                        chapter=self.object,
                        content=line,
                        serial=paragraph_count + i + 1
                    ),
                )
                novel.word_count += word_count
                form.instance.word_count += word_count
            novel.save()
            Paragraph.objects.bulk_create(paragraph_data)
        return super().form_valid(form)


class VolumeCreate(FormValidationMixin, CreateView):
    model = Volume
    form_class = VolumeCreateForm
    http_method_names = ['post']
    ajax = True

    def _template_response(self):
        return render(
            self.request,
            'portal/author/novel/blocks/menu_new_volume.html',
            context={'volume': self.object}
        )


class VolumeRename(FormValidationMixin, UpdateView):
    model = Volume
    fields = ('name',)
    pk_url_kwarg = 'volume_id'
    http_method_names = ['post']


class VolumeDelete(JSONDeleteView):
    model = Volume
    pk_url_kwarg = 'volume_id'
    http_method_names = ['delete']


class ChapterCreate(FormValidationMixin, CreateView):
    model = Chapter
    form_class = ChapterCreateForm
    http_method_names = ['post']
    ajax = True

    def _template_response(self):
        return render(
            self.request,
            'portal/author/novel/blocks/menu_new_chapter.html',
            context={'chapter': self.object}
        )


class ChapterDelete(DeleteView):
    model = Chapter
    pk_url_kwarg = 'chapter_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.volume.chapter_set.count() <= 1:
            messages.add_message(request, messages.WARNING, '卷中至少要保留一个章节')
            return HttpResponseRedirect(
                reverse_lazy('portal:novel_chapter_update', kwargs={
                    'novel_id': self.object.volume.novel_id,
                    'chapter_id': self.object.id
                })
            )
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('portal:novel_chapter_update', kwargs={
            'novel_id': self.object.volume.novel_id,
            'chapter_id': 0
        })
