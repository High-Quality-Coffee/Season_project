import { OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import ClassicEditor from '@wiz/libs/ckeditor/ckeditor';

export class Component implements OnInit {
    public title: any;
    public user;
    public category_list = [{ id: "notice", name: "공지사항" }, { id: "request", name: "요청사항" }, { id: "free", name: "자유게시판" }];
    public post = { id: "", category: "", content: "", user: {}, title: "" };
    public post_public = { title: "", email: "", files: [] }
    public comment = { community_id: this.post.id, content: "" };
    public comments;
    public edit_comment: boolean = false;
    public editor;

    constructor(
        public route: ActivatedRoute,
        public service: Service,
    ) { }

    public async ngOnInit() {
        this.load();
        await this.service.init();
        await this.service.render();
        this.public_load();
        await this.service.init();
        await this.service.render();
    }

    public async load() {
        this.post.title = window.localStorage.getItem('title');
        let { code, data } = await wiz.call('load', { title: this.post.title })
        if (code !== 200) {
            alert("로드실패. 다시 시도해주세요.")
        }
        this.post = data.post;
        this.post.files = JSON.parse(data.post.files.replace(/'/g, '"'));
        this.comment.community_id = this.post.id;

        const EDITOR_ID = 'textarea#editor';
        this.editor = await ClassicEditor.create(document.querySelector(EDITOR_ID), {})
        this.editor.isReadOnly = true;
        this.editor.data.set(this.post.content);
        this.editor.ui.view.toolbar.element.style.display = 'none';
        await this.service.render();
    }

    public async public_load() {
        this.post_public.title = window.localStorage.getItem('title');
        this.post_public.email = window.localStorage.getItem('email');
        const { code, data } = await wiz.call("public_load", { title: this.post_public.title, email: this.post_public.email });
        if (code != 200)
            alert("로드실패. 다시 시도해주세요.")
        this.post_public = data.post;
        this.post_public.files = JSON.parse(data.post.files.replace(/'/g, '"'));
        console.log(this.post_public.files);
        await this.service.render();
    }

    public go(item) {
        const obj = {
            category: item,
        }
        this.service.href([`/community/list`, obj]);
    }

    public async edit() {
        this.service.href(`/community/${this.post.category}/edit/${this.post.id}`);
    };

    public async create() {
        let comment = this.comment;
        let { code, data } = await wiz.call('create', comment)
        if (code === 200) this.comment = { post_id: this.post.id, content: "" };
        await this.load();
    };
    public async delete(comment) {
        let { code, data } = await wiz.call('delete', { id: comment.id })
        location.reload();
    };
    public async update(item) {
        let { code, data } = await wiz.call('update', item)
        location.reload();
    };

    public async movetoBack() {
        await this.service.render();
        location.href = "task/user/notice";
    }
} 
